import os
import cairosvg
from PIL import Image, ImageDraw

svg_file = os.path.join(os.path.dirname(__file__), "graduation-cap-solid.svg")

icon_sizes = {
    "favicon.ico": (64, 64),
    "apple-touch-icon-57x57.png": (57, 57),
    "apple-touch-icon-60x60.png": (60, 60),
    "apple-touch-icon-72x72.png": (72, 72),
    "apple-touch-icon-76x76.png": (76, 76),
    "apple-touch-icon-114x114.png": (114, 114),
    "apple-touch-icon-120x120.png": (120, 120),
    "apple-touch-icon-144x144.png": (144, 144),
    "apple-touch-icon-152x152.png": (152, 152),
    "apple-touch-icon-180x180.png": (180, 180),
    "favicon-16x16.png": (16, 16),
    "favicon-32x32.png": (32, 32),
    "favicon-96x96.png": (96, 96),
}

base_size = 512
temp_png = os.path.join(os.path.dirname(__file__), "original.png")

cairosvg.svg2png(
    url=svg_file,
    write_to=temp_png,
    output_width=base_size,
    output_height=base_size,
)

img = Image.open(temp_png).convert("RGBA")

img = Image.blend(img, Image.new("RGBA", img.size, (0, 0, 255, 0)), 0.03)

width, height = base_size, base_size
background = Image.new("RGBA", (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(background)
draw.ellipse((0, 0, width, height), fill=(255, 255, 255, 255))
resized_img = img.resize((int(0.8 * width), int(0.8 * height)), Image.LANCZOS)
background.paste(resized_img, (int(0.1 * width), int(0.1 * height)), resized_img)
img = background

for filename, size in icon_sizes.items():
    output_img = img.resize(size, Image.LANCZOS)
    output_img.save(
        os.path.join(os.path.dirname(__file__), filename),
        format="PNG" if filename.endswith(".png") else "ICO",
    )
