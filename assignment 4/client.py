import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asks the user for the server IP and tries to connect to it
ip = input("Enter server IP: ")
client.connect((ip, 4000))

# Asks the user for a username and channel
name = input("Enter username: ")
channel = input("Enter channel 1 or 2: ")

# Receives messages from the server and prints them
# If the message is 'USR', it sends the username to the server
# If the message is 'CHN', it sends the channel to the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'USR':
                client.send(name.encode('utf-8'))
            elif message == 'CHN':
                client.send(channel.encode('utf-8'))
            else:
                print(message)
        # Closes the client if the connection fails
        except:
            print("Connection failed")
            client.close()
            break

# Asks the user for message input and sends it to the server
# If the message starts with /msg, it sends a private message to the user
# If the message starts with /exit, it closes the client
def write():
    while True:
        message = f'{name}: {input("")}'
        if(message[len(name)+2:].startswith('/msg ')):
            client.send(f'MSG {name} {message[len(name)+2+5:]}'.encode('utf-8'))
        elif(message[len(name)+2:].startswith('/exit ')):
            print("Exiting server")
            client.close()
            break
        else:
            client.send(message.encode('utf-8'))

# Creating and starting receive and write threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
