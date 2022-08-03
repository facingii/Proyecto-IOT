# -*- coding: utf-8 -*-

import sqlite3
import os

class Persistance:
	SQL_CREATE = "CREATE TABLE NotDelivered (containerId text, temperature real, humidity real, latitude real, longitude real, datetime text)"
	SQL_INSERT = "INSERT INTO NotDelivered VALUES ('%s', %i, %i, %f, %f, '%s')"

	def __init__ (self, filepath):
		if not os.path.exists (filepath):
			try:
				self.conn = sqlite3.connect (filepath)
				cursor = self.conn.cursor ()
				cursor.execute (self.SQL_CREATE)
			except sqlite3.Error as e:
				print (e)

		self.conn = sqlite3.connect (filepath)

	def insert (self, data):
		sql = self.SQL_INSERT % (data ['containerId'], data ['temperature'], data ['humidity'], data ['geo']['latitude'], data ['geo']['longitude'], data ['timestamp'])
		print (sql)
		try:
			cursor = self.conn.cursor ()
			cursor.execute (sql)
			self.conn.commit ()
		except sqlite3.Error as e:
			print (e)

	def close (self):
		if self.conn:
			self.conn.close ()
