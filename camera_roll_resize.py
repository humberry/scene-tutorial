import clipboard
import Image
import sys
import os
import photos

pic_para_menu_fmt = """
0 = no change ({})
1 = black/white
2 = grey
3 = RGB no transparency
4 = RGB with transparency
5 = CMYK
6 = YCbCr
7 = 32bit Pixel"""

pic_info_menu_fmt = """Picture-Information: resolution = {width} x {height} ({megapixels} MP), mode = {image_mode}

!!! Changing the resolution is time-consuming !!! Resolution higher 6000 x 4000 (24MP) can cause a abend!

0 = Auto processing (Resolution = {width} x {height}), quality = 95%, mode = {image_mode}
1 = Same resolution ({width} x {height})
2 = Define resolution
3 = 3MP (2048 x 1536)
5 = 5MP (2592 x 1936)"""

def pic_save(image, image_mode, width, height, quality, resize):
	print
	print 'Picture save is in process ...'
	if resize:
		image = image.resize((width, height), Image.ANTIALIAS)
	background = Image.new(image_mode, (width,height), 'white')
	background.paste(image,(0,0))
	clipboard.set_image((background), format='jpeg', jpeg_quality=quality)
	photos.save_image(clipboard.get_image())

def pic_para(image_mode):
	quality = int(raw_input('\nQuality (0 - 100): ')) / 100.0
	if quality < 0.0:
		quality = 0.0
	elif quality > 1.0:
		quality = 1.0
	print(pic_para_menu_fmt.format(image_mode))
	mOld = image_mode
	image_mode = int(raw_input('Mode: '))
	menu_options = { 1 : '1',
			 2 : 'L',
			 3 : 'RGB',
			 4 : 'RGBA',
			 5 : 'CMYK',
			 6 : 'YCbCr',
			 7 : 'I' }
	return menu_options.get(image_mode, mOld), quality

def main():
	pics = photos.get_count()
	if not pics:
		print 'Sorry no access or no pictures.'
		return
	image = photos.pick_image()
	if not image:
		print 'Good bye!'
		return
	else:
		resize = False 
		quality = 95
		width, height = image.size
		if (width > height):
			orientation = 'vertical'
		elif (height > width):
			orientation = 'horizontal'
		else:
			orientation = 'square'
		megapixels = round(width * height / 1000000.0, 1)
		image_mode = image.mode
		print(pic_info_menu_fmt.format(**{'width':width,'height':height,'megapixels':megapixels,'image_mode':image_mode}))
		option = int(raw_input('Resolution: '))
		if option not in (0, 1, 2, 3, 5):
			print 'Cancel: ' + str(option) + ' is not valid input.'
			return
		if option == 0:
			pic_save(image, image_mode, width, height, quality, resize)
			quality = quality / 100.0  # are these two lines reversed??
		elif option == 1:
			image_mode, quality = pic_para(image_mode)
			pic_save(image, image_mode, width, height, quality, resize)
		elif option == 2:
			print
			print 'Changing the ratio causes picture deformation!'
			width2 = int(raw_input('Width: '))
			height2 = int(raw_input('Height: '))
			if (width2 == width and height2 == height):
				resize = False
			else:
				resize = True
				width = width2
				height = height2
			image_mode, quality = pic_para(image_mode)
			pic_save(image, image_mode, width, height, quality, resize)	
		elif option == 3:
			if (orientation == 'vertical' and width == 2048 and height == 1536):
				resize = False
				width = 2048
				height = 1536
			elif (orientation == 'horizontal' and width == 1536 and height == 2048):
				resize = False
				width = 1536
				height = 2048
			else:
				resize = True
				if (orientation == 'vertical' or orientation == 'square'):
					width = 2048
					height = 1536
				else:
					width = 1536
					height = 2048
			image_mode, quality = pic_para(image_mode)
			pic_save(image, image_mode, width, height, quality, resize)
		elif option == 5:
			if (orientation == 'vertical' and width == 2592 and height == 1936):
				resize = False
				width = 2592
				height = 1936
			elif (orientation == 'horizontal' and width == 1936 and height == 2592):
				resize = False
				width = 1936
				height = 2592
			else:
				resize = True
				if (orientation == 'vertical' or orientation == 'square'):
					width = 2592
					height = 1936
				else:
					width = 1936
					height = 2592
			image_mode, quality = pic_para(image_mode)
			pic_save(image, image_mode, width, height, quality, resize)
		print 'Completed!'
		print 'Resolution = {} x {}, quality = {:.0f}%, mode = {}'.format(width, height, quality*100, image_mode)
		
if __name__ == '__main__':
	main()
