from aiogram import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import *
from datetime import *
import random
from random import randint
from os import listdir
import time

client = MongoClient('localhost', 27017)

db_obj = client['MyDb_1']

collect_obj = db_obj['project']


bot = Bot(token='1804832946:AAH-SzmWs2IZMVp_SN72m7ZD8cQGOzmJXyk')
dp = Dispatcher(bot)


obj = {"user_id": "",
       "name_ul": "",
       "lvl": 1,
       "part_lvl": 0,
       "health": 0,
       "food_count": datetime(2010, 1, 1, 0, 0, 0, 0),
       "work": datetime(2010, 1, 1, 0, 0, 0, 0),
       "mood": 50,
       "duel_wins": 0,
       "duel_looses": 0,
       "duel_call": 0,
       "xp": 50,
       "money": 0,
       "sweets": 0,
       "drugs": 0,
       "potion": 0,
       "weapon_p": 0,
       "stick": 0,#палка
       "sword": 0, #меч
       "helmet": 0,#шлем
       "shell": 0,#панцырь
       "damage":0
       }

work_obj = ["money", "weapon_p", "food_count", "sweets", "drugs", "health"]

@dp.message_handler(commands=['start', 'help'])
async def get_command(msg: types.Message):
    if msg.text == "/start":
        await bot.send_message(msg.chat.id, "Приветствуем в боте с улитками 10/10")
    if msg.text == "/help":
        await bot.send_message(msg.chat.id, f"Чтобы было легче играть советую почитать {'https://telegra.ph/Komandy-bota-06-18'}")


kb = InlineKeyboardMarkup(row_width=2)

but_1 = InlineKeyboardButton('Инвентарь', switch_inline_query_current_chat='мой инвентарь')
but_2 = InlineKeyboardButton('Информация', switch_inline_query_current_chat='улитка инфо')

kb.add(but_1, but_2)

kb_2 = InlineKeyboardMarkup(row_width=2)
but_3 = InlineKeyboardButton('🍃подорожник🍃', switch_inline_query_current_chat='купить подорожник')
but_4 = InlineKeyboardButton('🍫шоколад🍫', switch_inline_query_current_chat='купить шоколадку')
kb_2.add(but_3, but_4)

kb_4 = InlineKeyboardMarkup(row_width=3)
but_6 = InlineKeyboardButton('покормить', switch_inline_query_current_chat='покормить улитку')
but_7 = InlineKeyboardButton('с работы', switch_inline_query_current_chat='завершить работу')
but_8 = InlineKeyboardButton('на работу', switch_inline_query_current_chat='отправиться на работу')
but_9 = InlineKeyboardButton('улитка', switch_inline_query_current_chat='моя улитка')
but_10 = InlineKeyboardButton('магазин', switch_inline_query_current_chat='магазин')
kb_4.add(but_9, but_10)


photo_address =["pr_ph/" + el for el in listdir("pr_ph") ]




@dp.message_handler()
async def uli(msg: types.Message):
    global user_id
    user_id = msg.from_user.id
    global user_name
    user_name = msg.from_user.first_name
    global player
    player = [el for el in collect_obj.find({"user_id": user_id})]


    if msg.text.lower() == "взять улитку":
        obj["user_id"] = user_id
        a = [a['user_id'] for a in collect_obj.find()]
        if user_id in a:
            await bot.send_message(msg.chat.id, "У тебя уже есть улитка, больше тебе не дадим")
        else:
            collect_obj.insert_one(obj)
            await bot.send_message(msg.chat.id, "Ураа!!!! Теперь у тебя есть улитка🐌🐌🐌")

    if msg.text.lower() == "моя улитка" or msg.text.lower() == '@ulitkii_bot моя улитка':
        b = [b['user_id'] for b in collect_obj.find()]
        if user_id not in b:
            await bot.send_message(msg.chat.id, "У тебя нет улитки")
        else:
            health = "Живая" if player[0]["health"] == 0 else "Мертвая"
            a = f"""
🐌Имя улитки: {player[0]["name_ul"]}
⭐Уровень улитки: {player[0]["lvl"]}
🍰Сытость: {player[0]["part_lvl"]} / {player[0]["lvl"] + 14}
❤Состояние: {health}
🦗Монетки: {player[0]["money"]}
👻Настроение: {player[0]["mood"]}



💪Количество побед: {player[0]["duel_wins"]}
👎Количество поражений: {player[0]["duel_looses"]}
                    """
            await bot.send_message(msg.chat.id, a, reply_markup=kb)

    if msg.text.lower()[:15] == "дать улитке имя" and len(msg.text.lower().split()) > 3:
        name = msg.text
        if player[0]["name_ul"] == "":
            collect_obj.update_one({"user_id": user_id}, {"$set": {"name_ul": name[16:]}})
            await bot.send_message(msg.chat.id, """Поздравляем с новым именем)
За последующие смены имен будет взыматься плата в 150 монеток""")
        else:
            await bot.send_message(msg.chat.id, "Имя уже есть, чтобы поменять имя используйте команду - Сменить имя [имя]")

    if msg.text.lower()[:11] == "сменить имя" and len(msg.text.lower().split()) > 2 :
        name = msg.text
        if player[0]["name_ul"] != "":
            collect_obj.update_one({"user_id": user_id}, {"$set": {"name_ul": name[12:]}})
            await bot.send_message(msg.chat.id, f"""Имя изменено на {name[12:]}""")
        else:
            await bot.send_message(msg.chat.id,
                                   "У улитки еще нет имени, используй команду - Дать улитке имя [имя]")

    if msg.text.lower() == "покормить улитку" or msg.text.lower() == '@ulitkii_bot покормить улитку':
        if player[0]["food_count"] < datetime.now():
            await bot.send_animation(msg.chat.id, open(photo_address[0], "rb"), caption= "Ваша улитка наелась! Поздравляю!💐😀")
            collect_obj.update_one({"user_id": user_id},
                                       {"$set": {"food_count": datetime.now() + timedelta(minutes=250)}})
            collect_obj.update_one({"user_id": user_id},
                                       {"$inc": {"part_lvl": +1}})
            collect_obj.update_one({"user_id": user_id}, {"$set": {"health": 0}})
            await new_lvl(user_id, msg)
        else:
            await bot.send_message(msg.chat.id, f"Улитка сможет подкрепиться чуть позже, подождите {str(player[0]['food_count'] - datetime.now())[:4]} ")

    if msg.text.lower() == "отправиться на работу" or msg.text.lower() == '@ulitkii_bot отправиться на работу':
        if player[0]["work"] < datetime.now():
            if player[0]["work"] + timedelta(minutes=240) < datetime.now():
                await bot.send_animation(msg.chat.id, open(photo_address[5], "rb"), caption = "Твоя улитка успешно поползла 💼работать!) Ты сможешь ее забрать через 2 часа")
                collect_obj.update_one({"user_id": user_id},
                                       {"$set": {"work": datetime.now() + timedelta(minutes=120)}})
            else:
                await bot.send_message(msg.chat.id, "Улитка может ходить на 💼работу только раз в 4 часа")
        else:
            await bot.send_message(msg.chat.id, "Твоя улитка и так 💼работает ")

    if msg.text.lower() == "завершить работу" or msg.text.lower() == "@ulitkii_bot завершить работу":
        rez = random.choice(work_obj)
        if player[0]["work"] == datetime(2010, 1, 1, 0, 0, 0, 0):
            await bot.send_message(msg.chat.id, "Ты не на работе")
        elif player[0]["work"] < datetime.now():
            give = randint(60, 150) + player[0]["mood"] - 60
            if rez == "drugs":
                a = randint(1, 3)
                collect_obj.update_one({"user_id": user_id}, {"$inc": {"drugs": +a}})
                await bot.send_message(msg.chat.id, f"💼 Поздравляю, ты завершил работу и получил {a} подорожник(ов)")
            if rez == "sweets":
                a = randint(1, 4)
                collect_obj.update_one({"user_id": user_id}, {"$inc": {"sweets": + a}})
                await bot.send_message(msg.chat.id, f"💼 Поздравляю, ты завершил работу и получил {a} шоколадки")
            if rez == "money":
                collect_obj.update_one({"user_id": user_id}, {"$inc": {"money": + give }})
                await bot.send_message(msg.chat.id, f"💼 Поздравляю, ты завершил работу и получил {give} монетки")
            if rez == "health":
                collect_obj.update_one({"user_id": user_id}, {"$set": {"health": 1}})
                collect_obj.update_one({"user_id": user_id}, {"$inc": {"money": - give}})
                await bot.send_message(msg.chat.id, f"О нет 🤯🤯🤯 , ты шел с работы и на тебя напали жабы!! Они побили твою улитку и отобрали все твои заработанные букашки")
            if rez == "food_count":
                collect_obj.update_one({"user_id": user_id}, {"$set": {"health": 0}})
                collect_obj.update_one({"user_id": user_id}, {"$inc": {"part_lvl": + randint(1, 3)}})
                await new_lvl(user_id, msg)
                await bot.send_message(msg.chat.id,
                                       f"После работы улитка заползла в столовую и подкрепилась 😋😋. Она получила несколько очков сытости а так же восстановила свое здоровье")
            if rez == "weapon_p":
                a = randint(1, 5)
                collect_obj.update_one({"user_id": user_id}, {"$inc": {"weapon_p": + a}})
                await bot.send_message(msg.chat.id, f"💼 Поздравляю, ты завершил работу и получил {a} оружейных кусочков")


            collect_obj.update_one({"user_id": user_id}, {"$set": {"work": datetime(2010, 1, 1, 0, 0, 0, 0)}})

        else:
            await bot.send_message(msg.chat.id,
                             f"Улитка еще на работе 😓😓, ты сможешь ее забрать через {str(player[0]['work'] - datetime.now())[:4]} ")


    if msg.text.lower() == "бой":
        user_id_2 = msg.reply_to_message.from_user.id
        user_name_2 = msg.reply_to_message.from_user.first_name
        player_1 = player
        player_2 = [el for el in collect_obj.find({"user_id": user_id_2})]

        if player_1[0]["duel_call"] != 0:
            await bot.send_message(msg.chat.id, "ТЫ не можешь сражаться, когда у тебя висит вызов на бой")
        elif player_2[0]["duel_call"] != 0:
            await bot.send_message(msg.chat.id, "Этого игрока уже вызвали на битву")
        elif user_id == user_id_2:
            await bot.send_message(msg.chat.id, "Ты не можешь сражаться сам с собой,умник")
        else:
            await bot.send_message(msg.chat.id,
                                   f"{user_name_2}, игрок {user_name} вызывает вас на бой. Надерите друг другу раковины!!!")

            collect_obj.update_one({"user_id": user_id_2}, {"$set": {"duel_call": str(user_id)+" "+str(user_name)}})



    if msg.text.lower() == "принять бой":
        if player[0]["duel_call"] == 0:
            await bot.send_message(msg.chat.id, "Улитке никто не кидал вызов на бой")
        else:
            player_1 = [el for el in collect_obj.find({"user_id": user_id})]
            user_id_2 = int(player_1[0]["duel_call"].split()[0])
            user_name_2 = player_1[0]["duel_call"].split()[1]
            player_2 = [el for el in collect_obj.find({"user_id": user_id_2})]


            if player_1[0]["work"] != datetime(2010, 1, 1, 0, 0, 0, 0) or player_2[0]["work"] != datetime(2010, 1, 1, 0, 0, 0, 0):
                await bot.send_message(msg.chat.id, "Кто-то из улиток сейчас работает!")

            if player_1[0]["health"] == 1 or player_2[0]["health"] == 1:
                await bot.send_message(msg.chat.id, "Нельзя начать бой, одна из улиток мертва")

            else:
                ph = random.choice(photo_address[1:5])
                await bot.send_animation(msg.chat.id, open(ph, "rb"))


                msg_id = await bot.send_message(msg.chat.id,
                                            text=f"""Улитка игрока {user_name}:
⚔️Приняла урона: 0
❤️Осталось здоровья: {player_1[0]["xp"]}

Улитка игрока {user_name_2}:
⚔️Приняла урона: 0
❤️Осталось здоровья: {player_2[0]["xp"]}
""", )

                while (True):
                    damage_1 = randint(randint(0,2)+player_1[0]["lvl"]//2, randint(7, 15)+player_1[0]["lvl"]//2) + randint(0, player_1[0]["damage"])
                    damage_2 = randint(randint(0,2)+player_1[0]["lvl"]//2, randint(7, 15)+player_1[0]["lvl"]//2) + randint(0, player_2[0]["damage"])

                    player_1[0]["xp"] -= damage_2
                    player_2[0]["xp"] -= damage_1


                    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id["message_id"], text = f"""Улитка игрока {user_name}:
⚔️Приняла урона: {damage_2}
❤️Осталось здоровья: {player_1[0]["xp"]}

Улитка игрока {user_name_2}:
⚔️Приняла урона: {damage_1}
❤️Осталось здоровья: {player_2[0]["xp"]}""")

                    time.sleep(1.5)


                    if player_1[0]["xp"] <= 0 and player_2[0]["xp"] <= 0:
                        await bot.send_message(msg.chat.id, "2 улитки отлетели, давайте заново!")
                        collect_obj.update_one({"user_id": user_id}, {"$set": {"duel_call": 0}})
                        collect_obj.update_one({"user_id": user_id_2}, {"$set": {"duel_call": 0}})
                        break
                    elif player_1[0]["xp"] <= 0:
                        await bot.send_message(msg.chat.id, f"Улитка игрока {user_name} проиграла")
                        await fix(user_id, msg)
                        await fix(user_id_2, msg)
                        collect_obj.update_one({"user_id": user_id}, {"$inc": {"duel_looses": +1}})
                        collect_obj.update_one({"user_id": user_id_2}, {"$inc": {"duel_wins": +1}})
                        collect_obj.update_one({"user_id": user_id_2}, {"$inc": {"money": +150}})

                        collect_obj.update_one({"user_id": user_id_2},
                                                     {"$inc": {"part_lvl": +1}})
                        await new_lvl(user_id_2, msg)
                        collect_obj.update_one({"user_id": user_id}, {"$set": {"health": 1}})
                        collect_obj.update_one({"user_id": user_id}, {"$set": {"duel_call": 0}})
                        collect_obj.update_one({"user_id": user_id_2}, {"$set": {"duel_call": 0}})
                        await new_lvl(user_id, msg)
                        break
                    elif player_2[0]["xp"] <= 0:
                        await bot.send_message(msg.chat.id, f"Улитка игрока {user_name_2} проиграла")
                        await fix(user_id, msg)
                        await fix(user_id_2, msg)
                        collect_obj.update_one({"user_id": user_id_2}, {"$inc": {"duel_looses": +1}})
                        collect_obj.update_one({"user_id": user_id}, {"$inc": {"duel_wins": +1}})
                        collect_obj.update_one({"user_id": user_id}, {"$inc": {"money": +150}})

                        collect_obj.update_one({"user_id": user_id},
                                                    {"$inc": {"part_lvl": +1}})
                        await new_lvl(user_id, msg)
                        collect_obj.update_one({"user_id": user_id_2}, {"$set": {"health": 1}})
                        collect_obj.update_one({"user_id": user_id}, {"$set": {"duel_call": 0}})
                        collect_obj.update_one({"user_id": user_id_2}, {"$set": {"duel_call": 0}})

                        await new_lvl(user_id_2, msg)
                        break

    if msg.text.lower() == "отклонить бой":
        await bot.send_message(msg.chat.id, f"И правильно, потом еще тратить лекарства!")

        collect_obj.update_one({"user_id": user_id}, {"$set": {"duel_call": 0}})

    if msg.text.lower() == "отозвать бой":
        player = [el for el in collect_obj.find({"duel_call": str(user_id)+" "+user_name})]
        if player != []:
            await bot.send_message(msg.chat.id, f"Ты отозвал бой")
            collect_obj.update_one({"duel_call": str(user_id)+" "+user_name}, {"$set": {"duel_call": 0}})
        else:
            await bot.send_message(msg.chat.id, f"Ты никого не вызывал на бой(")

    if msg.text.lower() == "сделать железный панцырь":
        if player[0]['weapon_p'] >= 6:
            collect_obj.update_one({"user_id": user_id}, {"$set": {"shell": 15}})
            collect_obj.update_one({"user_id": user_id}, {"$inc": {"xp": +10}})
            await bot.send_message(msg.chat.id, f"Успешно сделан панцырь")
        else:
            await bot.send_message(msg.chat.id, "Не хватает оружейных кусочков")
    if msg.text.lower() == "сделать шлем":
        if int(player[0]['weapon_p']) >= 3:
            collect_obj.update_one({"user_id": user_id}, {"$set": {"helmet": 10}})
            collect_obj.update_one({"user_id": user_id}, {"$inc": {"xp": +5}})
            await bot.send_message(msg.chat.id, f"Успешно сделан шлем")
        else:
            await bot.send_message(msg.chat.id, "Не хватает оружейных кусочков")
    if msg.text.lower() == "сделать палку":
        if player[0]['weapon_p'] >= 3:
            if player[0]['sword'] == 0:
                collect_obj.update_one({"user_id": user_id}, {"$set": {"stick": 10}})
                collect_obj.update_one({"user_id": user_id}, {"$inc": {"damage": +5}})
                await bot.send_message(msg.chat.id, f"Успешно сделана палка!")
            else:
                await bot.send_message(msg.chat.id, "У тебя уже есть другое оружие")
        else:
            await bot.send_message(msg.chat.id, "Не хватает оружейных кусочков")
    if msg.text.lower() == "сделать меч":
        if int(player[0]['weapon_p']) >= 8:
            if player[0]['stick'] == 0:
                collect_obj.update_one({"user_id": user_id}, {"$set": {"sword": 15}})
                collect_obj.update_one({"user_id": user_id}, {"$inc": {"damage": +12}})
                await bot.send_message(msg.chat.id, f"Успешно сделан меч!")
            else:
                await bot.send_message(msg.chat.id, "У тебя уже есть другое оружие")
        else:
            await bot.send_message(msg.chat.id, "Не хватает оружейных кусочков")



    if msg.text.lower() == "магазин" or msg.text.lower() == '@ulitkii_bot магазин':
        await bot.send_message(msg.chat.id, "Вот что вы можете здесь приобрести:", reply_markup=kb_2)



    if msg.text.lower() == "использовать подорожник":
        if player[0]["health"] == 0:
            await bot.send_message(msg.chat.id, "Твоя улитка пока что живая, побереги лекарства!")
        elif player[0]["drugs"] != 0:
            await bot.send_message(msg.chat.id,
                                   "Твоя улитка замоталась в подорожник и ей определенно стало лучше! Супер! ⛑")
            collect_obj.update_one({"user_id": user_id}, {"$inc": {"drugs": -1}})
            collect_obj.update_one({"user_id": user_id}, {"$set": {"health": 0}})
        else:
            await bot.send_message(msg.chat.id,
                                   "У тебя нет 🍃подорожника( Его можно найти на работе или купить в магазине за монетки")


    if msg.text.lower() == "купить подорожник" or msg.text.lower() == "@ulitkii_bot купить подорожник":
        if player[0]["money"] >= 225:
            collect_obj.update_one({"user_id": user_id}, {"$inc": {"drugs": +1}})
            collect_obj.update_one({"user_id": user_id}, {"$inc": {"money": -150}})
            await bot.send_message(msg.chat.id, "Ты успешно приобрел лекарство🍃")
        else:
            await bot.send_message(msg.chat.id, "Не хватает средств(")



    if msg.text.lower() == "использовать шоколадку":
        if player[0]["sweets"] != 0:
            await bot.send_message(msg.chat.id, "Твоя улитка наелась шоколада и стала чуточку щастливее!")
            collect_obj.update_one({"user_id": user_id}, {"$inc": {"sweets": -1}})
            collect_obj.update_one({"user_id": user_id}, {"$inc": {"mood": +5}})
        else:
            await bot.send_message(msg.chat.id,
                             "В твоем инвентаре нет 🍫шоколадки🍫, ты можешь приобрести его командой 'Магазин'")


    if msg.text.lower() == "купить шоколадку" or msg.text.lower() == "@ulitkii_bot купить шоколадку":
        if player[0]["money"] >= 75:
            collect_obj.update_one({"user_id": user_id}, {"$inc": {"sweets": +1}})
            collect_obj.update_one({"user_id": user_id}, {"$inc": {"money": -75}})
            await bot.send_message(msg.chat.id, "Ты успешно приобрел 🍫шоколадку🍫")
        else:
            await bot.send_message(msg.chat.id, "Не хватает средств(")



    if msg.text.lower().split()[0] == "передать" and len(msg.text.lower().split()) == 3:
        user_id_2 = msg.reply_to_message.from_user.id
        text = msg.text.lower().split()
        if text[1] == "подорожники":
            await give_to(user_id, user_id_2, 'drugs', int(text[2]), msg)
        if text[1] == "шоколадки":
            await give_to(user_id, user_id_2, 'sweets', int(text[2]), msg)
        if text[1] == "монетки":
            await give_to(user_id, user_id_2, 'money', int(text[2]), msg)


    if msg.text.lower() == 'мой инвентарь' or msg.text.lower() == '@ulitkii_bot мой инвентарь':
        await bot.send_message(msg.chat.id, f"""Инвентарь:
🍃Подорожники🍃 : {player[0]['drugs']}
🍫Шоколадки🍫 :{player[0]['sweets']}
🧃Зелье силы🧃 : {player[0]['potion']}
Оружейных кусочков : {player[0]["weapon_p"]}

Снаряжение:
палка : {player[0]['stick']} / 10
меч : {player[0]['sword']} / 15
шлем : {player[0]['helmet']} / 10
железный панцырь : {player[0]['shell']} / 15
""", reply_markup=kb_4)

    if msg.text.lower() == 'улитка инфо' or msg.text.lower() == "@ulitkii_bot улитка инфо":
        korm = f"через {str(player[0]['food_count'] - datetime.now())[:4]}" if player[0]["food_count"] > datetime.now() else ""
        if player[0]["work"] == datetime(2010, 1, 1, 0, 0, 0, 0):
            p = "Улитка не на работе"
        elif player[0]["work"] > datetime.now():
            p = f"Можно забрать улитку с работы через {str(player[0]['work'] - datetime.now())[:4]}"
        else:
            p = "Можно забрать улитку с работы"
        # print(str(player[0]['work'] - datetime.now())[:4])
        # print(str(player[0]['work']))

        duel = f"Бой с  {player[0]['duel_call'].split()[1]}" if player[0]["duel_call"] != 0 else "Не участвует в боe"
        a = f"""🍭:улитку можно покормить {korm}
🏃‍♂️:{p}
⚔️: {duel}
"""

        kb_3 = InlineKeyboardMarkup(row_width=2)
        kb_3.add(but_9)

        if player[0]["work"] < datetime.now() and player[0]["work"] != datetime(2010, 1, 1, 0, 0, 0, 0):
            kb_3.add(but_7)
        elif player[0]["work"] == datetime(2010, 1, 1, 0, 0, 0, 0):
            kb_3.add(but_8)
        if player[0]["food_count"] < datetime.now():
            kb_3.add(but_6)

        await bot.send_message(msg.chat.id, a, reply_markup=kb_3)



@dp.message_handler(content_types=['text'])
async def new_lvl(user_id, msg):
    player = [el for el in collect_obj.find({"user_id": user_id})]
    if player[0]["part_lvl"] >= player[0]["lvl"] + 14:
        collect_obj.update_one({"user_id": user_id},
                               {"$inc": {"lvl": +1}})
        collect_obj.update_one({"user_id": user_id},
                               {"$set": {"part_lvl": 0}})
        collect_obj.update_one({"user_id": user_id},
                               {"$inc": {"xp": +1}})
        await bot.send_message(msg.chat.id, f"Поздравляем! Улитка достигла нового, {player[0]['lvl'] + 1} уровня")




@dp.message_handler(content_types=['text'])
async def give_to(user_id, user_id_2, thing, count, msg):
    player = [el for el in collect_obj.find({"user_id": user_id})]
    if user_id == user_id_2:
        await bot.send_message(msg.chat.id, f"нельзя отправлять предметы самому себе")
    elif player[0][thing] >= count:
        collect_obj.update_one({"user_id": user_id_2},
                               {"$inc": {thing: + count}})
        collect_obj.update_one({"user_id": user_id},
                               {"$inc": {thing: - count}})
        await bot.send_message(msg.chat.id, f"Отправка успешно совершена!")
    else:
        await bot.send_message(msg.chat.id, f"У тебя столько нет")


@dp.message_handler(content_types=['text'])
async def fix(user_id, msg):
    player = [el for el in collect_obj.find({"user_id": user_id})]
    if player[0]["stick"] == 1:
        await bot.send_message(msg.chat.id, f"У тебя сломалась палка")
        collect_obj.update_one({"user_id": user_id}, {"$inc": {"xp": -6}})
    if player[0]["sword"] == 1:
        await bot.send_message(msg.chat.id, f"У тебя сломался меч")
        collect_obj.update_one({"user_id": user_id}, {"$inc": {"xp": -12}})
    if player[0]["helmet"] == 1:
        await bot.send_message(msg.chat.id, f"У тебя сломался шлем")
        collect_obj.update_one({"user_id": user_id}, {"$inc": {"protection": -5}})
    if player[0]["shell"] == 1:
        await bot.send_message(msg.chat.id, f"У тебя сломался железный панцырь")
        collect_obj.update_one({"user_id": user_id}, {"$inc": {"protection": -10}})
    if player[0]["helmet"] == 1:
        await bot.send_message(msg.chat.id, f"У тебя сломался железный панцырь")
        collect_obj.update_one({"user_id": user_id},
                               {"$inc": {"lvl": +1}})
    if player[0]["stick"] > 0:
        collect_obj.update_one({"user_id": user_id},
                               {"$inc": {"stick": -1}})
    if player[0]["sword"] > 0:
        collect_obj.update_one({"user_id": user_id},
                               {"$inc": {"sword": -1}})
    if player[0]["shell"] > 0:
        collect_obj.update_one({"user_id": user_id},
                               {"$inc": {"shell": -1}})
    if player[0]["helmet"] > 0:
        collect_obj.update_one({"user_id": user_id},
                               {"$inc": {"helmet": -1}})


if __name__ == '__main__':
    executor.start_polling(dp)