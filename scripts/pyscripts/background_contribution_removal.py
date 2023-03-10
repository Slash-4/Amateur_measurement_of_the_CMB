import numpy as np
import matplotlib.pyplot as plt
import math
import csv


#constants
boltzman = 1.3806503E-23 #m2 kg s-2 K-1
#TODO this is probably not actually a constant 
# receiving band
B = 1
pi = np.pi
e = np.e

class Reading():

	def __innit__(self):
		self.path
		self.pathToRawData

		self.timestamp
		self.powerMeasurement
		self.thetaFromZenith

	def getPower(self):
		return self.powerMeasurement

	def getTimestamp(self):
		return self.timestamp

	def writeCsv(self):
		with open(self.path, newline='') as csvfile:
			fieldnames = ['Timestamp', 'Power_measurement(P)', 'Theta_From_zenith(rad)']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			writer.writeheader()
			writer.writerow({
				fieldnames[0]: self.timestamp, 
				fieldnames[1]: self.powerMeasurement,
				fieldnames[2]: self.thetaFromZenith
				})

	def readCsv(self):
		with open(self.path, 'r', newline='') as csvfile:
			reader =  csv.DictReader(csvfile, delimiter=',')
			for row in reader:
				self.timestamp = row['Timestamp']
				self.powerMeasuremet = row['Power_measurement(P)']
				self.thetaFromZenith = row['Theta_From_zenith(rad)']
"""

Class constructed to input a lambda function with data

Instead of storing the result from the evaluation of the function we store the function and data into one
package to allow it to be manipulated later. Each computer models one set of environmental temperature 
contributions like Atmosphere Temp or Amplifier Temp (K)

"""
class Background_Temp_Computer():

	def __init__(self, lambdaF, *args):

		self.lambdaF = lambdaF
		self.data = args

	def compute(self):
		return self.lambdaF(self.data)
	
#object class used to measure the total contributions of environmental radio temperature
class Background_Comparison_Controller():

	def __init__(self, temperatureComputerArray = []):
		self.temperatureComputerArray = temperatureComputerArray

	def compute_calibration_temperature_contribution(self):
		total_system_temperature = 0

		for T_computer in self.temperatureComputerArray:
			total_system_temperature += T_computer.compute()

		return total_system_temperature



def main():
	print("==============Start experiment=================")

	temp_to_power = lambda temperature : temperature/(boltzman*B)

	
	SysT_Computer = Background_Temp_Computer(
		lambda t_hot, t_cold: (temp_to_power(t_hot)-temp_to_power(t_cold))/(t_hot-t_cold),
		#data
	)
	
	f = lambda t_zenith, t_theta, theta: t_zenith-np.sec(theta) *t_theta
	AtmT_Computer = Background_Temp_Computer(
			f,
			0
			)

	





if __name__=='__main__':
	main()