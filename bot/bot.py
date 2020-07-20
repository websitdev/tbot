from pyrogram import Client,Filters

##init##
app = Client(
    "bot",
    bot_token="1257512221:AAEN1R8ngditDaaseZwumjDmfzTlaI77Rd0"
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

app.run()

