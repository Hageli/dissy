import threading
import socket

# localhost
host = '127.0.0.1'
port = 4000

# Variables
channel_1 = []
channel_2 = []
c1_usernames = []
c2_usernames = []

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Broadcast functions
def broadcast_channel_1(message):
    for client in channel_1:
        client.send(message)

def broadcast_channel_2(message):
    for client in channel_2:
        client.send(message)

# Client handling
def handle_client(client, channel):
    while True:
        # Try to receive a message from the client
        try:
            temp = message = client.recv(1024)
            if(temp.decode('utf-8').startswith('MSG')):
                send_msg(temp.decode('utf-8')[4:].split(' ')[1], message)
            else:
                if(channel == '1'):
                    broadcast_channel_1(message)
                elif(channel == '2'):
                    broadcast_channel_2(message)
        # If client connection is lost, remove the client from the list 
        except:
            if(channel == '1'):
                index = channel_1.index(client)
                channel_1.remove(client)
                client.close()
                username = c1_usernames[index]
                broadcast_channel_1(f'{username} left the chat'.encode('utf-8'))
                c1_usernames.remove(username)
            elif(channel == '2'):
                index = channel_2.index(client)
                channel_2.remove(client)
                client.close()
                username = c2_usernames[index]
                broadcast_channel_2(f'{username} left the chat'.encode('utf-8'))
                c2_usernames.remove(username)
            break

# Server loop
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        client.send('USR'.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        # Check if the username already exists
        if(username in c1_usernames or username in c2_usernames):
            client.send('Username already exists'.encode('utf-8'))
            client.close()
            continue
        client.send('CHN'.encode('utf-8'))
        channel = client.recv(1024).decode('utf-8')
        if(channel == '1'):
            c1_usernames.append(username)
            channel_1.append(client)
            broadcast_channel_1(f'{username} joined the chat'.encode('utf-8'))
            client.send('Connected to channel 1'.encode('utf-8'))
        elif(channel == '2'):
            c2_usernames.append(username)
            channel_2.append(client)
            broadcast_channel_2(f'{username} joined the chat'.encode('utf-8'))
            client.send('Connected to channel 2'.encode('utf-8'))
        else:
            # If the channel is invalid, close the client
            client.send('Invalid channel'.encode('utf-8'))
            client.close()
            continue
        thread = threading.Thread(target=handle_client, args=(client, channel))
        thread.start()

# Send private message
def send_msg(rcv_user, message):
    final_message = message.decode('utf-8').split(' ', 3)
    if(rcv_user in c1_usernames):
        # Get the index of the user in the list and send the message
        index = c1_usernames.index(rcv_user)
        channel_1[index].send(f'PRIVATE {final_message[1]}: {final_message[3]}'.encode('utf-8'))
    elif(rcv_user in c2_usernames):
        # Get the index of the user in the list and send the message
        index = c2_usernames.index(rcv_user)
        channel_2[index].send(f'PRIVATE {final_message[1]}: {final_message[3]}'.encode('utf-8'))
    # If the user is not found, send a message to the server
    else:
        print('User not found')

# Start the server
print("Server active")
receive()
