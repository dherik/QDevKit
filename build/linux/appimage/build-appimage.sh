#!/bin/bash
#
# QDevKit AppImage Build Script
# Builds an AppImage from the PyInstaller output
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  Building QDevKit AppImage${NC}"
echo -e "${GREEN}================================================${NC}"

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$PROJECT_ROOT"

# Variables
APP_NAME="QDevKit"
APP_VERSION="${APP_VERSION:-1.0.0}"
APPDIR="$PROJECT_ROOT/build/AppDir"
DIST_DIR="$PROJECT_ROOT/dist"
PYINSTALLER_OUTPUT="$DIST_DIR/$APP_NAME"

# Debug output
echo "Project root: $PROJECT_ROOT"
echo "Dist directory: $DIST_DIR"
echo "Expected PyInstaller output: $PYINSTALLER_OUTPUT"
echo "Contents of dist directory:"
ls -la "$DIST_DIR/" || echo "Dist directory not found"

# Check if PyInstaller output exists
if [ ! -d "$PYINSTALLER_OUTPUT" ]; then
    echo -e "${RED}Error: PyInstaller output not found at $PYINSTALLER_OUTPUT${NC}"
    echo "Please run: python build.py"
    exit 1
fi

# Clean previous AppDir
echo -e "${YELLOW}Cleaning previous AppDir...${NC}"
rm -rf "$APPDIR"
mkdir -p "$APPDIR"

# Copy PyInstaller output to AppDir
echo -e "${YELLOW}Copying PyInstaller output to AppDir...${NC}"
cp -r "$PYINSTALLER_OUTPUT"/* "$APPDIR/"

# Create AppRun script
echo -e "${YELLOW}Creating AppRun script...${NC}"
cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export LD_LIBRARY_PATH="${HERE}/usr/lib:${HERE}/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PATH="${HERE}/usr/bin:${PATH}"
export QTCORE_PLUGIN_PATH="${HERE}/usr/plugins"
exec "${HERE}/QDevKit" "$@"
EOF
chmod +x "$APPDIR/AppRun"

# Copy desktop file
echo -e "${YELLOW}Installing desktop file...${NC}"
cp "$PROJECT_ROOT/build/linux/appimage/$APP_NAME.desktop" "$APPDIR/"

# Copy icon
echo -e "${YELLOW}Installing icon...${NC}"
mkdir -p "$APPDIR/usr/share/icons/hicolor/scalable/apps"
cp "$PROJECT_ROOT/build/linux/appimage/$APP_NAME.svg" "$APPDIR/$APP_NAME.svg"
cp "$PROJECT_ROOT/build/linux/appimage/$APP_NAME.svg" "$APPDIR/.DirIcon"
cp "$PROJECT_ROOT/build/linux/appimage/$APP_NAME.svg" "$APPDIR/usr/share/icons/hicolor/scalable/apps/$APP_NAME.svg"

# Create .desktop file with proper path
sed -i "s|^Exec=.*|Exec=AppRun|" "$APPDIR/$APP_NAME.desktop"

# Download linuxdeploy if not exists
LINUXDEPLOY="$HOME/.local/bin/linuxdeploy-x86_64.AppImage"
if [ ! -f "$LINUXDEPLOY" ]; then
    echo -e "${YELLOW}Downloading linuxdeploy...${NC}"
    mkdir -p "$HOME/.local/bin"
    wget -c "https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage" \
        -O "$LINUXDEPLOY"
    chmod +x "$LINUXDEPLOY"
fi

# Build AppImage
echo -e "${YELLOW}Building AppImage...${NC}"
export OUTPUT="$APP_VERSION-$APP_NAME-x86_64.AppImage"
"$LINUXDEPLOY" \
    --appdir="$APPDIR" \
    --output appimage \
    --desktop-file="$APPDIR/$APP_NAME.desktop" \
    --icon-file="$APPDIR/$APP_NAME.svg"

# Move AppImage to dist directory
mv "$OUTPUT" "$DIST_DIR/"

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  AppImage build completed!${NC}"
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}Output: $DIST_DIR/$OUTPUT${NC}"
echo -e "\nTo run:"
echo -e "  chmod +x $DIST_DIR/$OUTPUT"
echo -e "  ./$DIST_DIR/$OUTPUT"
echo ""
