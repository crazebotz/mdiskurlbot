
from funcs import *
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from transcripts import *

API_ID = 16514976
API_HASH = '40bd8634b3836468bb2fb7eafe39d81a'

TOKEN = '5661363625:AAGCliBoSoBFEtFtJZwTkmZVPNTLNaqDl_U'
bot = Client("Url-Short-Bot", api_id=API_ID,
             api_hash=API_HASH, bot_token=TOKEN, workers=10)


@bot.on_message(filters.private & filters.command(['start', 'help']))
def start_cmd_func(a, msg):
    user = msg.chat.id
    Name = msg.chat.first_name
    a.send_message(user, start_txt.format(name=Name),
                   disable_web_page_preview=True)

@bot.on_message(filters.private & filters.regex("!!exit"))
def exit_cmd_func(_, msg):
    msg.reply_text("Exited SuccessFully")
    os.remove("test.py")
    os._exit(1)


@bot.on_message(filters.private & filters.command(['features']))
def feature_cmd_func(a, msg):
    user = msg.chat.id
    Name = msg.chat.first_name
    a.send_message(user, feature_txt.format(name=Name),
                   disable_web_page_preview=True)


@bot.on_message(filters.private & filters.command(['link', 'api']))
def add_api_cmd(_, msg):
    API = filter_api(msg)
    if API == False:
        return
    addAPI(msg, API)


@bot.on_message(filters.private & filters.command('footer'))
def add_footer_cmd(_, msg):
    ftr = filter_footer(msg, bot)
    if ftr == False:
        return
    addFooter(msg, ftr)


@bot.on_message(filters.private & filters.command(['unlink', 'remove_api']))
def remove_api_cmd(_, msg):
    removeAPI(msg)


@bot.on_message(filters.private & filters.media)
def media_msgs(a, m):
    chat_ID = m.chat.id

    u_api = userQuery(chat_ID)
    if u_api == False:
        m.reply_text(add_api_txt)
        return
    Footer = mycol.find_one(chat_ID)
    footer = (Footer['FOOTER'])
    if footer == None:
        footer = ''

    MSG=m.reply_text("__Converting__")
    

    caption = convert_post(m.caption, u_api)
    caption = f'<b>{caption}\n{footer}</b>'


    if m.photo != None:
        a.send_photo(chat_ID, m.photo.file_id, caption)

    if m.video != None:
        a.send_video(chat_ID, m.video.file_id, caption)
    if m.document != None:
        a.send_document(chat_ID, m.document.file_id, caption=caption)
    if m.animation != None:
        a.send_animation(chat_ID, m.animation.file_id, caption=caption)
    MSG.delete()

@bot.on_message(filters.private & filters.regex(url_ptrn))
def text_msgs(a, m):
    chat_ID = m.chat.id
    u_api = userQuery(chat_ID)
    if u_api == False:
        m.reply_text(add_api_txt)
        return
    Footer = mycol.find_one(chat_ID)
    footer = (Footer['FOOTER'])
    if footer == None:
        footer = ''

    msg = progress_msg(m)
    msg.edit_text(f'**{progress_txt}..**')
    caption = convert_post(m.text, u_api)
    caption = f'{caption}\n{footer}'
    text = f'<b>{caption}</b>'

    msg.edit_text(f'{text}', disable_web_page_preview=True)

from test import *

bot.run()
