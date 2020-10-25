from crazyradio import Crazyradio
from inputs import get_gamepad #to read in controller data

#initialise crazyradio device in TX mode
def radio_tx_init():
	radio = Crazyradio()
	radio.set_channel(100)
	radio.set_data_rate(Crazyradio.DR_250KPS)
	radio.set_mode(Crazyradio.MODE_PTX)
	return radio

#TX test
def radio_tx_test(radio):
	for i in range(0, 100):
		res = radio.send_packet([i])
		print(res.data)

	radio.close()
	return

#send controller packet
def radio_send_pkt(radio, data):
	res = radio.send_packet(data)
	# print(res.data) #prints raw ack

	# decodes ack
	# recdlist = res.data.tolist()
	# print(''.join(map(chr,recdlist)))

	return

dms = False #dead man's switch flag
radio = radio_tx_init()
print("CrazyRadio Initialised.")

while 1:
	events = get_gamepad()
	for event in events:
		#uncomment to see all controller input events
		#print(event.ev_type,event.code,event.state)

		#deadmanswitch L1/LB flag setting
		if event.code == 'BTN_TL' and event.state == 1:
			dms = True
		elif event.code == 'BTN_TL' and event.state == 0:
			dms = False

		if dms: #dms pressed
			#joystick input -> tweak depending on controller
			if event.code == 'ABS_Y': #throttle
				if event.state > 0:
					print("back")
					radio_send_pkt(radio,'b '+ str(event.state))
				else:
					print("forward")
					radio_send_pkt(radio,'f '+ str(event.state))

			elif event.code == 'ABS_RX': #steering
				if event.state > 0:
					print("right")
					radio_send_pkt(radio,'r '+ str(event.state))
				else:
					print("left")
					radio_send_pkt(radio,'l '+ str(event.state))

		#terminate transmission with B button
		if event.code == 'BTN_EAST':
			radio.close()
			print("Radio Transmission Closed. Ctrl-C to terminate")