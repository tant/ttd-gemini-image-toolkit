import argparse
import mimetypes
import os
import sys
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

MODEL_NAME = "gemini-2.5-flash-image-preview"


def generate_image(
    prompt: str,
    output_dir: str,
):
    """
    Generates an image using the Google Generative AI model.

    Args:
        prompt: The prompt for generating the image.
        output_dir: Directory to save the generated image.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    client = genai.Client(api_key=api_key)

    contents = [genai.types.Part.from_text(text=prompt)]

    generate_content_config = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
    )

    print(f"Generating image with prompt: {prompt}")

    stream = client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=contents,
        config=generate_content_config,
    )

    _process_api_stream_response(stream, output_dir)


def _process_api_stream_response(stream, output_dir: str):
    """Processes the streaming response from the GenAI API, saving images and printing text."""
    file_index = 0
    for chunk in stream:
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue

        for part in chunk.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                timestamp = int(time.time())
                file_extension = mimetypes.guess_extension(part.inline_data.mime_type)
                file_name = os.path.join(
                    output_dir,
                    f"generated_image_{timestamp}_{file_index}{file_extension}",
                )
                _save_binary_file(file_name, part.inline_data.data)
                file_index += 1


def _save_binary_file(file_name: str, data: bytes):
    """Saves binary data to a specified file."""
    with open(file_name, "wb") as f:
        f.write(data)
    print(file_name)


def cli(argv):
    parser = argparse.ArgumentParser(
        description="Generate images using Google Generative AI."
    )
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument(
        "--prompt",
        type=str,
        help="Prompt for generating the image.",
    )
    prompt_group.add_argument(
        "--prompt-file",
        type=str,
        help="Path to a text file containing the prompt.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory to save the generated images.",
    )

    args = parser.parse_args(argv)

    # Determine the prompt
    if args.prompt_file:
        with open(args.prompt_file, "r") as f:
            final_prompt = f.read()
    else:
        final_prompt = args.prompt

    # Ensure output directory exists
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    generate_image(
        prompt=final_prompt,
        output_dir=output_dir,
    )


def main():
    load_dotenv()
    cli(sys.argv[1:])


if __name__ == "__main__":
    main()