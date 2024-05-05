import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Compressor")
        self.root.geometry("500x400")

        # Colors
        self.primary_color = "#2E8B57"  # Sea Green
        self.secondary_color = "#FFFFFF"  # White
        self.button_color = "#FFD700"  # Gold

        # Set up the main frame
        self.main_frame = tk.Frame(self.root, bg=self.primary_color, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title Label
        self.title_label = tk.Label(self.main_frame, text="Image Compressor", font=("Arial", 20), bg=self.primary_color, fg="black")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Upload Image Button
        self.upload_button = tk.Button(self.main_frame, text="Upload Image", command=self.upload_image, bg=self.button_color, fg="black", font=("Arial", 12, "bold"))
        self.upload_button.grid(row=1, column=0, pady=10, padx=5, sticky="ew")

        # Compress Buttons
        self.extreme_button = tk.Button(self.main_frame, text="Extreme Compression", command=lambda: self.compress_image(10), state=tk.DISABLED, bg=self.button_color, fg="black", font=("Arial", 12, "bold"))
        self.extreme_button.grid(row=2, column=0, pady=5, padx=5, sticky="ew")

        self.recommended_button = tk.Button(self.main_frame, text="Recommended Compression", command=lambda: self.compress_image(50), state=tk.DISABLED, bg=self.button_color, fg="black", font=("Arial", 12, "bold"))
        self.recommended_button.grid(row=3, column=0, pady=5, padx=5, sticky="ew")

        self.less_button = tk.Button(self.main_frame, text="Less Compression", command=lambda: self.compress_image(90), state=tk.DISABLED, bg=self.button_color, fg="black", font=("Arial", 12, "bold"))
        self.less_button.grid(row=4, column=0, pady=5, padx=5, sticky="ew")

        # Show Preview Button
        self.show_preview_button = tk.Button(self.main_frame, text="Show Preview", command=self.show_compressed_preview, state=tk.DISABLED, bg=self.button_color, fg="black", font=("Arial", 12, "bold"))
        self.show_preview_button.grid(row=5, column=0, pady=10, padx=5, sticky="ew")

        # Download Button
        self.download_button = tk.Button(self.main_frame, text="Download", command=self.download_image, state=tk.DISABLED, bg=self.button_color, fg="black", font=("Arial", 12, "bold"))
        self.download_button.grid(row=6, column=0, pady=10, padx=5, sticky="ew")

        

        # Image Frame
        self.image_frame = tk.Frame(self.main_frame, width=300, height=100, bd=2, relief="ridge", bg=self.secondary_color)
        self.image_frame.grid(row=1, column=1, rowspan=6, padx=10, pady=10, sticky="nsew")

        # Image Label
        self.image_label = tk.Label(self.image_frame, bg=self.secondary_color, text="See Preview Here", font=("Arial", 12, "italic"))
        self.image_label.pack(fill="both", expand=True)

        # Image paths
        self.original_image_path = None
        self.compressed_image_path = None
        self.compressed_photo = None

        # Configure grid weights
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure([1, 2, 3, 4, 5], weight=1)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[])
        if file_path:
            self.original_image_path = file_path
            self.show_original_preview()

    def show_original_preview(self):
        # Open the original image using Pillow
        image = Image.open(self.original_image_path)
          # Resize to fit in the label
        image = self.resize_image_to_frame(image)
        photo = ImageTk.PhotoImage(image)

        # Update the label with the original image
        self.image_label.config(image=photo)
        self.image_label.image = photo

        # Enable Compression Buttons
        self.extreme_button.config(state=tk.NORMAL)
        self.recommended_button.config(state=tk.NORMAL)
        self.less_button.config(state=tk.NORMAL)

    def compress_image(self, quality):
        if not self.original_image_path:
            messagebox.showerror("Error", "Please upload an image first.")
            return

        try:
            # Open the original image using Pillow
            image = Image.open(self.original_image_path)

            # Convert image to RGB mode if it has an alpha channel
            if image.mode == "RGBA":
                image = image.convert("RGB")
            # Compress the image
            compressed_image = image.copy()
            compressed_image.save("compressed_image.jpg", optimize=True, quality=quality)  # Save as compressed_image.jpg
            self.compressed_image_path = "compressed_image.jpg"

            messagebox.showinfo("Success", "Image compressed successfully!")

            # Enable Show Preview Button
            self.show_preview_button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_compressed_preview(self):
        if not self.compressed_image_path:
            messagebox.showerror("Error", "No compressed image available.")
            return

        # Open the compressed image using Pillow
        compressed_image = Image.open(self.compressed_image_path)
          # Resize to fit in the label
        compressed_image = self.resize_image_to_frame(compressed_image)
        self.compressed_photo = ImageTk.PhotoImage(compressed_image)

        # Update the label with the compressed image
        self.image_label.config(image=self.compressed_photo)

        # Enable Download Button
        self.download_button.config(state=tk.NORMAL)

        # Adjust coordinates to center the image
        x = (self.image_frame.winfo_width() - self.compressed_photo.width()) // 2
        y = (self.image_frame.winfo_height() - self.compressed_photo.height()) // 2
        self.image_label.place(x=x, y=y)
    def resize_image_to_frame(self, image):
        # Get the dimensions of the white frame
        frame_width = self.image_frame.winfo_width()
        frame_height = self.image_frame.winfo_height()

        # Resize the image to fit the dimensions of the white frame
        image = image.resize((frame_width, frame_height))


        return image
    
    def download_image(self):
        if not self.compressed_image_path:
            messagebox.showerror("Error", "No compressed image available.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if save_path:
            import shutil
            shutil.copyfile(self.compressed_image_path, save_path)
            messagebox.showinfo("Saved", f"Compressed image saved at {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCompressorApp(root)
    root.mainloop()