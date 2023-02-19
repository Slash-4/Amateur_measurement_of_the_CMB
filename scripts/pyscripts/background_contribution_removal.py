import numpy as np
import matplotlib.pyplot as plt
import math
import csv

class Reading():

	def __innit__(self):
		self.path
		self.pathToRawData

		self.timestamp
		self.powerMeasurement

	def getPower(self):
		return self.powerMeasurement

	def getTimestamp(self):
		return self.timestamp

	def writeCsv(self):
		with open(self.path, newline='') as csvfile:
			fieldnames = ['Timestamp', 'Power_measurment(P)']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			writer.writeheader()
			writer.writerow({fieldnames[0]: self.timestamp, fieldnames[1]: self.powerMeasuremen})

	def readCsv(self):
		with open(self.path, 'r', newline='') as csvfile:
			reader =  csv.DictReader(csvfile, delimiter=',')
			for row in reader:
				self.timestamp = row['Timestamp']
				self.powerMeasuremet = row['Power_measurment(P)']

			
class Background_Comparison_Controller():

	def __innit__(self):
		self.path_variable
		
		self.coldLoadR
		self.hotLoadR
		

	def measured_G(self):
		print('Error')
