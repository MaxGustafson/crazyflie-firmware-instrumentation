import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

URI = 'radio://0/80/2M'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


def fly_eight(cf):

	cf.param.set_value('kalman.resetEstimation', '1')
	time.sleep(0.1)
	cf.param.set_value('kalman.resetEstimation', '0')
	time.sleep(2)
		
	for y in range(10):
		cf.commander.send_hover_setpoint(0, 0, 0, y / 25)
		time.sleep(0.1)

	for _ in range(20):
		cf.commander.send_hover_setpoint(0, 0, 0, 0.4)
		time.sleep(0.1)

	for _ in range(50):
		cf.commander.send_hover_setpoint(0.5, 0, 36 * 2, 0.4)
		time.sleep(0.1)

	for _ in range(50):
		cf.commander.send_hover_setpoint(0.5, 0, -36 * 2, 0.4)
		time.sleep(0.1)

	for _ in range(20):
		cf.commander.send_hover_setpoint(0, 0, 0, 0.4)
		time.sleep(0.1)

	for y in range(10):
		cf.commander.send_hover_setpoint(0, 0, 0, (10 - y) / 25)
		time.sleep(0.1)

	cf.commander.send_stop_setpoint()

def fly_straight(cf):

	#Initial Statements
	cf.param.set_value('kalman.resetEstimation', '1')
	time.sleep(0.1)
	cf.param.set_value('kalman.resetEstimation', '0')
	time.sleep(2)


	#Lift...  
	for y in range(10):
		cf.commander.send_hover_setpoint(0, 0, 0, y / 25)
		time.sleep(0.1)

	# ... and Hover
	for _ in range(20):
		cf.commander.send_hover_setpoint(0, 0, 0, 0.4)
		time.sleep(0.1)


	#Quickly go back and forth
	for _ in range(4):

			cf.commander.send_hover_setpoint(0.6, 0, 0, 0.4)
			time.sleep(0.05)
			cf.commander.send_hover_setpoint(-0.6, 0, 0, 0.4)
			time.sleep(0.05)



	#Hover...
	for _ in range(20):
		cf.commander.send_hover_setpoint(0, 0, 0, 0.4)
		time.sleep(0.1)

	#... and land
	for y in range(10):
		cf.commander.send_hover_setpoint(0, 0, 0, (10 - y) / 25)
		time.sleep(0.1)


def fly_square(cf):

	#Initial Statements
	cf.param.set_value('kalman.resetEstimation', '1')
	time.sleep(0.1)
	cf.param.set_value('kalman.resetEstimation', '0')
	time.sleep(2)


	#Lift...  
	for y in range(10):
		cf.commander.send_hover_setpoint(0, 0, 0, y / 25)
		time.sleep(0.1)

	# ... and Hover
	for _ in range(20):
		cf.commander.send_hover_setpoint(0, 0, 0, 0.4)
		time.sleep(0.1)


	#Quickly go in square
	for _ in range(2):

			cf.commander.send_hover_setpoint(0.6, 0, 0, 0.4)
			time.sleep(0.05)
			cf.commander.send_hover_setpoint(0, 0.6, 0, 0.4)
			time.sleep(0.05)
			cf.commander.send_hover_setpoint(-0.6, 0, 0, 0.4)
			time.sleep(0.05)
			cf.commander.send_hover_setpoint(0, -0.6, 0, 0.4)
			time.sleep(0.05)


	#Hover...
	for _ in range(20):
		cf.commander.send_hover_setpoint(0, 0, 0, 0.4)
		time.sleep(0.1)

	#... and land
	for y in range(10):
		cf.commander.send_hover_setpoint(0, 0, 0, (10 - y) / 25)
		time.sleep(0.1)


def param_stab_est_callback(name, value):
    print('The crazyflie has parameter ' + name + ' set at number: ' + value)

if __name__ == '__main__':
	# Initialize the low-level drivers
	cflib.crtp.init_drivers()

	with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
		cf = scf.cf
		
		cf.param.add_update_callback(group='usd', name='logging',
                                 cb=param_stab_est_callback)
                                 
        
		time.sleep(5)
		cf.param.set_value('usd.logging',1)
		time.sleep(5)
		
		#fly_eight(cf)
		fly_straight(cf)
		fly_square(cf)
		
		time.sleep(5)
		cf.param.set_value('usd.logging',0)
		time.sleep(5)