from PIL import Image
import random

def load_image(path):
    return Image.open(path)

def save_image(image, path):
    image.save(path)

def xor_pixel(pixel, key):
    return tuple([value ^ key for value in pixel])

def swap_pixels(pixels, width, height, seed):
    random.seed(seed)
    pixel_list = [(x, y) for y in range(height) for x in range(width)]
    random.shuffle(pixel_list)
    return pixel_list

def encrypt_image(image_path, key, output_path):
    image = load_image(image_path)
    image = image.convert("RGB")
    width, height = image.size
    pixels = image.load()

    shuffled_positions = swap_pixels(pixels, width, height, key)
    encrypted_image = Image.new("RGB", (width, height))
    encrypted_pixels = encrypted_image.load()

    for i, (x, y) in enumerate(shuffled_positions):
        original_pixel = pixels[x, y]
        encrypted_pixel = xor_pixel(original_pixel, key)
        target_x, target_y = i % width, i // width
        encrypted_pixels[target_x, target_y] = encrypted_pixel

    save_image(encrypted_image, output_path)
    print(f"Encrypted image saved to {output_path}")

def decrypt_image(image_path, key, output_path):
    image = load_image(image_path)
    image = image.convert("RGB")
    width, height = image.size
    pixels = image.load()

    shuffled_positions = swap_pixels(pixels, width, height, key)
    decrypted_image = Image.new("RGB", (width, height))
    decrypted_pixels = decrypted_image.load()

    for i, (x, y) in enumerate(shuffled_positions):
        source_x, source_y = i % width, i // width
        encrypted_pixel = pixels[source_x, source_y]
        original_pixel = xor_pixel(encrypted_pixel, key)
        decrypted_pixels[x, y] = original_pixel

    save_image(decrypted_image, output_path)
    print(f"Decrypted image saved to {output_path}")

# ==== Example Usage ====
if __name__ == "__main__":
    key = 123  # Choose any key (0-255)
    encrypt_image("input.jpg", key, "encrypted.png")
    decrypt_image("encrypted.png", key, "decrypted.jpg")
