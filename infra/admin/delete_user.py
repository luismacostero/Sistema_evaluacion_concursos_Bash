#!/usr/bin/env python3

import sys
import os.path as op

sys.path.append(op.abspath(op.dirname(op.abspath(__file__)) + "/../common/"))

from db_userManager import dbUserManager
from userManager import userManager

def del_user(username):
        a = dbUserManager()

        ue = a.check_if_user_exists(username)
        
        if(ue is False):
                print("El usuario no existe")
        else:
            a.delete_user(username)
            u = userManager()
            u.delete_linux_user(username)



def del_from_file(filename):
    with open(filename) as f:
        usernames = f.read.splitlines()

    for user in usernames:
        del_user(user)
    

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: ")
        print("\t delete_user.py <username>")
        print("\t delete_user.py <filename_with_usernames>")
    else:
        if(op.isfile(sys.argv[1])):                
            del_from_file(sys.argv[1])
        else:
            del_user(sys.argv[1])
        
