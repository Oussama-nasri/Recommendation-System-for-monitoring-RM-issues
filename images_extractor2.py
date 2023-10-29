import cv2
import numpy as np

# Load the book page as an image
book_image = cv2.imread(r"C:\Users\Administrator\Desktop\Project AI\00\2.jpg")

# Convert the image to grayscale for better processing
gray_image = cv2.cvtColor(book_image, cv2.COLOR_BGR2GRAY)

# Apply an edge detection algorithm to identify the edges of text and images
edges = cv2.Canny(gray_image, 100, 200)

# Find contours in the edge-detected image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a mask for the images
image_mask = np.zeros_like(book_image)

# Specify a size threshold to exclude small contours (adjust as needed)
min_image_area = 1000

# Iterate through the contours and extract the images
for contour in contours:
    area = cv2.contourArea(contour)
    if area > min_image_area:
        x, y, w, h = cv2.boundingRect(contour)
        image = book_image[y:y + h, x:x + w]
        if cv2.imwrite(f"extracted_image_-----------------------------------------------------{area}.jpg", image):
            print("saved image")

# Release resources
#cv2.destroyAllWindows()
