#!/bin/python3
import tkinter as Tk
import cv2
import pytesseract
import functools
import re




def theAppFont(name="Consolas", size="12", style="normal"):
	return f"{name} {size} {style}"

def createElement(element, *args, toPack=True, **kwargs):
	if "font" not in kwargs.keys() and element not in [Tk.Canvas]:
		kwargs["font"] = theAppFont()
	result = element(*args, **kwargs)
	if toPack:
		result.pack()
	return result

def gridElement(element, *args, row, column, rowspan=1, columnspan=1, **kwargs):
	result = createElement(element, *args, toPack=False, **kwargs)
	result.grid(row = row, column = column, rowspan = rowspan, columnspan = columnspan)
	return result


def recognize(minLetters, maxLetters):
	maxLetters = max(minLetters+1, maxLetters+1)
	filename = 'MyImage.png'
	image = cv2.imread(filename)
	h, w, _ = image.shape
	boxes = pytesseract.image_to_data(image).splitlines()[1:]
	theBoxes = list(map(lambda box: box.split(), boxes))
	# vraca informacije o karakteru i pripadnom okruzujucem pravougaoniku
	theBoxes = list(filter(
		lambda box: 
			len(box) > 11 and len(box[11]) in range(minLetters, maxLetters),
		theBoxes
	))
	boxAllUpper = list(filter(
		lambda box: 
			re.match(r"[A-Z]*$", box[11]),
		theBoxes
	))
	boxNumbers = list(filter(
		lambda box: 
			re.match(r"[0-9'_]*([,.][0-9'_]*)?(e[0-9'_]*)?$", box[11]),
		theBoxes
	))
	
	listOfWords = []

	totalAmountWords = len(theBoxes)
	for box in theBoxes:
		x_pos, y_pos, width, height = list(map(lambda x: int(x), box[6:10]))
		try:
			box[11]
		except:
			totalAmountWords -= 1
			continue
		listOfWords += [box[11]]
		cv2.rectangle(image, (x_pos-5, y_pos-5), (width+x_pos+5, height+y_pos+5), (0, 0, 0), 3)
		cv2.putText(image, box[11], (x_pos, y_pos-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)


	for box in boxAllUpper:
		x_pos, y_pos, width, height = list(map(lambda x: int(x), box[6:10]))
		cv2.rectangle(image, (x_pos-5, y_pos-5), (width+x_pos+5, height+y_pos+5), (185, 95, 120), 3)
		cv2.putText(image, box[11], (x_pos, y_pos-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (185, 95, 120), 1)
	
	for box in boxNumbers:
		x_pos, y_pos, width, height = list(map(lambda x: int(x), box[6:10]))
		cv2.rectangle(image, (x_pos-5, y_pos-5), (width+x_pos+5, height+y_pos+5), (210, 75, 180), 3)
		cv2.putText(image, box[11], (x_pos, y_pos-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (210, 75, 180), 1)
	
	
	label_totalWords.config(text = f"Total Words Found = {totalAmountWords}.")
	try:
		label_allUpper.config(text = f"All Upper Letters = {len(boxAllUpper)*100 // totalAmountWords}%.")
		label_numbers.config(text = f"Numbers = {len(boxNumbers)*100 // totalAmountWords}%.")
	except ZeroDivisionError:
		label_allUpper.config(text = f"All Upper Letters = undefined%.")
		label_numbers.config(text = f"Numbers = undefined%.")
	
	stringOfWords = functools.reduce(lambda x, y: x + " " + y, listOfWords)
	
	tk = Tk.Tk()
	info = createElement(Tk.Label, tk, text=stringOfWords)

	# prikaz
	cv2.imshow(filename, image)
	cv2.waitKey(0)

if __name__ == "__main__":
	root = Tk.Tk()
	root.geometry("300x200")
	label_allUpper = gridElement(Tk.Label, root, row=0, column=0, columnspan=2)
	label_numbers = gridElement(Tk.Label, root, row=1, column=0, columnspan=2)
	scale_minLetters = gridElement(Tk.Scale, root , row=3, column=0, from_=1, to=30, orient=Tk.HORIZONTAL)
	scale_maxLetters = gridElement(Tk.Scale, root , row=3, column=1, from_=1, to=30, orient=Tk.HORIZONTAL)
	label_totalWords = gridElement(Tk.Label, root, row=4, column=1,)
	button_recognize = gridElement(
		Tk.Button, root, 
		row=5, column=0, 
		columnspan=2,
		text="recognize", 
		command=lambda: recognize(scale_minLetters.get(), scale_maxLetters.get())
	)
	root.mainloop()
