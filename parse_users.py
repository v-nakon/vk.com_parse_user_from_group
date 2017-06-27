# -*- coding: utf-8 -*-
import json
import urllib.request
import logging

logging.basicConfig(level=logging.DEBUG)

FILE_DATA = 'USERS_DATA.txt'# file for result
# write data to file
def write_to_file(path_file, user_data):
    file = open(path_file, "a", encoding="utf-8")
    file.write(user_data + '\n')
    file.close()


# get response API
def get_response(url, TOKEN):
    try:
        response = urllib.request.urlopen(url + TOKEN)
        return str(response.read().decode("utf-8"))
    except Exception:
        logging.error("Did not receive a response from VK API")
        exit(0)

# get users data and call write_to_file
def get_users_data(response):
    stop = False
    i = 0
    while stop == False:
        try:
            parsed_json = json.loads(response)
            uid = str(parsed_json['response']['users'][i]['uid'])
            first_name = str(parsed_json['response']['users'][i]['first_name'])
            last_name = str(parsed_json['response']['users'][i]['last_name'])
            user_data = '[' + uid + '] ' + '[' + first_name + '] ' + '[' + last_name + ']'
            write_to_file(FILE_DATA, user_data)
            i += 1
        except Exception:
            stop = True
            logging.debug(i)

# check user in response
def check_user(response):
    try:
        parsed_json = json.loads(response)
        uid = parsed_json['response']['users'][0]['uid']
        logging.debug('Users YES')
        return True
    except Exception:
        logging.warning("Not users")
        logging.debug('Answer VK API - ' + response)
        return False

def main():
    TOKEN = '' #vk.com your secret token
    GROUP_ID = str(46905358) #vk.com group id
    offset = 0 # offset
    while True:
        url = 'https://api.vk.com/method/groups.getMembers?group_id=' + GROUP_ID + '&fields=contacts&offset=' + str(offset) + '&access_token='

        response = get_response(url,TOKEN)

        if check_user(response) == False:
            logging.debug('End script')
            exit(0)
        get_users_data(response)
        logging.debug('offset [' + str(offset) + ']')
        offset += 1000

if __name__ == '__main__':
    main()