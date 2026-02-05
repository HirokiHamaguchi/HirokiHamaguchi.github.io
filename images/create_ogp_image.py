import os

from PIL import Image


def create_ogp_image():
    # Input and output paths
    input_path = os.path.join(os.path.dirname(__file__), "profile_black.webp")
    output_path = os.path.join(os.path.dirname(__file__), "profile_black_OGP.webp")

    # OGP standard dimensions
    ogp_width = 1200
    ogp_height = 630

    # Load the original image
    img = Image.open(input_path)
    print(f"Original image size: {img.size}")

    # Create a new image with black background (1200x630)
    ogp_img = Image.new("RGB", (ogp_width, ogp_height), color="black")

    # Convert input image to RGB if it has alpha channel
    if img.mode in ("RGBA", "LA", "P"):
        rgb_img = Image.new("RGB", img.size, color="black")
        rgb_img.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
        img = rgb_img

    # Resize image to fit the OGP height while maintaining aspect ratio
    # Scale to fill the height with some margin
    scale_factor = ogp_height / img.size[1]
    new_width = int(img.size[0] * scale_factor)
    new_height = int(img.size[1] * scale_factor)
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Calculate position to center the resized image
    x = (ogp_width - new_width) // 2
    y = (ogp_height - new_height) // 2

    # Paste the resized image onto the black background
    ogp_img.paste(img_resized, (x, y))

    # Save the result
    ogp_img.save(output_path, "WEBP", quality=95)
    print(f"OGP image created: {output_path}")
    print(f"Size: {ogp_width}x{ogp_height}")


if __name__ == "__main__":
    create_ogp_image()
