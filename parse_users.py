# -*- coding: utf-8 -*-
import json
import urllib.request
import logging
import sys
logging.basicConfig(level=logging.DEBUG)


FILE_DATA = 'USERS_DATA.txt'# file for result


def write_to_file(path_file, user_data):
    """Write result to file """
    try:
        file = open(path_file, "a", encoding="utf-8")
    except Exception:
        logging.warning("File - " + path_file + " is empty!")
        sys.exit()
    else:
        file.write(user_data + '\n')
        file.close()


def get_response(url, TOKEN):
    """get response VK API. Use """
    try:
        response = urllib.request.urlopen(url + TOKEN)
        return str(response.read().decode("utf-8"))
    except Exception:
        logging.error("Did not receive a response from VK API")
        exit(0)


def get_users_data(response):
    """get users data and call write_to_file """
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


def check_user(response):
    """Check user in response """
    try:
        parsed_json = json.loads(response)
        uid = parsed_json['response']['users'][0]['uid']
        logging.debug('Users YES')
        return True
    except Exception:
        logging.warning("Not users")
        logging.debug('Answer VK API - ' + response)
        return False


def get_group(path_file):
    """Get group_id from file """
    f = open(path_file)
    list_groups = f.readlines()
    try:
        line = list_groups[0]
    except Exception:
        logging.warning("File - " + path_file + " is empty!")
        sys.exit()
    else:
        f.close()
        logging.debug("Get group - [" + str(line).strip() + "]")
    return str(line)


def delete_group(path_file):
    """Delete first group_id from file """
    f = open(path_file)
    list_groups = f.readlines()
    try:
        line = list_groups.pop(0)
        #line = list_groups[0]
    except Exception:
        logging.warning("File - " + path_file + " is empty!")
        sys.exit()
    else:
        with open(path_file, 'w') as F:
            F.writelines(list_groups)
        logging.debug("Delete group - [" + str(line) + "]")
        f.close()

def main():
    file_with_groups = 'groups_id.txt'
    TOKEN = '14bb0bdb84bb0bdb84bb0bdb8674bec0ec344bb04bb0bdb812f2f044e81a3b86ec8ce8ca' #vk.com your secret token
    GROUP_ID = get_group(file_with_groups)
  
    offset = 0 # offset
    while True:
        url = 'https://api.vk.com/method/groups.getMembers?group_id=' + GROUP_ID + '&fields=contacts&offset=' + str(offset) + '&access_token='

        response = get_response(url,TOKEN)

        if check_user(response) == False:
            logging.debug('End script')
            delete_group(file_with_groups)
            exit(0)
        get_users_data(response)
        logging.debug('offset [' + str(offset) + ']')
        offset += 1000

if __name__ == '__main__':
    main()
