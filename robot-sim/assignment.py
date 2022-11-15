from __future__ import print_function

import time
from sr.robot import *

R = Robot()
a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

d_th_gold=0.7
""" float: Threshold for the control of the linear distance of a gold token
	must be greater then d_th otherwise the robot will never leave the silver token """

silver_taken=list()
""" list: contain the id of the silver marker taken"""

gold_taken=list()
""" list: contain the id of the gold marker taken"""

def drive(speed, seconds):
	"""
	Function for setting a linear velocity
    
	Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
	"""
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0
    
def turn(speed, seconds):
	"""
	Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
	"""
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = -speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

def find_silver_token():
	"""
 	Function to find the closest silver token
 	Returns:
 	dist(float): distance of the closest silver token( -1 if no token is detected)
 	rot_y(float): angle between the robot and the the closest silver token( -1 if not token is  detected)
 	code(int): id of the closest silver token (-1 if no token is detected)
	"""
	silver=[]
	for token in R.see():
		if(token.info.marker_type == MARKER_TOKEN_SILVER) & (not(token.info.code in silver_taken)):
			silver.append((token.dist, token.rot_y,token.info.code))
	if len(silver) ==0:
		return -1, -1, -1
	else: 
		silver.sort()
		dist=100
		if(silver[0][0]<dist):
			dist=silver[0][0]
			rot_y=silver[0][1]
			code=silver[0][2]
		if dist==100:
			return -1, -1, -1
		else:
			return dist, rot_y, code

def find_gold_token():
	"""
 	Function to find the closest gold token
 	Returns:
 	dist(float): distance of the closest gold token( -1 if no token is detected)
 	rot_y(float): angle between the robot and the the closest gold token( -1 if not token is detected)
 	
 	code(int): id of the closest gold token (-1 if no token is detected)
	"""
	gold=[]
	for token in R.see():
		if(token.info.marker_type == MARKER_TOKEN_GOLD) & (not(token.info.code in gold_taken)):
			gold.append((token.dist, token.rot_y,token.info.code))
	if len(gold) ==0:
		return -1, -1, -1
	else: 
		gold.sort()
		dist=100
		if(gold[0][0]<dist):
			dist=gold[0][0]
			rot_y=gold[0][1]
			code=gold[0][2]
		if dist==100:
			return -1, -1, -1
		else: 
			return dist, rot_y, code
			
def go_gold():
	"""
	Function to find the closest gold and go there, once the robot arrives to the gold token it
	will release the token he had grabbed previously
	"""
	while(len(gold_taken)<6):
		print("Looking for gold token")
		dist_gold, rot_y_gold, code_gold =find_gold_token()
		if dist_gold==-1:
		#if we don't see any gold token but haven take every gold token turn to se in other place
			print("No gold token found but there are, turning")
			turn(5,1)
		elif dist_gold <d_th_gold:
		#if we are close to the golden token leave the silver block 
			print("Found gold token!")
			R.release()
			print("silver token release")
			gold_taken.append(code_gold)
			return 0
		elif -a_th<= rot_y_gold <= a_th: # if the robot is well aligned with the token, we go forward
			print("Go forward...")
			drive(10, 2)
		elif rot_y_gold < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			print("Left a bit...")
			turn(-1, 1)
		elif rot_y_gold > a_th:
			print("Right a bit...")
			turn(+1, 1)
			
def go_silver():
	"""
	Function to find the closest silver token among the free ones, go there and grab it
	then call the function go_gold() untill it take every silver token
	"""
	
	while (len(silver_taken)<6):
		#find silver token
		print("Looking for silver token")
	 	dist, rot_y, code=find_silver_token()
		if dist==-1:
	 		#if we don't see any silver token we turn because there is still more that i haven't take
			print("I don't see any silver token!!")
			turn(5,1)
		elif dist <d_th: 
			# if we are close to the token, we grab it. and bring to the closes gold
			print("Found silver token!")
			if(R.grab()):
				print("grabbed silver token")
				silver_taken.append(code)
				turn(-10,4)
				go_gold()
		elif -a_th<= rot_y <= a_th: 
			# if the robot is well aligned with the token, we go forward
			print("Go forward...")
			drive(10, 2)
		elif rot_y < -a_th:
			# if the robot is not well aligned with the token, we move it on the left or on the right
			print("Left a bit...")
			turn(-1, 1)
		elif rot_y > a_th:
			print("Right a bit...")
			turn(+1, 1)

		
go_silver()		
turn(10,4)
drive(10,10)
print("Task complete!")
  
    
    
 
