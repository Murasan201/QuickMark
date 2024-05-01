
import os
from PIL import Image, ImageDraw, ImageFont

# Constants
FONT_PATH = 'arial.ttf'  # Path to the font file
FONT_SIZE = 36  # Font size
WATERMARK_TEXT = 'Sample Watermark'  # Watermark text (English)
WATERMARK_POSITION = 2  # Watermark position: 1 = Top, 2 = Center, 3 = Bottom
TRANSPARENCY = 50  # Watermark transparency (100=opaque, 0=transparent)
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp']  # Supported image file extensions

def add_watermark(image_path, output_path):
    # Open the image file and convert to RGBA
    with Image.open(image_path).convert("RGBA") as base:
        # Create a transparent layer for the watermark
        watermark_layer = Image.new("RGBA", base.size)
        draw = ImageDraw.Draw(watermark_layer)
        # Set up the font
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        # Calculate the text bounding box to get text size
        text_bbox = draw.textbbox((0, 0), WATERMARK_TEXT, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        # Calculate watermark position
        if WATERMARK_POSITION == 1:
            position = ((base.width - text_width) / 2, (base.height / 4) - text_height / 2)
        elif WATERMARK_POSITION == 2:
            position = ((base.width - text_width) / 2, (base.height / 2) - text_height / 2)
        elif WATERMARK_POSITION == 3:
            position = ((base.width - text_width) / 2, (3 * base.height / 4) - text_height / 2)
        # Draw the watermark with specified transparency
        draw.text(position, WATERMARK_TEXT, font=font, fill=(255, 255, 255, int(255 * TRANSPARENCY / 100)))
        # Composite the watermark layer onto the original image and convert to RGB
        combined = Image.alpha_composite(base, watermark_layer).convert("RGB")
        # Save the final image in JPEG format
        combined.save(output_path, 'JPEG')

def process_directory(directory_path):
    # Set the path for the output directory
    output_directory = os.path.join(directory_path, "watermarked_images")
    # Create the output directory if it does not exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    # Process all files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        # Process only supported image file formats
        if os.path.isfile(file_path) and any(file_path.endswith(ext) for ext in IMAGE_EXTENSIONS):
            output_path = os.path.join(output_directory, f"wm_{filename}")
            add_watermark(file_path, output_path)
            print(f"Processed {filename}")

if __name__ == '__main__':
    # Prompt the user to enter the directory path where images are stored
    directory_path = input("Enter the path to the directory containing the images: ")
    process_directory(directory_path)
