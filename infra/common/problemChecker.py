#!/bin/env python3

import sys
import os
import os.path as op
#sys.path.append(op.abspath(op.dirname(op.abspath(__file__)) + "/../common/"))


from configparser import ConfigParser

from utils import *
import tempfile



class problemChecker:
  def __init__(self):
    parser = ConfigParser()
    parser.read(op.dirname(op.abspath(__file__)) + "/config.ini")

    self.logfile=open(parser.get('linux','logfile'), "a")
    self.evaluation_path=parser.get('linux','evaluation_path')


  def check_solution(self, problem_path, script_path, working_directory):
    #print(f"===>{problem_path}, {working_directory}")

    args=""
    with open(problem_path+"/in_arguments", "r") as input_arguments:
      for l in input_arguments:
        args = l.strip()
        break

      
    stdin = problem_path + "/in_stdin"
    solution = problem_path + "/out"
    stdout = working_directory + "/output"

    #Ejecutamos el proceso
    command = "bash " + script_path + " " + args
    command += " < " + stdin
    command += " > " + stdout + " 2>&1"

    os.system(command)

    ## Comapamos
    diff_command = "/bin/bash -c 'diff --suppress-blank-empty -N -i -E -Z -b -w -B "
    diff_command += "<(sort " + solution + ") "
    diff_command += "<(sort " + stdout + " ) "
    diff_command += "> /dev/null 2>&1 '"

    ret = os.system(diff_command)

    return ret==0

  
  def check_public_solution(self, problemNumber, script_path, working_directory):
    problem_path=get_problem_path(problemNumber)
    
    return self.check_solution(problem_path + "/public_testcase", script_path, working_directory)


  def check_private_solutions(self, problemNumber, script_path, working_directory):
    problem_path=get_problem_path(problemNumber)

    testcases = glob.glob(problem_path + "/private_testcases/*/")

    cont = 1
    for test in testcases:
      pid = test.split("/")[-2]
      path = working_directory+"/"+pid+"/"
      if not op.isdir(path):
        os.mkdir(path)
      
      ret = self.check_solution(test, script_path, path)

      if ret is False:
        return (False, test.split("/")[-2])
      cont += 1


    return (True, "")
      
  def check_all_solutions(self, problemNumber, script_path, working_directory):
    if not op.isdir(working_directory):
      os.mkdir(working_directory)

    path=working_directory+"/public/"
    if not op.isdir(path):
      os.mkdir(path)

    ret = self.check_public_solution(problemNumber, script_path, path)
    if not ret:
      return (False, "public")
    
    path=working_directory+"/private/"
    if not op.isdir(path):
      os.mkdir(path)
    ret = self.check_private_solutions(problemNumber, script_path, path)

    return ret
  

if __name__=="__main__":
  a = problemChecker()
  #print(a.check_solution(sys.argv[1], sys.argv[2], "/tmp"))
  #print(a.check_private_solutions(int(sys.argv[1]), sys.argv[2], "/tmp"))
  print(a.check_all_solutions(int(sys.argv[1]), sys.argv[2], "/tmp"))
