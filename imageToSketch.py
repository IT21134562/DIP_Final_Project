import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk  # Import Image and ImageTk from the PIL library

def convert_to_sketch(input_image_path, output_image_path):
    # Read the input image and convert to grayscale
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(image, (5, 5), 0)

    # Detect edges using Canny
    edges = cv2.Canny(blur, 20, 80)

    # Find contours
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a white background
    white_background = np.ones_like(image) * 255

    # Create a sketch image with white background and black edges
    sketch = cv2.drawContours(white_background.copy(), contours, -1, 0, 1)

    # Save the final image with white background and black edges
    cv2.imwrite(output_image_path, sketch)

def browse_image():
    input_image_path = filedialog.askopenfilename()
    if input_image_path:
        output_image_path = "sketch_with_white_background.jpg"
        convert_to_sketch(input_image_path, output_image_path)

        # Open the sketch image using PIL and convert it to a Tkinter PhotoImage
        sketch_pil = Image.open(output_image_path)
        sketch_img = ImageTk.PhotoImage(sketch_pil)

        result_label.config(image=sketch_img)
        result_label.image = sketch_img  # Keep a reference to avoid garbage collection
        result_label.pack()
    else:
        result_label.config(text="No image selected.")

root = tk.Tk()
root.title("Sketch Converter")

browse_button = tk.Button(root, text="Browse Image", command=browse_image)
browse_button.pack()

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()

root.mainloop()
