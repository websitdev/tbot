from pyrogram import Client,Filters

##init##
app = Client(
    "bot",
    bot_token="1257512221:AAEN1R8ngditDaaseZwumjDmfzTlaI77Rd0"
)
#commands
@app.on_message(Filters.command("start"))
def on_start(client,message):
    print("/start command detected")

app.run()#starts the app