#!/bin/bash
# Image optimization script using uv
# Processes all images in ./images/ folder and subfolders
# Outputs to ./images/output/

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🖼️  Image Optimizer with uv${NC}"
echo "================================="

# Get the directory of this script (should be ./scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Set default paths based on project structure
DEFAULT_INPUT="$PROJECT_ROOT/images"
DEFAULT_OUTPUT="$PROJECT_ROOT/images/output"

# Use provided arguments or defaults
INPUT_DIR="${1:-$DEFAULT_INPUT}"
OUTPUT_DIR="${2:-$DEFAULT_OUTPUT}"
QUALITY="${3:-85}"

echo -e "${GREEN}📁 Project root:${NC} $PROJECT_ROOT"
echo -e "${GREEN}📁 Input folder:${NC} $INPUT_DIR"
echo -e "${GREEN}📁 Output folder:${NC} $OUTPUT_DIR"
echo -e "${GREEN}🎯 Quality setting:${NC} $QUALITY%"
echo ""

# Check if input folder exists
if [ ! -d "$INPUT_DIR" ]; then
    echo -e "${RED}❌ Error: Input folder '$INPUT_DIR' does not exist!${NC}"
    echo -e "${YELLOW}💡 Please create the './images' folder or specify a different path.${NC}"
    echo ""
    echo "Usage:"
    echo "  ./optimize.sh                          # Use default ./images folder"
    echo "  ./optimize.sh /path/to/images          # Use custom input folder"
    echo "  ./optimize.sh /path/to/images /output  # Custom input and output"
    exit 1
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}⚠️  uv not found. Installing uv...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Count images to process
IMAGE_COUNT=$(find "$INPUT_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.webp" -o -iname "*.bmp" -o -iname "*.tiff" -o -iname "*.heic" -o -iname "*.heif" \) | wc -l)

echo -e "${BLUE}🔍 Found $IMAGE_COUNT images to process (including subfolders)${NC}"
echo ""

# Run the optimization script with uv
echo -e "${BLUE}🚀 Starting optimization...${NC}"
cd "$SCRIPT_DIR"

# Check if the Python script exists
if [ ! -f "image_optimizer.py" ]; then
    echo -e "${RED}❌ Error: image_optimizer.py not found in $SCRIPT_DIR${NC}"
    echo -e "${YELLOW}💡 Make sure image_optimizer.py is in the scripts/ folder${NC}"
    exit 1
fi

# Check if pyproject.toml exists
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ Error: pyproject.toml not found in $SCRIPT_DIR${NC}"
    echo -e "${YELLOW}💡 Make sure pyproject.toml is in the scripts/ folder${NC}"
    exit 1
fi

uv run image_optimizer.py "$INPUT_DIR" -o "$OUTPUT_DIR" -q "$QUALITY"

echo ""
echo -e "${GREEN}✅ Optimization complete!${NC}"
echo -e "${BLUE}💡 Check '$OUTPUT_DIR/responsive_examples.html' for usage examples${NC}"
echo -e "${YELLOW}📂 Optimized images are organized by original subfolder structure${NC}"
