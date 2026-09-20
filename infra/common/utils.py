import os.path as op
from configparser import ConfigParser

import glob


def get_problem_path(problem_number):
    parser = ConfigParser()                
    parser.read(op.dirname(op.abspath(__file__)) + "/config.ini")

    basepath=parser.get('linux','problems_path')

    problem_id=str(problem_number) if problem_number >=10 else ("0"+str(problem_number))

    problems=glob.glob( basepath+"/"+problem_id+"_*", recursive=False)

    if not problems:
        raise Exception(f"El problema {problem_number} no existe en el disco")

    return (problems[0] + "/")
    
