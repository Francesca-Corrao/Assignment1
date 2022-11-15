Research Track 1- Assignment 1
================================

This the repository for the solution of the First Assignemnt for the course Research Trask 1.

The goal of the assignment is to develop a robot that make pairs of silver and gold marker on the map by taking a silver marker and bring it to a gold one.
To do this we will use a python robot simulator developed by [Student Robotics](https://studentrobotics.org) with arenas modified for the class.

How to Run the solution
----------------------
In order to run the solution inside the robot-sim folder you have to execute 
```
python2 run.py assignment.py
```
it's important to specify to use python 2 because otherwise it won't execute if try to execute with python 3

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

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

How it works 
---------
To reach the goal the robot will look for token in front of it and choose the closest one, go to it and grad it. After grabbing the token the robot will turn look for golden token in front of it and go to the closest one and once it is close enought to it will release the silver token. This untill it each silver is with a different gold. 
The pseudocode of an algorithm to do it is the following: 
```
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
to do this I implement four main function 
##find_silver_token()##
##find_gold_token()##
##go_silver()##
##go_gold()##


Improvement
-----------
