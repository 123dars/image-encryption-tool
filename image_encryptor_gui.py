import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random
import os

# ==== Image Operations ====

def xor_pixel(pixel, key):
    return tuple([value ^ key for value in pixel])

def swap_pixels(width, height, seed):
    random.seed(seed)
    pixel_list = [(x, y) for y in range(height) for x in range(width)]
    random.shuffle(pixel_list)
    return pixel_list

def process_image(path, key, mode):
    image = Image.open(path).convert("RGB")
    width, height = image.size
    pixels = image.load()
    positions = swap_pixels(width, height, key)

    new_img = Image.new("RGB", (width, height))
    new_pixels = new_img.load()

    for i, (x, y) in enumerate(positions):
        if mode == "encrypt":
            pixel = xor_pixel(pixels[x, y], key)
            target_x, target_y = i % width, i // width
            new_pixels[target_x, target_y] = pixel
        else:  # decrypt
            source_x, source_y = i % width, i // width
            pixel = xor_pixel(pixels[source_x, source_y], key)
            new_pixels[x, y] = pixel

    return new_img

# ==== GUI ====

class ImageEncryptorGUI:
    def __init__(self, master):
        self.master = master
        master.title("🔐 Image Encryption Tool")

        self.path = None

        self.label = tk.Label(master, text="Select an image to encrypt or decrypt:")
        self.label.pack(pady=10)

        self.browse_button = tk.Button(master, text="📁 Browse Image", command=self.browse_file)
        self.browse_button.pack(pady=5)

        self.key_label = tk.Label(master, text="Enter numeric key (0-255):")
        self.key_label.pack()

        self.key_entry = tk.Entry(master)
        self.key_entry.pack(pady=5)

        self.encrypt_button = tk.Button(master, text="🔒 Encrypt", command=self.encrypt_image)
        self.encrypt_button.pack(pady=5)

        self.decrypt_button = tk.Button(master, text="🔓 Decrypt", command=self.decrypt_image)
        self.decrypt_button.pack(pady=5)

        self.status = tk.Label(master, text="", fg="green")
        self.status.pack(pady=10)

    def browse_file(self):
        self.path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.path:
            self.status.config(text=f"Selected: {os.path.basename(self.path)}")

    def encrypt_image(self):
        self.process("encrypt")

    def decrypt_image(self):
        self.process("decrypt")

    def process(self, mode):
        if not self.path:
            messagebox.showerror("Error", "No image selected!")
            return

        try:
            key = int(self.key_entry.get())
            if not (0 <= key <= 255):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric key (0-255)!")
            return

        output_path = os.path.splitext(self.path)[0] + f"_{mode}.png"
        try:
            result_img = process_image(self.path, key, mode)
            result_img.save(output_path)
            messagebox.showinfo("Success", f"{mode.capitalize()}ed image saved as:\n{output_path}")
            self.status.config(text=f"{mode.capitalize()}ed: {os.path.basename(output_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image:\n{str(e)}")

# ==== Run App ====

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    app = ImageEncryptorGUI(root)
    root.mainloop()
