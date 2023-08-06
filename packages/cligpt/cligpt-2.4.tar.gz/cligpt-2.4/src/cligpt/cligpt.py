#%%
import os
import sys
import openai
import shutil
import readline
import json
import argparse
import re


class CLIGPT:
    def __init__(self, openai_api_key, config_file):
        with open(config_file, 'r') as f:
            self.configs = json.load(f)
        openai.api_key = openai_api_key

        self.roles = [key for key in self.configs]
        self.default_role_index = 0
        self.welcome()

    def welcome(self):
        print('The available roles are as follows, use @roles to switch.')
        for key in self.configs:
            print(f"{key}: {self.configs[key]}")
        print("-" * shutil.get_terminal_size().columns)

    def start(self):
        while True:
            if self.roles[self.default_role_index] == '@code': # (end with Ctrl+D)
                print(f'@code (at least two lines and ends with Ctrl+D):')
                user_input = sys.stdin.read()
            else:
                user_input = input(f"{self.roles[self.default_role_index]}: ")
            # user_input = sys.stdin.read()
            # user_input = sys.stdin.readlines()
            if user_input in ['q', 'exit']:
                break
            # check if user_input starts with @
            if user_input.startswith('@'):
                user_input = re.sub(r'\n', '', user_input)
                for role in self.roles:
                    if user_input in role:
                        self.default_role_index = self.roles.index(role)
                        break
                continue
            if self.roles[self.default_role_index] == '@generic':
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{
                                                "role": "user",
                                                "content": f"{user_input}"
                                            }])
            else:
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                        messages=[{
                                                            "role": "system",
                                                            "content": f"{self.configs[self.roles[self.default_role_index]]}"
                                                        }, {
                                                            "role": "user",
                                                            "content": f"{user_input}"
                                                        }])
            print(response.choices[0].message.content)
            print("-" * shutil.get_terminal_size().columns)


if __name__ == '__main__':
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        raise Exception("OpenAI API key not provided, please `export OPENAI_API_KEY=[Your API KEY]`")

    config_file = os.path.join('.', 'config.json')
    cligpt = CLIGPT(openai_api_key=OPENAI_API_KEY, config_file=config_file)
    cligpt.start()
