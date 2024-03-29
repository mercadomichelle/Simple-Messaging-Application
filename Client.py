import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.160.10.1'
PORT = 9876

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

#GUI 

DARK_GREY = '#121212'
CORAL = '#CD5B45'
WHITE = "white"
BLACK = "black"
FONT = ("Helvetica", 15)
BUTTON_FONT = ("Helvetica", 11)
SMALL_FONT = ("Helvetica", 13)

root = tk.Tk()
root.geometry("400x550")
root.title("Messenging App")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=500, height=100, bg=BLACK)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=DARK_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=BLACK)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=BLACK, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=2)

username_textbox = tk.Entry(top_frame, font=FONT, bg=DARK_GREY, fg=WHITE, width=17)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="JOIN", font=BUTTON_FONT, bg=CORAL, fg=BLACK, command=connect)
username_button.pack(side=tk.LEFT, padx=5)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=DARK_GREY, fg=WHITE, width=30)
message_textbox.pack(side=tk.LEFT, padx=5)

message_button = tk.Button(bottom_frame, text="SEND", font=BUTTON_FONT, bg=CORAL, fg=BLACK, command=send_message)
message_button.pack(side=tk.LEFT, padx=0)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=DARK_GREY, fg=WHITE, width=65, height=25.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

def listen_for_messages_from_server(client):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")
            
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")

def main():

    root.mainloop()
    
if __name__ == '__main__':
    main()