#!/usr/bin/env python3

import sys
import os.path as op

sys.path.append(op.abspath(op.dirname(op.abspath(__file__)) + "/../common/"))
from db_userManager import dbUserManager
from userManager import userManager

def add_user(username):
  db = dbUserManager()
  db.add_user(username)

  
  u = userManager()
  pwd=u.create_linux_user(username)
#  u.install_problem(username, 0)

  print(f"{username}:{pwd}")

  
def add_from_file(filename):
  with open(filename) as f:
    usernames = f.read().splitlines()

    for user in usernames:
      if user == "":
        continue
      else:
        add_user(user)


        
if __name__ == "__main__":
  if (len(sys.argv) != 2):
    print("Usage: ")
    print("\t script <username>")
    print("\t script <filename_with_usernames>")
  else:
    
    if(op.isfile(sys.argv[1])):                
      add_from_file(sys.argv[1])
    else:
      add_user(sys.argv[1])



