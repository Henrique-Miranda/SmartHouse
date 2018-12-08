import usocket, ujson
from machine import Pin

#Config of I/O Pins
'''
D1mini
bomba = Pin(5, Pin.OUT)
quintal = Pin(4, Pin.OUT)
scozinha = Pin(12, Pin.OUT)
quarto = Pin(14, Pin.OUT)
'''
#ESP03
bomba = Pin(16, Pin.OUT)
quintal = Pin(3, Pin.OUT)
scozinha = Pin(5, Pin.OUT)
quarto = Pin(4, Pin.OUT)

#Write in Json last states of Pins
def writelastcfg():
    
    lastcfg = {'BOMBA': bomba.value(), 'QUINTAL': quintal.value(), 'SCOZINHA': scozinha.value(), 'QUARTO': quarto.value()}
    with open('lastcfg.json', 'w') as f:
        ujson.dump(lastcfg, f)

#Retrive last Pin states saved in Json
def getlastcfg():
    
    try:
        with open('lastcfg.json', 'r') as f:
            lastcfg = ujson.load(f)
        bomba.value(lastcfg['BOMBA'])
        quintal.value(lastcfg['QUINTAL'])
        scozinha.value(lastcfg['SCOZINHA'])
        quarto.value(lastcfg['QUARTO'])
    except:
        bomba.value(0)
        quintal.value(0)
        scozinha.value(0)
        quarto.value(0)
        

def ok(socket, query):
    socket.write("HTTP/1.1 OK\r\n\r\n")
    socket.write("<!DOCTYPE html>")
    socket.write('<head><meta charset="utf-8"><link href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">')
    socket.write('<meta name="viewport" content="width=device-width, initial-scale=1" />')
    socket.write("<title>Smart House</title></head>")
    socket.write('<html lang="pt-br" dir="ltr"><body>')
    socket.write('<div class="jumbotron" align="center"><h2>Smart House</h2><h5>By Henrique Miranda</h5>')
    socket.write('<ul class="list-group">')

    if bomba.value():
        socket.write('<li class="list-group-item"><span>Bomba</span>&nbsp<span style="color:green">Ligada</span>&nbsp<form method="POST" action="/bombaoff?"'+query.decode()+'"><button type="submit" class="btn btn-danger">Desligar</button></form></li>')
    else:
        socket.write('<li class="list-group-item"><span>Bomba</span>&nbsp<span style="color:red">Desligada</span>&nbsp<form method="POST" action="/bombaon?"'+query.decode()+'"><button type="submit" class="btn btn-primary">Ligar</button></form></li>')

    if quintal.value():
        socket.write('<li class="list-group-item"><span>Quintal</span>&nbsp<span style="color:green">Ligada</span>&nbsp<form method="POST" action="/quintaloff?"'+query.decode()+'"><button type="submit" class="btn btn-danger">Desligar</button></form></li>')
    else:
        socket.write('<li class="list-group-item"><span>Quintal</span>&nbsp<span style="color:red">Desligada</span>&nbsp<form method="POST" action="/quintalon?"'+query.decode()+'"><button type="submit" class="btn btn-primary">Ligar</button></form></li>')

    if scozinha.value():
        socket.write('<li class="list-group-item"><span>Sala/Cozinha</span>&nbsp<span style="color:green">Ligada</span>&nbsp<form method="POST" action="/scozinhaoff?"'+query.decode()+'"><button type="submit" class="btn btn-danger">Desligar</button></form></li>')
    else:
        socket.write('<li class="list-group-item"><span>Sala/Cozinha</span>&nbsp<span style="color:red">Desligada</span>&nbsp<form method="POST" action="/scozinhaon?"'+query.decode()+'"><button type="submit" class="btn btn-primary">Ligar</button></form></li>')

    if quarto.value():
        socket.write('<li class="list-group-item"><span>Quarto</span>&nbsp<span style="color:green">Ligada</span>&nbsp<form method="POST" action="/quartooff?"'+query.decode()+'"><button type="submit" class="btn btn-danger">Desligar</button></form></li>')
    else:
        socket.write('<li class="list-group-item"><span>Quarto</span>&nbsp<span style="color:red">Desligada</span>&nbsp<form method="POST" action="/quartoon?"'+query.decode()+'"><button type="submit" class="btn btn-primary">Ligar</button></form></li></ul></div></body></html>')

def err(socket, code, message):
    socket.write("HTTP/1.1 "+code+" "+message+"\r\n\r\n")
    socket.write("<h1>"+message+"</h1>")

def handle(socket):
    (method, url, version) = socket.readline().split(b" ")
    if b"?" in url:
        (path, query) = url.split(b"?", 2)
    else:
        (path, query) = (url, b"")
    while True:
        header = socket.readline()
        if header == b"":
            return
        if header == b"\r\n":
            break

    if version != b"HTTP/1.0\r\n" and version != b"HTTP/1.1\r\n":
        err(socket, "505", "Version Not Supported")
    elif method == b"GET":
        if path == b"/":
            ok(socket, query)
        else:
            err(socket, "404", "Not Found")
    elif method == b"POST":
        if path == b"/bombaon":
            bomba.value(1)
            ok(socket, query)
        elif path == b"/bombaoff":
            bomba.value(0)
            ok(socket, query)
        elif path == b"/quintalon":
            quintal.value(1)
            ok(socket, query)
        elif path == b"/quintaloff":
            quintal.value(0)
            ok(socket, query)
        elif path == b"/scozinhaon":
            scozinha.value(1)
            ok(socket, query)
        elif path == b"/scozinhaoff":
            scozinha.value(0)
            ok(socket, query)
        elif path == b"/quartoon":
            quarto.value(1)
            ok(socket, query)
        elif path == b"/quartooff":
            quarto.value(0)
            ok(socket, query)
        else:
            err(socket, "404", "Not Found")

        writelastcfg()

    else:
        err(socket, "501", "Not Implemented")
        
#When the board turn on get last Pin states from json file
getlastcfg()
server = usocket.socket()
server.bind(('', 80))
server.listen(1)

while True:
    try:
        (socket, sockaddr) = server.accept()
        handle(socket)
    except:
        socket.write("HTTP/1.1 500 Internal Server Error\r\n\r\n")
        socket.write("<h1>Internal Server Error</h1>")
    socket.close()
