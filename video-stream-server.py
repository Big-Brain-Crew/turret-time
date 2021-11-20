# This code is for the server
# Lets import the libraries
import socket, cv2, pickle, struct, imutils

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(('', port))

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)


# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        vid = cv2.VideoCapture("/dev/video0")

        while True:
            img, frame = vid.read()
            frame = imutils.resize(frame, width=320)
            a = pickle.dumps(frame) #serialize frame to bytes
            message = struct.pack("Q", len(a)) + a # pack the serialized data
            # print(message)
            try:
                client_socket.sendall(message) #send message or data frames to client
            except Exception as e:
                print(e)
                raise Exception(e)


            cv2.imshow('TRANSMITTING VIDEO', frame) # will show video frame on server side.
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):

                client_socket.close()
