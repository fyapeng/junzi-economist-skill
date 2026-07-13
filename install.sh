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

for platform in $platforms; do
  skills_root="$HOME/.$platform/skills"
  destination="$skills_root/junzi-economist"
  mkdir -p "$skills_root"
  if [ -e "$destination" ]; then
    if [ "$force" != "--force" ]; then
      echo "Destination already exists: $destination. Re-run with --force after reviewing it." >&2
      exit 1
    fi
    rm -rf -- "$destination"
  fi
  cp -R "$source_dir" "$destination"
  printf 'Installed Junzi Economist for %s at %s\n' "$platform" "$destination"
done
