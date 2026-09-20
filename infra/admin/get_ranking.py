#!/usr/bin/env python3

import sys
import os.path as op

sys.path.append(op.abspath(op.dirname(op.abspath(__file__)) + "/../common/"))

from db_userManager import dbUserManager
from User import User

def get_ranking():
  """ Devuelve una lista con el ranking de los usuarios.
  Ordenados en función del número del número de Acs + score
  La lista está compuesta de tuplas de la forma:

  [(userId, nAcs, score), (...), ...]
  """

  db=dbUserManager()
  users=db.get_all_users()

  scores=[]
  for name in users:
    u = User(name)
    (nAcs, score) = u.get_score()
    scores.append((name, nAcs, score))


  scores.sort(key=lambda x: (x[1], -x[2]), reverse=True)
  return scores



if __name__ == "__main__":
  print(get_ranking())

  
  
  
  


