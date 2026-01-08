import os

from PIL import Image

input_path = "images/profile.png"
original_size = os.path.getsize(input_path)

with Image.open(input_path) as img:
    for size in [512, 256]:
        output_path = f"images/profile_icon{size}.webp"
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(output_path, quality=80)
        new_size = os.path.getsize(output_path)
        print(
            f"✓ {size}x{size}: {new_size:,} bytes ({100 * (original_size - new_size) / original_size:.1f}% 削減)"
        )
