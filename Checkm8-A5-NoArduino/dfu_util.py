import usb.core
import usb.util
import time

global device

# Define USB constants
USB_DIR_OUT = 0x00
USB_TYPE_CLASS = (0x01 << 5)
USB_RECIP_INTERFACE = 0x01

# Define endpoint and interface information (adjust as needed)
ENDPOINT_OUT = 0x01
INTERFACE = 0

# Define CPID as 8940
CPID_8940 = 8940

# Define the function to send a control transfer
def send_control_transfer(bmRequestType, bRequest, wValue, wIndex, data):
    try:
        device = usb.core.find(idVendor=0x05AC, idProduct=0x1227)
        if device is None:
            print(f'params: {bmRequestType}, {bRequest}, {wValue}, {wIndex}, {data}: DEBUG EXT: Device not found')
            exit()

        # Detach kernel driver if active
        if device.is_kernel_driver_active(INTERFACE):
            print(f"params: {bmRequestType}, {bRequest}, {wValue}, {wIndex}, {data}: Detaching kernel driver")
            device.detach_kernel_driver(INTERFACE)
            print(f"params: {bmRequestType}, {bRequest}, {wValue}, {wIndex}, {data}: Detached the kernel driver")
        else:
            print(f"params: {bmRequestType}, {bRequest}, {wValue}, {wIndex}, {data}: No kernel driver active, not detaching")

        # Set the active configuration
        print(f"params: {bmRequestType}, {bRequest}, {wValue}, {wIndex}, {data}: Setting active config")
        device.set_configuration() 

        # Send the control transfer
        print(f"params: {bmRequestType}, {bRequest}, {wValue}, {wIndex}, {data}: Sending the control transfer")
        device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, data)
        print(f"params: {bmRequestType}, {bRequest}, {wValue}, {wIndex}, {data}: Sent the control transfer")

    except Exception as e:
        print(f'\n--------------------\nError in send_control_transfer(): {e}\n-----------------------')

# Define the function to enter DFU mode
def enter_dfu_mode():
    try:
        # Send the necessary control transfers to enter DFU mode
        print("Attempting to enter DFU mode\n--------------------------")
        send_control_transfer(0x21, 1, 0, 0, b'')
        time.sleep(0.1)  # Add a delay if needed
        send_control_transfer(0xA1, 3, 1, INTERFACE, b'\x01')
        time.sleep(0.1)  # Add a delay if needed
        send_control_transfer(0xA1, 3, 1, INTERFACE, b'\x01')
        time.sleep(0.1)  # Add a delay if needed
        usb.util.dispose_resources(device)

        print("\n--------------------\nEntered DFU mode successfully.\n-----------------------------")

    except Exception as e:
        print(f'\n--------------------\nError in enter_dfu_mode(): {e}\n-----------------------')

# Define the function to send the payload
def send_payload(filename):
    with open(filename, 'rb') as f:
        payload = f.read()

    for i in range(0, len(payload), 64):
        chunk = payload[i:i+64]
        send_control_transfer(0x21, 1, 0, 0, chunk)

if __name__ == "__main__":
    pass  # Add any test code here
