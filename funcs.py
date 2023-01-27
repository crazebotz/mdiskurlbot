# funcs
import re
import time

import requests as rq
# from unshortenit import UnshortenIt
from transcripts import *
import pymongo

DB_URL = "mongodb+srv://mdisk:mdisk@cluster0.5f5kz5s.mongodb.net/?retryWrites=true&w=majority"

# URL Shortner
SHORT_API = '011fa9d202238764f8c23e300e6a8bb37b526271'

REAL_URL = 'https://mdiskshortners.in/api?'
url_ptrn = r'https?://[^\s]+'

# -----------------------------
myclient = pymongo.MongoClient(DB_URL)
mydb = myclient["mdiskdata"]
mycol = mydb["users"]


def userQuery(USER):
    user = mycol.find_one(USER)
    TYPE = str(type(user))
    if TYPE != "<class 'NoneType'>":
        U_API = (user['API'])
        return U_API
    else:
        return False


def filter_api(msg):
    ptn = r'[a-z0-9]{35,43}'
    try:
        user_api = re.findall(ptn, msg.text)[0]
        return user_api

    except:
        msg.reply_text(un_suc_text)
        return False


def addAPI(MSG, API):
    USER_ID = MSG.from_user.id
    RESULT = userQuery(USER_ID)
    if RESULT != False:
        return
    USER_NAME = MSG.from_user.first_name
    mydict = {"_id": USER_ID, "name": USER_NAME, "API": API, 'FOOTER': None}
    try:
        mycol.insert_one(mydict)
        MSG.reply_text(suc_txt)
    except:
        pass


def filter_footer(msg, a):
    user = msg.chat.id
    NAAM = msg.chat.first_name
    msg_list = msg.text.split(' ')
    if (len(msg_list)) < 2:
        a.send_message(user, footer_txt.format(name=NAAM),
                       disable_web_page_preview=True)
        return False
    else:
        msg_list.remove(msg_list[0])
        footer = ' '.join(msg_list)
        return footer


def addFooter(MSG, Footer):
    USER_ID = MSG.from_user.id
    RESULT = userQuery(USER_ID)
    if RESULT == False:
        MSG.reply_text(
            """You have to /link your Mdiskshortners.in account first.\nHit 👉 /help to know more...""")

    myquery = {"_id": USER_ID}
    newvalues = {"$set": {"FOOTER": Footer}}
    try:
        mycol.update_one(myquery, newvalues)
        MSG.reply_text("Hurrey!! Footer added successfully.")
    except:
        pass


def removeAPI(MSG):
    USER_ID = MSG.from_user.id
    myquery = {"_id": USER_ID}
    mycol.delete_one(myquery)
    MSG.reply_text(
        "<b>Account Unlinked Sucessfully✅</b>\n\n<i>Hit... /link to link again...</i>")


def short_urls(url_list, URL_API=SHORT_API):
    cnvt_urls = []
    for link in url_list:

        # if ('bit' in link ):
        #		      unshortener = UnshortenIt()
        #		      link = unshortener.unshorten(link)

        param = {'api': URL_API, 'url': link}
        try:
            res = (rq.get(REAL_URL, params=param))
        # res=(rq.get(r_url.format(r_token,link)))
            data = dict(res.json())
            link = data['shortenedUrl']
            cnvt_urls.append(link)

        except ConnectionResetError:
            cnvt_urls.append("Failed To Convert")
    
            
        except BaseException as ex:
            cnvt_urls.append(link)

    return cnvt_urls


def filter_tele_urls(urls):
    f_urls = []
    for link in urls:
        if 't.me' in link:
            pass
        else:
            f_urls.append(link)
    return f_urls


def convert_post(msg_text, Api):

    # msg_text=msg_text.text
    list_string = msg_text.splitlines()
    msg_text = ' \n'.join(list_string)
    new_msg_text = list(map(str, msg_text.split(" ")))
    new_join_str = "".join(new_msg_text)

    urls = re.findall(url_ptrn, new_join_str)
    urls = filter_tele_urls(urls)

    nml_len = len(new_msg_text)
    u_len = len(urls)
    url_index = []
    count = 0
    for i in range(nml_len):
        for j in range(u_len):
            if (urls[j] in new_msg_text[i]):
                url_index.append(count)
        count += 1
    new_urls = short_urls(urls,URL_API=Api)
    url_index = list(dict.fromkeys(url_index))
    i = 0

    for j in url_index:
        new_msg_text[j] = new_msg_text[j].replace(urls[i], new_urls[i])
        i += 1
    caption = " ".join(new_msg_text)
    return caption

# progress bar Funciton


def progress_msg(m):
    msg = m.reply_text(progress_txt)
    return msg
