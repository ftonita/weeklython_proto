import sys
import mysql.connector

from classic_utils import *

cnx = mysql.connector.connect(user='root', password='root',
							host='10.178.129.221',
							database='21_passbot')

def database_connect_attempt():
	cursor = cnx.cursor()
	print_log("Database connection successful!")
	# if (cnx):
	# 	cursor.close()
	# 	cnx.close()
	return 0

def database_add_user(user):
	cursor = cnx.cursor()
	print_log("Database connection successful!")
	try:
		query = "INSERT INTO `Users`(`user_id`, `nickname`, `full_name`, `email`, `role`, `campus`) VALUES ('"+ str(user.user_id) +"','"+ user.nickname +"','"+ user.full_name +"','"+ user.email +"','"+ str(user.role) +"','"+str(user.campus)+"')"
		cursor.execute(query)
		cnx.commit()
		print_log("User has added to database successful!")
	except Exception as ex:
		print_log("[Error] User has not added to database!")
		print_log(ex)
	# finally:
	# 	if (cnx):
	# 		cursor.close()
	# 		cnx.close()

def database_select_user(u_id):
	cursor = cnx.cursor()
	res = ""
	print_log("Database connection successful!")
	try:
		query = "SELECT `user_id` FROM `Users` WHERE `user_id` = "+ str(u_id)
		cursor.execute(query)
		for user_id in cursor:
			res = str(user_id)
		print_log("User has selected successful or no users have found!")
	except Exception as ex:
		print_log("[Error] User select error: ")
		print_log(ex)
	return res

def database_select_from_temp(u_id):
	cursor = cnx.cursor()
	res = ""
	print_log(" - temp - Database connection successful!")
	try:
		query = "SELECT `state` FROM `temp` WHERE `user_id` = "+ str(u_id)
		cursor.execute(query)
		for state in cursor:
			res = str(state)
		print_log(" - temp - User has selected successful or no users have found!")
	except Exception as ex:
		print_log("[Error] - temp - User select error: ")
		print_log(ex)
	return res

def setUserState(user_id, state):
	cursor = cnx.cursor()
	print_log("Database connection successful!")
	try:
		query = "UPDATE `temp` SET `state`='" + str(state) + "' WHERE `user_id` = "+ str(user_id)
		cursor.execute(query)
		cnx.commit()
		print_log("User state has updated successful!")
	except Exception as ex:
		print_log("[Error] User state has not updated!")
		print_log(ex)

def insertUserToTemp(user_id):
	cursor = cnx.cursor()
	print_log("Database connection successful!")
	try:
		query = "INSERT INTO `temp`(`user_id`, `state`) VALUES ('"+ str(user_id) +"','0')"
		cursor.execute(query)
		cnx.commit()
		print_log("User has added to temp successful!")
	except Exception as ex:
		print_log("[Error] User has not added to temp!")
		print_log(ex)