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
        filtered_image = cv2.Canny(gray_image, 100, 200)

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

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def process_image():
    input_path = input_entry.get()
    output_path = output_entry.get()
    filter_type = filter_var.get()
    filtered_image = apply_filters(input_path, output_path, filter_type)
    
    # Display original image
    original_img = Image.open(input_path)
    original_img.thumbnail((200, 200))
    original_img = ImageTk.PhotoImage(original_img)
    original_label.config(image=original_img)
    original_label.image = original_img
    
    # Display processed image
    filtered_img = Image.open(output_path)
    filtered_img.thumbnail((200, 200))
    filtered_img = ImageTk.PhotoImage(filtered_img)
    filtered_label.config(image=filtered_img)
    filtered_label.image = filtered_img

# Create the main window
root = tk.Tk()
root.title("Image Filter App")

# Create and set filter options
filter_var = tk.StringVar()
filter_var.set("Sharpening")  # Default filter option

# Create a label for filter selection
filter_label = tk.Label(root, text="Select a Filter:")
filter_label.pack()

# Create a dropdown menu for filter selection
filter_option_menu = tk.OptionMenu(root, filter_var, "Sharpening", "Smoothing", "Edge Detection", "Embossing")
filter_option_menu.pack()

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

# Create labels for displaying original and filtered images
original_label = tk.Label(root, text="Original Image")
original_label.pack()
filtered_label = tk.Label(root, text="Filtered Image")
filtered_label.pack()

# Create a button to process the image
process_button = tk.Button(root, text="Process Image", command=process_image)
process_button.pack()

root.mainloop()
