import cv2
from PIL import Image
import pytesseract
import re

# Read image using OpenCV
image = cv2.imread('2.jpg')

# Check if the image is loaded
if image is None:
    print("Failed to load image. Check the file path.")
else:
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    denoised_image = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive thresholding
    adaptive_thresh = cv2.adaptiveThreshold(denoised_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # OCR with pytesseract
    custom_config = r'--psm 6 --oem 3'  # Using PSM 6 and OEM 3 for better results
    text = pytesseract.image_to_string(adaptive_thresh, config=custom_config)

    # Clean the extracted text (optional)
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Output the result
    print("Extracted Text:", text)
