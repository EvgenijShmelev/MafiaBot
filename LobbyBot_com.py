import telebot

LobbyHost = telebot.TeleBot('6847605581:AAFshf6F811PHzdMu98gvEg26RRNOrLf2Y8')

@LobbyHost.message_handler(content_types=["new_chat_members"])
async def player_join(message: types.Message):
    pass
LobbyHost.polling(none_stop=True) # не даёт выключать компиляцию