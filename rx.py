from crazyradio import Crazyradio

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

def pkt_decode(data):
	pkt = data.tolist()

	#print(''.join(map(chr,pkt)))
	return ''.join(map(chr,pkt))

radio = radio_rx_init()
print('Ready to Receive')

while 1:
	res = radio.receive()
	if res:
		radio.sendAck('ack')
	print(pkt_decode(res))