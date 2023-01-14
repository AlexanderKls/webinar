#!/usr/bin/env python3

import string
import secrets
import re
from getpass import getpass


class bcolors:
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def wrote_psw(psw):
    var_file = '/opt/webinar-bastion/roles/webinar-deploy/defaults/main.yml'

    with open(var_file, 'r') as file:
        filedata = file.read()

    # Replace the target string
    match = re.findall(r'webinar_root_pw.*', filedata)
    filedata = filedata.replace(match[0], 'webinar_root_pw: ' + psw)

    # Write the file out again
    with open(var_file, 'w') as file:
        file.write(filedata)

def auto_psw():
    result = ''

    user_answer = input('Would you like to generate an automatic password? [y or n]')


    if user_answer.lower() == 'y':
      alphabet = string.ascii_letters + string.digits
      result = ''.join(secrets.choice(alphabet) for i in range(20))

    elif user_answer.lower() == 'n':
      result = set_psw()

    else:
      print(f'{bcolors.WARNING}Please, type y or n{bcolors.ENDC} \n')
      auto_psw()

    return result

def set_psw():
    result = ''

    pswd = getpass(prompt='Set mysql root password, minimum 16 symbols: \n')
    if len(pswd) < 16:
      print(f'{bcolors.WARNING}The password is too easy, count symbols: {len(pswd)}. Enter a password that is 16 or more characters long.{bcolors.ENDC} \n')
      set_psw()

    else:
      repeat_pswd = getpass(prompt='Repeat password: \n')

      if pswd == repeat_pswd:
          result = pswd
      else:
          print(f'{bcolors.FAIL}Passwords do not match.{bcolors.ENDC} \n')
          set_psw()

    return result


def main():
    wrote_psw(auto_psw())

if __name__ == '__main__':
    main()
