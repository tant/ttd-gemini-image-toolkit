# Image Generator Tool

This tool generates images using Google Gemini AI for blog post covers.

## Setup

### Prerequisites
- Python 3.10 or higher
- `uv` package manager (installed at `/home/tan/.local/bin/uv`)

### Installation

Using uv:
```bash
cd tools/image-generator
/home/tan/.local/bin/uv sync
```

### Configuration

Set your Google Gemini API key in `.env`:

```bash
GEMINI_API_KEY="your-api-key-here"
```

## Usage

### Via Blog Script (Recommended)

Use the blog cover generation script:

```bash
# From project root
./scripts/generate-blog-cover.sh <blog-slug>
```

Example:
```bash
./scripts/generate-blog-cover.sh gioi-thieu-ve-data-platform
```

### Direct Usage

Run the image generator directly:

```bash
cd tools/image-generator
/home/tan/.local/bin/uv run python image_generator.py --prompt "Your prompt here" --output-dir ../../public/blog
```

### With Prompt File

```bash
cd tools/image-generator
echo "A modern data platform architecture" > prompt.txt
/home/tan/.local/bin/uv run python image_generator.py --prompt-file prompt.txt --output-dir ../../public/blog
```

## Options

- `--prompt TEXT` - Text prompt for image generation
- `--prompt-file PATH` - Read prompt from file
- `--output-dir PATH` - Directory to save images (default: "output")

## Model

Uses `gemini-2.5-flash-image-preview` model for fast, high-quality image generation.

## Output

Generated images are saved with timestamp initially, then:
- Converted to optimized WebP format
- Original PNG is deleted to save space
- Final size: ~20-70KB (95% smaller than original)

## Integration with Project

This tool is integrated into the blog workflow:

1. Add `imagePrompt` field to blog post frontmatter
2. Run `./scripts/generate-blog-cover.sh <slug>`
3. Image is generated and saved to `public/blog/`
4. Run `./scripts/optimize-blog-images.sh` to create WebP versions

## Troubleshooting

### API Key Issues
- Verify your `.env` file has the correct API key
- Check the API key has Gemini API access enabled

### Module Not Found
```bash
cd tools/image-generator
/home/tan/.local/bin/uv sync
```

### Permission Errors
```bash
chmod +x ../../scripts/generate-blog-cover.sh
```

## License

Same as parent project.
