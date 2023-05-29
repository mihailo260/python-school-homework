import math
import socket
import threading
from tkinter import *
import time
import random
import sqlite3
import json

message = ""
response = ""

conn, cursor = "", ""

def start_server():
    global message, response, ID
    server_host = "localhost"
    server_port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen()

    while True:
        client_socket, client_address = server_socket.accept()
        data = client_socket.recv(1024).decode("utf-8")
        date = time.ctime(time.time())
        response = f"Poruka od klijenta {data} u {date}"
        client_socket.send(response.encode("utf-8"))
        client_socket.close()


def start_client():
    global message, response
    server_host = "localhost"
    server_port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    client_socket.send(message.encode("utf-8"))

    response = client_socket.recv(1024).decode("utf-8")
    print(f"od  servera poruka: {response}")
    client_socket.close()


def posalji_serveru():
    global conn, cursor
    global message
    message = en.get()
    start_client()
    conn = sqlite3.connect('domaci.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS COMPANY
                        (
                        NAME TEXT NOT NULL);'''
                   )
    print(message)
    conn.execute("INSERT INTO COMPANY (NAME) VALUES (?)", (message,))
    conn.commit()

def ucitaj_od_servera(listBox2, listBox):
    listBox2.insert(1, message)
    listBox.insert(1, response)


def kreirajSql_upit():
    global cursor, conn
    cursor.execute("SELECT * FROM COMPANY")
    rows = cursor.fetchall()
    file_path = "test.txt"
    file = open(file_path, "a")
    for row in rows:
        file.write(str(row)+"\n")
    file.close()
    cursor.close()
    conn.close()
def Json():
    data = {
        "name": "John",
        "age": 30,
        "city": "New York"
    }

    json_data = json.dumps(data)
    print(json_data)
    json_data = '{"name": "John", "age": 30, "city": "New York"}'
    data = json.loads(json_data)
    print(data["name"])
    print(data["age"])
    print(data["city"])


class Prozor():
    def __init__(self, root, response, message):
        self.root = root
        self.response = response
        self.message = message
        frame = Frame(root)
        frame.pack()
        label = Label(frame, text="Klijent:-->")
        label.pack(side=LEFT)
        listBox = Listbox(frame, width=50)
        listBox.insert(1, response)
        listBox.pack(side=LEFT)

        label2 = Label(frame, text="Server:-->")
        label2.pack(side=LEFT)
        listBox2 = Listbox(frame, width=50)
        listBox2.insert(1, message)
        listBox2.pack(side=LEFT)

        frame2 = Frame(root, width=900)

        frame2.pack()
        global en
        entry1 = Entry(frame2, textvariable=en)
        entry1.pack(side=LEFT)

        btn1 = Button(frame2, text="Posalji poruku serveru",
                      command=lambda: posalji_serveru())
        btn1.pack(side=LEFT)

        btn2 = Button(frame2, text="Procitaj poruku sa servera", command=lambda: ucitaj_od_servera(listBox2, listBox))
        btn2.pack(side=RIGHT)

        btn3 = Button(frame2, text="KreirajSqlIDatoteku", command=kreirajSql_upit)
        btn3.pack(side=RIGHT)

    def loptica(self):
        canvas = Canvas(root, width=500, height=500, bg="green")
        canvas.pack()
        deltaX = 1
        deltaY = 0
        centarKrugaX = 200
        centarKrugaY = 200
        poluprecnikKruga = 30

        kordinataX1 = centarKrugaX - poluprecnikKruga
        kordinataY1 = centarKrugaY - poluprecnikKruga
        kordinataX2 = centarKrugaX + poluprecnikKruga
        kordinataY2 = centarKrugaY + poluprecnikKruga

        arc = canvas.create_arc(kordinataX1, kordinataY1, kordinataX2, kordinataY2, start=0, extent=359,
                                fill="red")
        while True:
            time.sleep(1 / (10 * 100))
            canvas.move(arc, deltaX, deltaY)
            if canvas.coords(arc)[2] >= 500:
                deltaX = -1
                deltaY = math.sin(round(random.randint(-360, 360), 1))
            if canvas.coords(arc)[0] <= 0:
                deltaX = 1
                deltaY = math.sin(round(random.randint(-360, 360), 1))
            if canvas.coords(arc)[3] >= 500:
                deltaY = -1
                deltaX = math.cos(round(random.randint(-360, 360), 1))
            if canvas.coords(arc)[1] <= 0:
                deltaY = 1
                deltaX = math.cos(round(random.randint(-360, 360), 1))


root = Tk()

en = StringVar()
prozor = Prozor(root, response, message)
server_thread = threading.Thread(target=start_server)
server_thread.setDaemon(True)
server_thread.start()
lopticaNit= threading.Thread(target=prozor.loptica)
lopticaNit.setDaemon(True)
lopticaNit.start()

root.geometry("900x1000")

root.mainloop()
numbers = [1, 2, 3, 4, 5]

squared = map(lambda x: x**2, numbers)
print(list(squared))

numbers = [1, 2, 3, 4, 5]

even = filter(lambda x: x & 1 == 0, numbers)
print(list(even))


from functools import reduce

numbers = [1, 2, 3, 4, 5]

product = reduce(lambda x, y: x * y, numbers)
print(product)
Json()