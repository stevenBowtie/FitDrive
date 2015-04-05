#!/usr/bin/python
import sys
import cwiid
import sys
from time import sleep
import socket

def main():
	#Connect to address given on command-line, if present
	print 'Put Wiimote in discoverable mode now (press 1+2)...'
	global wiimote
	if len(sys.argv) > 1:
		wiimote = cwiid.Wiimote(sys.argv[1])
	else:
		wiimote = cwiid.Wiimote()

	wiimote.rpt_mode = cwiid.RPT_BALANCE | cwiid.RPT_BTN
	wiimote.request_status()


	balance_calibration = wiimote.get_balance_cal()
	named_calibration = { 'right_top': balance_calibration[0],
						  'right_bottom': balance_calibration[1],
						  'left_top': balance_calibration[2],
						  'left_bottom': balance_calibration[3],
						}

	exit = False
	#Begin Calibration
	print 'Stand on board and press enter'
	c = sys.stdin.read(1)
	wiimote.request_status()
	center=wiimote.state['balance']
	print 'Lean forward and left, press enter'
	c = sys.stdin.read(1)
	wiimote.request_status()
	lf_cal=wiimote.state['balance']['left_top']
	print 'Lean back and left, press enter'
	c = sys.stdin.read(1)
	wiimote.request_status()
	lb_cal=wiimote.state['balance']['left_bottom']
	print 'Lean back and right, press enter'
	c = sys.stdin.read(1)
	wiimote.request_status()
	rb_cal=wiimote.state['balance']['right_bottom']
	print 'Lean forward and right, press enter'
	c = sys.stdin.read(1)
	wiimote.request_status()
	rf_cal=wiimote.state['balance']['right_top']
	#determine ranges
	lf_range=lf_cal-center['left_top']
	lb_range=lf_cal-center['left_bottom']
	rb_range=rb_cal-center['right_bottom']
	rf_range=rf_cal-center['right_top']
	def calculate_xy():
		wiimote.request_status()
		lf=max(0,wiimote.state['balance']['left_top']-center['left_top'])
		rf=max(0,wiimote.state['balance']['right_top']-center['right_top'])
		lb=max(0,wiimote.state['balance']['left_bottom']-center['left_bottom'])
		rb=max(0,wiimote.state['balance']['right_bottom']-center['right_bottom'])
		left=(lf*1.0/lf_range)+(1.0*lb/lb_range)
		right=(1.0*rf/rf_range)+(1.0*rb/rb_range)
		y=max(0,min(128,int(right*64+64-left*64)))
		front=(rf*1.0/rf_range)+(lf*1.0/lf_range)
		back=(rb*1.0/rb_range)+(lb*1.0/lb_range)
		x=max(0,min(128,int(front*64+64-back*64)))
		return [x,y]
		
#	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
	while 1:
		coords=calculate_xy()
		print coords
		mesg=chr(coords[0])+chr(coords[1])
		sleep(0.1)
		#result=sock.sendto(mesg, ('10.10.2.20', 4444))
		#print result
main()
