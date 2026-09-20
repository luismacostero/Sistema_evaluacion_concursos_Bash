#!/usr/bin/env python3


import sys
import os
import os.path as op
sys.path.append(op.abspath(op.dirname(op.abspath(__file__)) + "/../common/"))

from configparser import ConfigParser

from utils import *
from User import User

import tempfile
import shutil
import pwd
from datetime import datetime

from problemChecker import problemChecker
from userManager import userManager


def comprueba_solucion(script_sol):

  ## Pre stuff
  parser = ConfigParser()
  parser.read(op.dirname(op.abspath(__file__)) + "/../common/config.ini")

  logfile=open(parser.get("linux", "logfile"), "a+")

  user_name = os.getenv("SUDO_USER")
  if user_name is None:
    user_name = pwd.getpwuid(os.getuid()).pw_name

  user = User(user_name)
  problemNo = user.get_num_problems_solved()

  working_dir = parser.get("linux", "evaluation_path")
  working_dir += "/" + user_name + "/" + str(problemNo) + "/"
  if not op.isdir(working_dir):
    os.makedirs(working_dir, mode=0o700)
    
  working_dir = tempfile.mkdtemp(dir=working_dir)

  #hacemos una copia del script a evaluar
  shutil.copy(script_sol, working_dir)

  ## Comprobamos la solucion
  pc = problemChecker()

  res = pc.check_private_solutions(problemNo,
                                   script_sol,
                                   working_dir)

  ## Post-procesamiento del resultado
  now = datetime.now()
  hora = now.strftime("%H:%M:%S")
  logfile.write(f"[{hora}]: {user_name} ha mandado el problema {problemNo} => {res} <{working_dir}>\n")


  

  if res[0] is False:
    user.increase_wa()
    print("False;-")
  else:
    user.add_ac()
    um = userManager()

    dst_path=um.install_problem(user_name, problemNo + 1)
    print("True;"+dst_path)
    


if __name__=="__main__":
  if len(sys.argv) != 2:
    print("Usage:")
    print("       valida_solucion.py <solution.sh>")
  else:
    comprueba_solucion(sys.argv[1])
