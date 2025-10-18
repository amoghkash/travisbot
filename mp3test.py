import serial
from time import sleep
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
sleep(4)
def df_command(command, param=0, feedback=True):
    """
    Build a 10-byte DFPlayer Mini command frame.
    
    Args:
        command (int): The DFPlayer command byte (e.g., 0x0F for play track)
        param (int): 16-bit parameter (e.g., track number)
        feedback (bool): True to request feedback from DFPlayer
        
    Returns:
        bytes: The complete 10-byte command frame ready to send.
    """
    start_byte = 0x7E
    version = 0xFF
    length = 0x06
    end_byte = 0xEF
    fb = 0x01

    param_high = (param >> 8) & 0xFF
    param_low = param & 0xFF

    # Calculate checksum (16-bit)
    checksum = 0xFFFF - (version + length + command + fb + param_high + param_low) + 1
    checksum_high = (checksum >> 8) & 0xFF
    checksum_low = checksum & 0xFF

    # Construct full command frame
    frame = bytes([
        start_byte,
        version,
        length,
        command,
        fb,
        param_high,
        param_low,
        checksum_high,
        checksum_low,
        end_byte
    ])
    return frame
cmd = df_command(0x06, 25)
#print(cmd)
ser.write(cmd)

cmd = df_command(0x0F, 2)  # 0x0F = "play track N"
ser.write(cmd)
ser.write(df_command(0x0F, 1, feedback=True))
ser.write(df_command(0x43))
print(ser.read_all())
try:
    while True:
        # Send "query current track" command with feedback
        ser.write(df_command(0x43, feedback=True))

        # Wait a short time for response
        sleep(0.1)

        # Read all bytes available in UART buffer
        response = ser.read_all()
        
        cmd = df_command(0x06, 25)
        ser.write(cmd)
        if response:
            # Basic validation: response should be 10 bytes
            if len(response) >= 10:
                print(f"respons is {response}")
                param_high = response[5]
                param_low  = response[6]
                print(f"param_high is {param_high}")
                print(f"param_low is {param_low}")
                current_track = (param_high << 8) | param_low
                print(f"Current track: {current_track}")
            else:
                print(f"Incomplete response: {response}")
        else:
            print("No response yet")

        # Optional: query every 1 second
        sleep(1)

except KeyboardInterrupt:
    print("Stopping DFPlayer listener")
    ser.close()
