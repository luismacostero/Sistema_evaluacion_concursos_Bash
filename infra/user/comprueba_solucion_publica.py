#!/usr/bin/env python3

## Este script sirve para comprobar una solución contra los casos públicos!!!!!
## Para comprobar con el privado, existe otro script

import sys
import os
import os.path as op
sys.path.append(op.abspath(op.dirname(op.abspath(__file__)) + "/../common/"))

from utils import *
from User import User

import tempfile
import shutil
import pwd



from problemChecker import problemChecker

def comprueba_solucion(problemNumber, script_sol, working_dir):
  pc = problemChecker()

  return pc.check_public_solution(problemNumber,
                                  script_sol,
                                  working_dir)


if __name__=="__main__":
  if len(sys.argv) != 2:
    print("Usage:")
    print("       comprueba_solucion.py <solution.sh>")
  else:
    working_path = tempfile.mkdtemp()
    user_name = os.getenv("SUDO_USER")
    if user_name is None:
      user_name = pwd.getpwuid(os.getuid()).pw_name

    user = User(user_name)
    problemNo = user.get_num_problems_solved()

    res=comprueba_solucion(problemNo, sys.argv[1], working_path)

    if res is True:
      print("[OK]!, tu solución funciona para los casos del ejemplo :)")
    else:
      print("[NO] :(, tu solución falla para los casos del ejemplo :(")
      print("")


      print("--- Tu salida -----------------------------")
      with open(working_path+"/output", "r") as f:
        print(f.read())

      print("--- Salida esperada ------------------------")
      problem_path=get_problem_path(problemNo)
      with open(problem_path+"/public_testcase/out", "r") as f:
        print(f.read())


    shutil.rmtree(working_path)
    

