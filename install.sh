#!/usr/bin/env sh
set -eu

force="${1:-}"
case "$force" in
  ""|--force) ;;
  *) echo "Usage: ./install.sh [--force]" >&2; exit 2 ;;
esac

source_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/skills/junzi-economist"
test -f "$source_dir/SKILL.md" || { echo "Runtime package not found: $source_dir" >&2; exit 1; }

root="$HOME/.codex/skills"
dest="$root/junzi-economist"
tx="$$"
stage="$root/.junzi-economist.install-$tx"
backup="$root/.junzi-economist.backup-$tx"
installed=0; had_old=0; success=0

if [ "$force" != "--force" ] && [ -e "$dest" ]; then
  echo "Destination already exists: $dest. Re-run with --force after reviewing it." >&2
  exit 1
fi

rollback() {
  [ "$success" -eq 1 ] && return 0
  [ "$installed" -eq 1 ] && [ -e "$dest" ] && rm -rf -- "$dest"
  [ "$had_old" -eq 1 ] && [ -e "$backup" ] && mv -- "$backup" "$dest"
  [ -e "$stage" ] && rm -rf -- "$stage"
}
trap rollback EXIT HUP INT TERM

mkdir -p "$root"
cp -R "$source_dir" "$stage"
test -f "$stage/SKILL.md" && test -f "$stage/LICENSE.txt" && test -f "$stage/scripts/validate.py"
if [ -e "$dest" ]; then
  mv -- "$dest" "$backup"
  had_old=1
fi
mv -- "$stage" "$dest"
installed=1
[ -e "$backup" ] && rm -rf -- "$backup"
success=1
trap - EXIT HUP INT TERM
printf 'Installed Junzi Economist for Codex at %s\n' "$dest"
