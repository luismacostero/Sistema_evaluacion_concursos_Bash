#!/usr/bin/env python3

from configparser import ConfigParser
import sqlite3
import os.path as op

class dbUserManager:
  def __init__(self):
    parser = ConfigParser()
    
    parser.read(op.dirname(op.abspath(__file__)) + "/config.ini")
    
    self.numProblems=parser.get('general','num_problems')
    
    self.db_name=parser.get('database','db_name')
    self.db_name=op.dirname(op.abspath(__file__)) + "/" + self.db_name
    
    
    self.contestants_table=parser.get('database','contestants_table')
    self.acs_table=parser.get('database','acs_table')
    self.was_table=parser.get('database','was_table')
    self.clues_table=parser.get('database','clues_table')
    
    self.con = sqlite3.connect(self.db_name)
    self.cur = self.con.cursor()

    
  def check_if_user_exists(self, username):
    command="SELECT * FROM " + self.contestants_table + \
      " WHERE userId LIKE " + "'" + username + "'"
    
    rows=self.cur.execute(command)
    row =rows.fetchone()
    return False if row is None else True

  def get_all_users(self):
    command="SELECT userId FROM " + self.contestants_table
    # rows = self.cur.execute(command).fetchall()
    sol = []
    for row in self.cur.execute(command):
      sol.append(row[0])


    return sol
    

  def delete_user(self, username):
    #a) users
    command="DELETE FROM " + self.contestants_table + \
      " WHERE userId = " + "'" + username + "'"
    self.cur.execute(command)

    
    #b) acs
    command="DELETE FROM " + self.acs_table + \
      " WHERE userId = " + "'" + username + "'"
    self.cur.execute(command)

    
    #c) was
    command="DELETE FROM " + self.was_table + \
      " WHERE userId = " + "'" + username + "'"
    self.cur.execute(command)

    
    #d) clues
    command="DELETE FROM " + self.clues_table + \
      " WHERE userId = " + "'" + username + "'"

    self.cur.execute(command)
    
    self.con.commit()
    
  def add_user(self, username):
    
    try:
      ## A) Users table
      command="INSERT INTO " + self.contestants_table + "(userId)" + \
        "VALUES " + "('" + username + "')"
      self.cur.execute(command)
      
      ## B) ACS table
      command="INSERT INTO " + self.acs_table + "(userId)" + \
        "VALUES " + "('" + username + "')"
      self.cur.execute(command)
      
      ## C) WAs table
      command="INSERT INTO " + self.was_table + "(userId)" + \
        "VALUES " + "('" + username + "')"
      self.cur.execute(command)
      
      ## D) clues table
      command="INSERT INTO " + self.clues_table + "(userId)" + \
        "VALUES " + "('" + username + "')"
      self.cur.execute(command)
      
      
      self.con.commit()
    except sqlite3.Error as err:
      if err.sqlite_errorcode == 1555:
        print("Error, el usuario ya existe: " + username)
      else:
        print("Algún error raro...")
        print('SQLite error: %s' % (' '.join(err.args)))
        
            

  def get_current_problem(self, username):
    if not self.check_if_user_exists(username):
      return -1

    command="SELECT Pr00"
    for i in range(1, int(self.numProblems)):
      command += (",Pr0" if i < 10 else ",Pr")
      command += str(i)
          

    command += " FROM " + self.acs_table
    command += " WHERE userId LIKE " + "'" + username + "'"

    row = self.cur.execute(command).fetchone()
    problem=0
    for p in row:
      if p == 0:
        break
      else:
        problem +=1
        

    return problem
  
  def get_problem_info(self, username, problem):
    """ Devuelve una tupla de la forma
    (acTime, nWas, nClues)
    """
    if not self.check_if_user_exists(username):
      return (-1,-1,-1)

    problem=("Pr0" if problem < 10 else "Pr") + str(problem)
    
    # ac
    command = "SELECT " + problem +\
              " FROM " + self.acs_table + \
              " WHERE userId LIKE " + "'" + username + "'" 
    
    row = self.cur.execute(command).fetchone()
    acs=row[0]

    # was
    command = "SELECT " + problem +\
              " FROM " + self.was_table + \
              " WHERE userId LIKE " + "'" + username + "'" 
    
    row = self.cur.execute(command).fetchone()
    was=row[0]

    # clues
    command = "SELECT " + problem +\
              " FROM " + self.clues_table + \
              " WHERE userId LIKE " + "'" + username + "'" 
    
    row = self.cur.execute(command).fetchone()
    clues=row[0]


    return (acs, was, clues)


  def add_ac(self, username, problem, value):
    problem=("Pr0" if problem < 10 else "Pr") + str(problem)
    command = "UPDATE " + self.acs_table +\
              " SET " + problem + " = " + value +\
              " WHERE userId LIKE " + "'" + username + "'" 

    self.cur.execute(command)
    self.con.commit()

  def increase_wa(self, username, problem):
    problem=("Pr0" if problem < 10 else "Pr") + str(problem)
    command = "UPDATE " + self.was_table +\
              " SET " + problem + " = " + problem + " + 1" +\
              " WHERE userId LIKE " + "'" + username + "'" 

    self.cur.execute(command)
    self.con.commit()

  def increase_clue(self, username, problem):
    problem=("Pr0" if problem < 10 else "Pr") + str(problem)
    command = "UPDATE " + self.clues_table +\
              " SET " + problem + " = " + problem + " + 1" +\
              " WHERE userId LIKE " + "'" + username + "'" 

    self.cur.execute(command)
    self.con.commit()




  def udpate_user_info(self, username, nombre, apellidos, email, titulacion, grupo, curso):
    command = "UPDATE " + self.contestants_table +\
              " SET " +\
              "nombre = '" + nombre + "', " +\
              "apellidos = '" + apellidos + "', " +\
              "email = '" + email + "', " +\
              "titulacion = '" + titulacion + "', " +\
              "grupo = '" + grupo + "', " +\
              "curso = '" + curso + "' " +\
              "WHERE userId LIKE " + "'" + username + "'" 

    self.cur.execute(command)
    self.con.commit()
