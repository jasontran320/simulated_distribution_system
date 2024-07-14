Our simulation model is built around a few core concepts, which need to be understood before delving into the implementation and testing details.

First, we are simulating a distributed system composed of Internet-connected electronic devices that can communicate with each other individually. The specific functionality of these devices is not important for our purposes; we only care that they can exchange messages.

Each device has a unique device ID, a non-negative integer, that distinguishes it from other devices. When a device detects an issue that might affect other devices, it raises an alert to notify them. It sends a message to a subset of devices, which then propagate the alert to others, a process we call propagation. This method ensures that the initial device doesn't need to send thousands of messages; instead, it relies on other devices to spread the alert.

Every alert has a unique description, a short string of text, which remains unchanged during propagation so all devices recognize it. When the issue is resolved, a device sends a cancellation message with the alert's description to inform other devices that the alert is no longer active. Once a device receives a cancellation, it stops propagating that alert.

Each device is set up to propagate alerts and cancellations to a predefined set of other devices, known as its propagation set. When a device receives an alert or cancellation, it immediately notifies its propagation set unless it has already received a cancellation for that alert. This process introduces a delay, meaning a message sent at a specific time will be received later. Delays can arise from the time it takes to process and forward messages or intentional slowing to avoid network flooding. The longer the delay, the less bandwidth is used, but the slower distant devices become aware of the alert.

The effect of these rules is straightforward. An alert raised by a device will propagate until all devices are notified of its cancellation. Communication delays mean there will be a lag between the alert being raised and all devices becoming aware, and some devices may act on outdated information until they receive the cancellation.

Consider a scenario with four devices: Device 1, Device 2, Device 3, and Device 4, with the following propagation set configurations:

    Device 1 to Device 2 with a delay of 750 milliseconds.
    Device 2 to Device 3 with a delay of 1,250 milliseconds.
    Device 3 to Device 4 with a delay of 500 milliseconds.
    Device 4 to Device 1 with a delay of 1,000 milliseconds.

If Device 1 raises an alert at time 0, the subsequent communication cascade can be simulated as follows:

    At time 0, Device 1 sends a message to Device 2.
    At time 750, Device 2 receives the alert and sends a message to Device 3.
    At time 2,000, Device 3 receives the alert and propagates it.
    At time 2,200, Device 1 cancels the alert and sends a cancellation to Device 2.
    At time 2,500, Device 4 receives the alert from Device 3 and propagates it to Device 1.
    At time 2,950, Device 2 receives the cancellation and propagates it to Device 3.
    At time 3,500, Device 1 receives the alert from Device 4 but does not propagate it due to the cancellation.
    At time 4,200, Device 3 receives the cancellation and propagates it to Device 4.
    At time 4,700, Device 4 receives the cancellation and propagates it to Device 1.
    At time 5,700, Device 1 receives the cancellation again but does not propagate it further.

With no messages in flight, the system remains quiet until another alert is raised.

Example run is running the following
```
python project1.py
```

Which will prompt the input where user will place the path to the sample input file:
```
sample_input.txt
```
