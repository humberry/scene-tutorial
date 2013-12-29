import clipboard
import Image
import sys
import os
import photos

def pic_save(image, m, x, y, q, r):
	print
	print 'Picture is in process ...'
	if r == True:
		image = image.resize((x, y), Image.ANTIALIAS)
	background = Image.new(m, (x,y), 'white')
	background.paste(image,(0,0))
	clipboard.set_image((background), format='jpeg', jpeg_quality=q)
	photos.save_image(clipboard.get_image())

def pic_para(m):
	print
	q = int(raw_input('Quality (0 - 100): '))
	q = q / 100.0
	if q < 0.0:
		q = 0.0
	elif q > 1.0:
		q = 1.0
	print
	print '0 = no change (' + m + ')'
	print '1 = black/white'
	print '2 = grey'
	print '3 = RGB no transparency'
	print '4 = RGB with transparency'
	print '5 = CMYK'
	print '6 = YCbCr'
	print '7 = 32bit Pixel'
	mOld = m
	m = int(raw_input('Mode: '))
	menu_options = { 1 : '1',
					2 : 'L',
					3 : 'RGB',
					4 : 'RGBA',
					5 : 'CMYK',
					6 : 'YCbCr',
					7 : 'I' }
	return menu_options.get(m, mOld), q

def main():
	pics = photos.get_count()
	if (pics == 0):
		print 'Sorry no access or no pictures.'
		sys.exit()
	image = photos.pick_image()
	if not image:
		print 'Good bye!'
	else:
		#Variables: q=quality, m=mode(e.g. RGBA), r=resize(True/False), a=return value from pic_para(), b=orientation, o=option, mp=resolution in megapixels
		r = False 
		q = 95
		x = image.size[0]
		y = image.size[1]
		if (x > y):
			b = 'v'	#vertical
		elif (y > x):
			b = 'h'	#horizontal
		else:
			b = 's'	#square
		mp = round(x * y / 1000000.0, 1)
		m = image.mode
		print 'Picture-Information:',
		print 'resolution = {} x {} ({} MP), mode = {}'.format(x, y, mp, m)
		print
		print '!!! Changing the resolution is time-consuming !!! Resolution higher 6000 x 4000 (24MP) can cause a abend!'
		print
		print '0 = Auto processing (Resolution = {} x {}), quality = 95%, mode = {}'.format(x, y, m)
		print '1 = Same resolution ({} x {})'.format(x, y)
		print '2 = Define resolution'
		print '3 = 3MP (2048 x 1536)'
		print '5 = 5MP (2592 x 1936)'
		o = int(raw_input('Resolution: '))
		if o == 0:
			pic_save(image, m, x, y, q, r)
			q = q / 100.0
		elif o == 1:
			a = pic_para(m)
			m = a[0]
			q = a[1]
			pic_save(image, m, x, y, q, r)
		elif o == 2:
			print
			print 'Changing the ratio causes picture deformation!'
			x2 = int(raw_input('Width: '))
			y2 = int(raw_input('Height: '))
			if (x2 == x and y2 == y):
				r = False
			else:
				r = True
				x = x2
				y = y2
			a = pic_para(m)
			m = a[0]
			q = a[1]
			pic_save(image, m, x, y, q, r)	
		elif o == 3:
			if (b == 'v' and x == 2048 and y == 1536):
				r = False
				x = 2048
				y = 1536
			elif (b == 'h' and x == 1536 and y == 2048):
				r = False
				x = 1536
				y = 2048
			else:
				r = True
				if (b == 'v' or b == 's'):
					x = 2048
					y = 1536
				else:
					x = 1536
					y = 2048
			a = pic_para(m)
			m = a[0]
			q = a[1]
			pic_save(image, m, x, y, q, r)
		elif o == 5:
			if (b == 'v' and x == 2592 and y == 1936):
				r = False
				x = 2592
				y = 1936
			elif (b == 'h' and x == 1936 and y == 2592):
				r = False
				x = 1936
				y = 2592
			else:
				r = True
				if (b == 'v' or b == 's'):
					x = 2592
					y = 1936
				else:
					x = 1936
					y = 2592
			a = pic_para(m)
			m = a[0]
			q = a[1]
			pic_save(image, m, x, y, q, r)
		else:
			print 'Cancel: ' + str(o) + ' is no valid input.'
			sys.exit()
		print 'Completed!'
		print 'Resolution = {} x {}, quality = {:.0f}%, mode = {}'.format(x, y, q*100, m)
		
if __name__ == '__main__':
	main()
