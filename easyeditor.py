from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QRadioButton, QGroupBox, QButtonGroup, QTextEdit, QListWidget, QLineEdit, QInputDialog, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter, ImageEnhance
import os

App = QApplication([])
mainWin = QWidget()
mainWin.setWindowTitle("The Easy Editor")

workdir = ''


mainLayout = QHBoxLayout()
layout1 = QVBoxLayout()
layout2 = QVBoxLayout()
layout3 = QHBoxLayout()
mainWin.setFixedSize(900,600)

picture = QLabel("Image")
fileList = QListWidget()
leftButton = QPushButton("Left")
rightButton = QPushButton('Right')
mirrorButton = QPushButton('Mirror')
sharpenButton = QPushButton("Sharpness")
bwButton = QPushButton("Black and White")
blurButton = QPushButton("Blur")
defaultButton = QPushButton("Default Image")
folderButton = QPushButton("Folder")

layout3.addWidget(leftButton)
layout3.addWidget(rightButton)
layout3.addWidget(mirrorButton)
layout3.addWidget(sharpenButton)
layout3.addWidget(bwButton)
layout3.addWidget(blurButton)
layout3.addWidget(defaultButton)


layout2.addWidget(picture, 95)
layout1.addWidget(folderButton)
layout1.addWidget(fileList)

class ImageProcessor:
	def __init__(self):
		global workdir
		self.fileName = None
		self.currentImage = None
		self.subFolder = "Images"

	def loadImage(self, fileName):
		self.fileName = fileName
		image_path = os.path.join(workdir, self.fileName)
		self.image = Image.open(image_path)

	def showImage(self, label, path):
		picture.hide()
		pixmapimage = QPixmap(path)
		w, h = picture.width(), picture.height()
		pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
		picture.setPixmap(pixmapimage)
		picture.show()

	def saveImage(self):
		path = os.path.join(workdir, self.subFolder)
		if not(os.path.exists(path) or os.path.isdir(path)):
			os.mkdir(path)
		imagePath = os.path.join(path, self.fileName)
		self.image.save(imagePath)

	def doBW(self):
		if fileList.currentRow() >= 0:
			filename = fileList.currentItem().text()
			image_path = os.path.join(workdir, self.fileName)
			newImage = Image.open(image_path)
			pic_gray = newImage.convert("L")
			self.image = pic_gray
			self.saveImage()
			pathToFolder = os.path.join(workdir, self.subFolder)
			pathToImage = os.path.join(pathToFolder, self.fileName)
			self.showImage(self, pathToImage)

	def doLeft(self):
		if fileList.currentRow() >= 0:
			filename = fileList.currentItem().text()
			image_path = os.path.join(workdir, self.fileName)
			newImage = Image.open(image_path)
			pic_left = newImage.transpose(Image.ROTATE_90)
			self.image = pic_left
			self.saveImage()
			pathToFolder = os.path.join(workdir, self.subFolder)
			pathToImage = os.path.join(pathToFolder, self.fileName)
			self.showImage(self, pathToImage)

	def doRight(self):
		if fileList.currentRow() >= 0:
			filename = fileList.currentItem().text()
			image_path = os.path.join(workdir, self.fileName)
			newImage = Image.open(image_path)
			pic_right = newImage.transpose(Image.ROTATE_270)
			self.image = pic_right
			self.saveImage()
			pathToFolder = os.path.join(workdir, self.subFolder)
			pathToImage = os.path.join(pathToFolder, self.fileName)
			self.showImage(self, pathToImage)

	def doMirror(self):
		if fileList.currentRow() >= 0:
			filename = fileList.currentItem().text()
			image_path = os.path.join(workdir, self.fileName)
			newImage = Image.open(image_path)
			pic_mirror = newImage.transpose(Image.FLIP_LEFT_RIGHT)
			self.image = pic_mirror
			self.saveImage()
			pathToFolder = os.path.join(workdir, self.subFolder)
			pathToImage = os.path.join(pathToFolder, self.fileName)
			self.showImage(self, pathToImage)

	def doDefault(self):
		if fileList.currentRow() >= 0:
			filename = fileList.currentItem().text()
			image_path = os.path.join(workdir, self.fileName)
			newImage = Image.open(image_path)
			self.image = newImage
			self.saveImage()
			pathToFolder = os.path.join(workdir, self.subFolder)
			pathToImage = os.path.join(pathToFolder, self.fileName)
			self.showImage(self, pathToImage)

	def doSharpen(self):
		if fileList.currentRow() >= 0:
			filename = fileList.currentItem().text()
			image_path = os.path.join(workdir, self.fileName)
			factor, result = QInputDialog.getText(mainWin, "Sharpen Factor", "Sharpen Factor: ")
			if result and factor != "":
				newImage = Image.open(image_path)
				enhancer = ImageEnhance.Sharpness(newImage)
				pic_sharpen = enhancer.enhance(float(factor))
				self.image = pic_sharpen
				self.saveImage()
				pathToFolder = os.path.join(workdir, self.subFolder)
				pathToImage = os.path.join(pathToFolder, self.fileName)
				self.showImage(self, pathToImage)

	def doBlur(self):
		if fileList.currentRow() >= 0:
			filename = fileList.currentItem().text()
			image_path = os.path.join(workdir, self.fileName)
			newImage = Image.open(image_path)
			pic_blur = newImage.filter(ImageFilter.BLUR)
			self.image = pic_blur
			self.saveImage()
			pathToFolder = os.path.join(workdir, self.subFolder)
			pathToImage = os.path.join(pathToFolder, self.fileName)
			self.showImage(self, pathToImage)


workimage = ImageProcessor()

def showChosenImage():
	global workdir
	if fileList.currentRow() >= 0:
		filename = fileList.currentItem().text()
		workimage.loadImage(filename)
		image_path = os.path.join(workdir, workimage.fileName)
		workimage.showImage(workimage, image_path)

def chooseWorkDir():
	global workdir
	workdir = QFileDialog.getExistingDirectory()
	return workdir


def filter(filenames, extensions):
	result = []
	for file in filenames:
		for ext in extensions:
			if file.endswith(ext):
				result.append(file)
	return result

def showFilenamesList():
	workdirectory = chooseWorkDir()
	extensions = ["png", "jpg"]
	filtered = filter(os.listdir(workdirectory), extensions)
	fileList.clear()
	for i in filtered:
		fileList.addItem(i)


		

folderButton.clicked.connect(showFilenamesList)
fileList.currentRowChanged.connect(showChosenImage)
bwButton.clicked.connect(workimage.doBW)
leftButton.clicked.connect(workimage.doLeft)
rightButton.clicked.connect(workimage.doRight)
mirrorButton.clicked.connect(workimage.doMirror)
defaultButton.clicked.connect(workimage.doDefault)
sharpenButton.clicked.connect(workimage.doSharpen)
blurButton.clicked.connect(workimage.doBlur)

layout2.addLayout(layout3)
mainLayout.addLayout(layout1)
mainLayout.addLayout(layout2)
mainWin.setLayout(mainLayout)
mainWin.show()
App.exec_()