import asyncio
import imaplib
import email
from email.header import decode_header
import base64
import dateutil
import re

from channels.db import database_sync_to_async
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()
from .models import File, EmailFile, Email, User

@database_sync_to_async

def save_email(login, subject, received_date, sent_date, text, files, filenames) -> int:
    user = User.objects.get(login__exact=login)
    print(user)
    email = Email(theme=subject, date_of_dispatch=sent_date,
                  date_of_receive=received_date, description=" ".join(text), user=user, files=' '.join(filenames))
    email.save()
    for i in range(len(files)):
        file = File(file=files[i], filename=filenames[i], email=email)
        file.save()
    return email.pk
@database_sync_to_async
def get_from_email(message) -> dict:
    email = Email.objects.get(pk=message['pk'])
    dct = {"theme": email.theme, "date_of_dispatch": email.date_of_dispatch,
           "date_of_receive": email.date_of_receive,
           "text": email.description,
           "filenames": email.files, "count": message["count"], "index": message["index"]}
    print(dct)
    return dct


async def parse_message(mail_pass: str, login: str, mail_name: str):
    imap_server = f"imap.{mail_name}"
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(login, mail_pass)
    imap.select()

    uids = imap.uid('search', "UNSEEN", "ALL")

    uids = uids[1][0].decode("utf-8").split(" ")

    count = len(uids)
    i = 0
    for uid in uids:
        if i == 25:
            break
        res, msg = imap.uid('fetch', uid.encode(), '(RFC822)')  # Для метода uid
        msg = email.message_from_bytes(msg[0][1])

        sent_date_str = msg["Date"]
        sent_date = dateutil.parser.parse(sent_date_str)

        received_str = msg["Received"]
        received_date_str = re.search(r'; (.*)', received_str).group(1)
        received_date = dateutil.parser.parse(received_date_str)

        subject = msg["Subject"]
        if subject is not None:
            try:
                subject = decode_header(msg["Subject"])[0][0].decode()
            except Exception as e:
                pass

        print(subject)
        text = []
        for part in msg.walk():
            if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                try:
                    text.append(base64.b64decode(part.get_payload()).decode(encoding="utf8"))
                except Exception as e:
                    print(e)

        filenames = []
        files = []
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                try:
                    filenames.append(decode_header(part.get_filename())[0][0].decode())
                except Exception as e:
                    pass
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                file_content = part.get_payload(decode=True)
                binary_data = bytearray(file_content)

                files.append(binary_data)
        pk=await save_email(subject=subject, sent_date=sent_date,
                         received_date=received_date, text=" ".join(text), login=login, files=files,
                         filenames=filenames)
        await asyncio.sleep(1)
        print(pk)
        # Convert  datetime datetime to str
        i += 1

        dct = {"pk":pk,"count": count, "index": i}

        cleaned_login = re.sub('[^a-zA-Z0-9_.-]', '_', login)

        await channel_layer.group_send(cleaned_login, {
            "type": "send.messages",
            "message": dct
        })
        print(11)
        count -= 1
