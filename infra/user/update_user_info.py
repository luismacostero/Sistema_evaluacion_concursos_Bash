#!/usr/bin/env python3
import sys
import os
import pwd
import os.path as op
sys.path.append(op.abspath(op.dirname(op.abspath(__file__)) + "/../common/"))

from db_userManager import dbUserManager
from userManager import userManager

def update_user(username):


  nombre     = input("Nombre: ")
  apellidos  = input("Apellidos: ")
  email      = input("Email: ")
  titulacion = input("Titulación: ")
  grupo      = input("Grupo: ")
  curso      = input("Curso: ")

  db = dbUserManager()
  db.udpate_user_info(username, nombre, apellidos, email, titulacion, grupo, curso)

def install_first_problem(username):

  um = userManager()
  um.install_problem(username, 0)
  


if __name__=="__main__":
  user_name = os.getenv("SUDO_USER")
  if user_name is None:
    user_name = pwd.getpwuid(os.getuid()).pw_name

  update_user(user_name)
  install_first_problem(user_name)
