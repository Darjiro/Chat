import customtkinter as ctk
import socket
import threading

SCREEN_SIZE = (400,400)


#Windows
#------------------------------------------------------------------------------------------------
# Main win
def log_win(window, port):
    address = socket.gethostname()
    port = port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((address, port))
    server.listen()
    clients = []
    usernames = []

    root_win = ctk.CTk()
    root_win.title('Log history')
    main_frame = ctk.CTkFrame(root_win, width=SCREEN_SIZE[0], height=SCREEN_SIZE[1])
    main_frame.pack()

    # Display all info here
    text_area_log = ctk.CTkTextbox(main_frame, width=380,height=380, state='disable')
    text_area_log.place(x=SCREEN_SIZE[0]//2,y=SCREEN_SIZE[1]//2, anchor=ctk.CENTER)
    
    # run()
    threading.Thread(target=run, args=(clients, usernames, server, text_area_log)).start()
    log_message(f'Server running at {address}:{port}', text_area_log,False)
    
    window.destroy()
    root_win.mainloop()

def home():
    root_win = ctk.CTk()
    root_win.title('Server')
    
    main_frame = ctk.CTkFrame(root_win, width=SCREEN_SIZE[0], height=SCREEN_SIZE[1])
    main_frame.pack()

    label_server = ctk.CTkLabel(main_frame, text='Server', font=ctk.CTkFont('sans-serif', 28))
    label_server.place(x=SCREEN_SIZE[0]//2, y=50, anchor=ctk.CENTER)
    
    entry_port = ctk.CTkEntry(main_frame, placeholder_text='Port:9999')
    entry_port.place(x=SCREEN_SIZE[0]//2, y=SCREEN_SIZE[1]//2, anchor=ctk.CENTER)
    
    label_error = ctk.CTkLabel(main_frame, text='', text_color='red', font=ctk.CTkFont('sans-serif', 14))
    label_error.place(x=SCREEN_SIZE[0]//2, y=SCREEN_SIZE[1]//2 + 130, anchor=ctk.CENTER)
    
    btn_start = ctk.CTkButton(main_frame, text='Start Server', width=45, command=lambda:btn_start_server(entry_port, label_error, root_win))
    btn_start.place(x=SCREEN_SIZE[0]//2, y=SCREEN_SIZE[1]//2 + 50, anchor=ctk.CENTER)

    
    root_win.mainloop()
    
def btn_start_server(entry_port, label_error, window):
    port_default = socket.gethostname()
    port_str = entry_port.get()
    port_int = ''
    
    if len(port_str) == 4:
        try:
            port_int = int(port_str)
            log_win(window, port_int)
        except:
            label_error.configure(text='Port no valid')
    elif port_str == '':
        port_int = 9999
        log_win(window, port_int)
    else:
        label_error.configure(text='Port no valid')
#------------------------------------------------------------------------------------------------

#SERVER LOGIC
#------------------------------------------------------------------------------------------------
def log_message(msg, text_box, end_line:bool):
    text_box.configure(state='normal')
    if end_line:
        text_box.insert(ctk.END, msg)
    else:
        text_box.insert(ctk.END, msg+'\n')
    text_box.configure(state='disable')

#Func to reply mssages to all clients
def reply_messages(message, _client, clients):
    for client in clients:
        if client != _client:
            client.send(message.encode('utf-8'))

#Func for recept all messages           
def recv_msg(client, username, clients, usernames, text_area_log):
        
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            reply_messages(msg, client, clients)
            log_message(msg, text_area_log, True)
            print(msg)

        except:                
            print(f'User {username} disconected')
            log_message(f'User {username} disconected', text_area_log, False)
            usernames.remove(username)
            clients.remove(client)
            break

#Func to recive connections
def run(clients, usernames, server, text_area_log):
    
    while True:
        client, addr = server.accept()
        clients.append(client)
        username = client.recv(1024).decode('utf-8')
        usernames.append(username)
        
        client.send(str(len(clients)).encode('utf-8'))
        
        print(f'User {username} connected')
        log_message(f'User {username} connected', text_area_log, False)
        threading.Thread(target=recv_msg, args=(client,username, clients, usernames, text_area_log)).start()

#------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    home()