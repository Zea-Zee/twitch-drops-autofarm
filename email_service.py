import os
import time
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv


load_dotenv()
IMAP_SERVER = "imap.gmail.com"
EMAIL_ADRESS = "thedarknessprince1997@gmail.com"
PASSWORD = os.getenv('GMAIL_PASS')
SENDER = "Twitch <no-reply@twitch.tv>"  # twitch email adress


def get_confirmation_code(email_addr: str) -> str:
    confirmation_code = None
    try:
        imap = imaplib.IMAP4_SSL(IMAP_SERVER)
        imap.login(EMAIL_ADRESS, PASSWORD)

        imap.select("INBOX")
        result, data = imap.uid(
            "search", None, f"(ALL HEADER To \"{email_addr}\")")
        email_uids = data[0].split()
        if not email_uids:
            print("No emails found.")
        else:
            for uid in email_uids:
                uid = uid.decode('utf-8')
                # print(uid)
                result, msg_data = imap.uid('fetch', str(uid), '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])
                recipient = decode_header(msg["To"])[0][0]
                sender = decode_header(msg["From"])[0][0]
                subject = decode_header(msg["Subject"])[0][0].decode()
                if sender != SENDER or recipient != email_addr or not subject:
                    continue
                confirmation_code = ''.join(
                    char for char in subject if char.isdigit())
                # print(recipient, sender, subject, confirmation_code, sep='\n')

    except imaplib.IMAP4.error as e:
        print(f"IMAP error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            imap.logout()
        except Exception as e:
            print(f"imap.logout unsucessful: {e}")

    if not confirmation_code:
        print("No confirmation code, we will try after 5 seconds")
        time.sleep(5)
        return get_confirmation_code(email_addr)


if __name__ == "__main__":
    print(get_confirmation_link("thed.arknessprince1997@gmail.com"))
