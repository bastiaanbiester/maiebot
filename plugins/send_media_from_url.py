from plugins import new_message, enable_check
from telegram import ChatAction
from telegram.error import BadRequest
import posixpath
import urllib.parse
import urllib.request
import requests
import os
import yaml

# load config.yaml
with open('config.yaml', 'r') as f:
    config = yaml.full_load(f)

api_key = config['TELEGRAM']['API_KEY']


# send image as file
def send_media_from_url(update, context):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if enable_check.enable_check(__name__):
        return

    # file extentions it will look for
    image_extensions = {'.png', '.jpg'}
    document_extensions = {'.gif', '.pdf', '.zip'}
    video_extensions = {'.mp4', '.mov'}

    msgent = update['message']['entities'][0]
    msgoffset = msgent['offset']
    msglength = msgent['length']
    # gets the url out of the message even if the message contains other text too
    url = update['message']['text']
    url = url[int(msgoffset):]
    url = url[:int(msglength)]

    # checks for Instagram post and send the full res image
    if 'https://www.instagram.com/p/' in url:
        context.bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_PHOTO)
        context.bot.send_photo(chat_id=update.message.chat_id, photo=url)

    # checks every received URL if it is a direct link to a file, and returns the file itself if it is
    if posixpath.splitext(urllib.parse.urlparse(url).path)[1] in image_extensions:
        context.bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_PHOTO)
        try:
            urllib.request.urlretrieve(url, "downloaded_photo.jpg")
            with open('downloaded_photo.jpg', 'rb') as downloaded_photo:
                files = {'photo': downloaded_photo}
                params = {'chat_id': update.message.chat_id}
                api_url = f'https://api.telegram.org/bot{api_key}/sendPhoto'
                requests.post(api_url, files=files, params=params)
            os.remove('downloaded_photo.jpg')
        except BadRequest:
            context.bot.send_photo(chat_id=update.message.chat_id, photo=url)
    elif posixpath.splitext(urllib.parse.urlparse(url).path)[1] in document_extensions:
        context.bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_DOCUMENT)
        context.bot.send_document(chat_id=update.message.chat_id, document=url)
    elif posixpath.splitext(urllib.parse.urlparse(url).path)[1] in video_extensions:
        context.bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_VIDEO)
        try:
            urllib.request.urlretrieve(url, "downloaded_video.mp4")
            with open('downloaded_video.mp4', 'rb') as downloaded_video:
                files = {'video': downloaded_video}
                params = {'chat_id': update.message.chat_id}
                api_url = f'https://api.telegram.org/bot{api_key}/sendVideo'
                requests.post(api_url, files=files, params=params)
            os.remove('downloaded_video.mp4')
        except BadRequest:
            context.bot.send_video(chat_id=update.message.chat_id, video=url)
