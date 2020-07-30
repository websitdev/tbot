#from packages import install
#install()
import telebot
#from remain_up import remain_up
from text import *
from random import *
import time
import json
import os
import traceback
import subprocess
import secrets
from threading import Thread

##init##
#import my_apis as api

#remain_up()


class Break(Exception):
    pass


try:
    import my_apis as api
    API_TOKEN = api.TOKEN

except ImportError:
    API_TOKEN = os.environ.get("BOT_API_TOKEN")
    #API_TOKEN = ""

##=====Variables ===========
if API_TOKEN is None or API_TOKEN == '':
    print("No token provided")
    exit(1)

msg = 0
print(API_TOKEN)

app = telebot.TeleBot(API_TOKEN)

##COMMANDS##


def restrict_user(user_id, until_date, *args):
    app.restrict_chat_member(
        can_send_messages="mute" in args,
        can_add_web_page_previews=True,
        can_invite_users="no_invite" in args,
        can_send_media_messages="no_media" in args,
        can_send_other_messages="no_msg" in args,
        )


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

def is_alive(threads):
    return True in [thread.is_alive() for thread in threads]


def delete_message(chat_id, msg_id):
    global msg

    try:
        app.delete_message(chat_id, msg_id)
        msg += 1
    except:
        pass


def bot_can_delete_messages(chat_id):
    admins = app.get_chat_administrators(chat_id)
    bot = app.get_me()

    for admin in admins:
        if admin.user.id == bot.id:
            if admin.can_delete_messages:
                return True


def bot_can_restrict_members(chat_id):
    admins = app.get_chat_administrators(chat_id)
    bot = app.get_me()

    for admin in admins:
        if admin.user.id == bot.id:
            if admin.can_restrict_members:
                return True


def is_bot_admin(chat_id):
    admins = app.get_chat_administrators(chat_id)
    bot = app.get_me()

    for admin in admins:
        if admin.user.id == bot.id:
            return True


def can_delete(message):
    return message.can_delete_messages()


def can_restrict_members(message):
    return message.can_restrict_members()


def is_admin(chat_id, user_id):
    user = app.get_chat_member(chat_id, user_id)
    user_type = user.status

    if user_type == "creator":
        return (True, True)

    elif user_type == "administrator":
        return (True, False)

    return (False, False)


def send(message, reply):
    app.reply_to(
        message,
        reply
    )


def get_user(message):
    try:
        user = message.reply_to_message
        user_id = message.reply_to_message.from_user.id
    except:
        user = message
        try:
            user_id = message.text.split()[1]
        except:
            return

    return(user, user_id)


@app.message_handler(commands=['hi', 'hello'])
def hi(message):
    send(message, 'hello')


@app.message_handler(commands=['leave'])
def hi(message):
    app.leave_chat(message.chat.id)
    send(message, 'screw you guys')

@app.message_handler(commands=['start'])
def start(message):
    send(message, about)


@app.message_handler(commands=['help'])
def help(message):
    send(message, help_)


@app.message_handler(commands=['bye'])
def bye(message):
    send(message, "bye i am going to sleep")


@app.message_handler(commands=['rules'])
def rules(message):
    send(message, rule)


@app.message_handler(commands=['start'])
def test(message):
    send(message, message.command)


@app.message_handler(commands=['todo'])
def todo(message):
    send(message, 'hmmm')


@app.message_handler(commands=['stupid'])
def stupid(message):
    send(message, "stupid")

@app.message_handler(commands=['die'])
def stupid(message):
    send(message, "bot died")

@app.message_handler(commands=['kick'])
def kick(message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        admin, can_kick = is_admin(chat_id, user_id)
        user = app.get_chat_member(chat_id, user_id)

        if not admin:
            send(message, "You need to be an admin to execute this command")
            return

        if admin and not can_kick:
            if not user.can_restrict_members:
                send(message, "You don't have sufficient permission")
                return

        if get_user(message) is None:
            send(message, kick_usage)
            return

        member, member_id = get_user(message)

        if member_id == app.get_me().id:
          send(message, '🧐')
          return

        if app.get_chat_member(chat_id, member_id).status == "left":
            send(message, "Not a member")
            return

        if not is_bot_admin(chat_id):
            send(message, "Bot is not admin")
            return

        if not bot_can_restrict_members(chat_id):
            send(message, "Bot cannot restrict members")
            return

        #user, user_id = get_user(message)

        if is_admin(chat_id, member_id)[0]:
            send(message, "Cannot kick admin")
            return

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
        pass


@app.message_handler(commands=['delete'])
def delete(message):
    global msg, to_delete
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    admin, can_edit = is_admin(chat_id, user_id)
    user = app.get_chat_member(message.chat.id,  message.from_user.id)

    if not is_bot_admin:
        send(message, "Bot is not admin")
        return

    if not bot_can_delete_messages(message.chat.id):
        send(message, "Bot can't delete messsages")
        return

    if not admin:
        send(message, "You need to be an admin to execute this command")
        return

    if admin and not can_edit:
        if not user.can_delete_messages:
            send(message, "Sorry, you dont have enough permission to execute this command")
            return

    if get_user(message) is None:
        send(message, delete_usage)
        return

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


@app.message_handler(commands=['test'])
def test(message):
    send(message, "bot is alive")


@app.message_handler(commands=['python3'])
def python3(message):
    print(message.text)
    send(message, run_python3(message))


@app.message_handler(commands=['whois'])
def whois(message):
    if get_user(message) is None:
        send(message, json.loads(whois_usage))
        return

    user, user_id = get_user(message)
    send(message, app.get_chat_member(message.chat.id, user_id))


@app.message_handler(commands=['members_count'])
def memb(message):
    send(message, app.get_chat_members_count(message.chat.id))


@app.message_handler(commands=['unpin'])
def mes_count(message):
    app.unpin_chat_message(message.chat.id)


@app.message_handler(commands=['pardon'])
def pardon(message):
    user, user_id = get_user(message)
    app.unban_chat_member(message.chat.id, user_id)
    send(message, f"{user_id} is unbaned")


@app.message_handler(commands=['unmute'])
def unmute(message):
    if get_user(message) is None:
        send(message, unmute_usage)
        return

    user, user_id = get_user(message)
    app.restrict_chat_member(
        message.chat.id, user_id,
        can_send_messages=True
        )

    send(message, f"{user_id} is unmuted")
    
@app.message_handler(commands=['mute24'])
def mute24(message):
    if get_user(message) is None:
        send(message, mute24_usage)
        return

    user, user_id = get_user(message)
    app.restrict_chat_member(
        message.chat.id, user_id, 
        until_date=time.time()+86400,
        can_send_messages=False
        )
    
    send(message, f"{user_id} is muted for 24 hours")

@app.message_handler(commands=['get_id'])
def get_id(message):
    if get_user(message) is None:
        send(message, get_id_usage)
        return
    
    user, user_id = get_user(message)
    send(message, user_id)
