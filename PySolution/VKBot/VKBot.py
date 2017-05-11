# -*- coding: utf-8 -*-
import vk_api
import re
import string
from itertools import *
from vk_api.longpoll import VkLongPoll, VkEventType

login, password = '89870195625', '258262St'
vk = vk_api.VkApi(login, password)
whitelist = (25069332,)

class answer:
    def __init__(self, d, a):
        self.dict = d
        self.ans = a

ans_for_end = [ answer(('тристо','триста','трицто','трицта',
	                    '300','3оо','3о0','30о',
		                '3сто','3ста','3цто','3цта',
		                'три100','три1оо','три1о0','три10о'),'отсоси у программиста'),
                answer(('ет',),'пидора ответ'),
                answer(('да',),'на хую борода')]

ans_for_last = [answer(('куда','кида'),'туда, куда не ходят поезда'),
                answer(('тоже','тоге','тойе'),'на говно похоже'),
                answer(('где',),'в караганде'),
                answer(('ок',),'пидора кусок'),
                answer(('я','йа','иа'),'головка от хуя'),
                answer(('кек',),'лол арбидол'),
                answer(('лол',),'кек чебурек'),
                answer(('че','чо'),'хуй через плечо'),
                answer(('нету','нети'),'нет слова "нету", безграмотный')]

def del_repeats(match):
	return match.group(0)[0]

def write_chat(id, mes):
    vk.method('messages.send', {'chat_id':id,'message':mes})

def write_user(id, mes):
    vk.method('messages.send', {'user_id':id,'message':mes})

def answer_mes(message, user_id, user_name, from_chat):
    if int(user_id) in whitelist: return 'nope'
    if from_chat: preff = '@id'+str(user_id)+' ('+user_name+'), '
    else: preff = ''
    delimetrs = str.maketrans(
        'qwertyuiopasdfghjklzxcvbnm',
        'квертиуиопасдфгхйклзхцвбнм',
        string.punctuation+'ьъ'+"!@#$%^&amp;*()-_=+{}[];:'&quot;&lt;&gt;,./?|\\")
    message = message.lower().translate(delimetrs)
    
    #300
    if message.endswith(tuple(ans_for_end[0].dict)): return preff+ans_for_end[0].ans

    message = message.translate(str.maketrans('','',string.digits))
    message = re.sub(r'(.)\1+', del_repeats, message)
    last_word = message.split(' ')[-1]
    message.replace(' ','')
    for e,l in zip_longest(ans_for_end,ans_for_last):
        if e != None and message.endswith(tuple(e.dict)): return preff+e.ans
        elif l != None and last_word in l.dict: return preff+l.ans
    return 'nope'

def main():
    try:
        vk.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    longpoll = VkLongPoll(vk)
    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение: ')
            user_name = vk.method('users.get', {'user_ids':event.user_id})[0]['first_name']
            mes = answer_mes(event.text, event.user_id, user_name, event.from_chat)
            print('От кого:',user_name)
            print('Ответочка:',mes)
            if event.from_me: print(u'От меня для:')
            elif event.to_me: print(u'Для меня от:')

            if event.from_user and event.to_me:
                if mes != 'nope': write_user(event.user_id, mes)
                print(event.user_id)
            elif event.from_chat and event.to_me:
                if mes != 'nope': write_chat(event.chat_id, mes)
                print(event.user_id, 'в беседе', event.chat_id)
            elif event.from_group:
                print('группы', event.group_id)

            print('Текст:',event.text)

        elif event.type == VkEventType.USER_TYPING:
            print('Печатает ')

            if event.from_user: print(event.user_id)
            elif event.from_group: print('администратор группы', event.group_id)

        elif event.type == VkEventType.USER_TYPING_IN_CHAT:
            print('Печатает', event.user_id, 'в беседе', event.chat_id)

        elif event.type == VkEventType.USER_ONLINE:
            print('Пользователь', event.user_id, 'онлайн', event.platform)

        elif event.type == VkEventType.USER_OFFLINE:
            print('Пользователь', event.user_id, 'оффлайн', event.offline_type)

        else:
            print(event.type, event.raw[1:])

if __name__ == '__main__':
    main()

