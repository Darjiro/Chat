import socket, threading

addr = 'localhost'
port = 9999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((addr, port))
server.listen()

clients = []
usernames = []

def reply_messages(message, _client):

    for client in clients:
        if client != _client:
            client.send(message.encode('utf-8'))
            
def recv_msg(client, username):
        
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            reply_messages(msg, client)
            print(msg)

        except:                
            print(f'User {username} disconected')
            usernames.remove(username)
            clients.remove(client)
            break

def run():
    print('Server running')
    while True:
        client, addr = server.accept()
        clients.append(client)
        username = client.recv(1024).decode('utf-8')
        usernames.append(username)
        
        client.send(str(len(clients)).encode('utf-8'))
        
        print(f'User {username} connected')
        threading.Thread(target=recv_msg, args=(client,username)).start()
        
run()