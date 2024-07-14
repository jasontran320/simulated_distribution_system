from pathlib import Path
from collections import namedtuple, OrderedDict
MessageType = namedtuple('MessageType', ['type', 'value', 'time'])
MessageType_receiving = namedtuple('MessageType', ['type', 'value', 'time_sent', 'time_received', 'received_from'])

class Devices:
    """Represents the different devices and handling of devices in our simulation"""
    something_sent_or_received = 0
    number_devices_with_empty_lists = 0
    @classmethod
    def create_device(cls, id_num):
        """A classmethod used to automate creating devices in the main function"""
        return cls(id_num)

    def __init__(self, id_num):
        """Initializes a device to have a specified id number, time of 0, empty lists of
        alerts and cancels the device has received and sent, and empty indexes for its lists
        as its attributes. For class attributes, will default to nothing has been sent by any device
        and 0 devices with an empty list"""
        self.device_id = id_num
        self.time = 0
        self.propogate = []
        self.alert = []
        self.alert_index = 0
        self.cancel = []
        self.cancel_index = 0
        self.receive_alert = []
        self.receive_alert_index = 0
        self.receive_cancel = []
        self.receive_cancel_index = 0
        self.did_received_cancel = 0
        self.receive_alert_after_cancel = []
        self.receive_alert_after_cancel_index = 0
        self.receive_cancel_after_cancel = []
        self.receive_cancel_after_cancel_index = 0

#Didn't create a unit test, but was able to test this in the main function instead
def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())

def _read_file(path: Path)-> list:
    """Reads input file using a given path or prints FILE NOT FOUND"""
    lst_of_lines = []
    try:
        with open(path, 'r') as input_file:
            for line in input_file.readlines():
                lst_of_lines.append(line.strip())
            return lst_of_lines
    except IOError:
        print("FILE NOT FOUND")
        return None

def creating_devices(lst: list) -> dict[str, Devices]:
    """Uses a list of read lines to create devices in an OrderedDictionary and return it,
    where keys represent device numbers and values represent a Devices class instance of that device number"""
    dct_of_devices = {}
    for line in lst:
        elements = line.split(" ")
        if elements[0] == "DEVICE":
            dct_of_devices[elements[1]] = Devices.create_device(elements[1])
    dct_of_devices = OrderedDict(sorted(dct_of_devices.items()))
    return dct_of_devices

def handling_simulation_info(lst: list, dct: dict[str, Devices]):
    """Reads the input given as a list, then appends the information to the device specified
    in the input given an OrderedDictionary of Devices class objects"""
    for line in lst:
        elements = line.split(" ")
        if elements[0] == "PROPAGATE":
            dct[elements[1]].propogate.append(MessageType(elements[0], elements[2], int(elements[3])))
        elif elements[0] == "ALERT":
            dct[elements[1]].alert.append(MessageType(elements[0], elements[2], int(elements[3])))
        elif elements[0] == "CANCEL":
            dct[elements[1]].cancel.append(MessageType(elements[0], elements[2], int(elements[3])))
        else:
            pass

def sorting_simulation_info(dct: dict[str, Devices]):
    """Given some dictionary full of Devices objects, this will sort the lists regarding
    cancels and alerts an individual device will need to initialize first by time, then by description"""
    for device in dct.values():
        device.propogate = sorted(device.propogate, key=lambda x: (x.value))
        device.alert = sorted(device.alert, key=lambda x: (x.time, x.value))
        device.cancel = sorted(device.cancel, key = lambda x: x.time)

def check_for_cancel(device, receive_cancel_index = "Default", recv_alerts = "Default"):
    """Function for checking whether or not a cancel/alert should be propagated any further
    based on if the device is aware of a cancel of that same description."""
    device.did_received_cancel = 0
    if recv_alerts != "Default":
        for cancel in device.cancel:
            if cancel.value == recv_alerts.value and cancel.time <= recv_alerts.time_received:
                device.did_received_cancel = 1
        for cancel in device.receive_cancel:
            if cancel.value == recv_alerts.value and cancel.time_received <= recv_alerts.time_received:
                device.did_received_cancel = 1
    elif receive_cancel_index != "Default":
        recv_cancel = device.receive_cancel[receive_cancel_index]
        for cancel in device.cancel:
            if cancel.value == recv_cancel.value and cancel.time <= recv_cancel.time_received:
                device.did_received_cancel = 1
        for i, cancel in enumerate(device.receive_cancel):
            if i != receive_cancel_index and cancel.value == recv_cancel.value and cancel.time_received <= recv_cancel.time_received:
                device.did_received_cancel = 1

#Didn't unit test whether alert_index or something_sent_is_received incremented.
#This is because that can be clearly seen in the print message. If a message is printed, the code preceding it will also be processed
def sending_alerts(dct: dict[str, Devices], device: Devices, alerts: MessageType):
    """Function for initializing an alert based off whether or not the simulation time matches the time the alert should
    be sent out."""
    if alerts.time == device.time:
        Devices.something_sent_or_received = 1
        device.alert_index += 1
        for number_to_send_to in device.propogate:
            named_tuple_to_send = MessageType_receiving(alerts.type, alerts.value, device.time,
                                  alerts.time + number_to_send_to.time, device.device_id)
            print(f"@{named_tuple_to_send.time_sent} #{named_tuple_to_send.received_from}: SENT {named_tuple_to_send.type} TO #{number_to_send_to.value}: {named_tuple_to_send.value}")
            dct[number_to_send_to.value].receive_alert.append(named_tuple_to_send)

#Didn't test certain attributes incrementing for the same reasons as above
def sending_cancels(dct: dict[str, Devices], device: Devices, cancels: MessageType):
    """Function for initializing an alert based off whether a given device is aware of a cancel
    of the same description, and whether or not the simulation time matches the time the alert should
    be sent out."""
    if cancels.time == device.time:
        Devices.something_sent_or_received = 1
        device.cancel_index += 1
        for number_to_send_to in device.propogate:
            named_tuple_to_send = MessageType_receiving(cancels.type, cancels.value, device.time,
                                  cancels.time + number_to_send_to.time, device.device_id)
            print(f"@{named_tuple_to_send.time_sent} #{named_tuple_to_send.received_from}: SENT CANCELLATION TO #{number_to_send_to.value}: {named_tuple_to_send.value}")
            dct[number_to_send_to.value].receive_cancel.append(named_tuple_to_send)

#Didn't test certain attributes incrementing for the same reasons as above
#Didn't unittest for if device times matched up or not
#This is because I already tested a similar process in sending_alerts
#Bottom line is that a cancel doesn't send or receive until it is supposed to
def receiving_cancels(dct: dict[str, Devices], device: Devices, recv_cancel: MessageType_receiving):
    """Function for receiving cancels and then determining whether to send it out based off of
    did_received_cancel."""
    check_for_cancel(device, receive_cancel_index = device.receive_cancel_index)
    if device.did_received_cancel != 1:
        if recv_cancel.time_received == device.time:
            Devices.something_sent_or_received = 1
            print(f"@{device.time} #{device.device_id}: RECEIVED CANCELLATION FROM #{recv_cancel.received_from}: {recv_cancel.value}")
            device.receive_cancel_index += 1
            for number_to_send_to in device.propogate:
                named_tuple_to_send = MessageType_receiving(recv_cancel.type, recv_cancel.value, device.time,
                                      recv_cancel.time_received + number_to_send_to.time, device.device_id)
                print(f"@{named_tuple_to_send.time_sent} #{named_tuple_to_send.received_from}: SENT CANCELLATION TO #{number_to_send_to.value}: {named_tuple_to_send.value}")
                dct[number_to_send_to.value].receive_cancel.append(named_tuple_to_send)
    else:
        if recv_cancel.time_received == device.time:
            device.receive_cancel_after_cancel.append(recv_cancel)
            device.receive_cancel_index += 1

#Didn't test certain attributes incrementing for the same reasons as above
#Again, did not test for if a device didn't have a matching time
#Same reasons for why I didn't test receiving_cancels in this sense
def receiving_alerts(dct: dict[str, Devices], device: Devices, recv_alert: MessageType_receiving):
    """Function for receiving alerts and then determining whether to send it out based off of
    did_received_cancel."""
    check_for_cancel(device, recv_alerts = recv_alert)
    if device.did_received_cancel != 1:
        if recv_alert.time_received == device.time:
            Devices.something_sent_or_received = 1
            print(f"@{device.time} #{device.device_id}: RECEIVED ALERT FROM #{recv_alert.received_from}: {recv_alert.value}")
            device.receive_alert_index += 1
            for number_to_send_to in device.propogate:
                named_tuple_to_send = MessageType_receiving(recv_alert.type, recv_alert.value, device.time,
                                      recv_alert.time_received + number_to_send_to.time, device.device_id)
                print(f"@{named_tuple_to_send.time_sent} #{named_tuple_to_send.received_from}: SENT {named_tuple_to_send.type} TO #{number_to_send_to.value}: {named_tuple_to_send.value}")
                dct[number_to_send_to.value].receive_alert.append(named_tuple_to_send)
    else:
        if recv_alert.time_received == device.time:
            device.receive_alert_after_cancel.append(recv_alert)
            device.receive_alert_index += 1

#Didn't test certain attributes incrementing for the same reasons as above
#Again, did not test for if a device didn't have a matching time
#Same reasons for why I didn't test receiving_cancels in this sense
def receiving_cancels_when_in_cancel(device: Devices):
    """Handles the case for when a cancel is received when a given device is already aware
    of that cancel of the same description."""
    cancel = device.receive_cancel_after_cancel[device.receive_cancel_after_cancel_index]
    if cancel.time_received == device.time:
        Devices.something_sent_or_received = 1
        print(f"@{device.time} #{device.device_id}: RECEIVED CANCELLATION FROM #{cancel.received_from}: {cancel.value}")
        device.receive_cancel_after_cancel_index += 1

#Didn't test certain attributes incrementing for the same reasons as above
#Again, did not test for if a device didn't have a matching time
#Same reasons for why I didn't test receiving_cancels in this sense
def receiving_alerts_when_in_cancel(device: Devices):
    """Handles the case for when a cancel is received when a given device is already aware
    of that cancel of the same description."""
    alert = device.receive_alert_after_cancel[device.receive_alert_after_cancel_index]
    if alert.time_received == device.time:
        Devices.something_sent_or_received = 1
        print(f"@{device.time} #{device.device_id}: RECEIVED ALERT FROM #{alert.received_from}: {alert.value}")
        device.receive_alert_after_cancel_index += 1

#Didn't test for all cases for when lists are not empty
#This is because I wanted to test that this function will return true when they are empty, and false otherwise
#That is why one counter example was sufficient enough
def all_lists_are_empty(device: Devices)-> bool:
    """Checks for if a given device has anything to propagate or receive. If a device has nothing
     to propagate or receive, returns True and False otherwise"""
    truthy = 0
    if len(device.alert) - 1 < device.alert_index:
        truthy += 1
    if len(device.cancel) - 1 < device.cancel_index:
        truthy += 1
    if len(device.receive_cancel) - 1 < device.receive_cancel_index:
        truthy += 1
    if len(device.receive_alert) - 1 < device.receive_alert_index:
        truthy += 1
    if len(device.receive_cancel_after_cancel) == 0 or len(device.receive_cancel_after_cancel) - 1 < device.receive_cancel_after_cancel_index:
        truthy += 1
    if len(device.receive_alert_after_cancel) == 0 or len(device.receive_alert_after_cancel) - 1 < device.receive_alert_after_cancel_index:
        truthy += 1
    if truthy == 6:
        return True
    else:
        return False

def sort_recv_alert_and_cancel(device: Devices):
    """Sorts the lists containing received messages of a given device first by time the device
    should receive it, then description, then the ID of the device that sent it."""
    if len(device.receive_alert) > 1:
        device.receive_alert = sorted(device.receive_alert, key=lambda x: (x.time_received, x.value, x.received_from))
    if len(device.receive_cancel) > 1:
        device.receive_cancel = sorted(device.receive_cancel, key=lambda x: (x.time_received, x.value, x.received_from))

def simulation_loop(dct: dict[str, Devices]):
    """Represents the simulation run. Will keep on running until all alerts and cancellations in the
    input file have been sent and all propagating messages have been sent and received"""
    while True:
        Devices.something_sent_or_received = 0
        if Devices.number_devices_with_empty_lists == len(dct):
            break
        else:
            Devices.number_devices_with_empty_lists = 0
        for device in dct.values():
            if all_lists_are_empty(device) == True:
                Devices.number_devices_with_empty_lists += 1
            else:
                sort_recv_alert_and_cancel(device)
                if len(device.receive_cancel) - 1 >= device.receive_cancel_index:
                    receiving_cancels(dct, device, device.receive_cancel[device.receive_cancel_index])
                if len(device.receive_alert) - 1 >= device.receive_alert_index:
                    receiving_alerts(dct, device, device.receive_alert[device.receive_alert_index])
                if len(device.receive_cancel_after_cancel) - 1 >= device.receive_cancel_after_cancel_index:
                    receiving_cancels_when_in_cancel(device)
                if len(device.receive_alert_after_cancel) - 1 >= device.receive_alert_after_cancel_index:
                    receiving_alerts_when_in_cancel(device)
                if len(device.alert) - 1 >= device.alert_index:
                    sending_alerts(dct, device, device.alert[device.alert_index])
                if len(device.cancel) - 1 >= device.cancel_index:
                    sending_cancels(dct, device, device.cancel[device.cancel_index])
        if Devices.something_sent_or_received == 0:
            for device in dct.values():
                device.time += 1

#Opted not to make a unittest for main, as it is just as easily testable in the main module
def main() -> None:
    """Runs the simulation program in its entirety"""
    p = _read_input_file_path()
    lst = _read_file(p)
    if lst != None:
        dct = creating_devices(lst)
        handling_simulation_info(lst, dct)
        sorting_simulation_info(dct)
        simulation_loop(dct)

if __name__ == '__main__':
    main()
