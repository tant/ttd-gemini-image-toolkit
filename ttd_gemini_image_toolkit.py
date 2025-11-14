import argparse
import io
import os
import sys
import time
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from google import genai
from google.genai import types

MODEL_NAME = "imagen-4.0-generate-001"
VISION_MODEL_NAME = "gemini-pro-vision" # New constant for vision model


def generate_image_core(
    prompt: str,
    output_dir: str,
    model: str = MODEL_NAME,
    number_of_images: int = 1,
    image_size: str = "1K",
    person_generation: str = "allow_adult",
):
    """
    Generates an image using the Google Generative AI Imagen v4 models.

    Args:
        prompt: The prompt for generating the image.
        output_dir: Directory to save the generated image.
        model: Imagen model to use (e.g. imagen-4.0-generate-001).
        number_of_images: How many images to request (1-4).
        image_size: `1K` or `2K` (if supported by the model).
        person_generation: `dont_allow`, `allow_adult`, or `allow_all`.
    """
    try:
        client = genai.Client()

        print(
            f"Generating image with model={model}, image_size={image_size}, number_of_images={number_of_images}"
        )

        config = types.GenerateImagesConfig(
            number_of_images=number_of_images,
            image_size=image_size,
            person_generation=person_generation,
        )

        response = client.models.generate_images(model=model, prompt=prompt, config=config)

        if getattr(response, "generated_images", None):
            for i, gen_img in enumerate(response.generated_images):
                try:
                    img_val = getattr(gen_img, "image", None)
                    if img_val is None:
                        print(f"Generated image {i} has no .image attribute; skipping.")
                        continue

                    # If SDK returns raw bytes
                    if isinstance(img_val, (bytes, bytearray)):
                        image = Image.open(io.BytesIO(img_val))
                    else:
                        # If it's already a PIL Image-like object, try to use it directly
                        try:
                            image = img_val
                        except Exception:
                            # Fallback: try to read a data attribute
                            data = getattr(img_val, "data", None)
                            if isinstance(data, (bytes, bytearray)):
                                image = Image.open(io.BytesIO(data))
                            else:
                                raise

                    timestamp = int(time.time())
                    file_name = os.path.join(output_dir, f"generated_image_{timestamp}_{i}.png")
                    image.save(file_name)
                    print(f"Image successfully generated and saved to {file_name}")
                except Exception as e:
                    print(f"Failed to save generated image {i}: {e}")
        else:
            print("No generated_images found in response.")

    except Exception as e:
        print(f"An error occurred: {e}")


def _get_image_description_from_vision_model(image_path: str, user_instruction: str) -> str:
    """
    Sends an image and a user instruction to the gemini-pro-vision model
    to get a text description of a new image incorporating the changes.
    """
    try:
        vision_client = genai.GenerativeModel(model=VISION_MODEL_NAME)
        img = Image.open(image_path)

        # Prepare the content for the vision model
        # The prompt instructs the model to describe a new image based on the original and user's request
        prompt_parts = [
            img,
            f"Based on this image, describe a new image that incorporates the following change: '{user_instruction}'. "
            "Provide a detailed and creative text description suitable for an image generation model. "
            "Focus on how the new image should look, including style, elements, and overall mood, "
            "as if you are giving instructions to an artist to create a new image from scratch. "
            "Do not mention the original image or the editing process. Just describe the final desired image."
        ]

        print(f"Analyzing image and instruction with {VISION_MODEL_NAME}...")
        response = vision_client.generate_content(prompt_parts)
        description = response.text.strip()
        print(f"Received description from vision model: {description[:100]}...") # Print first 100 chars
        return description

    except Exception as e:
        print(f"Error getting image description from vision model: {e}")
        return ""


def generate_image_command(args):
    """Handles the 'generate' subcommand."""
    if args.prompt_file:
        with open(args.prompt_file, "r") as f:
            final_prompt = f.read()
    else:
        final_prompt = args.prompt

    os.makedirs(args.output_dir, exist_ok=True)
    generate_image_core(
        prompt=final_prompt,
        output_dir=args.output_dir,
        model=args.model,
        number_of_images=args.number_of_images,
        image_size=args.image_size,
        person_generation=args.person_generation,
    )


def _add_text_to_image(
    image_path: str,
    text: str,
    font_size: int,
    color: str,
    position: str,
    output_dir: str,
):
    """Adds text to an image and saves the result."""
    try:
        img = Image.open(image_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # Try to load a default font, or use a generic one
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
            print("Warning: arial.ttf not found, using default font.")

        # Calculate text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate position
        img_width, img_height = img.size
        x, y = 0, 0

        if "center" in position:
            x = (img_width - text_width) / 2
        elif "right" in position:
            x = img_width - text_width - 10  # 10 pixels padding
        else:  # default to left
            x = 10

        if "middle" in position:
            y = (img_height - text_height) / 2
        elif "bottom" in position:
            y = img_height - text_height - 10
        else:  # default to top
            y = 10

        draw.text((x, y), text, font=font, fill=color)

        # Save the modified image
        base_name = os.path.basename(image_path)
        name, ext = os.path.splitext(base_name)
        output_file_name = os.path.join(output_dir, f"{name}_with_text{ext}")
        img.save(output_file_name)
        print(f"Text successfully added and saved to {output_file_name}")

    except Exception as e:
        print(f"Error adding text to image: {e}")


def add_text_command(args):
    """Handles the 'add-text' subcommand."""
    os.makedirs(args.output_dir, exist_ok=True)
    _add_text_to_image(
        image_path=args.input_image,
        text=args.text,
        font_size=args.font_size,
        color=args.color,
        position=args.position,
        output_dir=args.output_dir,
    )


def refine_image_command(args):
    """Handles the 'refine' subcommand."""
    os.makedirs(args.output_dir, exist_ok=True)
    print(f"Attempting to refine image: {args.input_image} with prompt: '{args.prompt}'")
    
    # Step 1: Get a text description of the refined image from gemini-pro-vision
    refined_description = _get_image_description_from_vision_model(
        image_path=args.input_image,
        user_instruction=args.prompt
    )

    if refined_description:
        # Step 2: Generate a new image using the text description
        generate_image_core(prompt=refined_description, output_dir=args.output_dir)
    else:
        print("Failed to get a refined description from the vision model. Image generation aborted.")


def edit_image_command(args):
    """Handles the 'edit' subcommand."""
    os.makedirs(args.output_dir, exist_ok=True)
    print(f"Attempting to edit image: {args.input_image} with instruction: '{args.instruction}'")

    # Step 1: Get a text description of the edited image from gemini-pro-vision
    edited_description = _get_image_description_from_vision_model(
        image_path=args.input_image,
        user_instruction=args.instruction
    )

    if edited_description:
        # Step 2: Generate a new image using the text description
        generate_image_core(prompt=edited_description, output_dir=args.output_dir)
    else:
        print("Failed to get an edited description from the vision model. Image generation aborted.")


def cli(argv):
    parser = argparse.ArgumentParser(
        description="Generate and manipulate images using Google Generative AI."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate subcommand
    generate_parser = subparsers.add_parser(
        "generate", help="Generate a new image from a text prompt."
    )
    prompt_group = generate_parser.add_mutually_exclusive_group(required=True)
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
    generate_parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory to save the generated images.",
    )
    generate_parser.add_argument(
        "--model",
        type=str,
        default=MODEL_NAME,
        help="Imagen model to use (e.g. imagen-4.0-generate-001).",
    )
    generate_parser.add_argument(
        "--number-of-images",
        type=int,
        default=1,
        choices=[1, 2, 3, 4],
        help="Number of images to generate (1-4).",
    )
    generate_parser.add_argument(
        "--image-size",
        type=str,
        default="1K",
        choices=["1K", "2K"],
        help="Image size to request (1K or 2K).",
    )
    generate_parser.add_argument(
        "--person-generation",
        type=str,
        default="allow_adult",
        choices=["dont_allow", "allow_adult", "allow_all"],
        help="Controls generation of people in images.",
    )
    generate_parser.set_defaults(func=generate_image_command)

    # Refine subcommand
    refine_parser = subparsers.add_parser(
        "refine", help="Refine an existing image with a new prompt."
    )
    refine_parser.add_argument(
        "--input-image", type=str, help="Path to the image to refine.", required=True
    )
    refine_parser.add_argument(
        "--prompt", type=str, help="Refinement prompt.", required=True
    )
    refine_parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory to save the refined image.",
    )
    refine_parser.set_defaults(func=refine_image_command)

    # Add-text subcommand
    add_text_parser = subparsers.add_parser("add-text", help="Add text to an image.")
    add_text_parser.add_argument(
        "--input-image",
        type=str,
        help="Path to the image to add text to.",
        required=True,
    )
    add_text_parser.add_argument(
        "--text", type=str, help="Text to add to the image.", required=True
    )
    add_text_parser.add_argument(
        "--font-size", type=int, default=24, help="Font size of the text."
    )
    add_text_parser.add_argument(
        "--color", type=str, default="white", help="Color of the text (e.g., 'red', '#FFFFFF')."
    )
    add_text_parser.add_argument(
        "--position",
        type=str,
        default="bottom-center",
        help="Position of the text (e.g., 'top-left', 'center').",
    )
    add_text_parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory to save the image with text.",
    )
    add_text_parser.set_defaults(func=add_text_command)

    # Edit subcommand
    edit_parser = subparsers.add_parser(
        "edit", help="Edit an existing image based on an instruction."
    )
    edit_parser.add_argument(
        "--input-image", type=str, help="Path to the image to edit.", required=True
    )
    edit_parser.add_argument(
        "--instruction",
        type=str,
        help="Editing instruction (e.g., 'remove the car').",
        required=True,
    )
    edit_parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory to save the edited image.",
    )
    edit_parser.set_defaults(func=edit_image_command)

    args = parser.parse_args(argv)

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    cli(sys.argv[1:])


if __name__ == "__main__":
    main()