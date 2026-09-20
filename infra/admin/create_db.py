#!/usr/bin/env python3

from configparser import ConfigParser
import sqlite3
import os.path as op


## NOTA: se podrían usar foreginers keys entre las tablas, pero
# para lo que queremos hacer, con esto debería de ser suficiente

class db_creator:
  def __init__(self):
    parser = ConfigParser()
    common_path=op.dirname(op.abspath(__file__)) + "/../common/"
    parser.read(common_path + "config.ini")

    self.numProblems=parser.get('general','num_problems');
    
    self.db_name=parser.get('database','db_name');
    self.db_name=common_path + self.db_name
    
    self.contestants_table=parser.get('database','contestants_table');
    self.acs_table=parser.get('database','acs_table');
    self.was_table=parser.get('database','was_table');
    self.clues_table=parser.get('database','clues_table');
    
    self.con = sqlite3.connect(self.db_name)
    self.cur = self.con.cursor()
    
  def create_contestants_table(self):
    command="CREATE TABLE " + \
            self.contestants_table + \
            "(userId STRING PRIMARY KEY, " \
            "nombre, " \
            "apellidos, " \
            "email, " \
            "titulacion, " \
            "grupo, " \
            "curso)"
    self.cur.execute(command)

  def create_acs_table(self):
    command="CREATE TABLE " + self.acs_table + \
      "(userId STRING PRIMARY KEY"
    
    for i in range(int(self.numProblems)):
      num="Pr"
      num+="0"+str(i) if i<10 else str(i)
      command += ", " + num + " INTEGER DEFAULT 0"
      
    command +=")"
      
    self.cur.execute(command)

  def create_was_table(self):
    command="CREATE TABLE " + self.was_table + \
            "(userId STRING PRIMARY KEY"
        
    for i in range(int(self.numProblems)):
      num="Pr"
      num+="0"+str(i) if i<10 else str(i)
      command += ", " + num + " INTEGER DEFAULT 0"
      
    command +=")"

    self.cur.execute(command)

  def create_clues_table(self):
    command="CREATE TABLE " + self.clues_table + \
            "(userId STRING PRIMARY KEY"
        
    for i in range(int(self.numProblems)):
      num="Pr"
      num+="0"+str(i) if i<10 else str(i)
      command += ", " + num + " INTEGER DEFAULT 0"

    command +=")"

    self.cur.execute(command)
        
if __name__ == "__main__":
  a = db_creator()
  a.create_contestants_table()
  a.create_acs_table()
  a.create_was_table()
  a.create_clues_table()
