import os
import random
from PIL import Image, ImageEnhance, ImageFilter

# === Configuration ===
input_dir = 'train (1)/train'
output_dir = 'simpson_train_augmented'
target_images_per_class = 5000  # 🔧 Set your target per character class

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Augmentation functions
def augment_image(img):
    operations = []

    # Random rotation
    angle = random.randint(-25, 25)
    operations.append(img.rotate(angle))

    # Sharpening
    operations.append(img.filter(ImageFilter.SHARPEN))

    # Contrast enhancement
    contrast = ImageEnhance.Contrast(img)
    operations.append(contrast.enhance(1.5))

    # Horizontal flip
    operations.append(img.transpose(Image.FLIP_LEFT_RIGHT))

    # Slight brightness change
    brightness = ImageEnhance.Brightness(img)
    operations.append(brightness.enhance(random.uniform(0.8, 1.2)))

    return operations

# Go through each character folder
for character in os.listdir(input_dir):
    char_input_path = os.path.join(input_dir, character)
    if not os.path.isdir(char_input_path):
        continue

    char_output_path = os.path.join(output_dir, character)
    os.makedirs(char_output_path, exist_ok=True)

    images = [f for f in os.listdir(char_input_path) if f.lower().endswith(('.jpg', '.png'))]
    original_count = len(images)

    print(f"[{character}] Found {original_count} images")

    if original_count >= target_images_per_class:
        # Just copy the originals if enough exist
        for img_name in images:
            img_path = os.path.join(char_input_path, img_name)
            try:
                img = Image.open(img_path).convert('RGB')
                img.save(os.path.join(char_output_path, img_name))
            except:
                continue
        continue

    # Copy originals
    for img_name in images:
        img_path = os.path.join(char_input_path, img_name)
        try:
            img = Image.open(img_path).convert('RGB')
            img.save(os.path.join(char_output_path, img_name))
        except:
            continue

    # Start augmenting
    img_index = 0
    while len(os.listdir(char_output_path)) < target_images_per_class:
        base_img_name = images[img_index % original_count]
        base_img_path = os.path.join(char_input_path, base_img_name)

        try:
            base_img = Image.open(base_img_path).convert('RGB')
            augmented_imgs = augment_image(base_img)
        except:
            img_index += 1
            continue

        for aug_img in augmented_imgs:
            if len(os.listdir(char_output_path)) >= target_images_per_class:
                break
            aug_name = f"{base_img_name[:-4]}_aug{random.randint(10000,99999)}.jpg"
            aug_img.save(os.path.join(char_output_path, aug_name))

        img_index += 1

    print(f"  → Augmented to {len(os.listdir(char_output_path))} images")

