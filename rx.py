from crazyradio import Crazyradio
from evdev import UInput, AbsInfo, ecodes as e

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
#to change this for different controllers, print device capabiilities using evdev and replace
#adjust virtual input events accordingly

#xinput
#cap = {1L: [304L, 305L, 307L, 308L, 310L, 311L, 314L, 315L, 316L, 317L, 318L], 3L: [(0L, AbsInfo(value=0, min=-32768, max=32767, fuzz=16, flat=128, resolution=0)), (1L, AbsInfo(value=0, min=-32768, max=32767, fuzz=16, flat=128, resolution=0)), (2L, AbsInfo(value=0, min=0, max=255, fuzz=0, flat=0, resolution=0)), (3L, AbsInfo(value=0, min=-32768, max=32767, fuzz=16, flat=128, resolution=0)), (4L, AbsInfo(value=0, min=-32768, max=32767, fuzz=16, flat=128, resolution=0)), (5L, AbsInfo(value=0, min=0, max=255, fuzz=0, flat=0, resolution=0)), (16L, AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0)), (17L, AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0))], 21L: [80L, 81L, 88L, 89L, 90L, 96L]}

#dualshock
cap = {1L: [272L, 325L, 330L, 333L], 3L: [(0L, AbsInfo(value=0, min=0, max=1920, fuzz=0, flat=0, resolution=0)), (1L, AbsInfo(value=0, min=0, max=942, fuzz=0, flat=0, resolution=0)), (47L, AbsInfo(value=0, min=0, max=1, fuzz=0, flat=0, resolution=0)), (53L, AbsInfo(value=0, min=0, max=1920, fuzz=0, flat=0, resolution=0)), (54L, AbsInfo(value=0, min=0, max=942, fuzz=0, flat=0, resolution=0)), (57L, AbsInfo(value=0, min=0, max=65535, fuzz=0, flat=0, resolution=0))]}

radio = radio_rx_init()
ui = UInput(cap, name = 'Virtual Radio Controller')
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