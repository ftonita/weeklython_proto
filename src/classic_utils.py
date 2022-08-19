import os
import struct
import sys
import datetime

class User():
	def __init__(self):
		self.user_id = -1
		self.verified = -1
		self.nickname = ""
		self.full_name = ""
		self.email = ""
		self.role = -1
		self.campus = -1

class Pass():
	def __init__(self):
		self.inviter_id = ""
		self.guest_name = ""
		self.doc_number = ""
		self.start_datetime = datetime.datetime(-1, -1, -1)
		self.status = -1
		self.campus = -1

def print_log(event):
	time = str(datetime.datetime.now())
	log = '['+ time +'] >> ' + str(event)
	print(log)
