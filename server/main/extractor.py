import json
import pytesseract
import os
from PIL import Image
import imutils
import numpy as np
import cv2
#from re import replace

def passport(image, file_name):
	if not os.path.isfile(image):
		print(f"Error: Unable to read {image}")
		return

	img = cv2.imread(image)

	if img is None:
		print(f"Error: Unable to read {image}")
		return

	img = imutils.resize(img, height=600)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
	sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
	gray = cv2.GaussianBlur(gray, (3, 3), 0)
	blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
	gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
	gradX = np.absolute(gradX)
	(minVal, maxVal) = (np.min(gradX), np.max(gradX))
	gradX = (255 * ((gradX - minVal) / (maxVal - minVal))).astype("uint8")
	gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
	thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
	thresh = cv2.erode(thresh, None, iterations=4)
	p = int(img.shape[1] * 0.05)
	thresh[:, 0:p] = 0
	thresh[:, img.shape[1] - p:] = 0
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

	roi = None

	for c in cnts:
		(x, y, w, h) = cv2.boundingRect(c)
		ar = w / float(h)
		crWidth = w / float(gray.shape[1])
		if ar > 5 and crWidth > 0.75:
			pX = int((x + w) * 0.03)
			pY = int((y + h) * 0.03)
			(x, y) = (x - pX, y - pY)
			(w, h) = (w + (pX * 2), h + (pY * 2))
			roi = img[y:y + h, x:x + w].copy()
			cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
			break

	if roi is None:
		roi = np.zeros_like(img)
		return

	# cv2.imshow("Image", img)
	# cv2.imshow("ROI", roi)
	# cv2.waitKey(0)

	filename = 	"{}.png".format(os.getpid())
	cv2.imwrite(filename, roi)

	text = pytesseract.image_to_string(Image.open(filename))
	text = text.split('\n')
	os.remove(filename)

	name = text[0][5:44].split('<')
	while 'K' in name:
		name.remove('K')
	
	test = text[0][5:44].split('<')
	while 'K' in test:
		test.remove('K')
	while '' in test:
		test.remove('')

	text[0] = text[0].replace(" ", "")
	text[1] = text[1].replace(" ", "")
	'''print(text)'''
	pc = text[0][2:5]
	pType = text[0][0]
	issuingCountry = text[0][2:5]
	surname = test[0]
	firstName = test[1]
	passportNumber = text[1][2:9]
	nationality = text[1][10:13]
	dateOfBirth = text[1][17:19] + "-" + text[1][15:17] + "-" + text[1][13:15]
	sex = text[1][20]
	dateOfExpiry = text[1][25:27] + "-" + text[1][23:25] + "-" + text[1][21:23]
	dict_sample = {'Type': pType, 'Issuing_Country': issuingCountry, 'Surname': surname, 'Name' : firstName, 'Passport_Number' : passportNumber, 'Nationality' : nationality, 'DOB' : dateOfBirth, 'Sex' : sex, 'DOE' : dateOfExpiry}
	with open(file_name, 'w') as f: json.dump(dict_sample, f)
	
# passport("C:\\Users\\fariduni.bahodur_2\\Desktop\\server\\media\\images\\passport_08.jpg", "data.json")