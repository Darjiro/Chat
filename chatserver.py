import customtkinter as ctk
import socket
import threading

SCREEN_SIZE = (400,400)


#Windows
#------------------------------------------------------------------------------------------------
# Main win
def log_win(window,ip):
    address = ip
    port = 9999
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((address, port))
    server.listen()
    clients = []
    usernames = []

    root_win = ctk.CTk()
    main_frame = ctk.CTkFrame(root_win, width=SCREEN_SIZE[0], height=SCREEN_SIZE[1])
    main_frame.pack()

    # Display all info here
    text_area_log = ctk.CTkTextbox(main_frame, width=380,height=380, state='disable')
    text_area_log.place(x=SCREEN_SIZE[0]//2,y=SCREEN_SIZE[1]//2, anchor=ctk.CENTER)
    
    # run()
    threading.Thread(target=run, args=(clients, usernames, server, text_area_log)).start()
    log_message(f'Server running at {ip}', text_area_log,False)
    
    window.destroy()
    root_win.mainloop()

def home():

    root_win = ctk.CTk()
    main_frame = ctk.CTkFrame(root_win, width=SCREEN_SIZE[0], height=SCREEN_SIZE[1])
    main_frame.pack()

    label_ip = ctk.CTkLabel(main_frame, text='Server', font=ctk.CTkFont('sans-serif', 28))
    label_ip.place(x=SCREEN_SIZE[0]//2, y=50, anchor=ctk.CENTER)
    
    entry_ip = ctk.CTkEntry(main_frame, placeholder_text='Ip:127.0.0.1')
    entry_ip.place(x=SCREEN_SIZE[0]//2, y=SCREEN_SIZE[1]//2, anchor=ctk.CENTER)
    
    label_error = ctk.CTkLabel(main_frame, text='', text_color='red', font=ctk.CTkFont('sans-serif', 14))
    label_error.place(x=SCREEN_SIZE[0]//2, y=SCREEN_SIZE[1]//2 + 130, anchor=ctk.CENTER)
    
    btn_start = ctk.CTkButton(main_frame, text='Start Server', width=45, command=lambda:btn_start_server(entry_ip, label_error, root_win))
    btn_start.place(x=SCREEN_SIZE[0]//2, y=SCREEN_SIZE[1]//2 + 50, anchor=ctk.CENTER)

    
    root_win.mainloop()
    
def btn_start_server(entry_ip, label_error, window):
    ip_default = socket.gethostname()
    ip_str = entry_ip.get()
    ip_int = ''
    
    char_point = 0
    
    for char in ip_str:
        if char=='.':
            char_point+=1
        else:
            ip_int += char
  
    #Valid ip
    if ip_str == '':
        
        log_win(window, ip_default)
    
    #If have any text
    else:
        
        #verificando la longitud correcta
        if len(ip_str) >= 7 and len(ip_str) <= 15 and char_point == 3:
            #Verificando q sean numeros
            try:
                ip_int = int(ip_int)
                log_win(window, ip_str)
            except:
                label_error.configure(text='Ip no valid')
        
        else:
            label_error.configure(text='Ip no valid')
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