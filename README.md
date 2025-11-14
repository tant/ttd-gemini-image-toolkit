# Image Generator Tool

This tool generates images using Google Gemini AI for blog post covers.

## Setup

### Prerequisites
- Python 3.10 or higher
- `uv` package manager

### Installation

uv sync
```

### Configuration

Set your Google Gemini API key in `.env`:

```bash
GEMINI_API_KEY="your-api-key-here"
```

## Usage

Run the image generator directly:

```bash
uv run python image_generator.py --prompt "Your prompt here"
```

Or with a prompt from a file:

```bash
uv run python image_generator.py --prompt-file prompt.txt
```

## Options

- `--prompt TEXT` - Text prompt for image generation
- `--prompt-file PATH` - Read prompt from file
- `--output-dir PATH` - Directory to save images (default: "output")

## Model

Uses `gemini-2.5-flash-image-preview` model for fast, high-quality image generation.





## Troubleshooting

### API Key Issues
- Verify your `.env` file has the correct API key
- Check the API key has Gemini API access enabled

### Module Not Found
```bash
uv sync
```



## License

Same as parent project.
