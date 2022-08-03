# -*- coding: utf-8 -*-

import sqlite3
import os

class Persistance:
	SQL_CREATE = "CREATE TABLE NotDelivered (containerId text, temperature real, humidity real, latitude real, longitude real, datetime text)"
	SQL_INSERT = "INSERT INTO NotDelivered VALUES ('%s', %i, %i, %f, %f, '%s')"
	SQL_COUNT = "SELECT COUNT (containerId) AS ROWS FROM NotDelivered"
	SQL_QUERY = "SELECT * FROM NotDelivered"
	SQL_REMOVE_ALL = "DELETE FROM NotDelivered"

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

	def num_rows (self):
		try:
			cursor = self.conn.cursor ()
			rows = cursor.execute (self.SQL_COUNT)
			return rows.fetchone () [0]
		except sqlite3.Error as e:
			print (e)
		
		return 0

	def get_data (self):
		try:
			cursor = self.conn.cursor ()
			query = cursor.execute (self.SQL_QUERY)
			rows = query.fetchall ()

			data = [{'containerId': row [0], 'temperature': row [1], 
					'humidity': [2], 'timestamp': row [5], 'status': 'ok', 
					'geo': {'latitude': row [3], 'longitude': row [4]}} for row in rows]
			
			return data
		except sqlite3.Error as e:
			print (e)

	def remove (self):
		try:
			cursor = self.conn.cursor ()
			cursor.execute (self.SQL_REMOVE_ALL)
			self.conn.commit ()
		except sqlite3.Error as e:
			print (e)

	def close (self):
		if self.conn:
			self.conn.close ()
