import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def apply_filters(input_image_path, output_image_path, filter_type):
    # Read the input image
    image = cv2.imread(input_image_path)

    if image is None:
        print("The file could not be read. Please check the file path.")
        return

    # Apply selected filter
    if filter_type == "Sharpening":
        # Sharpening filter
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
        filtered_image = cv2.filter2D(image, -1, kernel)

    elif filter_type == "Smoothing":
        # Smoothing filter (Gaussian blur)
        filtered_image = cv2.GaussianBlur(image, (15, 15), 0)

    elif filter_type == "Edge Detection":
        # Edge detection filter
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        filtered_image = cv2.Canny(gray_image, 20, 80)

    elif filter_type == "Embossing":
        # Embossing filter
        kernel = np.array([[-2, -1, 0],
                           [-1, 1, 1],
                           [0, 1, 2]])
        filtered_image = cv2.filter2D(image, -1, kernel)

    else:
        print("Filter type not recognized.")
        return

    # Save the filtered image
    cv2.imwrite(output_image_path, filtered_image)

    return filtered_image

def convert_to_sketch(input_image_path, output_image_path):
    # Read the input image and convert to grayscale. Grayscale is used to simplify the image and focus on its intensity information.
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Gaussian blur. Gaussian blur is applied to the grayscale image to reduce noise. This smoothing process helps in getting more coherent edges.
    blur = cv2.GaussianBlur(image, (5, 5), 0)

    # Detect edges using Canny.
    edges = cv2.Canny(blur, 20, 80)

    # Find contours
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a white background
    white_background = np.ones_like(image) * 255

    # Create a sketch image with white background and black edges. The color 0 is specified, which corresponds to black in grayscale. This results in the edges being drawn in black on the white background.
    sketch = cv2.drawContours(white_background.copy(), contours, -1, 0, 1)

    # Save the final image with white background and black edges
    cv2.imwrite(output_image_path, sketch)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def process_image():
    input_path = input_entry.get()
    output_path = output_entry.get()
    filter_type = filter_var.get()
    sketch_mode = sketch_var.get()

    if sketch_mode:
        convert_to_sketch(input_path, output_path)
    else:
        apply_filters(input_path, output_path, filter_type)

    # Display the processed image
    processed_img = Image.open(output_path)
    processed_img.thumbnail((500, 500))
    processed_img = ImageTk.PhotoImage(processed_img)
    result_label.config(image=processed_img)
    result_label.image = processed_img

# Create the main window
root = tk.Tk()
root.title("Image Filter and Sketch Converter")

# Create and set filter options
filter_var = tk.StringVar()
filter_var.set("Sharpening")  # Default filter option

# Create and set sketch mode option
sketch_var = tk.BooleanVar()
sketch_var.set(False)  # Default: Filter Mode

# Create a label for filter selection
filter_label = tk.Label(root, text="Select a Filter:")
filter_label.pack()

# Create a dropdown menu for filter selection
filter_option_menu = tk.OptionMenu(root, filter_var, "Sharpening", "Smoothing", "Edge Detection", "Embossing")
filter_option_menu.pack()

# Create a radio button for selecting sketch mode
sketch_radio_button = tk.Checkbutton(root, text="Convert to Sketch", variable=sketch_var)
sketch_radio_button.pack()

# Create an entry for the input image path
input_label = tk.Label(root, text="Input Image:")
input_label.pack()
input_entry = tk.Entry(root)
input_entry.pack()
input_button = tk.Button(root, text="Browse", command=open_file)
input_button.pack()

# Create an entry for the output image path
output_label = tk.Label(root, text="Output Image:")
output_label.pack()
output_entry = tk.Entry(root)
output_entry.pack()

# Create a label for displaying the processed image
result_label = tk.Label(root, text="Processed Image")
result_label.pack()

# Create a button to process the image
process_button = tk.Button(root, text="Process Image", command=process_image)
process_button.pack()

root.mainloop()
