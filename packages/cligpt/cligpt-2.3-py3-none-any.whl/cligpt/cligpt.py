#%%
import os
import openai
import shutil
import readline
import json
import argparse


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
            user_input = input(f"{self.roles[self.default_role_index]}: ")
            if user_input in ['q', 'exit']:
                break
            # check if user_input starts with @
            if user_input.startswith('@'):
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



# if __name__ == '__main__':
#     config_dir = os.path.expanduser('~/.cligpt')
#     json_file = os.path.join(config_dir, 'config.json')
#     if not os.path.exists(config_dir):
#         os.makedirs(config_dir)
#     if not os.path.exists(json_file):
#         shutil.copyfile(os.path.join(os.path.dirname(__file__), 'config.json'), json_file)

#     parser = argparse.ArgumentParser(description='CLI GPT-3')
#     # parser.add_argument('--config', type=str, default='/Users/ramdrop/Documents/github/cligpt/src/config.json', help='path to config file')
#     parser.add_argument('--api_key', type=str, default='', help='path to config file')
#     args = parser.parse_args()

#     if args.api_key != '':
#         with open(json_file, 'r') as f:
#             configs = json.load(f)
#         configs['api_key'] = args.api_key
#         with open(json_file, 'w') as f:
#             json.dump(configs, f)

#     cligpt = CLIGPT(json_file)
#     cligpt.start()