import json
# from utils.chatgpt import *


# external imports
import re
from typing import Dict, List, Tuple
from colorama import Fore, Style

"""
this file contains functions for generating strings
"""
def now() -> str:
	"""
	returns a string formatted as YYYYMMDD-HHmmSS (Year, Month, Day, Hour, Minute, Second in order)
	"""

	from datetime import datetime
	return datetime.now().strftime('%Y%m%d-%H%M%S')

def clean_multiline(text: str) -> str:
	"""
	removes unwanted tabs and returns from a multiline string
	"""
	text = re.sub('\n *', '\n', text)
	text = re.sub('\n\t*', '\n', text)
	return text.strip('\n')

def replace_slot(text: str, entries: str) -> str:
    for key, value in entries.items():
        if not isinstance(value, str):
            value = str(value)
        text = text.replace("{{" + key +"}}", value.replace('"', "'").replace('\n', ""))
    return text

def remove_tilde(text: str) -> str:
    return text.split('```')[1] 

def extract_yamls(text: str) -> List:
    yaml_blocks = []
    pattern = re.compile(r'```(.*?)```', re.DOTALL)
    matches = pattern.findall(text)
    for match in matches:
        yaml_blocks.append(match.strip())
    return yaml_blocks

def white_space_trail(msg: str) -> List[str]:
    """
    split but keep trailing whitespace at the end of each word

    :param msg:
    :type str:

    :return: list of split tokens
    :rtype: str
    """
    return  re.findall(r'\S+\s*', msg)


#################################################################
### this section contains repetitive colored string functions ###
#################################################################
def green(msg: str):
    """
    returns a given string in green text
    """
    return Fore.GREEN + msg + Style.RESET_ALL

def red(msg: str):
    """
    returns a given string in red text
    """
    return Fore.RED + msg + Style.RESET_ALL

def yellow(msg: str):
    """
    returns a given string in yellow text
    """
    return Fore.YELLOW + msg + Style.RESET_ALL

def blue(msg: str):
    """
    returns a given string in blue text
    """
    return Fore.BLUE + msg + Style.RESET_ALL

def cyan(msg: str):
    """
    returns a given string in cyan text
    """
    return Fore.CYAN + msg + Style.RESET_ALL

def magenta(msg: str):
    """
    returns a given string in magenta text
    """
    return Fore.MAGENTA + msg + Style.RESET_ALL


def replace_slot(text, entries):
    for key, value in entries.items():
        if not isinstance(value, str):
            value = str(value)
        text = text.replace("{{" + key +"}}", value.replace('"', "'").replace('\n', ""))
    return text

def convert_messages_to_string(messages, config):
    str_msg = ""
    for message in messages:
        if message['role'] == 'user':
            str_msg += f"{message['role']}: {message['content']}\n"
        else:
            msg = message['content']
            str_msg += f"\n {message['role']}: {msg}\n"
    return str_msg

def is_json(string):
    try:
        json_object = json.loads(string)
    except ValueError:
        return False
    return True

def get_json(string):
    try:
        json_obj = json.loads(string)
    except ValueError:
        return None
    
    return json_obj

def petel_completed(slot_values):
    # json_obj = json.loads(slot_values)
    if 'None' in str(slot_values):
        return False
    else:
        return True
    
    
def intent_detected(intent_str='chitchat', config=None):
    return intent_str in config["intent_list"]

