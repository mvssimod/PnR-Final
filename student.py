import pigo
import time
import random
from gopigo import *


'''
MR. A's Final Project Student Helper
'''

class GoPiggy(pigo.Pigo):

    ########################
    ### CONTSTRUCTOR - this special method auto-runs when we instantiate a class
    #### (your constructor lasted about 9 months)
    ########################

    def __init__(self):
        print("Your piggy has be instantiated!")
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 90
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.STOP_DIST = 35
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 70
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 70
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.menu()

    def encR(self, enc):
        pigo.Pigo.encR(self, enc)
        self.turn_track += enc

    def encL(self, enc):
        pigo.Pigo.encL(self, enc)
        self.turn_track -= enc


    ########################
    ### CLASS METHODS - these are the actions that your object can run
    #### (they can take parameters can return stuff to you, too)
    #### (they all take self as a param because they're not static methods)
    ########################


    ##### DISPLAY THE MENU, CALL METHODS BASED ON RESPONSE
    def menu(self):
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "c": ("Calibrate", self.calibrate),
                "t": ("Turn test", self.turn_test),
                "s": ("Check status", self.status),
                "q": ("Quit", quit),
                "w": ("Wide scan", self.wide_scan)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    def count_obstacles(self):
        # Run a scan
        self.wide_scan()
        # Count how many obstacles I've found
        counter = 0
        # Starting state assumes no obstacle
        found_something = False
        # Loop through all scan data
        for x in self.scan:
            # If x is not None and really close
            if x and x <= self.STOP_DIST:
                # If I've already found something
                if found_something:
                    print("Obstacle continues")
                # If this is a new obstacle
                else:
                    # Switch my tracker
                    found_something = True
                    print("Start of new obstacle")
                # If my data shows safe distances...
                if x and x > self.STOP_DIST:
                    # If my tracker had been triggered...
                    if found_something:
                        print("End of obstacle")
                        # Reset tracker
                        found_something = False
                        # Increase count of obstacles
                        counter += 1
        print ('Total number of obstacles in this scan: ' + str(counter))
        return counter

    def total_obstacles(self):
        counter = 0
        for x in range(4):
            counter += self.count_obstacles()
            self.encR(7)
        print('Total number of obstacles in this scan: ' + str(counter))

    def turn_test(self):
        while True:
            ans = raw_input('Turn right, left or stop? (r/l/s): ')
            if ans == 'r':
                val = int(raw_input('/nBy how much?: '))
                self.encR(val)
            elif ans == 'l':
                val = int(raw_input('/nBy how much?: '))
                self.encL(val)
            else:
                break
        self.restore_heading()

    def restore_heading(self):
        print ("Now I'll turn back to the starting position")
        if self.turn_track > 0:
            self.encL(self.turn_track)
        elif self.turn_track < 0:
            self.encR(abs(self.turn_track))
        # assignment: make self.turn_track go back to zero

    #YOU DECIDE: How does your GoPiggy dance?
    def dance(self):
        print("Piggy dance")
        ##### WRITE YOUR FIRST PROJECT HERE
        self.shimmy()
        self.cha_cha_slide()
        self.freestyle()
        self.moonwalk()
        self.head_shake()
        # self.sprinkler()
        # self.back_it_up()

    def shimmy(self):
        print('Shimmy')
        for x in range(3):
            self.servo(30)
            self.encR(3)
            self.servo(140)
            self.encL(3)

    def cha_cha_slide(self):
        print('Cha Cha Slide')
        for x in range(3):
            self.encL(30)
            time.sleep(1)
            self.encB(30)
            time.sleep(1)
            self.servo(45)
            self.servo(45)
            self.encL(30)
            self.encR(30)

    def freestyle(self):
        print('Freestyle!')
        for x in range(3):
            self.servo(45)
            self.encR(30)
            self.servo(140)
            time.sleep(1)
            self.encL(30)
            self.encF(30)
            self.encB(30)
            self.encR(30)

    def moonwalk(self):
        print('Now for a little moonwalk')
        for x in range(2):
            self.encB(30)
            self.servo(160)
            self.encB(30)
            self.servo(160)

    def head_shake(self):
        for x in range(2):
            self.servo(30)
            self.servo(150)
        self.servo(self.MIDPOINT)


        ##################################################################################################################

    # AUTONOMOUS DRIVING
    # central logic loop of my navigation
    def nav(self):
        print("Piggy nav")
        # if loop fails, it will check for other paths
        # main app loop
        while True:
            if self.is_clear():
                self.cruise()
                self.encB(7)
            # trying to get robot to choose a new path if it cannot go forward
            answer = self.choose_path()
            # if the path is clear to the left, it will turn 45 degrees
            if answer == "left":
                self.encL(8)
            # if the path is clear to the right and not left, it will go right
            elif answer == "right":
                self.encR(8)
                # how many degrees do we actually want to turn?

    def cruise(self):
        # cruise method, tells it to go forward until something is in front of it
        time.sleep(.1)
        fwd()
        while True:
            if us_dist(15) < self.STOP_DIST:
                break
            time.sleep(.05)
        self.stop()

        ###################################################################################################################

    # this code helps me to calibrate motor speed,
    # tells me if it was driving straight
    def calibrate(self):
        print("Calibrating...")
        servo(self.MIDPOINT)
        response = input("Am I looking straight ahead? (y/n): ")
        if response == 'n':
            # Will ask what we want to do, turn r, l, or done?
            while True:
                response = input("Turn right, left, or am I done? (r/l/d): ")
                # If we want to turn right...
                if response == "r":
                    self.MIDPOINT += 1
                    print("Midpoint: " + str(self.MIDPOINT))
                    servo(self.MIDPOINT)
                    time.sleep(.01)
                # If we want to turn left...
                elif response == "l":
                    self.MIDPOINT -= 1
                    print("Midpoint: " + str(self.MIDPOINT))
                    servo(self.MIDPOINT)
                    time.sleep(.01)
                else:
                    print("Midpoint now saved to: " + str(self.MIDPOINT))
                    break
        response = input("Do you want to check if I'm driving straight? (y/n)")
        if response == 'y':

            while True:
                set_left_speed(self.LEFT_SPEED)
                set_right_speed(self.RIGHT_SPEED)
                print("Left: " + str(self.LEFT_SPEED) + "//  Right: " + str(self.RIGHT_SPEED))
                self.encF(19)
                response = input("Reduce left, reduce right or done? (l/r/d): ")
                if response == 'l':
                    self.LEFT_SPEED -= 10
                elif response == 'r':
                    self.RIGHT_SPEED -= 10
                elif response == 'd':
                    break

                    ##################################################################################################################



####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy

try:
    g = GoPiggy()
except (KeyboardInterrupt, SystemExit):
    from gopigo import *
    stop()
