# class Leo():
#     leo_id = -91050183

#     def __init__(self, session, token: str, my_id: int, filters: list):

#         self.__session = session
#         self.token = token
#         self.filters = filters
#         self.my_id = my_id
    

    
#     @classmethod
#     def validate_token(cls, __token):
#         if type(__token) != str:
#             raise TypeError("Токен должен быть str")
        
#     @classmethod
#     def validate_filters(cls, __filters):
#         if type(__filters) != list:
#             raise TypeError("Фильтры должны быть list")

#     @classmethod
#     def validate_my_id(cls, __my_id):
#         if type(__my_id) != int:
#             raise TypeError("Айди должен быть типом int")
#         if len(str(__my_id)) != 9:
#             raise TypeError("Длина id должна быть равна 9 символам")

#     @property
#     def session(self):
#         return self.__session

#     @property
#     def token(self):
#         return self.__token
    
#     @token.setter
#     def token(self, token):
#         self.validate_token(token)
#         self.__token = token

#     @property
#     def my_id(self):
#         return self.__my_id
    
#     @my_id.setter
#     def my_id(self, my_id):
#         self.validate_my_id(my_id)
#         self.__my_id = my_id

#     @property
#     def filters(self):
#         return self.__filters
    
#     @filters.setter
#     def filters(self, filters):
#         self.validate_filters(filters)
#         self.__filters = filters


import multiprocessing as mp
import vk_api
from vk_api import VkApiError
from vk_api.longpoll import VkLongPoll, VkEventType
import time
from backend.controller import load_settings, save_data
from GUI.components import eror_message

Leo_id = -91050183
proc =[]

def get_process_list():
    return proc

def kill_process():
    pass

def start_process():
    pass


def kill_processes():
    while len(proc) != 0:
        for p in proc:
            p.terminate()
            proc.remove(p)

def get_user_info(local_settings):
    session=vk_api.VkApi(token = local_settings['token'])
    api = session.get_api()
    # try:
    #     vk_api.ApiError(api, api.account.getProfileInfo(), None, None)
    # except vk_api.exceptions.ApiError as e:
    #     eror_message(box_title="Ошибка", 
    #             msg = "Во время выполнения произошла ошибка",
    #             eror=e)
    return session, api


def start_processes():
    settings = load_settings()
    for ex in settings:
        try:
            session, api = get_user_info(ex)
            user = api.account.getProfileInfo()
            name = user['first_name']
            last_name = user['last_name']

            p = mp.Process(target=listener, args=(ex,), name=f"{name} {last_name}")
            p.daemon = True
            p.start()
            proc.append(p)
            print(f"Запущен поток {p.name} с параметрами:\n{ex}")

        except Exception as e:
            print(e)


def listener(local_settings):
    session, api = get_user_info(local_settings)
    root_user_id = api.account.getProfileInfo()['id']

    for event in VkLongPoll(session, wait=15).listen():
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
                leo(api, 
                    user_id, 
                    text, 
                    root_user_id, 
                    local_settings['checklist'],
                    local_settings['ignore_mode'],
                    local_settings['passive_mode'],
                    local_settings['cooldown_time'])


def leo(api, user_id, text, me, filters, ignore_mode, passive_mode, cooldown_time):
    print(f"Leo: {text}")
    if "есть взаимная симпатия! добавляй в друзья -" in text or 'надеюсь хорошо проведете время' in text:
        s = text

        k = s[s.find('vk.com/'):s.find('\n')]

        save_data(text)
        api.messages.send(user_id = me,
                        message = "Я кое кого нашел: " + 'https://' + k,
                        random_id = 0)
        time.sleep(cooldown_time)

    elif ("бот знакомств дайвинчик" in text and "слишком много лайков за сегодня" not in text) and passive_mode is False:
        api.messages.send(user_id = user_id,
                          message = '1',
                          random_id = 0)
        time.sleep(cooldown_time) 

    elif "ты понравился" in text or "ты понравилась" in text:
        api.messages.send(user_id = user_id,
                    message = '1',
                    random_id = 0)
        time.sleep(cooldown_time) 

    elif "слишком много лайков за сегодня" in text:
        api.messages.send(user_id = me,
                    message = "Лайки закончились",
                    random_id = 0)
        time.sleep(cooldown_time)

    elif "чтобы получать больше лайков" in text and passive_mode is False:
        api.messages.send(user_id = user_id,
                    message = "1",
                    random_id = 0)
        time.sleep(cooldown_time)

    elif "хочешь больше взаимок?" in text and passive_mode is False:
        api.messages.send(user_id = user_id,
                    message = '2',
                    random_id = 0)
        time.sleep(cooldown_time)

    elif "кому-то понравилась твоя анкета!" in text:
        if ignore_mode is False:
            api.messages.send(user_id = user_id,
                        message = "1",
                        random_id = 0)
        else:
            api.messages.send(user_id = user_id,
                        message = "3",
                        random_id = 0)
        time.sleep(cooldown_time)

    elif "нет такого варианта ответа," in text: #or "пришли мне свое местоположение" in text or "Время просмотра анкеты истекло,":
        api.messages.send(user_id = user_id,
            message = '2',
            random_id = 0)
        time.sleep(cooldown_time)

    elif "пришли мне свое местоположение" in text: # or "Время просмотра анкеты истекло,":
        api.messages.send(user_id = user_id,
            message = '2',
            random_id = 0)
        time.sleep(cooldown_time)

    elif "предлагаю тебе сделку:" in text:
        api.messages.send(user_id = user_id,
            message = '2',
            random_id = 0)
        time.sleep(cooldown_time)

    else:
        splited_text = set(text.split())
        if passive_mode is False:
            if splited_text.intersection(set(filters)) or ignore_mode is True:
                api.messages.send(user_id = user_id,
                        message = "3",
                        random_id = 0)
            else:
                api.messages.send(user_id = user_id,
                        message = "1",
                        random_id = 0)
        time.sleep(cooldown_time)


# def leo(api, user_id, text, me, filters, ignore_mode, passive_mode, cooldown_time):
#     print(f"Leo: {text}")

#     if "есть взаимная симпатия! добавляй в друзья -" in text or 'надеюсь хорошо проведете время' in text:
#         s = text

#         k = s[s.find('vk.com/'):s.find('\n')]

#         save_data(text)
#         api.messages.send(user_id = me,
#                         message = "Я кое кого нашел: " + 'https://' + k,
#                         random_id = 0)
#         time.sleep(cooldown_time)

#     elif ("бот знакомств дайвинчик" in text and "слишком много лайков за сегодня" not in text) and passive_mode is False:
#         api.messages.send(user_id = user_id,
#                           message = '1',
#                           random_id = 0)
#         time.sleep(cooldown_time) 

#     elif "ты понравился" in text or "ты понравилась" in text:
#         api.messages.send(user_id = user_id,
#                     message = '1',
#                     random_id = 0)
#         time.sleep(cooldown_time) 

#     elif "слишком много лайков за сегодня" in text:
#         api.messages.send(user_id = me,
#                     message = "Лайки закончились",
#                     random_id = 0)
#         time.sleep(cooldown_time)

#     elif "чтобы получать больше лайков" in text and passive_mode is False:
#         api.messages.send(user_id = user_id,
#                     message = "1",
#                     random_id = 0)
#         time.sleep(cooldown_time)

#     elif "хочешь больше взаимок?" in text and passive_mode is False:
#         api.messages.send(user_id = user_id,
#                     message = '2',
#                     random_id = 0)
#         time.sleep(cooldown_time)

#     elif "кому-то понравилась твоя анкета!" in text:
#         if ignore_mode is False:
#             api.messages.send(user_id = user_id,
#                         message = "1",
#                         random_id = 0)
#         else:
#             api.messages.send(user_id = user_id,
#                         message = "3",
#                         random_id = 0)
#         time.sleep(cooldown_time)

#     elif "нет такого варианта ответа," in text: #or "пришли мне свое местоположение" in text or "Время просмотра анкеты истекло,":
#         api.messages.send(user_id = user_id,
#             message = '2',
#             random_id = 0)
#         time.sleep(cooldown_time)

#     elif "пришли мне свое местоположение" in text: # or "Время просмотра анкеты истекло,":
#         api.messages.send(user_id = user_id,
#             message = '2',
#             random_id = 0)
#         time.sleep(cooldown_time)
    
#     else:
#         splited_text = set(text.split())
#         if passive_mode is False:
#             if splited_text.intersection(set(filters)) or ignore_mode is True:
#                 api.messages.send(user_id = user_id,
#                         message = "3",
#                         random_id = 0)
#             else:
#                 api.messages.send(user_id = user_id,
#                         message = "1",
#                         random_id = 0)
#         time.sleep(cooldown_time)