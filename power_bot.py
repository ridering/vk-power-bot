import io
import json
import mimetypes
import os
import random
import re

import vk_api
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, DEFAULT_CHUNK_SIZE
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

load_dotenv()

dats = {
    "type": "service_account",
    "project_id": os.environ.get('project_id'),
    "private_key_id": os.environ.get('private_key_id'),
    "private_key": os.environ.get('private_key'),
    "client_email": os.environ.get('client_email'),
    "client_id": os.environ.get('client_id'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ.get('client_x509_cert_url')
}

with open('datum.json', encoding='UTF-8', mode='w') as datum:
    json.dump(dats, fp=datum, ensure_ascii=False, indent=2)

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'datum.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

folder_id = '1N_joe7WdtyRuu_v_3FP-yaK5WMGAqkfO'


class Upload(MediaIoBaseUpload):
    def __init__(
            self, filename, data, mimetype=None, chunksize=DEFAULT_CHUNK_SIZE, resumable=False
    ):
        self._filename = filename
        fd = io.BytesIO(data.encode('utf-8'))
        if mimetype is None:
            mimetype, _ = mimetypes.guess_type(filename)
            if mimetype is None:
                mimetype = "application/octet-stream"
        super(Upload, self).__init__(
            fd, mimetype, chunksize=chunksize, resumable=resumable
        )

    def __del__(self):
        pass


def send(name, num):
    file_path = 'power.txt'
    file_metadata = {
        'name': name,
        'parents': [folder_id]
    }
    media = Upload(file_path, str(num), resumable=True)
    r = service.files().create(body=file_metadata, media_body=media,
                               fields='id').execute()


def main():
    with open('vip-users.json', encoding='UTF-8', mode='r') as users:
        vip = json.load(users)["users"]

    vk_session = vk_api.VkApi(token=os.environ.get('token'))

    longpoll = VkBotLongPoll(vk_session, os.environ.get('num'))

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            user_id = event.obj.message['from_id']
            message = event.obj.message['text'].replace(' ', '')
            message = re.split('\*\*|\^', message)
            try:
                base, power = [int(message[0]), int(message[1])]

                if user_id in vip:
                    if base == 2 and power % 100000000 == 0:
                        if power == 500000000:
                            with open('2^400000000.txt', mode='r') as four_hundred_mil:
                                with open('2^100000000.txt', mode='r') as one_hundred_mil:
                                    num = int(four_hundred_mil.read()) * int(one_hundred_mil.read())
                        elif power == 1000000000:
                            with open('2^400000000.txt', mode='r') as four_hundred_mil:
                                with open('2^200000000.txt', mode='r') as two_hundred_mil:
                                    four = int(four_hundred_mil.read())
                                    num = four * four * int(two_hundred_mil.read())
                        else:
                            with open('2^100000000.txt', mode='r') as one_hundred_mil:
                                num = int(one_hundred_mil.read()) ** (power // 100000000)
                    else:
                        num = base ** power

                    send(f'{base}^{power}.txt', num)
                    vk.messages.send(user_id=user_id,
                                     message='Готово',
                                     random_id=random.randint(0, 2 ** 64))
                else:
                    if base > 10000 or power > 10000:
                        vk.messages.send(user_id=user_id,
                                         message='У Вас нет доступа к операциям '
                                                 'с такими числами.\n'
                                                 'Ваш лимит: 10000^10000',
                                         random_id=random.randint(0, 2 ** 64))
                    else:
                        num = base ** power
                        send(f'{base}^{power}.txt', num)
                        vk.messages.send(user_id=user_id,
                                         message='Готово',
                                         random_id=random.randint(0, 2 ** 64))

            except Exception:
                vk.messages.send(user_id=user_id,
                                 message='Некорректный ввод\n'
                                         'Ну или ошибка сервера',
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
