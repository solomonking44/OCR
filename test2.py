import cv2 as cv
# import pytesseract

image = cv.imread('letter.jpg')

# print(pytesseract.image_to_string(image))

cv.imshow('Result', image)

cv.waitKey(0)

