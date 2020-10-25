from crazyradio import Crazyradio
from evdev import UInput, ecodes as e

#initialise crazyradio device in RX mode
def radio_rx_init():
	radio = Crazyradio()
	radio.set_channel(100)
	radio.set_data_rate(Crazyradio.DR_250KPS)
	radio.set_mode(Crazyradio.MODE_PRX)
	return radio

#RX test
def radio_rx_test(radio):
	for i in range(0, 100):
		res = radio.receive()
		if res:
			radio.sendAck([i])
		print(res)
	radio.close()
	return

#decodes incoming radio packets (array B)
#returns ASCII string
def pkt_decode(data):
	pkt = data.tolist()

	#print(''.join(map(chr,pkt)))
	return ''.join(map(chr,pkt))

#writes to joystick
def write_joy(ui, intype, inval):
	joy = {'b' : e.ABS_Y, 'f' : e.ABS_Y,
		   'r' : e.ABS_RX, 'l' : e.ABS_RX}

	ui.write(e.EV_ABS, joy.get(intype), inval)
	ui.syn()

	return

def dms_on(ui):
	ui.write(e.EV_KEY, e.BTN_TL, 1)
	ui.syn()
	return

def dms_off(ui):
	ui.write(e.EV_KEY, e.BTN_TL, 0)
	ui.syn()
	return
#virtual controller dictionary

cap = { e.EV_KEY: [e.BTN_TL], #dms
		e.EV_ABS: [e.ABS_Y, e.ABS_RX]} #joysticks for throttle and steering

radio = radio_rx_init()
ui = UInput(cap)
dms = False
print('Ready to Receive')

while 1:
	res = radio.receive()
	if res:
		dms = True
		radio.sendAck('ack')
		msg = (pkt_decode(res))
		#print(msg)

		intype = msg[0] #char code for movement type b,f,r,l
		inval = int(msg[2:]) #joystick input value

		dms_on(ui)
		write_joy(ui, intype, inval)

	elif res == None and dms == True:
		dms = False
		dms_off(ui)