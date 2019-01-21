#encoding:utf-8
from ftplib import FTP
import os
import fileinput

ftp = FTP()
localdir = '/home/pi/Desktop/drrobot/files'

def init_transfer():
	ftp.set_debuglevel(2)
	ftp.connect('www.mokuzaru.com', 21)
	ftp.login('eva@mokuzaru.com','Miltonyeah')
	ftp.cwd('/')

def ftp_upload(localfile, remotefile):
	fp = open(localfile, 'rb')
	ftp.storbinary('STOR %s' % os.path.basename(localfile), fp, 1024)
	fp.close()
	# print('after upload ' + localfile + ' to ' + remotefile)

def upload_file(file):
	ftp_upload(localdir + '/' + file, file)
	
def end_transfer():
	ftp.quit()
