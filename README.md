Research Track I: Assignment 1
================================

This the repository for the solution of Research Track 1 first assignment.

The goal of the assignment is to develop a code that make pairs of silver and gold marker on the map by taking a silver marker and bring it to a gold one.
To do this we will use a python robot simulator developed by [Student Robotics](https://studentrobotics.org) with arenas modified for the class.

How to Run the solution
----------------------
In order to run the solution inside the robot-sim folder you have to execute the comand
```
python2 run.py assignment.py
```

How it works 
---------
To reach the goal the robot will look for tokens in front of it and choose the closest one, go to it and grab it. After grabbing the token the robot will turn looking for closest gold token in front of it, go to the closest one and once it is close enought to it will release the silver token. This will be done untill every silver token is with a different gold token. 

The pseudocode of an algorithm to do it is the following: 
``` python
while you haven't grab every token
	find the closest silver
	if your distance less then threshold
		grab silver token
		turn around 
		find the closest gold
		go to the golden token 
		if you are close to the golden token
			release silver token
	else go to the the silver token 
```

To do this there have been implement different function and a main 

### main ###

```python
	initialize the robot 
	set the threshold for the orientation a_th
	set linear distance threshold for grab silver token d_th
	set linear distance threshold for release gold token d_th_gold
	set an empty list where it will put the silver token once it grab it silver
	set an empty list where put the golden token once it release the silver token near to it gold
	go_silver()
	turn
	drive
	notice task ended
	
```

### go_silver() ###
function that got the distance of the closest silver token using the function find_silver_token(), turn and drive in order to go to it and once it's there grab the token, put the code of it in the list of already taken silver token and call the function go_gold().

```python
	while haven't got every silver token (list of silver token has less then 6 elements):
		find_silver_token()
		if it doesn't see any token:
			turn
		elif the distance is less than the linear distance threshold
			grab the silver token
			add the id of the token to the list of taken silver token
			call function go_gold()
			return
		elif robot is aligned with the token
			go forward
		elif robot not aligned with the token, token on the left
			turn left
		elif robot not aligned with the token, token on the right
			turn right
```
### go_gold() ###
function that get distance, orientation and code of the closest gold token, drive and turn to go to it and once it is there release the silver token it grabbed before and add the code of the gold token to the list of already taken gold token.

```python 
	while haven't go to every gold token (list of gold token has less then 6 elements):
		find_gold_token()
		if it doesn't see any token:
			turn
		elif the distance is less than the linear distance threshold for gold
			release silver token
			add the id of the token to the list of taken gold token
			return
		elif robot is aligned with the token
			go forward
		elif robot not aligned with the token, token on the left
			turn left
		elif robot not aligned with the token, token on the right
			turn right
```
### find_silver_token() ###
function to find the closest silver token and return it's distance, rotation and code

```python
	set an empty list
	for every token seen
		if the token is silver and it isn't already taken
			add to the list of silver token, distance, orientation and code of the token
	if silver is empty 
		return -1, -1 , -1
	else 
		sort list of silver token by increasing distances
		set dist to 100 
		if distance of the first element in list of silver token is less then dist
			set dist to distance of first element in the list of silver token
			set orienation to the orienation to the first silver token 
			set code to the code of the first silver token
		if dist is 100 
			return -1, -1,-1
		else 
			return dist, orientation, code
```
### find_gold_token() ###
function to find the closest gold token and return it's distance, orientation and code. It is the same of find_silver_token changing silver with gold so the only important changes are in the first if by checking if the silver token is gold and the code isn't in the list of already taken gold token. 

### turn and drive ###
these are two function that will make the robot move:
* `drive`: given a speed and a time will make the robot go forward for time making the motors move with the speed passed
* `turn`: given a speed and a time will make the robot turn for a time by making the motors rotate in different rotation with the speed passed

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

To drop the token, call the `R.release` method.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

Improvement
-----------
This code work very weel for the specific problem it has to face but there are some improvements that can be done in order to make the code more :
* when choosing a silver token we can verify that there are no golden token in the trajectory between the closest and the robot otherwise the robot when go to the silver token will take the golden one with it and so can never grab the silver token. The same can happen when choosing the gold token
* modify the ending condition of the while so the robot can search for more or less then 6 token depend on how many there are non the map 

