import Streamclass2 as SC
from Arduino import Arduino

servox = 9
servoy = 10

arduino = Arduino()
client = SC.Socket()
client.Client(IP='192.168.1.8')

arduino.Servos.attach(servox)
arduino.Servos.attach(servoy)

while True:
    client.ClientStream()
    data = client.Clientreceive()
    data = data.decode()
    Servpos = data.split('-')
    servxp = float(Servpos[0])
    servyp = float(Servpos[1])
    arduino.Servos.write(servox, servxp)
    arduino.Servos.write(servoy, servyp)