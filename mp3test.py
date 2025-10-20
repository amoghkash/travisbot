import serial
from time import sleep
ser = serial.Serial('/dev/serial0', 9600, timeout=1)
sleep(2)
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
    start_byte = 0x7e
    version = 0xff
    length = 0x06
    end_byte = 0xef
    fb = 0x01

    param_high = (param >> 8) & 0xFF
    param_low = param & 0xFF

    # Calculate checksum (16-bit)
    checksum = 0xFFFF - (version + length + command + fb + param_high + param_low) + 1
    checksum_high = (checksum >> 8) & 0xFF
    checksum_low = checksum & 0xFF

    # Construct full command frame
    frame = bytes([start_byte, version, length,
                   command, fb, param_high, param_low,
                   checksum_high, checksum_low, end_byte])
    # 10/19/2025: First command: cmd: 0c params: 00 00
    # 10/19/2025: 2nd command: cmd: 06 params: 00 0f
    # 10/19/2025: third command: cmd: 07 params: 00 00  
    # 10/19/2025: fourth command: cmd: 09 params: 00 01
    
    #print(frame)
    return frame
media = 1 #what should the media equal? Answer: should equal 1
#cmd = df_command(0x09, media) 
#ser.write(cmd)
#cmd = df_command(0x06, 0x0F)
#print(cmd)
#ser.write(cmd)

#ser.write(cmd)
#ser.write(df_command(0x0F, 2, feedback=True))
#ser.write(df_command(0x43))
#while True:

sleep(0.1)
cmd = df_command(0x0C, 0) #this command resets the player
ser.write(serial.to_bytes(cmd))
sleep(1)
cmd = df_command(0x09, 1) #this cmd specifies playback source to TF card (0x09 is cmd to specify playback src)
ser.write(serial.to_bytes(cmd))
sleep(1)
cmd = df_command(0x07, 0)  # 0x07 = Specify EQ to normal (0)
ser.write(serial.to_bytes(cmd)) #trying this shit out from stack exchange
sleep(1)
cmd = df_command(0x06, 9) #this cmd specifies the volume to 9 (0x06 is cmd to specify volume, 9 is parameter)\
ser.write(serial.to_bytes(cmd)) 
sleep(1)
cmd = df_command(0x11 , 1) #cmd to specify start repeat play
ser.write(serial.to_bytes(cmd))
