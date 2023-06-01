import math
import socket
import threading
from tkinter import *
import time
import random
import sqlite3
from functools import *
import requests
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
    if len(message) < 1:
        return
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
        file.write(str(row) + "\n")
    file.close()
    cursor.close()
    conn.close()



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

        frame3 = Frame(root, width=300, height=100)

        label3 = Label(frame3, text="Prosti brojevi")
        label3.pack()

        var4 = DoubleVar()
        var5 = StringVar()
        var6 = StringVar()
        var7 = StringVar()
        var8 = StringVar()
        label4 = Label(frame3, width=110, textvariable=var5, bg="green", foreground="white")
        label4.pack()
        label5 = Label(frame3, width=110, height=5, textvariable=var6, bg="red", foreground="white")
        label5.pack()
        label6 = Label(frame3, width=110, textvariable=var7, bg="blue", foreground="white")
        label6.pack()
        frame3.pack(anchor=CENTER)
        frame4 = Frame(root, width=300, height=300)
        label7 = Label(frame4, textvariable=var8, bg="blue", foreground="white")
        label7.pack()

        def apiPoziv():
            url = "https://www.boredapi.com/api/activity"
            response = requests.get(url)
            data = response.json()
            var8.set(data['activity'])
        btn4 = Button(frame4, text="api poziv", command=lambda :threading.Thread(target=apiPoziv).start())
        btn4.pack()
        frame4.pack()
        def rezultaltUdvaReda(res):
            novi = ""
            for i ,elem in enumerate(res):
                novi += elem
                if i % 140-1 == 0:
                    novi += "\n"
            return novi

        def prostiBrojevi():
            selection = int(var4.get())
            if selection < 1:
                return
            nums = range(2, selection)
            for i in range(2, selection):
                nums = list(filter(lambda x: x == i or x % i, nums))
            var5.set(str(nums))
            nums2 = list(range(0, selection))
            nums2 = list(map(lambda x: x ** 2, nums2))
            temp = "Prosti brojevi na kvadrat-->" + str(nums2)


            if len(temp)> 150:
                temp = rezultaltUdvaReda(temp)
            var6.set(temp)

            nums3 = reduce(lambda x, y: x + y, list(range(1, selection)))
            var7.set("Suma prostih brojeva" + str(nums3))

        Scala2 = Scale(frame3, from_=0, to=100, variable=var4, orient=HORIZONTAL)
        Scala2.pack(padx=5, pady=5)

        btn4 = Button(frame3, text="prosti brojevi generator", command=lambda: prostiBrojevi())
        btn4.pack()

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
                deltaY = math.sin(random.randint(-360, 360))
            if canvas.coords(arc)[0] <= 0:
                deltaX = 1
                deltaY = math.sin(random.randint(-360, 360))
            if canvas.coords(arc)[3] >= 500:
                deltaY = -1
                deltaX = math.cos(random.randint(-360, 360))
            if canvas.coords(arc)[1] <= 0:
                deltaY = 1
                deltaX = math.cos(random.randint(-360, 360))


root = Tk()
en = StringVar()
prozor = Prozor(root, response, message)
server_thread = threading.Thread(target=start_server)
server_thread.setDaemon(True)
server_thread.start()
lopticaNit = threading.Thread(target=prozor.loptica)
lopticaNit.setDaemon(True)
lopticaNit.start()

root.geometry("900x1000")

root.mainloop()
