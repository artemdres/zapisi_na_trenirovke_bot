import telebot
import json
import datetime
import requests 

tokin = "7282555430:AAE26KGN3lTPA7BeKpsNDf3xP-qKuCa9Yb8"

requests.get(f"https://api.telegram.org/bot{tokin}/deleteWebhook")


bot=telebot.TeleBot(tokin)






fail=open("slovar.json", "r", encoding="UTF-8")
slovar=json.load(fail)
fail.close()



spisok_s_vremenim=[]
q=0
while q<24:
    time=datetime.time(q,0)
    spisok_s_vremenim.append(str(time))
    q=q+1






dni_neeli=["понедельник", "вторник", "среда", "четверг", "пятница", "субота", "воскресенье"]
trenirovki=["Кардиотренировка", "Силовая тренировка", "Тренировка на гибкость", "Функциональная тренировка"]
slovar_polovatela={}
dnevnik_polzovatela={}














@bot.message_handler(["start"]) 
def obrabotak_start(message):
    knopki=name_trenirovok()
    bot.send_message(message.chat.id, "добро пожаловать", reply_markup=knopki)
    

def knopki_s_dni_nedel():
    spisok_knopok=telebot.types.InlineKeyboardMarkup()
    for den in dni_neeli:
        knopka=telebot.types.InlineKeyboardButton( den, callback_data="den_"+den)
        spisok_knopok.add(knopka)
    return spisok_knopok
















def sostoynie_polzovatrla(message):
    bot.send_message(message.chat.id, "ваше состояние "+message.text)
    dnevnik_polzovatela[message.chat.id]=[str(datetime.date.today()), message.text]
    bot.send_message(message.chat.id, "ваш вес?"  )
    bot.register_next_step_handler_by_chat_id(message.chat.id, ves_polzovatela)

def ves_polzovatela(message):
    
    bot.send_message(message.chat.id, "ваш вес "+message.text)
    dnevnik_polzovatela[message.chat.id].append(message.text)
    fail=open("dnevnik.json", "r", encoding="UTF-8")
    slovar=json.load(fail)
    fail.close()
    if str(message.chat.id) not in slovar:
        slovar[str(message.chat.id)]=[dnevnik_polzovatela[message.chat.id]]
    else:
        slovar[str(message.chat.id)].append(dnevnik_polzovatela[message.chat.id])
    fail=open("dnevnik.json", "w", encoding="UTF-8")
    json.dump(slovar, fail, ensure_ascii=False, indent=4)
    fail.close()
    
    
        
        

@bot.message_handler(["write_journal"]) 
def obrabotka_dnevnik(message):
    bot.send_message(message.chat.id, "ваше состояние?"  )
    
    bot.register_next_step_handler_by_chat_id(message.chat.id, sostoynie_polzovatrla)
    
    













def name_trenirovok():
    spisok_knopok=telebot.types.InlineKeyboardMarkup()
    for trenorovka in trenirovki:
        knopka=telebot.types.InlineKeyboardButton( trenorovka, callback_data="trenerovka_"+trenorovka)
        spisok_knopok.add(knopka)
    return spisok_knopok

def nazvanie_trenerovak_polzovateka(Id):
    spisok_knopok=telebot.types.InlineKeyboardMarkup()
    fail=open("slovar.json","r", encoding="UTF=8")
    slovar=json.load(fail)    
    slovar_polzovatelajson=slovar[Id]
    for trenerovka in slovar_polzovatelajson:
        knopka=telebot.types.InlineKeyboardButton( trenerovka, callback_data="ydalenie_"+trenerovka)
        spisok_knopok.add(knopka)
    return spisok_knopok



def knopli_s_vremenim():
    spisok_knopk=telebot.types.InlineKeyboardMarkup()
    for tim in spisok_s_vremenim:
        knopka=telebot.types.InlineKeyboardButton( tim, callback_data="vrema_"+tim)
        spisok_knopk.add(knopka)
    return spisok_knopk




@bot.message_handler(["read_journal"])
def obrabotka_read_journal(message):
    fail=open("dnevnik.json", "r", encoding="UTF-8")
    dnevnik=json.load(fail)
    if str(message.chat.id) in dnevnik:
        dnevnik_polzovatela=dnevnik[str(message.chat.id)]
        big_soobsenie=""
        for  zapis_polzovatela in dnevnik_polzovatela:
            soobsenie="дата "+zapis_polzovatela[0]+"\n"+"состояние "+zapis_polzovatela[1]+"\n"+"ваш вес "+zapis_polzovatela[2]
            big_soobsenie=big_soobsenie+soobsenie+"\n\n\n"
        bot.send_message(message.chat.id, big_soobsenie)
    else:
        bot.send_message(message.chat.id, "у вас нет записей")
    

@bot.message_handler(["yadalit"])
def obrabotak_yadalit(message):
    fail=open("slovar.json","r", encoding="UTF=8")
    slovar=json.load(fail)   
    if str(message.chat.id) in slovar:
        slovar_polovatelajson=slovar[str(message.chat.id)]
        if len(slovar_polovatelajson)>0 :
            knopki=nazvanie_trenerovak_polzovateka(str(message.chat.id))
            bot.send_message(message.chat.id, "выбирете тренерову которую вы хотите удалить ", reply_markup=knopki)
        else:
            bot.send_message(message.chat.id, "у вас нет тренеровок")
    else:
        bot.send_message(message.chat.id, "у вас нет тренеровок ")
    

    

def true(message):
    return True


@bot.callback_query_handler(func=true)
def nazatie (clik):
    spisok=clik.data.split("_")
    if spisok[0]=="trenerovka":
        bot.send_message(clik.message.chat.id, "Вы выбрали тренеровку "+spisok[1], reply_markup=knopki_s_dni_nedel())
        slovar_polovatela[clik.message.chat.id]=[spisok[1]]
    elif spisok[0]=="den":
        bot.send_message(clik.message.chat.id, "Вы выбрали день "+spisok[1], reply_markup=knopli_s_vremenim())
        slovar_polovatela[clik.message.chat.id].append(spisok[1])
    elif spisok[0]=="vrema":
        bot.send_message(clik.message.chat.id, "Вы выбрали время "+spisok[1])
        slovar_polovatela[clik.message.chat.id].append(spisok[1])
        fail=open("slovar.json","r", encoding="UTF-8")
        slovar=json.load(fail)
        spisok_info=slovar_polovatela[clik.message.chat.id]
        if str(clik.message.chat.id) in slovar:
            slovar_tenerovok=slovar[str(clik.message.chat.id)]
            slovar_tenerovok[spisok_info[0]]=[spisok_info[1], spisok_info[2]]
        else:
    
            slovar[str(clik.message.chat.id)]={spisok_info[0]:[spisok_info[1], spisok_info[2]]}  
                     
        fail.close()
        fail=open("slovar.json","w", encoding="UTF-8")
        json.dump(slovar, fail, ensure_ascii=False, indent=4)
        fail.close()
    elif spisok[0]=="ydalenie":
        
        fail=open("slovar.json", "r", encoding="UTF=8")
        slovar=json.load(fail)
        slovar_polovatelajson=slovar[str(clik.message.chat.id)]
        del slovar_polovatelajson[spisok[1]]        
        fail.close()        
        fail=open("slovar.json", "w", encoding="UTF=8")
        json.dump(slovar,fail,ensure_ascii=False, indent=4)
        fail.close()
        if len(slovar_polovatelajson)>0 :
            knopki=nazvanie_trenerovak_polzovateka(str(clik.message.chat.id))
            bot.edit_message_text("выбирете тренерову которую вы хотите удалить ", clik.message.chat.id, clik.message.message_id, reply_markup=knopki )
        else:
            bot.edit_message_text("у вас не тренеровок ", clik.message.chat.id, clik.message.message_id )



@bot.message_handler(["zapisat_dnevnil"]) 
def obrabotak_zapisat_dnevnik(message):
    bot.send_message(message.chat.id, "вы вошли во в кладку дневник")
     


















































bot.polling()