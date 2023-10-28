#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
import numpy as np

# Read the image
image = cv2.imread('C:/Users/Vidula Adikari/Downloads/ai.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
gray_blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Define a threshold for the foreground and background
foreground_threshold = 150  # You can adjust this threshold value
background_threshold = 50   # You can adjust this threshold value

# Create masks for the foreground and background
foreground_mask = (gray_blurred > foreground_threshold).astype(np.int32)
background_mask = (gray_blurred < background_threshold).astype(np.int32)

# Set markers based on the masks
marker = np.zeros_like(gray, dtype=np.int32)
marker[foreground_mask == 1] = 1  # Mark foreground as 1
marker[background_mask == 1] = 2  # Mark background as 2

# Apply the watershed algorithm
cv2.watershed(image, marker)

# Visualize the segmented image
segmented_image = np.zeros_like(image, dtype=np.uint8)
segmented_image[marker == 1] = [0, 0, 255]  # Mark the foreground in red
segmented_image[marker == 2] = [0, 255, 0]  # Mark the background in green

# Display the segmented image
cv2.imshow('Segmented Image', segmented_image)
cv2.waitKey(0)


# In[ ]:





# In[ ]:




