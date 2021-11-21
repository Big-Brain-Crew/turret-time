import socket
import pygame
import asyncio

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 12000))

pygame.display.init()
pygame.joystick.init()
pygame.joystick.Joystick(0).init()

# Prints the joystick's name
JoyName = pygame.joystick.Joystick(0).get_name()
print("Name of the joystick:")
print(JoyName)
# Gets the number of axes
JoyAx = pygame.joystick.Joystick(0).get_numaxes()
print("Number of axis:")
print(JoyAx)



#while True:
message, address = server_socket.recvfrom(1024)
print(message.decode('utf-8'))

while True:
    pygame.event.pump()
    return_message = (str(pygame.joystick.Joystick(0).get_axis(0))+", "+str(pygame.joystick.Joystick(0).get_axis(1)))

    #message, address = server_socket.recvfrom(1024)
    #print(message.decode('utf-8'))
    #message = message.upper()
    if return_message:
        server_socket.sendto(bytes(return_message, 'utf-8'), address)