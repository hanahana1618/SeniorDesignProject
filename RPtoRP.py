from socket import *
import time #from time import sleep

 
#static IP to access the endpoint pi 
static_ip = '192.168.43.200'
port = 5000

address = (static_ip, port) #Define who you are talking to (must match arduino IP and port)
client_socket = socket(AF_INET, SOCK_DGRAM) #Set Up the Socket
client_socket.settimeout(1) #only wait 1 second for a response

#run loop continuously to check for any data incoming
while(1):

    data = "Blue" #Set data to Blue Command
    client_socket.sendto(data, address)#send command to arduino

    try:
        rec_data, addr = client_socket.recvfrom(2048) #Read response from arduino
        print(rec_data) #Print the response from Arduino
    except:
    	print("Something went wrong") 
        pass

'''
	#delay before sending next command
    time.sleep(2) 

    data = "Red" #Set data to Blue Command
    client_socket.sendto(data, address) #send command to arduino
    try:
        rec_data, addr = client_socket.recvfrom(2048) #Read response from arduino
        print rec_data #Print the response from Arduino
    except:
        pass

	#delay before sending next command
    time.sleep(2) 

    data = "Green" #Set data to Blue Command
    client_socket.sendto(data, address) #send command to arduino
    try:
        rec_data, addr = client_socket.recvfrom(2048) #Read response from arduino
        print rec_data #Print the response from Arduino
    except:
        pass
        
    #delay before sending next command
    time.sleep(2) 
'''
