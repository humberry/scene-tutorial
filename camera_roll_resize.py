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

pic_info_menu_fmt = """
Picture-Information:',
resolution = {x} x {y} ({mp} MP), mode = {m}

!!! Changing the resolution is time-consuming !!! Resolution higher 6000 x 4000 (24MP) can cause a abend!'

0 = Auto processing (Resolution = {x} x {y}), quality = 95%, mode = {m}
1 = Same resolution ({x} x {y})
2 = Define resolution
3 = 3MP (2048 x 1536)
5 = 5MP (2592 x 1936)"""

def pic_save(image, m, x, y, q, r):
	print
	print 'Picture save is in process ...'
	if r:
		image = image.resize((x, y), Image.ANTIALIAS)
	background = Image.new(m, (x,y), 'white')
	background.paste(image,(0,0))
	clipboard.set_image((background), format='jpeg', jpeg_quality=q)
	photos.save_image(clipboard.get_image())

def pic_para(m):
	q = int(raw_input('\nQuality (0 - 100): ')) / 100.0
	if q < 0.0:
		q = 0.0
	elif q > 1.0:
		q = 1.0
	print(pic_para_menu_fmt.format(m))
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
	if not pics:
		print 'Sorry no access or no pictures.'
		return  # sys.exit()
	image = photos.pick_image()
	if not image:
		print 'Good bye!'
                return  # ???
	else:
		#Variables: q=quality, m=mode(e.g. RGBA), r=resize(True/False), a=return value from pic_para(), b=orientation, o=option, mp=resolution in megapixels
		r = False 
		q = 95
		x, y = image.size
		if (x > y):
			b = 'v'	#vertical
		elif (y > x):
			b = 'h'	#horizontal
		else:
			b = 's'	#square
		mp = round(x * y / 1000000.0, 1)
		m = image.mode
		print(pic_info_menu_fmt.format(**{'x':x,'y':y,'mp':mp,'m':m}))
		o = int(raw_input('Resolution: '))
                if o not in (0, 1, 2, 3, 5):
			print 'Cancel: ' + str(o) + ' is not valid input.'
			return  # sys.exit()
		if o == 0:
			pic_save(image, m, x, y, q, r)
			q = q / 100.0  # are these two lines reversed??
		elif o == 1:
			m, q = pic_para(m)
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
			m, q = pic_para(m)
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
			m, q = pic_para(m)
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
			m, q = pic_para(m)
			pic_save(image, m, x, y, q, r)
		print 'Completed!'
		print 'Resolution = {} x {}, quality = {:.0f}%, mode = {}'.format(x, y, q*100, m)
		
if __name__ == '__main__':
	main()
