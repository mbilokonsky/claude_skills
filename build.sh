#!/bin/bash
#
# Build script for Claude Code plugins
# Generates distributable plugin packages from source skills
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$SCRIPT_DIR/dist"

echo "Building Claude Code plugins..."
echo ""

# Clean and create dist directory
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# Build function
build_plugin() {
  local src_dir="$1"
  local plugin_name="$2"
  local src_path="$SCRIPT_DIR/$src_dir"
  local dest_path="$DIST_DIR/$plugin_name"

  echo "Building: $plugin_name"

  # Check required files exist
  if [[ ! -f "$src_path/plugin.json" ]]; then
    echo "  ERROR: Missing plugin.json in $src_dir"
    exit 1
  fi

  if [[ ! -f "$src_path/src/SKILL.md" ]]; then
    echo "  ERROR: Missing src/SKILL.md in $src_dir"
    exit 1
  fi

  # Create plugin directory structure
  mkdir -p "$dest_path/.claude-plugin"
  mkdir -p "$dest_path/skills/$plugin_name"

  # Copy plugin manifest
  cp "$src_path/plugin.json" "$dest_path/.claude-plugin/plugin.json"

  # Copy skill file
  cp "$src_path/src/SKILL.md" "$dest_path/skills/$plugin_name/SKILL.md"

  # Copy any additional files in src/ (supporting files, examples, etc.)
  for file in "$src_path/src/"*; do
    if [[ -f "$file" && "$(basename "$file")" != "SKILL.md" ]]; then
      cp "$file" "$dest_path/skills/$plugin_name/"
      echo "  Copied: $(basename "$file")"
    fi
  done

  echo "  Created: dist/$plugin_name/"
}

# Build each plugin
build_plugin "flight-lines" "flight-lines"
build_plugin "semantic_walk" "semantic-walk"

echo ""
echo "Build complete! Plugins available in: $DIST_DIR"
echo ""
echo "To install a plugin locally:"
echo "  claude --plugin-dir $DIST_DIR/<plugin-name>"
echo ""
echo "To install permanently:"
echo "  /plugin install $DIST_DIR/<plugin-name>"

# Check for --zip flag to create web UI packages
if [[ "$1" == "--zip" ]]; then
  echo ""
  echo "Creating ZIP files for Claude.ai web upload..."

  ZIP_DIR="$DIST_DIR/web"
  mkdir -p "$ZIP_DIR"

  for plugin_dir in "$DIST_DIR"/*/; do
    plugin_name=$(basename "$plugin_dir")
    if [[ "$plugin_name" != "web" ]]; then
      skill_dir="$plugin_dir/skills/$plugin_name"
      if [[ -d "$skill_dir" ]]; then
        (cd "$skill_dir" && zip -r "$ZIP_DIR/$plugin_name.zip" .)
        echo "  Created: dist/web/$plugin_name.zip"
      fi
    fi
  done

  echo ""
  echo "ZIP files for web upload: $ZIP_DIR"
  echo "Upload via Claude.ai > Settings > Features"
fi
