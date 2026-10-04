import socket

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except:
        return False

# def is_connected(): --> Old (Used to work, for some reason...)
#     try:
#         import pywhatkit
#         return True
#     except:
#         return False

#*----------END_OF_CODE----------*