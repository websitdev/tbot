from pyrogram import Client,Filters,ChatPermissions,ChatMember
from text import *
from random import* 
import time
import os

##init##
#import my_apis as api

try:
    import my_apis as api
    API_TOKEN=api.TOKEN

except ImportError:
    API_TOKEN=os.environ.get('API_TOKEN')

##=====Variables ===========
global ADMIN=["owner","administrator")


app = Client(
    "bot",
    bot_token=API_TOKEN
)
##COMMANDS##
class AdminCheck:
    def __init__(self,message):
        self.chatId   = message.chat.id
        self.userId   = message.from_user.id
        self.user     = app.get_chat_member(chatId,userId)
        self.userType = user.status

    def isAdmin():
        if userType == "member":
            return 0

        else:
            if UserType == "administrator":
                return 1
            return 2

     
              
def send(message,reply):
    app.send_message(
        chat_id=message.chat.id,
        text=reply,
        reply_to_message_id=message.message_id
    )

def usage(message):
    try:
        user   = message.reply_to_message
        userId = message.reply_to_message.from_user.id
    except:
        user   = message
        try:
            userId = message.command[1]:
        except:
            send(message,f"Invalid usage.\n/{message.command[0]} username or tag message and use /kick")
            exit(1)
    return(user,userId)

              

@app.on_message(Filters.command("hi"))
def hi(client,message):
    send(message,'hello')

@app.on_message(Filters.command("start"))
def start(client,message):
    send(message,abouth)

@app.on_message(Filters.command("help"))
def help(client,message):
    send(message,help_)

@app.on_message(Filters.command("bye"))
def bye(client,message):
    send(message,"bye i am going to sleep")

@app.on_message(Filters.command("rules"))
def rules(client,message):
    send(message,rule)

@app.on_message(Filters.command(["test","num"]))
def test(client,message):
    send(message,message.command)

@app.on_message(Filters.command('todo'))
def todo(client,message):
    f=open('todo.txt',"r")
    a=f.read()
    f.close()
    send(message,a)

@app.on_message(Filters.command(['stupid','id']))
def stupid(client,message):
    i=choice(stupi)
    if message.command[1] is '@Arydev' or 'Arydev':
        i='is not'
    send(message,f"{message.command[1]} {i} stupid")

@app.on_message(Filters.command(['kick','id']))
def kick(client,message): 
    admin = AdminCheck(message)

    if admin.isAdmin() == 0:
        send(message,"You need to be an admin to execute this command")
    elif admin.isadmin() == 1  and not admin.user.can_restrict_members:
        send(message,"Sorry, you dont have enough permission to execute this command")
    else:
        user,userId = usage(message)
        status = app.kick_chat_member(
            chat_id=user.chat.id,
            user_id=userId, 
            int(time.time()+60)
        )

        if type(status) != bool:
            send(message,f"Kicked {message.command[1]}")
        else:
            send(message,"Some error occured")



@app.on_message(Filters.command('kill'))
def delete(client,message):
    admin    = AdminCheck(message)   

    if admin.isAdmin() == 0:
        send(message,"You need to be an admin to execute this command")
    elif admin == 1  and not admin.user.can_delete_messages:
        send(message,"Sorry, you dont have enough permission to execute this command")
    else:
        message.reply_to_message.delete()

@app.on_message(Filters.command(["whois",'id']))
def whois(client,message):
    send(message,app.get_users(message.command[1]))

@app.on_message(Filters.command('members'))
def memb(client,message):
    send(message,app.get_chat_members_count(message.chat.id))

@app.on_message(Filters.command('unpin'))
def mes_count(client,message):
    app.unpin_chat_message(message.chat.id)

@app.on_message(Filters.command(['pardon','id']))
def pardon(client,message):

    app.unban_chat_member(message.chat.id,message.command[1])
    send(message,f"{message.command[1]} is unbaned")
    app.send_message(message.command[1],bu)

@app.on_message(Filters.command(['mute24','id']))
def mute24(client,message):
    app.restrict_chat_member(message.chat.id, message.command[1], ChatPermissions(), int(time.time() + 86400))
    send(message,f"{message.command[1]} is muted for 24 hours")
    app.send_message(message.command[1],bu)


app.run()
