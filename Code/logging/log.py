import logging
import logging.handlers
import os

class Logger:
	def __new__ (cls, *args, **kwargs):
		return super().__new__(cls)

	def __init__ (self, logfile):
		print ("logfile path: %s", logfile)
		self.log_file = logfile

	def info (self):
		pass

	def error (self):
		pass

	def debug (self):
		pass

