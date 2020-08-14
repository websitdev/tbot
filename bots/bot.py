#from packages import install
#install()
import telebot
#from remain_up import remain_up
from random import *
import time
import json
import os
import traceback
import subprocess
import secrets
from threading import Thread
from Admin import Admin_handler as Adm
from Variables import *

##======================  init  =====================##
try:
    import my_apis as api
    API_TOKEN = api.TOKEN

except ImportError:
    API_TOKEN = os.environ.get("BOT_API_TOKEN")
    API_TOKEN = "1273279578:AAF3S-tLX-IYkHWF4jnImvugQ5WPV6wlj8Q"

##====================  Variables  ====================##
if API_TOKEN is None or API_TOKEN == '':
    print("No token provided")
    exit(1)

msg = 0
to_delete = 0

app = telebot.TeleBot(API_TOKEN)

##===================  COMMANDS  ======================##
def get_user(message):
    try:
        user = message.reply_to_message
        user_id = message.reply_to_message.from_user.id
    except:
        user = message
        try:
            user_id = message.text.split()[1]
        except:
            return (user, None)

    return(user, user_id)


"""
def run_python3(message):
    run = message.text.replace('/python3', '')

    script = 'import sys\n'
    script += 'import traceback\n'
    script += "err = ''\n"
    script += 'try:\n'
    for line in run.splitlines():
        script += f'\t{line}\n'
    script += 'except:\n'
    script += '\ttraceback.print_exc(file=sys.stdout)\n'
    #script += '\tsys.stdout.write(err)'

    py_file = os.path.join(
      "scripts",
      secrets.token_hex(nbytes=16)
      )
    py_file_wrapper = open(
    py_file,
    "w"
    )

    py_file_wrapper.write(script)

    py_file_wrapper.close()

    try:
        result = os.popen(f"python3 {py_file}").read()
        if result is None or result == '':
            os.remove(py_file)
            return "No output"

        os.remove(py_file)
        return result

    except:
        err = traceback.format_exc()
        os.remove(py_file)
        if err is None or err == '':
            return "Error in executing script"
        return err

    os.remove(py_file)
"""

def is_alive(threads):
    return True in [thread.is_alive() for thread in threads]


def delete_message(chat_id, msg_id):
    global msg

    try:
        app.delete_message(chat_id, msg_id)
        msg += 1
    except:
        pass


def send(message, reply):
    app.reply_to(
        message,
        reply
    )


##================  Message Handlers  =======================##

@app.message_handler(commands=['hi', 'hello'])
def hi(message):
    send(message, 'hello')


@app.message_handler(commands=['kick_bot'])
def leave(message):
    app.leave_chat(message.chat.id)
    send(message, 'Hahaha, NO!')

@app.message_handler(commands=['about'])
def about(message):
    send(message, ABOUT)


@app.message_handler(commands=['help'])
def help(message):
    send(message, HELP)


@app.message_handler(commands=['bye'])
def bye(message):
    message = get_user(message)
    send(message[0], "bye i am going to sleep")

@app.message_handler(commands=['rules'])
def rules(message):
    send(message, RULES)


@app.message_handler(commands=['start'])
def start(message):
    send(message, "Start (does nothing for now)")


@app.message_handler(commands=['todo'])
def todo(message):
    send(message, TODO)


@app.message_handler(commands=['stupid'])
def stupid(message):
    message = get_user(message)
    if message[1] is None:
        send(message[0], f"You are {STUPID[randint(0,1)]}")
    else:
        send(message[0], f"{message.command[1]} is {STUPID[randint(0,1)]}")

@app.message_handler(commands=['die'])
def died(message):
    send(message, "You are ded 🔪")

@app.message_handler(commands=['kick'])
def kick(message):
    try:
        kick_usage = "Usage: /kick username \nor \nreply with /kick to the user's message"
        admin_obj  = Adm(app,message)
        admin, can_kick = admin_obj.is_admin()
        chat_id    = admin_obj.chat_id
        member, member_id = get_user(message)


        if admin_obj.bot_can_restrict_members():
            send(message, "I dont have enough priveleges :(")
            return

        if admin:
            send(message, "You need to be an admin to execute this command")
            return

        if admin and not can_kick:
            if not admin_obj.user.can_restrict_members:
                send(message, "You don't have sufficient permission")
                return
        

        if get_user(message) is None:
            send(message, kick_usage)
            return

        if member_id is app.get_me().id:
            send(message, '🧐')
            return

        if member_id in admin_obj.admin_list:
            send(message, 'I don\'t kick admins :V')
            return

        if app.get_chat_member(chat_id, member_id).status == "left":
            send(message, "Not a member (Feature will be added in future updates)")
            return

        
        #user, user_id = get_user(message)
        status = app.kick_chat_member(
            chat_id,
            member_id,
            (int(time.time()+60))
        )

        if status:
            send(message, f"Kicked {member_id}")
        else:
            send(message, "Some error occured")

    except ImportError:
        send(message, "Internal Error")        


@app.message_handler(commands=['delete'])
def delete(message):
    global msg, to_delete
    admin_obj = Adm(app,message)

    admin, can_edit = admin_obj.is_admin()
    user = app.get_chat_member(message.chat.id,  message.from_user.id)

    if admin_obj.bot_can_delete_messages():
        send(message, "Bot is not admin")
        return

    if admin:
        send(message, "You need to be an admin to execute this command")
        return
    
    if admin and not can_edit:
        if not user.can_delete_messages:
            send(message, "Sorry, you dont have enough permission to execute this command")
            return

    if get_user(message)[1] is None:
        send(message, DELETE_USAGE)
        return

##=======================  Threading Start  ===============================##

    user, user_id = get_user(message)
    to_delete = 1
    deleted = 0
    last_message = message.message_id
    threads = []
    thread_count = 0
    msg = 0

    if len(message.text.split()) > 1:
        to_delete = int(message.text.split()[1])

    else:
        app.delete_message(
            message.chat.id,
            message.reply_to_message.message_id
        )
        app.delete_message(
            message.chat.id,
            last_message
        )
        return

    if to_delete > 10:
        last_message -= 1
        while 1:
            if last_message == 0 or thread_count > 500:
                break

            d_thread = Thread(
                target=delete_message,
                args=[message.chat.id, last_message]
                )

            threads.append(d_thread)

            d_thread.start()
            thread_count += 1

            if thread_count % 50 == 0:
                while is_alive(threads):
                    if msg >= to_delete:
                        break
                    time.sleep(0.0001)

            if msg >= to_delete:
                break

            last_message -= 1
        return

    msg += 1

    while deleted != to_delete:

        try:
            app.delete_message(
                message.chat.id,
                last_message-msg
            )
            deleted += 1
        except:
            pass

        msg += 1
##=======================  Threading End  ==========================##

@app.message_handler(commands=['test'])
def test(message):
    send(message, "bot is alive")


#@app.message_handler(commands=['python3'])
#def python3(message):
#    print(message.text)
#    send(message, run_python3(message))


@app.message_handler(commands=['whois'])
def whois(message):
    user, user_id = get_user(message)

    if user_id is None:
        send(message, WHOIS_USAGE)
        return

    user, user_id = get_user(message)
    send(message, app.get_chat_member(message.chat.id, user_id))


@app.message_handler(commands=['members_count'])
def memb(message):
    send(message, app.get_chat_members_count(message.chat.id))

##--------------------------------  unpin  ----------------------------------##

@app.message_handler(commands=['unpin'])
def mes_count(message):
    admin_obj = Adm(app, message)
    admin, can_pin = admin_obj.is_admin()

    user = app.get_chat_member(message.chat.id,  message.from_user.id)


    if admin_obj.bot_can_pin_messages():
        send(message, "I don't have enough priveleges :(")
        return

    if not admin:
        send(message, "You need to be an admin to execute this command")
        return

    if admin and not can_pin:
        if not user.can_pin_messages:
            send(message, "Sorry, you dont have enough permission to execute this command")
            return
    

    app.unpin_chat_message(message.chat.id)

##---------------------- pardon ----------------------##
@app.message_handler(commands=['pardon'])
def pardon(message):
    admin_obj = Adm(app, message)
    admin, can_restrict_members = admin_obj.is_admin()
    user, user_id = get_user(message)


    user = app.get_chat_member(message.chat.id,  message.from_user.id)


    if admin_obj.bot_can_restrict_members:
        send(message, "Bot is not admin")
        return

    if not admin:
        send(message, "You need to be an admin to execute this command")
        return

    if admin and not can_restrict_members:
        if not user.can_pin_messages:
            send(message, "Sorry, you dont have enough permission to execute this command")
            return
    
    if user_id is None:
        send(message,PARDON_USAGE)


    app.unban_chat_member(admin_obj.chat_id, user_id)
    send(message, f"{user_id} is unbaned")

##-----------------------  unmute  -------------------------------------##
@app.message_handler(commands=['speak'])
def unmute(message):
    unmute_usage = "Use /unmute username"

    admin_obj = Adm(app, message)
    admin, can_restrict_members = admin_obj.is_admin()
    user, user_id = get_user(message)


    user = app.get_chat_member(message.chat.id,  message.from_user.id)


    if not admin_obj.bot_can_restrict_members:
        send(message, "Bot is not admin")
        return

    if not admin:
        send(message, "You need to be an admin to execute this command")
        return

    if admin and not can_restrict_members:
        if not user.can_restrict_members:
            send(message, "Sorry, you dont have enough permission to execute this command")
            return

    if user_id is None:
        send(message, unmute_usage)
        return

    user, user_id = get_user(message)
    app.restrict_chat_member(
        message.chat.id, user_id,
        can_send_messages=True
        )

    send(message, f"{user_id} is unmuted")
    
##-------------------------  mute24  ------------------------------------##
@app.message_handler(commands=['shutup'])
def mute24(message):
    mute24_usage = "Use /mute24 username"


    admin_obj = Adm(app, message)
    admin, can_restrict_members = admin_obj.is_admin()
    user, user_id = get_user(message)

    user = app.get_chat_member(message.chat.id,  message.from_user.id)


    if not admin_obj.bot_can_restrict_members:
        send(message, "Bot is not admin")
        return

    if not admin:
        send(message, "You need to be an admin to execute this command")
        return

    if admin and not can_restrict_members:
        if not user.can_restrict_members:
            send(message, "Sorry, you dont have enough permission to execute this command")
            return

    if user_id is None:
        send(message, mute24_usage)
        return

    if user_id == admin_obj.bot_id:
        send(message, '🧐')
        return

    if app.get_chat_member(admin_obj.chat_id, user_id).status == "left":
        send(message, "Not a member")
        return


    #user, user_id = get_user(message)

    if user_id in admin_obj.admin_list:
        send(message, "Cannot mute admin")
        return


    user, user_id = get_user(message)
    app.restrict_chat_member(
        message.chat.id, user_id, 
        until_date=time.time()+86400,
        can_send_messages=False
        )    
    send(message, f"{user_id} is muted for 24 hours")

##-------------------------- GET ID ---------------------------------------##
@app.message_handler(commands=['get_id'])
def get_id(message):
    get_id_usage = "Usage /id username \nor \nreply to the user's message with /id"
    user, user_id = get_user(message)

    if user_id is None:
        send(message, get_id_usage)
        return
    
    user, user_id = get_user(message)
    send(message, user_id)



app.polling()

"""
[pyrogram]
api_id = 1443823
api_hash = f89fac5dd9f2ddacd257d637a5980f04
"""
