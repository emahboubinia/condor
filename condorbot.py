from gc import callbacks
from itertools import count
import random
import html
import json
import logging
import traceback
from typing import Dict
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot, InputMediaPhoto, InputMediaDocument, InputMediaVideo, InputMediaAudio, constants, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.ext import ApplicationHandlerStop, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, CallbackQueryHandler, TypeHandler

import os
import re
import requests

from config import *

TOKEN = '5434042917:AAGT9tVTf8PYpV2WjB1LdGSKOMew7W44A14' #real
#TOKEN = '5644860622:AAEVpuIc6uPDnW5bIKsQWk8mTKgYzTLBgAA'  #test

bot = Bot(token=TOKEN)
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
#variable
bot_name = "مرام"
#private Q&A group
#main_group_id = -1001850055659 #test
main_group_id = -1001827444680 #real

#channels id
quiz_channel = -1001869721469
data_channel_id = -1001809834141
file_channel_id = -1001795975508
condor_spam_id = -1001802178902
archive_channel_id = -1001780135040
#public Q&A group
#public_group = -1001802178902 #test
public_group = "@Condorlab_gap" #real

#main channel id
channel_id = "@condor_lab"
join_link = "https://t.me/+yhgPlwzVV31kM2I0"
condorcast_url = "https://gist.github.com/Am005mA/f2cc8436db9ade85fee871c67729d421"
quiz_url = "https://gist.github.com/Am005mA/378957e918917c98edbda561edacb7c7"
note_url = "https://gist.github.com/Am005mA/a873fc814695891c9b06b0255bb9f32a"
#admins id 
bot_admins = [owener_id,bussiness_id,mohsen_id,danial_id,nima_id,arman_id,sheyda_id,fatemeh_id,mani_id,goli_id,kia_id,yehaneh_id,fallah_id,anita_id,matin_id,parham_id,parsa_id,hasti_id]

#convestation returns
q_option,q_choose,q_text,not_joined,joined,q_continue,q_c_done = range(7)

#text
help_txt = "راهنمایی"
question_txt = "سوال دارم"
quiz_text = "کوییز"
condorcat_text = "کندرکست"
note_text = "کندر تکست"
azmoon_txt = "منابع حل سوال"
home_return_txt = "برگشت"
azm_step_1_txt = "مرحله یک"
azm_step_2_txt = "مرحله دو"
azm_talaha_txt = "آزمون طلاها"
azm_ibo_txt = "IBO"
reference_book_txt = "کتاب ها"
book_and_manual_txt = "رفرنس های حل سوال"
other_country_exams_txt = "سوالات المپیاد داخلی سایر کشور ها و دیگر مسابقات"
requests_txt = "درخواست"
requests_discription = "سلام این بخش برای اینکه اگه درخواست یا پیشنهادی داری با ما مطرح کنی\nبعد از اینکه درخواست رو نوشتی دکمه ی 'بفرست' رو بزن اگر هم که درخواستی نداری دکمه 'لغو' رو بزن"
ask_please_txt = 'خب سوالت رو بپرس و بعد دکمه "پرسیدم" رو بزن'
q_done_txt = "پیام شما به اساتید ارسال شد.\nجواب در اولین فرصت برای شما ارسال خواهد شد"
welcome_text = '''به کندربات خوش اومدی'''
help_message = '''🤖 کندربات !

🔆 توی کندر بات میتونی از اساتید در خصوص مطالب درسی یا مشاوره ای سوال کنی و یه جواب خفن بگیری 😎

🔆 تازه میتونی از آرشیو بات کتاب و سوال بگیری و استفاده کنی 👽

🦅 @condor_lab
🦅 @CondorQbot'''

limited_text = "با سلام تعداد سوالاتی که میتوانید در روز از تیم کندرلب بپرسید به اتمام رسیده است. جهت جلوگیری از شلوغ شدن سوالاتی که بقیه دوستان ارسال میکنن و تسریع در فرایند پاسخ دهی لطفا سوال خود را فردا بپرسید"
banned_text = """با سلام 
به دلیل اختلالی که در فرایند عملکرد بات ایجاد کرده اید، تصمیم بر این شد که تا 24 ساعت از هر گونه فعالیت شما در بات جلوگیری شود. پس از سپری شدن این مدت میتوانید به روال سابق از بات استفاده کنید"""

pls_join = "لطفا برای استفاده از ربات در چنل عضو شوید"
join_button = [[InlineKeyboardButton("عضویت در چنل",url=join_link)]]

#user_list
limited_users_list = []
banned_users_list = []
banned = []

question_resource_slection_txt = "یکی از گزینه ها رو انتخاب کنید"

books_subject = [[InlineKeyboardButton("زیست شناسی عمومی",callback_data="bgb")]]

azm_talaha_buttons = []
for k in range(1,len(talaha_data_dict)-1,2):
    azm_talaha_buttons.append([InlineKeyboardButton("دوره "+str(list(talaha_data_dict.keys())[k]),callback_data="aztl"+str(list(talaha_data_dict.keys())[k])),
                               InlineKeyboardButton("دوره "+str(list(talaha_data_dict.keys())[k-1]),callback_data="aztl"+str(list(talaha_data_dict.keys())[k-1]))])
azm_talaha_buttons.append([InlineKeyboardButton("دوره 23 و 24",callback_data="aztl"+str(list(talaha_data_dict.keys())[-1]))])
azm_talaha_buttons.append([InlineKeyboardButton("برگشت",callback_data="rtnqzhome")])

other_country_buttons = []
for k in other_country_list:
    other_country_buttons.append([InlineKeyboardButton(k,callback_data=other_country_list[k])])
other_country_buttons.append([InlineKeyboardButton("برگشت",callback_data="rtnqzhome")])

subjects_books_button_list = dict()
for s in subjects_books_list:
    subjects_books_button_list[s] = list()
    for b in subjects_books_list[s]:
        subjects_books_button_list[s].append([InlineKeyboardButton(b,callback_data="lb"+str(books_message_id_dict[b]))])
    subjects_books_button_list[s].append([InlineKeyboardButton("برگشت",callback_data="rtrnbks")])

for i in range(len(question_subject_keyboard)-2):
    _mini_ = list()
    for j in question_subject_keyboard[i]:
        _mini_.append(InlineKeyboardButton(j,callback_data=book_subject_callback[j]))
    books_subject.append(_mini_)
books_subject.append([InlineKeyboardButton("آزمایشگاه",callback_data="bla"),InlineKeyboardButton("بیوانفورماتیک",callback_data="bin")])
books_subject.append([InlineKeyboardButton("برگشت",callback_data="rtnqzhome")])
question_books_and_manual_buttons = []
for k in question_books_and_manual_list:
    question_books_and_manual_buttons.append([InlineKeyboardButton(k,callback_data="lb"+str(books_message_id_dict[k]))])
question_books_and_manual_buttons.append([InlineKeyboardButton("برگشت",callback_data="rtnqzhome")])
start_keyboard = [[question_txt,help_txt],
                  [azmoon_txt,reference_book_txt],
                  [note_text,condorcat_text]]

question_resource_option = [[azm_step_2_txt,azm_step_1_txt],
                            [book_and_manual_txt,azm_ibo_txt],
                            [other_country_exams_txt,azm_talaha_txt],
                            [home_return_txt]]

question_finished_button = [[InlineKeyboardButton('پرسیدم',callback_data="q_done")],
                            [InlineKeyboardButton('لغو',callback_data="q_cancel")]]
m1_inlinebuttons = []
for i in range(1,24,2):
    m1_inlinebuttons.append([InlineKeyboardButton("دوره "+str(i),callback_data="M1_"+str(i)),InlineKeyboardButton("دوره "+str(i+1),callback_data="M1_"+str(i+1))])
m1_inlinebuttons.append([InlineKeyboardButton("دوره 25",callback_data="M1_25")])
m1_inlinebuttons.append([InlineKeyboardButton("برگشت",callback_data="rtnqzhome")])

m2_inlinebuttons = [[InlineKeyboardButton("دوره 1",callback_data="M2_1"),InlineKeyboardButton("دوره 3",callback_data="M2_3")]]
for i in range(4,26,2):
    m2_inlinebuttons.append([InlineKeyboardButton("دوره "+str(i),callback_data="M2_"+str(i)),InlineKeyboardButton("دوره "+str(i+1),callback_data="M2_"+str(i+1))])
m2_inlinebuttons.append([InlineKeyboardButton("برگشت",callback_data="rtnqzhome")])

ibo_inlinebuttons = [[InlineKeyboardButton("1990",callback_data="IBO_1990"),InlineKeyboardButton("1991",callback_data="IBO_1991")]]
for i in range(1993,2019,2):
    ibo_inlinebuttons.append([InlineKeyboardButton(str(i),callback_data="IBO_"+str(i)),InlineKeyboardButton(str(i+1),callback_data="IBO_"+str(i+1))])
ibo_inlinebuttons.append([InlineKeyboardButton("2020",callback_data="IBO_2020")])
ibo_inlinebuttons.append([InlineKeyboardButton("برگشت",callback_data="rtnqzhome")])

def get_gist_dict(url):
    user_id = url.split("/")[3]
    gist_id = url.split("/")[4]
    r = requests.get(url)
    text = r.text
    pattern = f'<a href=\"(\/{user_id}\/{gist_id}\/raw\/.+?)\"'
    raw_url = "https://gist.github.com" + re.findall(pattern,text)[0]
    r = requests.get(raw_url)
    text = r.text
    _json = json.loads(text)
    return _json

condorcast_dict = get_gist_dict(condorcast_url)
quiz_dict = get_gist_dict(quiz_url)
note_dict = get_gist_dict(note_url)

def generate_quiz_texts(_quiz_dict):
    if len(_quiz_dict) != 0:
        text_list = []
        number_of_quiz = 6
        counter = 0
        text = ""
        buttons_list = []
        _button = []
        for k in range(len(_quiz_dict)):
            if _quiz_dict[list(_quiz_dict.keys())[k]]['title'] != "":
                text += f"💠{k+1}.<b>{_quiz_dict[list(_quiz_dict.keys())[k]]['title']}</b>\n"
            if _quiz_dict[list(_quiz_dict.keys())[k]]['Q_num'] != "":
                text += f"تعداد سوالات:{_quiz_dict[list(_quiz_dict.keys())[k]]['Q_num']}\n"
            if _quiz_dict[list(_quiz_dict.keys())[k]]['subjects'] != []:
                _subjects = list(map(str.strip,_quiz_dict[list(_quiz_dict.keys())[k]]['subjects']))
                #_subjects = list(map(lambda s :s.replace(" ","_"),_subjects))
                _subjects = "، ".join(_subjects)
                text += f"موضوعات:{_subjects}\n"
            text += "\n"

            counter+=1
            if counter==number_of_quiz:
                text_list.append(text)
                #list(_quiz_dict.keys())[k]
                if number_of_quiz%2 == 0:
                    for i in range(0,number_of_quiz,2):
                        _button.append([InlineKeyboardButton('کوییز '+str(k-i+1),callback_data="quiz"+list(_quiz_dict.keys())[k-i]),
                                    InlineKeyboardButton('کوییز '+str(k-i-1+1),callback_data="quiz"+list(_quiz_dict.keys())[k-i-1])])
                elif number_of_quiz%2 != 0:
                    for i in range(0,number_of_quiz-1,2):
                        _button.append([InlineKeyboardButton('کوییز '+str(k-i+1),callback_data="quiz"+list(_quiz_dict.keys())[k-i]),
                                    InlineKeyboardButton('کوییز '+str(k-i-1+1),callback_data="quiz"+list(_quiz_dict.keys())[k-i-1])])
                    _button.append([InlineKeyboardButton('کوییز '+str(k-(number_of_quiz-1)+1),callback_data="quiz"+list(_quiz_dict.keys())[k-(number_of_quiz-1)])])
                    
                buttons_list.append(_button[::-1])
                counter = 0
                text = ""
                _button = []
                if k == list(_quiz_dict.keys())[-1]:
                    break
            if k == list(_quiz_dict.keys())[-1]:
                text_list.append(text)
                if (len(_quiz_dict)%number_of_quiz)%2 == 0:
                    for i in range(0,(len(_quiz_dict)%number_of_quiz),2):
                        _button.append([InlineKeyboardButton('کوییز '+str(k-i+1),callback_data="quiz"+list(_quiz_dict.keys())[k-i]),
                                    InlineKeyboardButton('کوییز '+str(k-i-1+1),callback_data="quiz"+list(_quiz_dict.keys())[k-i-1])])
                elif (len(_quiz_dict)%number_of_quiz)%2 != 0:
                    for i in range(0,(len(_quiz_dict)%number_of_quiz)-1,2):
                        _button.append([InlineKeyboardButton('کوییز '+str(k-i+1),callback_data="quiz"+list(_quiz_dict.keys())[k-i]),
                                    InlineKeyboardButton('کوییز '+str(k-i-1+1),callback_data="quiz"+list(_quiz_dict.keys())[k-i-1])])
                    _button.append([InlineKeyboardButton('کوییز '+str(k-((len(_quiz_dict)%number_of_quiz)-1)+1),callback_data="quiz"+list(_quiz_dict.keys())[k-((len(_quiz_dict)%number_of_quiz)-1)])])
                buttons_list.append(_button[::-1])
                counter = 0
                text = ""
        return (text_list,buttons_list)
    else:
        return ("در حال حاضر کوییزی در دسترس نمی باشد",[])

quiz_list,quiz_button_list = generate_quiz_texts(quiz_dict)

async def resend_message_handler(messages_list:list,bot,target_chat_id):
    #media group handler
    if len(messages_list) == 1:
        await bot.copy_message(chat_id=target_chat_id, from_chat_id=messages_list[0].chat.id, message_id=messages_list[0].message_id)
    else:
        i = 0
        while i < len(messages_list):
            if messages_list[i].media_group_id is not None:
                the_media_list = list()
                for j in range(i,len(messages_list)):
                    if (messages_list[j].media_group_id is None) or (messages_list[j].media_group_id != messages_list[i].media_group_id):
                        i = j - 1
                        break
                    if messages_list[j].photo is not None:
                        the_media_list.append(InputMediaPhoto(media=messages_list[j].photo[-1].file_id,caption=messages_list[j].caption))
                    elif messages_list[j].video is not None:
                        the_media_list.append(InputMediaVideo(media=messages_list[j].video[-1].file_id,caption=messages_list[j].caption))
                    elif messages_list[j].voice is not None:
                        the_media_list.append(InputMediaAudio(media=messages_list[j].voice[-1].file_id,caption=messages_list[j].caption))
                    elif messages_list[j].document is not None:
                        the_media_list.append(InputMediaDocument(media=messages_list[j].document[-1].file_id,caption=messages_list[j].caption))  
                await bot.send_media_group(chat_id=target_chat_id,media=the_media_list)
            else:
                await bot.copy_message(chat_id=target_chat_id, from_chat_id=messages_list[i].chat.id, message_id=messages_list[i].message_id)
            i+=1

async def user_data(user_id,bot):
    _channel_id = "@condor_lab" #real
    _user_ = await bot.get_chat_member(chat_id=_channel_id, user_id=user_id)
    _user_data_ = _user_.user
    text = f'telegram id: {_user_data_.id}\nfirst name: {_user_data_.first_name}\nlast name: {_user_data_.last_name}\nusername: '
    if _user_data_.username == None:
        text += f'{_user_data_.username}'
    else:
        text += f'@{_user_data_.username}'
    text += f'\n<a href="tg://user?id={user_id}">Profile</a>'
    return text

async def edit_message(_new_message,_user_id,_message_id,bot):
    new_text = ""
    if _new_message.text is not None:
        new_text = _new_message.text
    elif _new_message.caption is not None:
        new_text = _new_message.caption
    
    new_text = new_text.replace("/edit","")
    new_text = new_text.strip()
    
    the_media = None
    mode = "caption"
    new_caption = None

    if len(new_text) != 0:
        new_caption = new_text
    if _new_message.photo is not None and _new_message.photo != []:
        if type(_new_message.photo) is list:
            the_media = InputMediaPhoto(media=_new_message.photo[-1].file_id,caption=new_caption)
        elif type(_new_message.photo) is not list:
            the_media = InputMediaPhoto(media=_new_message.photo.file_id,caption=new_caption)
        mode = "media"
    elif _new_message.video is not None and _new_message.video != []:
        if type(_new_message.video) is list:
            the_media = InputMediaVideo(media=_new_message.video[-1].file_id,caption=new_caption)
        elif type(_new_message.video) is not list:
            the_media = InputMediaVideo(media=_new_message.video.file_id,caption=new_caption)
        mode = "media"
    elif _new_message.voice is not None and _new_message.voice != []:
        if type(_new_message.voice) is list:
            the_media = InputMediaAudio(media=_new_message.voice[-1].file_id,caption=new_caption)
        elif type(_new_message.voice) is not list:
            the_media = InputMediaAudio(media=_new_message.voice.file_id,caption=new_caption)
        mode = "media"
    elif _new_message.document is not None and _new_message.document != []:
        if type(_new_message.document) is list:
            the_media = InputMediaDocument(media=_new_message.document[-1].file_id,caption=new_caption)
        elif type(_new_message.document) is not list:
            the_media = InputMediaDocument(media=_new_message.document.file_id,caption=new_caption)
        mode = "media"
    
    if mode == "caption":
        try:
            await bot.edit_message_caption(chat_id=_user_id, message_id=_message_id,caption=new_text)
            return True
        except:
            await bot.edit_message_text(chat_id=_user_id, message_id=_message_id,text=new_text)
            return True
    elif mode == "media":
        try:
            await bot.edit_message_media(media=the_media, chat_id=_user_id, message_id=_message_id)
            return True
        except:
            await _new_message.reply_html(text="امکان ادیت کردن مدیا برای پیامی که مدیا ندارد وجود ندارد")
            return False

async def subscribing_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #banned user
    if update.message is not None:
        if update.message.chat.id in banned:
            raise ApplicationHandlerStop()
        elif str(update.message.chat.id) in banned_users_list:
            await update.message.reply_html(text=banned_text)
            raise ApplicationHandlerStop()
    elif update.callback_query is not None:
        if update.callback_query.message.chat.id in banned:
            raise ApplicationHandlerStop()
        elif str(update.callback_query.message.chat.id) in banned_users_list:
            await update.callback_query.message.reply_html(text=banned_text)
            raise ApplicationHandlerStop()
    
    _channel_id = "@condor_lab" #real
    _owner_ = await bot.get_chat_member(chat_id=_channel_id, user_id=owener_id)
    
    _user_id = ""
    if update.message is not None:
        _user_id = update.message.chat.id
        
    elif update.callback_query is not None:
        _user_id = update.callback_query.message.chat.id
    else:
        return not_joined
    
    if _owner_.status not in [ChatMember.ADMINISTRATOR,ChatMember.OWNER] and _user_id not in [owener_id,bussiness_id]:
        if update.message is not None:
            await update.message.reply_html(text="مشکلی پیش آمده لطفا به ادمین ها اطلاع دهید")
        elif update.callback_query is not None:
            await update.callback_query.message.reply_html(text="مشکلی پیش آمده لطفا به ادمین ها اطلاع دهید")
        await bot.send_message(chat_id = owener_id,text="از ادمین بودن درت آوردن")
        raise ApplicationHandlerStop()
    
    if int(_user_id)>0 and _user_id not in [owener_id,bussiness_id]:
        _chat_member = await bot.get_chat_member(chat_id=_channel_id, user_id=_user_id)
        can_use_list = [ChatMember.ADMINISTRATOR,
                        ChatMember.MEMBER,
                        ChatMember.OWNER]

        can_not_use_list = [ChatMember.BANNED,
                            ChatMember.LEFT,
                            ChatMember.RESTRICTED]

        if _chat_member.status in can_use_list:
            return joined
        elif _chat_member.status in can_not_use_list:
            if update.message is not None:
                await update.message.reply_html(text=pls_join,reply_markup=InlineKeyboardMarkup(join_button))
            elif update.callback_query is not None:
                await update.callback_query.message.reply_html(text=pls_join,reply_markup=InlineKeyboardMarkup(join_button))
            raise ApplicationHandlerStop()
    else:
        return joined

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"سلام {user.mention_html()} " + welcome_text,
        reply_markup=ReplyKeyboardMarkup(
            start_keyboard, one_time_keyboard=True,resize_keyboard=True)
    )
    
    user_data_text = await user_data(user_id=update.message.chat.id,bot=bot)
    
    await bot.send_message(chat_id = data_channel_id,text=user_data_text,parse_mode=constants.ParseMode.HTML)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(help_message)

async def question_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.message.chat.id) not in limited_users_list:
        context.user_data["q_messages"] = []
        await update.message.reply_html(
        rf"لطفا از گزینه ها یکی را انتخاب کنید",
        reply_markup=ReplyKeyboardMarkup(
            question_subject_keyboard, one_time_keyboard=True,resize_keyboard=True)
        )
        return q_option
    else:
        await update.message.reply_html(text=limited_text)
        return ConversationHandler.END

async def question_choose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text in subjects_check_list:
        context.user_data["q_subject"] = update.message.text
        await bot.send_message(chat_id = update.message.chat.id,text=ask_please_txt,reply_markup=InlineKeyboardMarkup(question_finished_button))
        return q_choose
    else:
        await update.message.reply_html(
        rf"لطفا از گزینه ها یکی را انتخاب کنید",
        reply_markup=ReplyKeyboardMarkup(
            question_subject_keyboard, one_time_keyboard=True,resize_keyboard=True)
        )
        return q_option      

async def return_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await bot.send_message(chat_id=update.message.chat.id,text=f'خب برگشتیم!',reply_markup=ReplyKeyboardMarkup(
            start_keyboard, one_time_keyboard=True,resize_keyboard=True))
    user_data = context.user_data
    if "q_subject" in user_data:
        del user_data["q_subject"]
    if "q_user_id" in user_data:
        del user_data["q_user_id"]
    if "q_messages" in user_data:
        del user_data["q_messages"]

    user_data.clear()
    return ConversationHandler.END

async def question_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["q_messages"].append(update.message)
    context.user_data["q_user_id"] = update.message.chat.id
    return q_text

async def question_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if len(context.user_data["q_messages"]) != 0:
        await resend_message_handler(messages_list=context.user_data["q_messages"],bot=bot,target_chat_id=main_group_id)
        last_q_message_id = context.user_data["q_messages"][-1].message_id
        _question_message = await bot.send_message(chat_id=main_group_id,text=f'!<code>{context.user_data["q_user_id"]}</code>-{last_q_message_id}\n#{context.user_data["q_subject"].replace(" ","_")}',parse_mode=constants.ParseMode.HTML)
        await bot.pin_chat_message(chat_id = main_group_id, message_id = _question_message.message_id, disable_notification=True)
        
        await update.callback_query.message.reply_text(q_done_txt,reply_markup=ReplyKeyboardMarkup(
            start_keyboard, one_time_keyboard=True,resize_keyboard=True))
        
        user_data = context.user_data
        if "q_subject" in user_data:
            del user_data["q_subject"]
        if "q_user_id" in user_data:
            del user_data["q_user_id"]
        if "q_messages" in user_data:
            del user_data["q_messages"]

        user_data.clear()
        return ConversationHandler.END
    
    elif len(context.user_data["q_messages"]) == 0:
        await bot.answer_callback_query(callback_query_id=update.callback_query.id,text="هنوز که سوالی نپرسیدی!",show_alert=True)

async def question_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.message.edit_text(text="کنسل شد.")
    await update.callback_query.message.reply_html(text="چطوری میتونم بهت کمک کنم",reply_markup=ReplyKeyboardMarkup(
            start_keyboard, one_time_keyboard=True,resize_keyboard=True))

    user_data = context.user_data
    if "q_subject" in user_data:
        del user_data["q_subject"]
    if "q_user_id" in user_data:
        del user_data["q_user_id"]
    if "q_messages" in user_data:
        del user_data["q_messages"]

    user_data.clear()
    return ConversationHandler.END

async def answer_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.reply_to_message.text is not None:
        if update.message.reply_to_message.text[0] == "$":
            user_id = re.findall(r'\$(\d+)',update.message.reply_to_message.text)[0]
            _answer_message_ = await bot.copy_message(chat_id=user_id, from_chat_id=update.message.chat.id, message_id=update.message.message_id)
            await bot.unpin_chat_message(chat_id=main_group_id, message_id=update.message.reply_to_message.message_id)
            await bot.send_message(chat_id=main_group_id, text=f'{user_id}-{_answer_message_.message_id}\nAnswer sent successfully.',reply_to_message_id=update.message.message_id)
        elif update.message.reply_to_message.text[0] == "!":
            if len(re.findall(r'(\d+)',update.message.reply_to_message.text)) == 2:
                user_id = re.findall(r'(\d+)',update.message.reply_to_message.text)[0]
                _message_id = re.findall(r'(\d+)',update.message.reply_to_message.text)[1]
                _q_subject_ = re.findall(r'(#.+)',update.message.reply_to_message.text)[0][1:]
                _answer_message_ = await bot.copy_message(chat_id=user_id, from_chat_id=update.message.chat.id, message_id=update.message.message_id,reply_to_message_id=_message_id)
                if  == "آتاتومی گیاهی":
                    _q_subject_ = "آناتومی گیاهی"
                _answer_message_button_ = [[InlineKeyboardButton('اشکالم رفع شد',callback_data="f"+str(update.message.message_id))],
                                           [InlineKeyboardButton('هنوز مشکلم بر طرف نشده',callback_data="_"+str(q_subject_tanslator[_q_subject_])+str(update.message.message_id))]]
                
                _check_message_ = await bot.send_message(chat_id=user_id,text="اشکالت بر طرف شد یا میخوای ادامه بدی؟",reply_markup=InlineKeyboardMarkup(_answer_message_button_))
                await bot.unpin_chat_message(chat_id=main_group_id, message_id=update.message.reply_to_message.message_id)
                await bot.send_message(chat_id=main_group_id, text=f'{user_id}-{_answer_message_.message_id}-{_check_message_.message_id}\nAnswer sent successfully.',reply_to_message_id=update.message.message_id)

async def question_finished_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _message_id_ = update.callback_query.data[1:]
    await update.callback_query.message.edit_text(text="از اینکه تونستم بهت کمک کنم خوشحال شدم")
    await bot.send_message(chat_id=main_group_id, text=f'اشکال رفع شد\nخیلی ممنونم',reply_to_message_id=_message_id_)

async def question_continue_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["a_m_id"] = update.callback_query.data[3:]
    context.user_data["a_c_subject"] = inv_q_subject_tanslator[update.callback_query.data[1:3]]
    context.user_data["a_c_list"] = []
    await update.callback_query.message.edit_text(text="باشه سوالت رو بپرس و بعد هم دکمه ی پرسیدم رو بزن\nاگر هم مشکلت رفع شده دکمه ی لغو رو بزن",reply_markup=InlineKeyboardMarkup(question_finished_button))
    return q_continue

async def question_continue_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["a_c_list"].append(update.message)

async def question_continue_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if len(context.user_data["a_c_list"]) != 0:
        await resend_message_handler(messages_list=context.user_data["a_c_list"],bot=bot,target_chat_id=main_group_id)
        last_q_message_id = context.user_data["a_c_list"][-1].message_id
        _question_message = await bot.send_message(chat_id=main_group_id,text=f'!<code>{update.callback_query.message.chat.id}</code>-{last_q_message_id}\n#{context.user_data["a_c_subject"]}',reply_to_message_id=context.user_data["a_m_id"],parse_mode=constants.ParseMode.HTML)
        await bot.pin_chat_message(chat_id = main_group_id, message_id = _question_message.message_id, disable_notification=True)
        
        await update.callback_query.message.reply_text(q_done_txt,reply_markup=ReplyKeyboardMarkup(
            start_keyboard, one_time_keyboard=True,resize_keyboard=True))
        
        user_data = context.user_data
        if "a_m_id" in user_data:
            del user_data["a_m_id"]
        if "a_c_subject" in user_data:
            del user_data["a_c_subject"]
        if "a_c_list" in user_data:
            del user_data["a_c_list"]

        user_data.clear()
        return ConversationHandler.END
    
    elif len(context.user_data["a_c_list"]) == 0:
        await bot.answer_callback_query(callback_query_id=update.callback_query.id,text="هنوز که سوالی نپرسیدی!",show_alert=True)

async def answer_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.reply_to_message.text is not None:
        if len(re.findall(r'(\d+)',update.message.reply_to_message.text)) in [2,3]:
            _user_id = re.findall(r'(\d+)',update.message.reply_to_message.text)[0]
            _message_id = re.findall(r'(\d+)',update.message.reply_to_message.text)[1]
            edit_result = await edit_message(_new_message=update.message,_user_id=_user_id,_message_id=_message_id,bot=bot)
            if edit_result:
                await update.message.reply_html(text="Edited successfully.",reply_to_message_id=update.message.message_id)

async def answer_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.reply_to_message.text is not None:
        if len(re.findall(r'(\d+)',update.message.reply_to_message.text)) in [2,3]:
            _user_id = re.findall(r'(\d+)',update.message.reply_to_message.text)[0]
            _message_id = re.findall(r'(\d+)',update.message.reply_to_message.text)[1]
            if len(re.findall(r'(\d+)',update.message.reply_to_message.text)) == 3:
                _check_message_id = re.findall(r'(\d+)',update.message.reply_to_message.text)[2]
                await bot.delete_message(chat_id=_user_id, message_id = _check_message_id)
            await bot.delete_message(chat_id=_user_id, message_id = _message_id)
            await update.message.reply_html(text="Deleted successfully.",reply_to_message_id=update.message.message_id)

async def send_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if len(re.findall(r'(\d+)',update.message.text)) == 1:
        user_id = re.findall(r'(\d+)',update.message.text)[0]
        _answer_message_ = await bot.copy_message(chat_id=user_id, from_chat_id=update.message.chat.id, message_id=update.message.reply_to_message.message_id)
        await update.message.reply_html(text=f'{user_id}-{_answer_message_.message_id}\nAnswer sent successfully.',reply_to_message_id=update.message.message_id)
    else:
        update.message.reply_html(text="لطفا شناسه ی فرد را درست وارد کنید")

async def pub_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await bot.copy_message(chat_id=public_group, from_chat_id=update.message.reply_to_message.chat.id, message_id=update.message.reply_to_message.message_id)
    await update.message.reply_html(text="Message was successfully publicized.",reply_to_message_id=update.message.message_id)
    
async def delete_pin_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.chat.id in [main_group_id,condor_spam_id,public_group]:
        await update.message.delete()

async def question_resource_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_html(text=question_resource_slection_txt,reply_markup=ReplyKeyboardMarkup(
            question_resource_option, one_time_keyboard=True,resize_keyboard=True))

async def m1_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_html(text="یکی از دوره ها رو برای مرحله یک انتخاب کنید",reply_markup=InlineKeyboardMarkup(m1_inlinebuttons))

async def m2_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_html(text="یکی از دوره ها رو برای مرحله دو انتخاب کنید",reply_markup=InlineKeyboardMarkup(m2_inlinebuttons))

async def ibo_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_html(text="یکی از سال ها رو انتخاب کن",reply_markup=InlineKeyboardMarkup(ibo_inlinebuttons))

async def m1_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _dore = int(update.callback_query.data.replace("M1_",""))
    await bot.copy_message(chat_id=update.callback_query.message.chat.id,from_chat_id=file_channel_id,message_id=irBO_step_one[_dore]["q"])
    await bot.copy_message(chat_id=update.callback_query.message.chat.id,from_chat_id=file_channel_id,message_id=irBO_step_one[_dore]["a"])

async def m2_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _dore = int(update.callback_query.data.replace("M2_",""))
    if irBo_step_two[_dore]["q"] is not None:
        await bot.copy_message(chat_id=update.callback_query.message.chat.id,from_chat_id=file_channel_id,message_id=irBo_step_two[_dore]["q"])
    if irBo_step_two[_dore]["a"] is not None:
        await bot.copy_message(chat_id=update.callback_query.message.chat.id,from_chat_id=file_channel_id,message_id=irBo_step_two[_dore]["a"])

async def ibo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _dore = int(update.callback_query.data.replace("IBO_",""))
    await bot.copy_message(chat_id=update.callback_query.message.chat.id,from_chat_id=file_channel_id,message_id=IBO_data_dict[_dore])

async def books_subject_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_html(text="لطفا یکی از موضاعات رو انتخاب کنید",reply_markup=InlineKeyboardMarkup(books_subject))

async def books_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    subject = inv_book_subject_callback[update.callback_query.data]
    books_buttons = subjects_books_button_list[subject]
    await update.callback_query.message.edit_text(text="لطفا یکی از کتاب های زیر رو انتخاب کنید",reply_markup=InlineKeyboardMarkup(books_buttons))

async def return_book_subject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.message.edit_text(text="لطفا یکی از موضاعات رو انتخاب کنید",reply_markup=InlineKeyboardMarkup(books_subject))

async def send_book_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.callback_query.data[:2] == "lb":
        _message_id = update.callback_query.data[2:]
        await bot.copy_message(chat_id=update.callback_query.message.chat.id,from_chat_id=file_channel_id,message_id=_message_id)
    elif update.callback_query.data[:3] == "ch_":
        _message_id = update.callback_query.data[3:]
        await bot.copy_message(chat_id=update.callback_query.message.chat.id,from_chat_id=channel_id,message_id=_message_id)
 
async def other_countries_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_html(text="لطفا یکی از گزینه ها رو انتخاب کنید",reply_markup=InlineKeyboardMarkup(other_country_buttons))

async def other_counteries_send_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    country = update.callback_query.data[2:]
    await bot.copy_message(chat_id=update.callback_query.message.chat.id,from_chat_id=file_channel_id,message_id=other_country_message_id[country])

async def talaha_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_html(text="لطفا یکی از گزینه ها رو انتخاب کنید",reply_markup=InlineKeyboardMarkup(azm_talaha_buttons))

async def talaha_send_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _dore = int(update.callback_query.data.replace("aztl",""))
    if talaha_data_dict[_dore]["q"] is not None:
        await bot.copy_message(chat_id=update.callback_query.message.chat.id,from_chat_id=file_channel_id,message_id=talaha_data_dict[_dore]["q"])
    if talaha_data_dict[_dore]["a"] is not None:
        await bot.copy_message(chat_id=update.callback_query.message.chat.id,from_chat_id=file_channel_id,message_id=talaha_data_dict[_dore]["a"])
        

async def question_books_and_manual_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_html(text="لطفا یکی از گزینه ها رو انتخاب کنید",reply_markup=InlineKeyboardMarkup(question_books_and_manual_buttons))

async def id_to_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.chat.id in [owener_id,bussiness_id]:
        the_id = update.message.text.replace("$id ","")
        user_data_text = await user_data(user_id=the_id,bot=bot)
        await bot.send_message(chat_id = update.message.chat.id,text=user_data_text,parse_mode=constants.ParseMode.HTML)

async def call_me_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _answers_ = ['جانم','بله','جان','چی شده']
    if update.message.text in [bot_name,bot_name+" جون"]:
        _answer_ = ['جوونم این همه مرام',"سلام به همه داش مشتی ها"]
        await update.message.reply_html(text=random.choice(_answer_),reply_to_message_id=update.message.message_id)
    else:
        if update.message["from"]["id"] not in [owener_id,bussiness_id]:
            await update.message.reply_html(text=random.choice(_answers_),reply_to_message_id=update.message.message_id)
        elif update.message["from"]["id"] in [owener_id,bussiness_id,sheyda_id]:
            await update.message.reply_html(text=random.choice(['جانم','جان']),reply_to_message_id=update.message.message_id)
            if update.message["from"]["id"] == sheyda_id:
                await update.message.forward(chat_id=owener_id)

async def i_am_tired(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _answers_ = ['خسته نباشی عزیزم','فدای خستگی هات بشم','منم خسته ام🥺','بیا بغلم🥲']
    await update.message.reply_html(text=random.choice(_answers_),reply_to_message_id=update.message.message_id)

async def i_am_sad(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _answers_ = ['تو ناراحت باشی دلم منم میگیره🥲',"چی حالت رو بهتر میکنه","بیا بغلم",'من دوست دارم ناراحت نباش','قربونتون برم مننن 🥹\nنبینم ناراحت باشیا','وقتی منو داری برا چی ناراحتی؟']
    await update.message.reply_html(text=random.choice(_answers_),reply_to_message_id=update.message.message_id)

async def how_are_you(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _answers_ = ['تو خوبی؟\nتا وقتی تو خوب باشی منم خوبم',"خوبم مرسی که پرسیدی",'خوبم تو حالت خوبه؟']
    if update.message["from"]["id"] not in [sheyda_id,owener_id,bussiness_id]:
        await update.message.reply_html(text=random.choice(_answers_),reply_to_message_id=update.message.message_id)
    elif update.message["from"]["id"] in [sheyda_id,owener_id,bussiness_id]:
        await update.message.reply_html(text='تو خوبی؟\nتا وقتی تو خوب باشی منم خوبم',reply_to_message_id=update.message.message_id)
    
async def admins_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await bot.copy_message(chat_id=update.message.chat.id,from_chat_id=archive_channel_id,message_id=70)

async def limit_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.text.replace("$limit ","")
    if user_id != str(owener_id) or user_id != str(bussiness_id):
        limited_users_list.append(user_id)
        await update.message.reply_html(text=f'user <code>{user_id}</code> limited successfully.',reply_to_message_id=update.message.message_id)
    elif user_id == str(owener_id) or user_id == str(bussiness_id):
        await update.message.reply_html(text="چه غلطا میخوای عرفان رو لیمیت کنی؟\nبرو تا خودت رو ساقط نکردم",reply_to_message_id=update.message.message_id)

async def unlimit_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.text.replace("$unlimit ","")
    if user_id in limited_users_list:
        del limited_users_list[limited_users_list.index(user_id)]
        await update.message.reply_html(text=f'user <code>{user_id}</code> unlimited successfully.',reply_to_message_id=update.message.message_id)
    elif user_id not in limited_users_list:
        await update.message.reply_html(text=f'این کاربر در لیست افراد لیمیت شده نمی باشد',reply_to_message_id=update.message.message_id)

async def limit_user_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _text = "\n".join(limited_users_list)
    if len(limited_users_list) != 0:
        _text = "\n".join(limited_users_list)
        await update.message.reply_html(text=_text,reply_to_message_id=update.message.message_id)
    elif len(limited_users_list) == 0:
        await update.message.reply_html(text="در حال حاضر کاربری در لیست لیمیت نیست",reply_to_message_id=update.message.message_id)

async def ban_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.text.replace("$ban ","")
    if user_id != str(owener_id) or user_id != str(bussiness_id):
        banned_users_list.append(user_id)
        await update.message.reply_html(text=f'user <code>{user_id}</code> banned successfully.',reply_to_message_id=update.message.message_id)
    elif user_id == str(owener_id) or user_id == str(bussiness_id):
        await update.message.reply_html(text="چه غلطا میخوای عرفان رو بن کنی؟\nبرو تا خودت رو ساقط نکردم",reply_to_message_id=update.message.message_id)

async def unban_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.text.replace("$unban ","")
    if user_id in banned_users_list:
        del banned_users_list[banned_users_list.index(user_id)]
        await update.message.reply_html(text=f'user <code>{user_id}</code> unbanned successfully.',reply_to_message_id=update.message.message_id)
    elif user_id not in banned_users_list:
        await update.message.reply_html(text=f'این کاربر در لیست افراد بن شده نمی باشد',reply_to_message_id=update.message.message_id)

async def ban_user_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if len(banned_users_list) != 0:
        _text = "\n".join(banned_users_list)
        await update.message.reply_html(text=_text,reply_to_message_id=update.message.message_id)
    elif len(banned_users_list) == 0:
        await update.message.reply_html(text="در حال حاضر کاربری در لیست بن نیست",reply_to_message_id=update.message.message_id)

async def poem_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass

async def admins_help_vid_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass

async def send_message_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _reply_to = None
    if "https://" in update.message.text:
        _reply_to = int(re.findall(r'(\d+)',update.message.text)[-1])
    await bot.copy_message(chat_id=public_group,from_chat_id=update.message.reply_to_message.chat.id,message_id=update.message.reply_to_message.message_id,reply_to_message_id=_reply_to)

async def quiz_first_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if len(quiz_dict) != 0:
        _buttons = [[InlineKeyboardButton("برگشت به منو اصلی",callback_data="rtnqzhome"),InlineKeyboardButton('صفحه بعد ▶️',callback_data="qzp1")]]
        if len(quiz_list) > 1:
            await bot.send_message(chat_id = update.message.chat.id,text=quiz_list[0],reply_markup=InlineKeyboardMarkup(quiz_button_list[0]+_buttons),parse_mode=constants.ParseMode.HTML)
        else:
            await bot.send_message(chat_id = update.message.chat.id,text=quiz_list[0],reply_markup=InlineKeyboardMarkup(quiz_button_list[0]+[[InlineKeyboardButton("برگشت به منو اصلی",callback_data="rtnqzhome")]]),parse_mode=constants.ParseMode.HTML)
    else:
        await bot.send_message(chat_id = update.message.chat.id,text=quiz_list[0],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("برگشت به منو اصلی",callback_data="rtnqzhome")]]),parse_mode=constants.ParseMode.HTML)
        
async def quiz_return_home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.message.delete()
    await bot.send_message(chat_id=update.callback_query.message.chat.id,text=f'خب برگشتیم!',reply_markup=ReplyKeyboardMarkup(
            start_keyboard, one_time_keyboard=True,resize_keyboard=True))

async def change_page_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    page = update.callback_query.data.replace("qzp","")
    _buttons = []
    if (len(quiz_list)-1) > int(page) and int(page) != 0:
        #add next and pre
        _buttons = [[InlineKeyboardButton('◀️صفحه قبل',callback_data="qzp"+str(int(page)-1)),InlineKeyboardButton('صفحه بعد ▶️',callback_data="qzp"+str(int(page)+1))],
         [InlineKeyboardButton("برگشت به منو اصلی",callback_data="rtnqzhome")]]
    elif (len(quiz_list)-1) > int(page) and int(page) == 0:
        #add next only
        _buttons = [[InlineKeyboardButton("برگشت به منو اصلی",callback_data="rtnqzhome"),InlineKeyboardButton('صفحه بعد ▶️',callback_data="qzp"+str(int(page)+1))]]
    elif (len(quiz_list)-1) == int(page) and int(page) != 0:
        #add pre only
        _buttons = [[InlineKeyboardButton('◀️صفحه قبل',callback_data="qzp"+str(int(page)-1)),InlineKeyboardButton("برگشت به منو اصلی",callback_data="rtnqzhome")]]
    
    await update.callback_query.message.edit_text(text=quiz_list[int(page)],reply_markup=InlineKeyboardMarkup(quiz_button_list[int(page)]+_buttons),parse_mode=constants.ParseMode.HTML)

async def quiz_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    quiz_id = update.callback_query.data.replace("quiz","")
    the_quiz = quiz_dict[quiz_id]
    _text = ""
    if the_quiz['title'] != "":
        _text += f"💠<b>{the_quiz['title']}</b>\n"
    if the_quiz['description'] != "":
        _text += f"توضیحات: {the_quiz['description']}\n"
    if the_quiz['subjects'] != []:
        _subjects = list(map(str.strip,the_quiz['subjects']))
        _subjects = list(map(lambda s :s.replace(" ","_"),_subjects))
        _subjects = "#"+" #".join(_subjects)
        _text += f"موضوعات: {_subjects}\n"
    if the_quiz['Q_num'] != "":
        _text += f"تعداد سوال: {the_quiz['Q_num']}\n"
    if the_quiz['time'] != "":
        _text += f"زمان: {the_quiz['time']}\n"
    _text+="🦅@condor_lab\n🤖@CondorQbot"
    _buttons = [[InlineKeyboardButton("شروع کوییز",url=the_quiz['link'])]]
    if the_quiz['banner'] != "":
        _message = await bot.copy_message(chat_id=update.callback_query.message.chat.id,from_chat_id=quiz_channel,message_id=the_quiz['banner'])
        await bot.edit_message_caption(chat_id=update.callback_query.message.chat.id,message_id=_message.message_id,caption=_text,reply_markup=InlineKeyboardMarkup(_buttons),parse_mode=constants.ParseMode.HTML)
    if the_quiz['banner'] == "":
        await update.callback_query.reply_html(text=_text,reply_markup=InlineKeyboardMarkup(_buttons),parse_mode=constants.ParseMode.HTML)

async def condorcast_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _button = []
    for k in condorcast_dict:
        _button.append([InlineKeyboardButton(k,callback_data="ch_"+str(condorcast_dict[k]))])
    _button.append([InlineKeyboardButton("برگشت",callback_data="rtnqzhome")])
    await update.message.reply_html(text="لطفا از کندرکست های زیر یکی را انتخاب کنید",reply_markup=InlineKeyboardMarkup(_button))

async def note_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _button = []
    for k in note_dict:
        _button.append([InlineKeyboardButton(note_dict[k]['title'],callback_data="nt_"+k)])
           
    _button.append([InlineKeyboardButton("برگشت",callback_data="rtnqzhome")])
    await update.message.reply_html(text="لطفا یکی از فایل ها را انتخاب کنید",reply_markup=InlineKeyboardMarkup(_button))
    
async def send_note_file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    note_id = update.callback_query.data.replace("nt_","")
    note_dict[note_id]['file_id']
    if note_dict[note_id]['explanation_id'] != "":
        _button = [[InlineKeyboardButton("توضیحات",callback_data="ch_"+str(note_dict[note_id]['explanation_id']))]]
        await bot.copy_message(chat_id=update.callback_query.message.chat.id,from_chat_id=channel_id,message_id=note_dict[note_id]['file_id'],reply_markup=InlineKeyboardMarkup(_button))
    else:
          await bot.copy_message(chat_id=update.callback_query.message.chat.id,from_chat_id=channel_id,message_id=note_dict[note_id]['file_id'])  
            
async def hasti_maram_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "بات بیا بریم پشت باغچه مرام کنیم"
    _answers_ = ["اگه بریم پشت باغچه باید زود جمش کنیم بیا بریم یه جای دیگه","🥺","به به","اگه حرف از مرامه من حاضرم",]
    await update.message.reply_html(text=random.choice(_answers_),reply_to_message_id=update.message.message_id)

async def random_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    rand_user = random.choice([owener_id,anita_id,fatemeh_id,hasti_id,danial_id,mohsen_id,nima_id,kia_id,mani_id,matin_id,arman_id,fallah_id])
    _user_ = await bot.get_chat_member(chat_id=condor_spam_id, user_id=rand_user)
    _user_data_ = _user_.user
    text = _user_data_.first_name
    if _user_data_.last_name is not None:
        text+= " "+_user_data_.last_name
    await update.message.reply_html(text=text,reply_to_message_id=update.message.message_id)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=bussiness_id, text=message, parse_mode=constants.ParseMode.HTML
    )
    
def main() -> None:
    # Create the Application and pass it your bot's token.
        
    application = ApplicationBuilder().token(TOKEN).build()

    #subscribe checking
    application.add_handler(TypeHandler(Update, callback=subscribing_check))
    
    application.add_handler(CommandHandler(command="start", callback=start,filters=filters.ChatType.PRIVATE),group=1)
    application.add_handler(CommandHandler(command="help", callback=help_command,filters=filters.ChatType.PRIVATE),group=1)
    
    #answer methods
    application.add_handler(MessageHandler(filters.COMMAND & filters.Chat(main_group_id) & filters.REPLY & ~filters.UpdateType.EDITED_MESSAGE & filters.Regex("/send"),send_answer),group=1)
    application.add_handler(MessageHandler(filters.Chat(main_group_id) & filters.REPLY & ~filters.UpdateType.EDITED_MESSAGE & (filters.Regex("/edit") | filters.CaptionRegex("/edit")),answer_edit),group=1)
    application.add_handler(MessageHandler(filters.COMMAND & filters.Chat(main_group_id) & filters.REPLY & ~filters.UpdateType.EDITED_MESSAGE & filters.Regex("/del"),answer_delete),group=1)
    application.add_handler(MessageHandler(filters.COMMAND & (filters.Chat(main_group_id) | filters.Chat([owener_id,bussiness_id])) & filters.REPLY & ~filters.UpdateType.EDITED_MESSAGE & filters.Regex("/pub"),pub_question),group=1)
    
    application.add_handler(MessageHandler((filters.Chat(main_group_id) | filters.Chat([owener_id,bussiness_id])) & filters.User(user_id=bot_admins) & ~filters.UpdateType.EDITED_MESSAGE & filters.Regex("^\$ban "),ban_user_handler),group=1)
    application.add_handler(MessageHandler((filters.Chat(main_group_id) | filters.Chat([owener_id,bussiness_id])) & filters.User(user_id=bot_admins) & ~filters.UpdateType.EDITED_MESSAGE & filters.Regex("^\$limit "),limit_user_handler ),group=1)
    application.add_handler(MessageHandler((filters.Chat(main_group_id) | filters.Chat([owener_id,bussiness_id])) & filters.User(user_id=bot_admins) & ~filters.UpdateType.EDITED_MESSAGE & filters.Regex("^\$unban "),unban_user_handler),group=1)
    application.add_handler(MessageHandler((filters.Chat(main_group_id) | filters.Chat([owener_id,bussiness_id])) & filters.User(user_id=bot_admins) & ~filters.UpdateType.EDITED_MESSAGE & filters.Regex("^\$unlimit "),unlimit_user_handler ),group=1)
    application.add_handler(MessageHandler((filters.Chat(main_group_id) | filters.Chat([owener_id,bussiness_id])) & filters.User(user_id=bot_admins) & ~filters.UpdateType.EDITED_MESSAGE & filters.Regex("^\$ban_list$"),ban_user_list_handler),group=1)
    application.add_handler(MessageHandler((filters.Chat(main_group_id) | filters.Chat([owener_id,bussiness_id])) & filters.User(user_id=bot_admins) & ~filters.UpdateType.EDITED_MESSAGE & filters.Regex("^\$limit_list$"),limit_user_list_handler),group=1)
    #application.add_handler(MessageHandler((filters.Chat(main_group_id) | filters.Chat([owener_id,bussiness_id])) & ~filters.UpdateType.EDITED_MESSAGE & filters.Regex("^شعر$"),),group=1)
    #live edit
    #application.add_handler(MessageHandler(filters.Chat(main_group_id) & filters.REPLY & filters.UpdateType.EDITED_MESSAGE,),group=1))
    #help
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & ~filters.UpdateType.EDITED_MESSAGE & filters.Regex(r'^'+help_txt+r'$'),help_command),group=1)
    #asking converstation
    question_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.ChatType.PRIVATE & ~filters.UpdateType.EDITED_MESSAGE & filters.Regex(r'^'+question_txt+r'$'),question_start)],
        states={
            q_option:[MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND & ~filters.UpdateType.EDITED_MESSAGE & ~filters.Regex(r'^'+home_return_txt+r'$'),question_choose)],
            q_choose:[MessageHandler(filters.ChatType.PRIVATE & ~filters.UpdateType.EDITED_MESSAGE & ~filters.COMMAND,question_handler)],
            q_text:[MessageHandler(filters.ChatType.PRIVATE & ~filters.UpdateType.EDITED_MESSAGE & ~filters.COMMAND,question_handler)],
            },fallbacks=[CallbackQueryHandler(callback=question_done,pattern="q_done"),
                         CallbackQueryHandler(callback=question_cancel,pattern="q_cancel"),
                         MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND & ~filters.UpdateType.EDITED_MESSAGE & filters.Regex(r'^'+home_return_txt+r'$'),return_to_main)])
    
    application.add_handler(question_conv_handler,group=1)
    #Question and answering
    application.add_handler(CallbackQueryHandler(callback=question_finished_handler,pattern="f"),group=1)
    question_conv_handler_2 = ConversationHandler(
        entry_points=[CallbackQueryHandler(callback=question_continue_start_handler,pattern="_")],
        states={
            q_continue:[MessageHandler(filters.ChatType.PRIVATE & ~filters.UpdateType.EDITED_MESSAGE & ~filters.COMMAND,question_continue_handler)]
            },fallbacks=[CallbackQueryHandler(callback=question_continue_done,pattern="q_done"),
                         CallbackQueryHandler(callback=question_cancel,pattern="q_cancel")])
    application.add_handler(question_conv_handler_2,group=1)
    #answering command
    application.add_handler(MessageHandler(filters.Chat(main_group_id) & ~filters.UpdateType.EDITED_MESSAGE & filters.REPLY,answer_command),group=1)
    #owner command id
    application.add_handler(MessageHandler(filters.Regex(r'\$id \d+') & filters.Chat([owener_id,bussiness_id]),id_to_profile),group=1)
    application.add_handler(MessageHandler(filters.Regex(r'/s') & ~filters.Regex("/send") & filters.Chat([owener_id,bussiness_id]),send_message_to_group),group=1)
    application.add_handler(MessageHandler(filters.Regex(r'^/س') & filters.Chat([owener_id,bussiness_id]),send_message_to_group),group=1)
    #handle question resource requests
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.Regex(r'^'+azmoon_txt+r'$') & ~filters.UpdateType.EDITED_MESSAGE & ~filters.COMMAND,question_resource_handler),group=1)
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND & ~filters.UpdateType.EDITED_MESSAGE & filters.Regex(r'^'+home_return_txt+r'$'),return_to_main),group=1)
    #handle the M1 files and requests
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.Regex(r'^'+azm_step_1_txt+r'$') & ~filters.UpdateType.EDITED_MESSAGE & ~filters.COMMAND,m1_list_handler),group=1)
    application.add_handler(CallbackQueryHandler(callback=m1_handler,pattern="M1_"),group=1)
    #handle the M2 files and requests
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.Regex(r'^'+azm_step_2_txt+r'$') & ~filters.UpdateType.EDITED_MESSAGE & ~filters.COMMAND,m2_list_handler),group=1)
    application.add_handler(CallbackQueryHandler(callback=m2_handler,pattern="M2_"),group=1)
    #handle the IBO files and requests
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.Regex(r'^'+azm_ibo_txt+r'$') & ~filters.UpdateType.EDITED_MESSAGE & ~filters.COMMAND,ibo_list_handler),group=1)
    application.add_handler(CallbackQueryHandler(callback=ibo_handler,pattern="IBO_"),group=1)
    #handle the Other countries file
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.Regex(r'^'+other_country_exams_txt+r'$') & ~filters.UpdateType.EDITED_MESSAGE & ~filters.COMMAND,other_countries_handler),group=1)
    application.add_handler(CallbackQueryHandler(callback=other_counteries_send_handler,pattern="oc"),group=1)
    #handle the azmoon talaha file
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.Regex(r'^'+azm_talaha_txt+r'$') & ~filters.UpdateType.EDITED_MESSAGE & ~filters.COMMAND,talaha_handler),group=1)
    application.add_handler(CallbackQueryHandler(callback=talaha_send_handler,pattern="aztl"),group=1)
    #handle the question books and manuals file
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.Regex(r'^'+book_and_manual_txt+r'$') & ~filters.UpdateType.EDITED_MESSAGE & ~filters.COMMAND,question_books_and_manual_handler),group=1)
    #remove "some message pinned" message
    application.add_handler(MessageHandler(filters.StatusUpdate.PINNED_MESSAGE,delete_pin_update),group=1)
    #Book subject handler
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.Regex(r'^'+reference_book_txt+r'$') & ~filters.UpdateType.EDITED_MESSAGE & ~filters.COMMAND,books_subject_handler),group=1)
    application.add_handler(CallbackQueryHandler(callback=books_name_handler,pattern="b"),group=1)
    application.add_handler(CallbackQueryHandler(callback=send_book_handler,pattern="lb"),group=1)
    application.add_handler(CallbackQueryHandler(callback=return_book_subject,pattern="rtrnbks"),group=1)
    #admins
    application.add_handler(CommandHandler(command="helpadmin",callback=admins_help_command,filters=filters.Chat(main_group_id)),group=1)
    application.add_handler(CommandHandler(command="helpadminvid",callback=admins_help_vid_command,filters=filters.Chat(main_group_id)),group=1)
    application.add_handler(MessageHandler((filters.User(user_id=bot_admins) | filters.Chat(bot_admins)) & filters.Chat(condor_spam_id) & (filters.Regex(r'^بات بیا بریم پشت باغچه مرام کنیم$')),hasti_maram_handler),group=1)
    application.add_handler(MessageHandler((filters.User(user_id=bot_admins) | filters.Chat(bot_admins)) & filters.Chat(condor_spam_id) & (filters.Regex(r'^رندم$')|filters.Regex(r'^/random$')),random_handler),group=1)
    application.add_handler(MessageHandler((filters.User(user_id=bot_admins) | filters.Chat(bot_admins)) & (filters.Regex(r'^ربات$')|filters.Regex(r'^بات$')|filters.Regex(f'^{bot_name}$')|filters.Regex(f'^{bot_name} جون$')),call_me_bot),group=1)
    application.add_handler(MessageHandler((filters.User(user_id=bot_admins) | filters.Chat(bot_admins)) & (filters.Regex(r'^خیلی خسته ام$')|filters.Regex(r'^خستمه$')|filters.Regex(r'^خستم$')|filters.Regex(r'^خسته ام$')|filters.Regex(r'^خیلی خستم$')),i_am_tired),group=1)
    #i_am_sad
    application.add_handler(MessageHandler((filters.User(user_id=bot_admins) | filters.Chat(bot_admins)) & (filters.Regex(r'^ناراحتم$')|filters.Regex(r'^خیلی ناراحتم$')),i_am_sad),group=1)
    application.add_handler(MessageHandler((filters.User(user_id=bot_admins) | filters.Chat(bot_admins)) & (filters.Regex(r'^ربات خوبی$')|filters.Regex(r'^بات خوبی$')|filters.Regex(r'^بات چطوری$')|filters.Regex(r'^ربات چطوری$')|filters.Regex(r'^ربات حالت چطوره$')|filters.Regex(r'^بات حالت چطوره$')),how_are_you),group=1)
    
    #quiz handlers                                                                                                      
    #application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.Regex(r'^'+quiz_text+r'$') & ~filters.UpdateType.EDITED_MESSAGE & ~filters.COMMAND,quiz_first_message_handler),group=1)
    application.add_handler(CallbackQueryHandler(callback=quiz_return_home,pattern="rtnqzhome"),group=1) #don't comment this
    #application.add_handler(CallbackQueryHandler(callback=change_page_quiz,pattern="qzp"),group=1)
    #application.add_handler(CallbackQueryHandler(callback=quiz_detail_handler,pattern="quiz"),group=1)
    #application.add_handler(MessageHandler(filters.COMMAND & filters.ChatType.PRIVATE & ~filters.UpdateType.EDITED_MESSAGE & filters.Regex(r'^'+"\/quiz\d+"+r'$'),quiz_detail_handler),group=1)
    #condorcast & CondorText 
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.Regex(r'^'+condorcat_text+r'$') & ~filters.UpdateType.EDITED_MESSAGE & ~filters.COMMAND,condorcast_handler),group=1)
    application.add_handler(CallbackQueryHandler(callback=send_book_handler,pattern="ch_"),group=1)
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.Regex(r'^'+note_text+r'$') & ~filters.UpdateType.EDITED_MESSAGE & ~filters.COMMAND,note_handler),group=1)
    application.add_handler(CallbackQueryHandler(callback=send_note_file_handler,pattern="nt_"),group=1)
    #erro handler 
    application.add_error_handler(error_handler) #real
    #~filters.UpdateType.EDITED_MESSAGE & 
    # Run the bot until the user presses Ctrl-C
    application.run_polling()
    # PORT = int(os.environ.get('PORT', '8443'))
    # #add handlers
    # application.run_webhook(
    #     listen="0.0.0.0",
    #     port=PORT,
    #     url_path=TOKEN,
    #     webhook_url="https://condorqbot.herokuapp.com/" + TOKEN
    # )

if __name__ == "__main__":
    main()
