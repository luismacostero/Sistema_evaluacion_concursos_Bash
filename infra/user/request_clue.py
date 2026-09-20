#!/usr/bin/env python3
import sys
import os
import pwd
import subprocess
from configparser import ConfigParser


import os.path as op
sys.path.append(op.abspath(op.dirname(op.abspath(__file__)) + "/../common/"))

from User import User
from utils import *

def request_clue(username):
  u = User(username)

  #clue number
  curProb  = u.get_num_problems_solved()
  (_, _, nextClue) =u.get_problem_info(curProb)
  nextClue += 1

  ## Check if the next clue exists
  parser = ConfigParser()
  parser.read(op.dirname(op.abspath(__file__)) + "/../common/config.ini")
  problem_path=get_problem_path(curProb);


  clue_path = problem_path + "/pistas/"
  if nextClue < 10:
    clue_path +="0"
  clue_path += str(nextClue) + ".txt"

  if op.isfile(clue_path):
    u.increase_clue()

    #Write the clue into the file:
    dst_path = "/home/" + username + "/problem_"
    dst_path += str(curProb) if curProb>=10 else ("0" + str(curProb))
    dst_path +="/pistas.txt"


    #show clue
    with open(clue_path,"r") as f:
      with open(dst_path, "a") as f2:
        f2.write(" ---------- [[ PISTA ]] ----------\n")
        
        for l in f:
          f2.write(l)
          print(l)

        f2.write("\n\n")


    # ACL: make the user able to read,write and execute
    #      even he is not the owner of the file
    os.chmod(dst_path, 0o664)
    subprocess.run(['setfacl', '-m', 'u:' + username + ':rwx', dst_path])

    
  else:
    print("Este problema no tiene más pistas :(")
    print("Si sigues atascado, quizás algún profesor te pueda ayudar ...")
    


if __name__=="__main__":
  user_name = os.getenv("SUDO_USER")
  if user_name is None:
    user_name = pwd.getpwuid(os.getuid()).pw_name

  request_clue(user_name)
