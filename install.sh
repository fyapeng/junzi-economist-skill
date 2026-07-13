#!/usr/bin/env sh
set -eu

target="${1:-codex}"
case "$target" in
  codex|claude) platforms="$target" ;;
  both) platforms="codex claude" ;;
  *) echo "Usage: ./install.sh [codex|claude|both] [--force]" >&2; exit 2 ;;
esac
force="${2:-}"
source_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/skills/junzi-economist"
test -f "$source_dir/SKILL.md" || { echo "Runtime package not found: $source_dir" >&2; exit 1; }

tx="$$"
codex_root="$HOME/.codex/skills"
claude_root="$HOME/.claude/skills"
codex_dest="$codex_root/junzi-economist"
claude_dest="$claude_root/junzi-economist"
codex_stage="$codex_root/.junzi-economist.install-$tx"
claude_stage="$claude_root/.junzi-economist.install-$tx"
codex_backup="$codex_root/.junzi-economist.backup-$tx"
claude_backup="$claude_root/.junzi-economist.backup-$tx"
codex_done=0; claude_done=0; codex_old=0; claude_old=0; success=0

selected() { case " $platforms " in *" $1 "*) return 0 ;; *) return 1 ;; esac; }

# Preflight all targets before changing any target.
if [ "$force" != "--force" ]; then
  selected codex && [ -e "$codex_dest" ] && { echo "Destination already exists: $codex_dest. Re-run with --force after reviewing it." >&2; exit 1; }
  selected claude && [ -e "$claude_dest" ] && { echo "Destination already exists: $claude_dest. Re-run with --force after reviewing it." >&2; exit 1; }
fi

rollback() {
  [ "$success" -eq 1 ] && return 0
  if selected claude; then
    [ "$claude_done" -eq 1 ] && rm -rf -- "$claude_dest"
    [ "$claude_old" -eq 1 ] && [ -e "$claude_backup" ] && mv -- "$claude_backup" "$claude_dest"
    [ -e "$claude_stage" ] && rm -rf -- "$claude_stage"
  fi
  if selected codex; then
    [ "$codex_done" -eq 1 ] && rm -rf -- "$codex_dest"
    [ "$codex_old" -eq 1 ] && [ -e "$codex_backup" ] && mv -- "$codex_backup" "$codex_dest"
    [ -e "$codex_stage" ] && rm -rf -- "$codex_stage"
  fi
}
trap rollback EXIT HUP INT TERM

# Stage and verify all copies first.
for platform in $platforms; do
  eval "root=\${${platform}_root}"
  eval "stage=\${${platform}_stage}"
  mkdir -p "$root"
  cp -R "$source_dir" "$stage"
  test -f "$stage/SKILL.md" && test -f "$stage/LICENSE.txt" && test -f "$stage/scripts/validate.py"
done

for platform in $platforms; do
  eval "dest=\${${platform}_dest}"
  eval "stage=\${${platform}_stage}"
  eval "backup=\${${platform}_backup}"
  if [ -e "$dest" ]; then
    mv -- "$dest" "$backup"
    eval "${platform}_old=1"
  fi
  mv -- "$stage" "$dest"
  eval "${platform}_done=1"
done

for platform in $platforms; do
  eval "backup=\${${platform}_backup}"
  [ -e "$backup" ] && rm -rf -- "$backup"
done
success=1
trap - EXIT HUP INT TERM

for platform in $platforms; do
  eval "dest=\${${platform}_dest}"
  printf 'Installed Junzi Economist for %s at %s\n' "$platform" "$dest"
done
