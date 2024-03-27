import telebot
from telebot import types
from roles import MafiaPlayer
import random

Mafia = telebot.TeleBot('6847605581:AAFshf6F811PHzdMu98gvEg26RRNOrLf2Y8')

users = set()

Name = ["Bob", "Alpha", "Sugar", "Pahan", "Noob", "Thief", "Tim", "Logan"]

Role = ["Mafia", "Mafia", "cityzen", "cityzen", "cityzen", "cityzen", "Doctor", "Sheriff"]

waiting_room = []

lobby = []

@Mafia.message_handler(commands=['find'])
def finde_thegame(message):

    waiting_room.append(message.from_user.id)

    
    Mafia.send_message(message.from_user.id, f"Вы попали в комнату ожидания. В ней {len(waiting_room)} игрок(а)") 

    for user in waiting_room:
        if user != message.from_user.id:
            Mafia.send_message(user, f'Количество игроков в комнате ожидания = {len (waiting_room)}')  # Сообщение всем остальным игрокам о появление нового игрока
            
    if len(waiting_room) == 2:
        random_name = Name  
        random.shuffle(random_name)  # перебор массива имён
        random_role = Role 
        random.shuffle(random_role)   # перебор массива ролей

        for i in range(0, len(waiting_room)):
            player = MafiaPlayer()
            player.id_chat = waiting_room[i]
            player.name = random_name[i]
            player.role = random_role[i]
            lobby.append(player)


        for i in range(0,len(lobby)):
            player = lobby[i]
            Mafia.send_message(player.id_chat, f"Ваше имя {player.name}, ваша роль {player.role}") 


@Mafia.message_handler(func=lambda message: True)
def on_message(message):
    print(message)

    for user in users:
        if user != message.from_user.id:
            Mafia.send_message(user, message.text)   # общий анонимный чат

    users.add(message.from_user.id)

Mafia.polling(none_stop=True)   # точка входа







