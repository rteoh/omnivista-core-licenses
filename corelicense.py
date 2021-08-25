import os
import sys
import requests
import getpass
import ipaddress
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# Hide SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Enter OmniVista URL
ov_url = "localhost"


# Create request session
session = requests.Session() 


# Output information
output = ""


# Input data
input_data = ""





# Get API Function
def getData():


	# POST login credentials into OV API
	try:


		# Get username and password
		username = input("Enter Username:")
		password = getpass.getpass(prompt = "Enter Password:")


		# Use Login API to login
		login = session.post(ov_url + 'api/login', json = {'userName': username, 'password': password}, verify=False)


		# Check if login was successful
		if login.json()['message'] == "Login failed":
			print("Incorrect Omnivista login credentials.")
			exit()



	except:
		print("Cannot connect to " + ov_url)
		exit()


	try:

		# Define cookie
		cookie = session.cookies.get_dict()
		device_api = session.get(ov_url + 'api/devices?fieldSetName=discovery', cookies=cookie, verify=False)


		# Convert requests to JSON
		return device_api.json()["response"]

	except:
		# Error! Cannot fetch API
		print("Cannot fetch device API.")
		exit()



# Get Switch Information Function
def getSwitchInfo(data, ip):


	global output


	# Parse through entire data
	for switch in data:


		# If IP address is found
		if switch['ipAddress'] == ip:



			# Format Data
			switch_data = """%s - %s - %s \n""" % (switch['name'], switch['ipAddress'], switch['others']['coreLicenseUsed'])
			
			# Output Data
			print(switch_data)
			output += switch_data

			return


	# If IP Address could not be found
	error_message = """

	========================================
	ERROR: Could not locate %s
	========================================

	""" % (ip)
	print(error_message)
	output += error_message
	return


def allSwitchInfo(data):


	global output


	# Parse through entire data
	for num in range(len(data)):

		# Format Data
		switch_data = """%s - %s - %s \n""" % (data[num]['name'], data[num]['ipAddress'], data[num]['others']['coreLicenseUsed'])
		
		# Output Data
		print(switch_data)
		output += switch_data


	return








# Arguments

# Search for IP Address data
try: 

	# Get argument length
	arg_length = len(sys.argv)


	# If argument length is one
	if(arg_length == 1):
		exit()


	# Parse through IP Addresses
	for arg_position in range(1, arg_length):


		# Fetch IP address given to the script
		inputted_ip = sys.argv[arg_position]


		# If output option is given
		if "-output" in inputted_ip:


			# Get script directory
			directory = os.path.dirname(__file__)
			# Get text file directory
			filename = os.path.join(directory, 'license_usage_' + datetime.today().strftime("%m_%d_%Y") + '.txt')
			

			# Write to file
			f = open(filename, "w")
			f.write(output)
			f.close()

			continue


		# If output option is given
		if "-all" in inputted_ip:

			# Fetch data
			data = getData()

			# Fetch all switch info
			allSwitchInfo(data)
			

			continue


		# If txt file is given
		if ".txt" in inputted_ip:


			# Check to see if file exist
			if os.path.isfile(inputted_ip):


				# Read file
				f = open(inputted_ip, "r")


				# Fetch data
				data = getData()


				# Parse through each IP line by line
				for ip in f:


					# Remove newline from each line to get only IP address
					ip = ip.replace("\n", "")


					# Find information for each IP address
					getSwitchInfo(data, ip)

			else:

				# If file does not exist
				print('Input file does not exist.')
				exit()

			continue



		# Check to see if IP is valid
		ip_address = ipaddress.ip_address(inputted_ip)

		# Log in to API if running first loop
		if arg_position == 1:
			data = getData()

		# If IP is valid, find information
		getSwitchInfo(data, inputted_ip)


# IP address is invalid
except ValueError:

	print('\n')
	print('Error: Invalid IP Address')
	print('Usage: python corelicense.py <ip or .txt file> -all [Get all IP] -output')
	exit()
except:

	print('\n')
	print('Usage: python corelicense.py <ip or .txt file> -all [Get all IP] -output')
	exit()




