from queue import Queue
from beacontools import BeaconScanner, IBeaconFilter

data_dict = {}

Beacon_Data = ""
Accelerometer_Data = ""
Input_Data = ""
input_data = ""


def callback(bt_addr, rssi, packet, additional_info):
    global Input_Data
    Input_Data = packet
    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))


def uuid_acc(data):
    s = data[12:16]
    x = int(s, 16)
    # print(x)
    return x


def x_axis(data):
    s = data[30:34]
    x = int(str(s), 16)
    # print(x)
    return x


def y_axis(data):
    s = data[34:38]
    x = int(str(s), 16)
    # print(x)
    return x


def z_axis(data):
    s = data[38:42]
    x = int(str(s), 16)
    # print(x)
    return x


def mac_addr_acc(data):
    s = data[42:54]
    x = int(str(s), 16)
    # print(x)
    return x


def uuid_ibeacon(data):
    s = data[20:52]
    x = int(str(s), 16)
    # print(x)
    return x


def check_stationary(uuid):
    q = data_dict[uuid]
    if q.qsize() == 5:
        list_queue = list(q.queue)

        if (list_queue[0] == list_queue[1] == list_queue[2] == list_queue[3] == list_queue[4]):
            print("Stationary")
        else:
            print("Moving")
    else:
        print("5 elements not available")


def data_queue(uuid, x_y_z):  # Creating Dataset
    if uuid in data_dict:
        q = data_dict[uuid]

    else:
        q = Queue(maxsize=5)

    if q.qsize() == 5:
        q.get()
        q.put(x_y_z)
    else:
        q.put(x_y_z)
    data_dict[uuid] = q


while 1:  # Main Code

    # scan for all iBeacon advertisements from beacons with the specified uuid
    #scanner = BeaconScanner(callback,
    #                        device_filter=IBeaconFilter(uuid="53594F4F-4B53-4F43-4941-4C4449535445")
    #                        )
    
    # scan for all iBeacon advertisements regardless from which beacon
    
    scanner = BeaconScanner(callback,
    packet_filter=IBeaconAdvertisement
    )

    scanner.start()
    
    global Input_Data, input_data
    
    if (Input_Data != input_data):
        
        input_data = Input_Data
        Length = len(input_data)
    
        if Length > 56:  # Check if it is a Beacon Data or Accelerometer Data
            Beacon = input_data
    
        else:
            Accelerometer_Data = input_data
    
        uuid_acc_data = uuid_acc(Accelerometer_Data)  # Parsing value from the uuid data packet
        x_axis_data = x_axis(Accelerometer_Data)  # Parsing value from the x_axis data packet
        y_axis_data = y_axis(Accelerometer_Data)  # Parsing value from the y_axis data packet
        z_axis_data = z_axis(Accelerometer_Data)  # Parsing value from the z_axis data packet
        x_y_z_data = str(x_axis_data) + '*' + str(y_axis_data) + '*' + str(z_axis_data)
    
        data_queue(uuid_acc_data, x_y_z_data)
        check_stationary(uuid_acc_data)
