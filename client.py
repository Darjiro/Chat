import customtkinter as ctk
import socket
import threading

ctk.set_appearance_mode('dark')

SCREEN_SIZE = (400,400)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = socket.gethostname()

def send_message(username, entry, text_area):
    message = entry.get()
    message_formated = f'{username}: {message}\n'
    
    entry.delete(0, 'end')
    
    text_area.configure(state='normal')
    text_area.insert(ctk.END, message_formated)
    text_area.configure(state='disable')
    client.send(message_formated.encode('utf-8'))

def recive_mesages(text_area):
    while True:
        message = client.recv(1024).decode('utf-8')
        text_area.configure(state='normal')
        text_area.insert(ctk.END, f'{message}')
        text_area.configure(state='disable')

def connect(username, ip, port, label_error, win):
    try:
        client.connect((ip, port))
        client.send(username.encode('utf-8'))
        
        chat_screen(username, label_error, win)
    except:
        label_error.configure(text=f'Cant connect to {ip}:{port}') 
    
def chat_screen(username, win):
    
    _font = ctk.CTkFont('sans-serif', 20)

    root = ctk.CTk()
    root.resizable(False, False)
    root.geometry(f'{SCREEN_SIZE[0]}x{SCREEN_SIZE[1]}')

    frame_top = ctk.CTkFrame(root, width=SCREEN_SIZE[0], height=40,bg_color='gray', fg_color='gray', corner_radius=10)
    frame_center = ctk.CTkFrame(root, width=SCREEN_SIZE[0], height=SCREEN_SIZE[1]-70)
    frame_bottom = ctk.CTkFrame(root, width=SCREEN_SIZE[0], height=30,bg_color='gray', fg_color='gray')
    
    frame_top.place(x=0, y=0)
    frame_center.place(x=0, y=40)
    frame_bottom.place(x=0, y=SCREEN_SIZE[1]-30)
    
    #Top
    label_username = ctk.CTkLabel(frame_top, text=f'{username}', text_color='white', font=_font)
    label_ip = ctk.CTkLabel(frame_top, text=f'', text_color='white', font=_font)
    # label_users = ctk.CTkLabel(frame_top, text=f'Users: {users_amount}', text_color='white', font=ctk.CTkFont('sans-serif', 15))
    
    label_username.place(x=SCREEN_SIZE[0]//2 - 150 , y=20, anchor=ctk.CENTER)
    label_ip.place(x=SCREEN_SIZE[0]//2 + 30 , y=20, anchor=ctk.CENTER)
    # label_users.place(x=SCREEN_SIZE[0]//2 + 140 , y=20, anchor=ctk.CENTER)
    
    #Center
    text_area = ctk.CTkTextbox(frame_center,width=SCREEN_SIZE[0], height=SCREEN_SIZE[1]-70, state='disable')
    text_area.place(x=0)

    #Bottom
    entry_message = ctk.CTkEntry(frame_bottom,placeholder_text='Type here', height=30, width=SCREEN_SIZE[0]-100, border_width=1)
    btn_send = ctk.CTkButton(frame_bottom,text='Send', height=30, width=99, border_width=1, command=lambda:send_message(username, entry_message, text_area))
    
    entry_message.grid(row=0, column=0)
    btn_send.grid(row=0,column=1)
    
    try:
        thread = threading.Thread(target=recive_mesages, args=(text_area,))
        thread.daemon = True
        thread.start()
        
    except Exception as e:
        print(e)   
                
    win.destroy()
    root.mainloop()

def main_screen():
    root = ctk.CTk()
    frame = ctk.CTkFrame(root, width=SCREEN_SIZE[0], height=SCREEN_SIZE[1])
    frame.pack()

    # image_logo = ctk.CTkImage()
    entry_username = ctk.CTkEntry(frame, placeholder_text='Username')
    entry_ip = ctk.CTkEntry(frame, placeholder_text='Ip:127.0.0.1')
    entry_port = ctk.CTkEntry(frame, placeholder_text='Port:9999')
    btn_login = ctk.CTkButton(frame, text='Login', width=70, command=lambda:login(
        entry_username,
        entry_ip,
        entry_port,
        label_error,
        root
    ))
    label_error = ctk.CTkLabel(frame, text='', text_color='red')
    
    entry_username.place(x=SCREEN_SIZE[0]//2, y=SCREEN_SIZE[1]//2 -30, anchor=ctk.CENTER)
    entry_ip.place(x=SCREEN_SIZE[0]//2, y=SCREEN_SIZE[1]//2 + 20, anchor=ctk.CENTER)
    entry_port.place(x=SCREEN_SIZE[0]//2, y=SCREEN_SIZE[1]//2 + 50, anchor=ctk.CENTER)
    btn_login.place(x=SCREEN_SIZE[0]//2, y=SCREEN_SIZE[1]//2 + 140, anchor=ctk.CENTER)
    label_error.place(x=SCREEN_SIZE[0]//2, y=SCREEN_SIZE[1]//2 + 100, anchor=ctk.CENTER)
    
    root.mainloop()
    
def login(entry_username, entry_ip, entry_port, label_error, win):

    username = entry_username.get()

    #ip
    ip_str = entry_ip.get()
    ip_int = ''
    ip_char_point = 0
    
    #port
    port_str = entry_port.get()
    port_int = None
    
    for char in ip_str:
        if char=='.':
            ip_char_point+=1
        else:
            ip_int += char
    
    if username:
        #Valid ip
        if ip_str == '':
            ip_str = '127.0.0.1'
            
            if len(port_str) == 4:
                try:
                    port_int = int(port_str)
                    
                    #If all is ok connect to server
                    connect(username, ip_str, port_int, label_error, win)           
                except:
                    label_error.configure(text='Port no valid')
            
            elif port_str == '':
                port_int = 9999
                connect(username, ip_str, port_int, label_error, win)
            
            else:
                label_error.configure(text='Port no valid') 
            
        #If ip have any text
        else: 
            #verificando la longitud correcta
            if len(ip_str) >= 7 and len(ip_str) <= 15 and ip_char_point == 3:
                #Verificando q sean numeros
                try:
                    ip_int = int(ip_int)             
                    
                    #Comprobando el puerto
                    if len(port_str) == 4:
                        try:
                            port_int = int(port_str)
                            
                            #If all is ok connect to server
                            connect(username, ip_str, port_int, label_error, win)
                        except:
                            label_error.configure(text='Port no valid')
                    elif port_str == '':
                        #If all is ok connect to server
                        port_int = 9999
                        connect(username, ip_str, port_int, label_error, win)
                    else:
                        label_error.configure(text='Port no valid') 
                except:
                    label_error.configure(text='Ip no valid')
            else:
                label_error.configure(text='Ip no valid')
    else:
        label_error.configure(text='Username required!')
    
if __name__=='__main__':
    main_screen()