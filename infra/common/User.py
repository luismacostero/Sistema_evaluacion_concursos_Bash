from db_userManager import dbUserManager
from configparser import ConfigParser
import os.path as op
import time


## Esta clase representa a un usuario que _existe_ en la DB

class User:
  def __init__(self, username):
    self.username = username

    self.dbUser = dbUserManager()
    if not self.dbUser.check_if_user_exists(username):
      raise Exception("El usuario "+ username +" no existe en la DB")


    parser = ConfigParser()
    parser.read(op.dirname(op.abspath(__file__)) + "/config.ini")
    
    self.wa_penalty=float(parser.get('evaluation','wa_penalty'))
    self.clue_penalty=float(parser.get('evaluation','clue_penalty'))

    
  def get_num_problems_solved(self):
    return self.dbUser.get_current_problem(self.username)


  def get_problem_info(self, problem):
    """
    Return (acTime, was, clues)
    """
    return self.dbUser.get_problem_info(self.username, problem)
    
  def get_score(self):
    """ Devuelve una tupla con el siguiente formato:
    (nAcs, score)
    donde el score se calcula como:
    - Se suma el tiempo de cada Ac
    - Se suma el número de Was*penalización (solo de los problemas con Acs)
    - Se suma el número de Clues*penalización (solo de los problemas con Acs)
    """


    nAcs = self.get_num_problems_solved()
    score=0
    for problem in range(0, nAcs):
      (time,was,clues)=self.dbUser.get_problem_info(self.username, problem)

      score += time
      score += was*self.wa_penalty
      score += clues*self.clue_penalty

    return (nAcs, score)

  
  def add_ac(self):
    currProb = self.get_num_problems_solved()

    timestamp = int(time.time())
    self.dbUser.add_ac(self.username, currProb, str(timestamp))

  def increase_wa(self):
    currProb = self.get_num_problems_solved()

    self.dbUser.increase_wa(self.username, currProb)

  def increase_clue(self):
    currProb = self.get_num_problems_solved()

    self.dbUser.increase_clue(self.username, currProb)
