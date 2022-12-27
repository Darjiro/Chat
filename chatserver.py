# import customtkinter as ctk
import socket
import threading

addr = socket.gethostname()
port = 9999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((addr, port))
server.listen()

#Main root
# SCREEN_SIZE = (400,400)
# root_win = ctk.CTk()
# main_frame = ctk.CTkFrame(root_win, width=SCREEN_SIZE[0], height=SCREEN_SIZE[1])
# main_frame.pack()

#Display all info here
# text_area_log = ctk.CTkTextbox(main_frame, width=380,height=380, state='disable')
# text_area_log.place(x=SCREEN_SIZE[0]//2,y=SCREEN_SIZE[1]//2, anchor=ctk.CENTER)

clients = []
usernames = []


# def log_message(msg, text_box, end_line:bool):
#     text_box.configure(state='normal')
#     if end_line:
#         text_box.insert(ctk.END, msg)
#     else:
#         text_box.insert(ctk.END, msg+'\n')
#     text_box.configure(state='disable')

def reply_messages(message, _client):

    for client in clients:
        if client != _client:
            client.send(message.encode('utf-8'))
            
def recv_msg(client, username):
        
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            reply_messages(msg, client)
#             log_message(msg, text_area_log, True)
            print(msg)

        except:                
            print(f'User {username} disconected')
#             log_message(f'User {username} disconected', text_area_log, False)
            usernames.remove(username)
            clients.remove(client)
            break

def run():
    print(f'Server running on {addr}')
#     log_message('Server runnig', text_area_log, False)
    while True:
        client, addr = server.accept()
        clients.append(client)
        username = client.recv(1024).decode('utf-8')
        usernames.append(username)
        
        client.send(str(len(clients)).encode('utf-8'))
        
        print(f'User {username} connected')
#         log_message(f'User {username} connected', text_area_log, False)
        threading.Thread(target=recv_msg, args=(client,username)).start()

# run()
threading.Thread(target=run).start()
# root_win.mainloop()
