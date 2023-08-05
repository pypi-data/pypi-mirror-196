#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    llmapi-cli
    
    LLMApi is OpenAPI for Large Language Models

    :date:      02/22/2023
    :author:    llmapi <llmapi@163.com>
    :homepage:  https://github.com/llmapi/
    :license:   MIT, see LICENSE for more details.
    :copyright: Copyright (c) 2023 llmapi. All rights reserved
"""
from threading import Thread
import sys
import json
import os
import argparse as ap
from argparse import RawTextHelpFormatter
import getpass
import requests
import time

__name__ = 'llmapi'
__version__ = '1.0.7'
__description__ = 'Do you want to talk directly to the LLMs? Try llmapi.'
__keywords__ = 'LLM OpenAPI LargeLanguageModel GPT3 ChatGPT'
__author__ = 'llmapi'
__contact__ = 'llmapi@163.com'
__url__ = 'https://github.com/llmapi/'
__license__ = 'MIT'

sys.stdout.encoding
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

lock = [True,'Waiting']
def _loading():
    chars = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
    i = 0
    global lock
    t1 = time.time()
    cost_time = 0
    while lock[0]:
        i = (i+1) % len(chars)
        em = '✓' if lock[1] != "Waiting" else chars[i]
        print('\033[A%s %s [%.2f s]' %
              (em, lock[1] or '' if len(lock) >= 2 else '', time.time() - t1))
        time.sleep(0.1)

def _make_post(url,content):
    try:
        res = requests.post(url, data = json.dumps(content))
        rep = res.json()
        return rep
    except Exception:
        return {'code':-1,'msg':'request failed'}

def _get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

def _save_cache(host:str, apikey:str, bot_type:str):
    path = os.environ.get('HOME') + '/.llmapi'
    if not os.path.exists(path):
        os.mkdir(path)
    with open(path + '/cache','w+') as f:
        info = {'host':host,'apikey':apikey,'bot_type':bot_type}
        f.write(json.dumps(info))
        f.flush()
        f.close()

def _load_cache()->dict:
    path = os.environ.get('HOME') + '/.llmapi'
    if not os.path.exists(path + '/cache'):
        return {}
    with open(path + '/cache','r') as f:
        try:
            info = json.loads(f.read())
            return info
        except Exception:
            return {}
class LLMApi():
    def __init__(self, host:str='https://api.llmapi.online', apikey:str='your_apikey', bot_type:str='gpt3'):
        self.host = host
        self.apikey = apikey
        self.bot_type = bot_type
        self.session = self._start_session()
        if self.session == 0:
            print('start session failed')
            exit()

    def _start_session(self):
        url = self.host + '/v1/chat/start'
        content = {'apikey':self.apikey, 'bot_type':self.bot_type, 'timestamp':int(time.time())}
        rep = _make_post(url,content)
        if rep['code'] == 0:
            return rep['session']
        else:
            print("error message : ", rep['msg'])
            return 0
 
    def _end_session(self):
        try:
            url = self.host + '/v1/chat/end'
            content = {'apikey':self.apikey, 'session':self.session, 'timestamp':int(time.time())}
            r = _make_post(url,content)
            return r
        except Exception:
            return None

    def ask(self, prompt:str):
        url = self.host + '/v1/chat/ask'
        content = {'apikey':self.apikey, 'session':self.session, 'timestamp':int(time.time()), 'content':prompt, 'timeout':60}
        rep = _make_post(url,content)

        if rep['reply'] == 'None':
            return -1,'timeout'
        if rep['code'] == 0:
            return rep['code'],rep['reply']
        else:
            return rep['code'],rep['msg']

    def __str__(self):
        print(f"| [host]:{self.host}")
        print(f"| [session]:{self.session}")
        print(f"| [bot_type]:{self.bot_type}")
        return ""
   
                                       
def _parse_arg():
    parse = ap.ArgumentParser(formatter_class=RawTextHelpFormatter,description=f"""
----------------------------------------------------------
 LLMApi is unified OpenApi for Large Language Models.
 [Version]:{__version__}, [HomePage]:https://llmapi.online
----------------------------------------------------------""")
    parse.add_argument('--bot', default='gpt3', type=str, help="""Type of LLM bot you want to talk with:
  - gpt3           GPT-3 is openai's classic LLM with 175B Params
  - chatgpt        ChatGPT is openai's popular and powerful LLM based on GPT-3.5
            """)
    parse.add_argument('--apikey', type=str, help='Your api key.')
    arg = parse.parse_args()
    return arg

def main():
    arg = _parse_arg()

    cache_info = _load_cache()

    if len(cache_info) == 0 and not arg.apikey:
        print('----------------------------------------------------------')
        print('LLMApi is unified OpenApi for Large Language Models.')
        print(f'[Version]:{__version__}, [HomePage]:https://llmapi.online')
        print('----------------------------------------------------------')
        print('\nSpecify your apikey first.')
        print('example:llmapi --apikey="xxxx"\n')
        exit()

    cache_info['host'] = 'https://api.llmapi.online'

    if arg.bot:
        cache_info['bot_type'] = arg.bot
    if arg.apikey:
        cache_info['apikey'] = arg.apikey

    _save_cache(cache_info['host'], cache_info['apikey'], cache_info['bot_type'])

    client = LLMApi(cache_info['host'], cache_info['apikey'], cache_info['bot_type'])
    print( "\n =================================================")
    print(f" * LLMApi version {__version__}")
    print(f" * Visit 'https://llmapi.online' for more info.")
    print( " -------------------------------------------------")
    print(f" * Start talking with '{client.bot_type}'.")
    print( " * Press 'Ctrl+c' to quit.")
    print( " * Input your word and press 'Enter' key to send.")
    print( " =================================================\n\n")
    try:
        global lock
        count = 0
        while True:
            count += 1
            print(f"\033[1;32;44m ---- [{_get_time()}] [count:{count}] Input: \033[0m\n")
            while True:
                try:
                    prompt = input()
                    if prompt != "":
                        break
                except Exception:
                    print("[ERR] Invalid chars, please input again:")

            print("")
            print("")

            lock = [True, 'Waiting']
            try:
                t = Thread(target=_loading)
                t.start()
            except Exception as e:
                print(e)
            try:
                ret,rep = client.ask(prompt)
            except Exception as e:
                lock[0] = False
                print("[ERR] Get reply failed, please try again.")
                continue

            lock[1] = f'[{client.bot_type}] Replied {_get_time()}'
            time.sleep(0.3)
            lock[0] = False

            print("-----------------< BEGIN OF REPLY >-----------------")
            for i in rep:
                time.sleep(0.01)
                sys.stdout.write(i)
                sys.stdout.flush()
            print("")
            print("-----------------<  END OF REPLY  >-----------------")
            print("")
    except KeyboardInterrupt:
        r = client._end_session()
        if r != None:
            print('\n >> [End session success]')
        print(' >> [Bye~]')
        exit()

if __name__ == '__main__':
    main()
