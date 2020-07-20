from pyrogram import Client,Filters
from text import *
from random import *

##init##

BOT_TOKEN="1257512221:AAEN1R8ngditDaaseZwumjDmfzTlaI77Rd0"
app = Client(
    "bot",
    bot_token=BOT_TOKEN
)
##COMMANDS##
def send(msg_get,msg_send):
    app.send_message(
        chat_id=msg_get.chat.id,
        text=msg_send,
        reply_to_message_id=msg_get.message_id
        )

@app.on_message(Filters.command("hi"))
def hi(client,message):
    send(message,'hello')

@app.on_message(Filters.command("start"))
def start(client,message):
    send(message,abouth)

@app.on_message(Filters.command("help"))
def help(client,message):
    send(message,'help me not working')

@app.on_message(Filters.command("bye"))
def bye(client,message):
    send(message,"bye i am going to sleep")

@app.on_message(Filters.command("rules"))
def rules(client,message):
    send(message,rule)

@app.on_message(Filters.command(["test","num"]))
def test(client,message):
    send(message,smessage.command)

@app.on_message(Filters.command('todo'))
def todo(client,message):
    f=open('todo.txt',"r")
    a=f.read()
    f.close()
    send(message,a)

@app.on_message(Filters.command(['stupid','id']))
def stupid(client,message):
    i=choice(stupi)
    send(message,f"{message.command[1]} {i} stupid")

app.run()

