import argparse
import io
import os
import sys
import time
from dotenv import load_dotenv
from PIL import Image
from google import genai

MODEL_NAME = "gemini-2.5-flash-image"


def generate_image(prompt: str, output_dir: str):
    """
    Generates an image using the Google Generative AI model.

    Args:
        prompt: The prompt for generating the image.
        output_dir: Directory to save the generated image.
    """
    try:
        client = genai.GenerativeModel(model=MODEL_NAME)

        print(f"Generating image with prompt: {prompt}")

        response = client.generate_content(
            contents=[prompt],
            generation_config=genai.GenerationConfig(
                response_mime_type="image/png",
            ),
        )

        if response.candidates and response.candidates[0].content.parts:
            for i, part in enumerate(response.candidates[0].content.parts):
                if part.inline_data:
                    image_data = part.inline_data.data
                    image = Image.open(io.BytesIO(image_data))
                    timestamp = int(time.time())
                    file_name = os.path.join(
                        output_dir, f"generated_image_{timestamp}_{i}.png"
                    )
                    image.save(file_name)
                    print(f"Image successfully generated and saved to {file_name}")
                elif part.text:
                    print(f"Text response received: {part.text}")
        else:
            print("No image data found in the response.")
            if response.prompt_feedback:
                print(f"Prompt feedback: {response.prompt_feedback}")

    except Exception as e:
        print(f"An error occurred: {e}")


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

    if args.prompt_file:
        with open(args.prompt_file, "r") as f:
            final_prompt = f.read()
    else:
        final_prompt = args.prompt

    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    generate_image(
        prompt=final_prompt,
        output_dir=output_dir,
    )


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    cli(sys.argv[1:])


if __name__ == "__main__":
    main()
