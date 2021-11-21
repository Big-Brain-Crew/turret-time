import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = b'Connected'
addr = ("127.0.0.1", 12000)
client_socket.sendto(message, addr)

while True:
    message, address = client_socket.recvfrom(1024)
    print(message.decode('utf-8'))
#try:
#    data, server = client_socket.recvfrom(1024)
#    end = time.time()
#    elapsed = end - start
#    print(f'{data} {pings} {elapsed}')
#except socket.timeout:
#    print('REQUEST TIMED OUT')