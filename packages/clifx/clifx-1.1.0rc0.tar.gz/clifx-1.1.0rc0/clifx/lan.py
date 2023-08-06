import sys
from time import sleep

def fetch_device(lifxLAN, label, max_attempts, timeout):
    attempt = 1
    while attempt <= max_attempts:
        try:
            device = lifxLAN.get_device_by_name(label)
            if device is None:
                raise Exception(f"Failed to find a device with the label '{label}'")
            return device
        except Exception as e:
            print(
                f"Failed to find '{label}', trying again"
                + f" [{attempt}/{max_attempts}]: {e}",
                file=sys.stderr
            )
            sleep(timeout)
            attempt += 1
    print("FAILED!")
    exit()
