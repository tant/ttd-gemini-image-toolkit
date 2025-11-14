# TTD Gemini Image Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

The TTD Gemini Image Toolkit is a powerful command-line interface (CLI) tool designed for seamless interaction with Google Gemini AI for image generation, manipulation, and generative editing. This toolkit empowers users to create new images from text prompts, add text overlays to existing images, and intelligently refine or edit images through a two-step generative process.

## Repository

**GitHub:** [https://github.com/tant/ttd-gemini-image-toolkit](https://github.com/tant/ttd-gemini-image-toolkit)

## Features

*   **Image Generation:** Create diverse images from descriptive text prompts using `gemini-2.5-flash-image`.
*   **Text Overlay:** Add custom text to existing images with options for font size, color, and precise positioning.
*   **Generative Refinement:** Refine images by providing a prompt that guides the AI to generate a new image incorporating desired changes (e.g., "make the sky bluer").
*   **Generative Editing:** Edit images by instructing the AI to replace or modify elements within an image (e.g., "remove the car and replace it with a bicycle").
*   **Flexible Input:** Generate images from direct prompts or content from a file.
*   **Output Management:** Specify output directories for organized storage of generated and edited images.
*   **Standalone Executables:** Package the application into a single executable for easy distribution and use without a Python environment.

## Setup

### Prerequisites
- Python 3.10 or higher
- `uv` package manager

### Installation

```bash
uv sync
```

### Configuration

Set your Google Gemini API key in a `.env` file in the project root:

```
GEMINI_API_KEY="your-api-key-here"
```

## Usage

The `ttd_gemini_image_toolkit.py` script uses subcommands to perform different operations.

### Generate Images

Generate a new image from a text prompt:

```bash
uv run python ttd_gemini_image_toolkit.py generate --prompt "Your prompt here"
```

Or with a prompt from a file:

```bash
uv run python ttd_gemini_image_toolkit.py generate --prompt-file prompt.txt
```

You can specify an output directory (defaults to `output`):

```bash
uv run python ttd_gemini_image_toolkit.py generate --prompt "A serene landscape" --output-dir my_images
```

### Add Text to an Image

Add text to an existing image:

```bash
uv run python ttd_gemini_image_toolkit.py add-text --input-image path/to/your_image.png --text "My Blog Title"
```

You can customize font size, color, and position:

```bash
uv run python ttd_gemini_image_toolkit.py add-text --input-image path/to/your_image.png --text "Important Note" --font-size 36 --color "red" --position "top-right" --output-dir edited_images
```

Available positions: `top-left`, `top-center`, `top-right`, `middle-left`, `center`, `middle-right`, `bottom-left`, `bottom-center`, `bottom-right`.

### Refine and Edit Images

The `refine` and `edit` subcommands allow you to modify existing images using a two-step generative process:

1.  **Analyze and Describe:** The input image and your prompt/instruction are sent to the `gemini-pro-vision` model, which generates a detailed text description of a *new image* incorporating your requested changes.
2.  **Generate New Image:** This text description is then used as a prompt for the `gemini-2.5-flash-image` model to generate the final, modified image.

**Refine an image:**

```bash
uv run python ttd_gemini_image_toolkit.py refine --input-image path/to/original.png --prompt "make the sky bluer and add a rainbow" --output-dir refined_images
```

**Edit an image:**

```bash
uv run python ttd_gemini_image_toolkit.py edit --input-image path/to/original.png --instruction "remove the car and replace it with a bicycle" --output-dir edited_images
```

**Important Note:** This process generates a *new image* based on a text interpretation of your request, rather than directly modifying the pixels of the original image. The output may vary based on the clarity of your prompt and the model's interpretation.

## Model

Uses `gemini-2.5-flash-image` model for fast, high-quality image generation.

## Troubleshooting

### API Key Issues
- Verify your `.env` file has the correct API key
- Check the API key has Gemini API access enabled

### Module Not Found
- Ensure all dependencies are installed:
  ```bash
  uv sync
  ```
- Make sure you are running the script using `uv run python ttd_gemini_image_toolkit.py ...`

After installation, you can run the script using `uv run python ttd_gemini_image_toolkit.py <command> ...`

## Generating Standalone Executables

You can package this application into a standalone executable that can be run without a Python installation. This is done using PyInstaller.

**Important Note:** PyInstaller creates executables specific to the operating system it is run on. To get an executable for Windows, you must run PyInstaller on a Windows machine. Similarly, for macOS, you must run it on a macOS machine.

### Prerequisites for Executable Generation

1.  **Python and `uv`**: Ensure Python (3.10+) and `uv` are installed on the target OS.
2.  **PyInstaller**: Install PyInstaller into your project's virtual environment:
    ```bash
    uv pip install pyinstaller
    ```
3.  **System Dependencies (Linux only)**: On Linux, you might need `binutils` (which provides `objdump`). Install it using your distribution's package manager (e.g., `sudo apt-get install binutils` on Debian/Ubuntu).

### Steps to Generate Executable

1.  **Navigate to the project directory.**
2.  **Activate your virtual environment** (if not already active, though `uv run` handles this).
3.  **Run PyInstaller**:
    ```bash
    .venv/bin/pyinstaller --onefile --name ttd_gemini_image_toolkit --add-data ".env.sample:." ttd_gemini_image_toolkit.py
    ```
    *   `--onefile`: Packages the application into a single executable file.
    *   `--name ttd_gemini_image_toolkit`: Sets the name of the executable.
    *   `--add-data ".env.sample:."`: Includes the `.env.sample` file, making it accessible to the executable.

### Locating the Executable

After a successful build, the executable will be found in the `dist/` directory within your project folder. For example, on Linux, it will be `dist/ttd_gemini_image_toolkit`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. Copyright (c) 2025 Tan Tran.

## Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please open an issue or submit a pull request on the [GitHub repository](https://github.com/tant/ttd-gemini-image-toolkit).

## Contact

For questions or support, please open an issue on the [GitHub repository](https://github.com/tant/ttd-gemini-image-toolkit).
