from PIL import Image
import binascii
import hashlib
import optparse

def rgb2hex(r, g, b):
	return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hex2rgb(hexcode):
	return tuple(map(ord, hexcode[1:].decode('hex')))

def str2bin(message):
	binary = bin(int(binascii.hexlify(message), 16))
	return binary[2:]

def bin2str(binary):
	message = binascii.unhexlify('%x' % (int('0b' + binary, 2)))
	return message

def encode(hexcode, digit):
	if hexcode[-1] in ('0', '1', '2', '3', '4', '5'):
		hexcode = hexcode[:-1] + digit
		return hexcode
	else:
		return None

def decode(hexcode):
	if hexcode[-1] in ('0', '1'):
		return hexcode[-1]
	else:
		return None

def hide(filename, message, password = None):
	img = Image.open(filename)
	pass_binary = None
	binary = str2bin(message) + '1111111111111110'
	if password:
		pass_binary = str2bin(hashlib.sha224(password).hexdigest()) + '0000000000000001'
		binary = pass_binary + binary
	if img.mode in ('RGBA'):
		img = img.convert('RGBA')
		datas = img.getdata()

		newData = []
		digit = 0
		temp = ''
		for item in datas:
			if(digit < len(binary)):
				newpix = encode(rgb2hex(item[0], item[1], item[2]), binary[digit])
				if newpix == None:
					newData.append(item)
				else:
					r, g, b = hex2rgb(newpix)
					newData.append((r,g,b,255))
					digit += 1
			else:
				newData.append(item)
		img.putdata(newData)
		img.save('other' + filename, "PNG")
		return "Completed"
	return "Incorrect image mode, couldn't hide"

def retr(filename):
	img = Image.open(filename)
	if img.mode in ('RGBA'):
		img = img.convert('RGBA')
		datas = img.getdata()

		binary = ''
		for item in datas:
			sBin = decode(rgb2hex(item[0], item[1], item[2]))
			if sBin == None:
				pass
			else:
				binary = binary + sBin
				if binary[-16:] == '1111111111111110':
					return bin2str(binary[:-16])
				if binary[-16:] == '0000000000000001':
					password = raw_input('Password: ')
					if not hashlib.sha224(password).hexdigest() == bin2str(binary[:-16]):
						return 'Incorrect passphrase'
					else:
						binary = ''
		return 'No message found'
	else:
		return 'Incorrect file type'










