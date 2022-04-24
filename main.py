import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import time
from random import randint 
from settings import token, set_me

session=vk_api.VkApi(token = token)

me = set_me
s = []
Leo_id = -91050183

def send_message(user_id, message):
    session.method("messages.send", {
        "user_id": user_id,
        "message": message,
        "random_id": 0
    })

def listener():
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text.lower()
            if event.from_user == True:
                user_id = event.user_id
            elif event.from_group == True:
                group_id = "-" + str(event.group_id)
                user_id = int(group_id)
            else:
                pass
            if user_id == Leo_id:
                Leo(user_id, text)
                
    
def Leo(user_id, text):
    if "есть взаимная симпатия! добавляй в друзья -" in text:
        s = text

        k = s[s.find('vk.com/'):s.find('\n')]  # поиск до новой строчки
        # k = s[s.find('vk.com/'):s.find(' ', s.find('vk.com/'))] #Поиск до пробела
        # k = s[s.find('vk.com/'):s.find('"', s.find('vk.com/'))] #Поиск до ""

        f = open('like.txt', 'a')
        f.write('https://' + k)
        time.sleep(3)
        send_message(user_id, '1')
        send_message(user_id = me, message = "Я кое кого нашел: " + 'https://' + k)
        time.sleep(4) 

    elif text == "бот знакомств дайвинчик":
        send_message(user_id, "1")
        time.sleep(4) 

    elif "ты понравился" in text:
        send_message(user_id, '1')
        time.sleep(4) 

    elif "слишком много лайков за сегодня" in text:
        send_message(user_id = me, message = "Лайки закончились")
        time.sleep(4)

    elif "чтобы получать больше лайков" in text:
        send_message(user_id, "1")
        time.sleep(4) 
    elif "кому-то понравилась твоя анкета!":
        send_message(user_id, "1")
        time.sleep(2)
    else:
        send_message(user_id, "1")    
        time.sleep(4)


def main():
    print("Для запуска бота введите: start")
    a = input()
    if a == 'start':
        listener()
    else:
        main()

main()



