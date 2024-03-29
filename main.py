import telebot
from telebot import types
from roles import MafiaPlayer
import random, threading
from time import sleep

Mafia_room = []

Mafia = telebot.TeleBot('6847605581:AAFshf6F811PHzdMu98gvEg26RRNOrLf2Y8')

users = set()

Name = ["Bob", "Alpha", "Sugar", "Pahan", "Noob", "Thief", "Tim", "Logan" ]

Role = ["Mafia", "cityzen"]

choice_mafia = []

waiting_room = []

lobby = []

Mafia_chat_mode = False   # переменная режима для мафии

@Mafia.message_handler(commands=['find'])
def finde_thegame(message):

    waiting_room.append(message.from_user.id)

    Mafia.send_message(message.from_user.id, f"Вы попали в комнату ожидания. В ней {len(waiting_room)} игрок(а)")

    for user in waiting_room:
        if user != message.from_user.id:
            Mafia.send_message(user, f'Количество игроков в комнате ожидания = {len (waiting_room)}')  # Сообщение всем остальным игрокам о появление нового игрока

    if len(waiting_room) >= 2:
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
        waiting_room.clear()

        for i in range(0,len(lobby)):
            player = lobby[i]
            Mafia.send_message(player.id_chat, f"Ваше имя {player.name}, ваша роль {player.role}")
            if player.role == "Mafia":
                Mafia_room.append(player)  # Добавляет людей с ролью мафии в отдельный масив Mafia_room
            Mafia.send_message(player.id_chat, "Игра начинается")
        start_game(message)


def start_game(message):
    for i in range(0,len(lobby)):
        player = lobby[i]
        Mafia.send_message(player.id_chat, f"Наступил день. Самое время друг с другом познакомиться, вам даётся 1 минута.")
    time_sleep(5)
    for i in range(0,len(lobby)):
        player = lobby[i]
        Mafia.send_message(player.id_chat, f"Наступила ночь")
        Mafia.send_message(player.id_chat, f"Просыпается Мафия")
    global Mafia_chat_mode
    Mafia_chat_mode = True
    time_sleep(5)
    for i in range(0,len(lobby)):
        player = lobby[i]
        Mafia.send_message(player.id_chat, f"Мафия делает свой выбор")
    file = open('Mafia-knife3.png', 'rb')
    for i in range(0,len(Mafia_room)):
        id = Mafia_room[i].id_chat
        markup = mafia_buttons_photo(message)
        Mafia.send_photo(id, file, reply_markup=markup)
    time_sleep(5)


    finally_choice_mafia = process_mafia_choice(choice_mafia)



    for i in range(0,len(lobby)):
        player = lobby[i]
        Mafia.send_message(player.id_chat, f"Мафия сделала свой выбор")# Всем игрокам отсылается сообщение


def mafia_buttons_photo(message):
    markup = types.InlineKeyboardMarkup()
    for i in range(0,len(lobby)):
        player = lobby[i]
        if player.alive == True and player.role != "Mafia":
            markup.add(types.InlineKeyboardButton(f"{player.name}", callback_data=player))
    return markup

def doca(callback):
    choice_mafia.append(callback.data)
    Mafia.delete_message(callback.message.chat.id, callback.message.message_id)

def process_mafia_choice(choice_mafia):
    if len(choice_mafia) == 2:
        name1 = choice_mafia.name[0]
        name2 = choice_mafia.name[1]
        if name1 == name2:
            return name1
        if name1 != name2:
           k = random.randint(0, 1)
           if k == 0:
               return name1
           if k == 1:
               return name2
    if len(choice_mafia) == 1:
        name1 = choice_mafia.name[0]
        return name1
    if len(choice_mafia) == 0:
        pass




@Mafia.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data.name == 'Bob':   #Обрабатываем выбор мафиии после нажатия на кнопки
        doca(callback)
    if callback.data.name == 'Alpha':
        doca(callback)
    if callback.data.name == 'Sugar':
        doca(callback)
    if callback.data.name == 'Pahan':
        doca(callback)
    if callback.data.name == 'Noob':
        doca(callback)
    if callback.data.name == 'Thief':
        doca(callback)
    if callback.data.name == 'Tim':
        doca(callback)
    if callback.data.name == 'Logan':
        doca(callback)

def time_sleep(second):
    sleep(second)

@Mafia.message_handler(func=lambda message: True)
def on_message(message):
    print(message)
    for i in range(0, len(lobby)):
            id = lobby[i].id_chat
            if id == message.from_user.id: # Обрабатывает сообщение если человек находится в лобби
                name = lobby[i].name
                if Mafia_chat_mode == False:   # Если чат общий
                    for a in range(0, len(lobby)):
                            id = lobby[a].id_chat
                            if id != message.from_user.id:  # Убирает эфект эхо
                                Mafia.send_message(id, f"{name}: {message.text}")   # общий анонимный чат
                else:
                    for a in range(0, len(Mafia_room)):
                        id = Mafia_room[a].id_chat
                        if id == message.from_user.id: # Обрабатывает сообщение если человек находится в лобби мафии
                            for b in range(0, len(Mafia_room)):
                                    id = Mafia_room[b].id_chat
                                    if id != message.from_user.id:  # Убирает эфект эхо
                                        Mafia.send_message(id, f"{name}: {message.text}")


Mafia.polling(none_stop=True)   # точка входа
