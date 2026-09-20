#!/usr/bin/env python3

from configparser import ConfigParser
import sqlite3
import sys
import os
import os.path as op
import subprocess
import secrets
import string
from utils import *
import shutil

class userManager:
    def __init__(self):
        parser = ConfigParser()
                
        parser.read(op.dirname(op.abspath(__file__)) + "/config.ini")

        self.pwd_length=int(parser.get('linux','password_length'))

        

    def create_linux_user(self, username):
        """
        Returns the generated password
        """
        try:
            os.system(f'id {username} > /dev/null 2>&1')
        except:
            raise Exception(f'El usuario {username} ya existe en linux ...')

        pwd_chars = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(pwd_chars) for _ in range(self.pwd_length))
        password += "\n" + password + "\n"
        try:
            subprocess.run(['useradd', '-m', username])
            subprocess.run(['passwd', username], input=password.encode(), check=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            subprocess.run(['usermod', '-G', 'contestant', username])

            os.system(f'setfacl -m u:tester:rwx /home/{username}')
        except:
            raise Exception(f'Error al crear el usuario {username} en el sistema linux ...')
                            

        return password


    
    def delete_linux_user(self, username):
        try:
            os.system(f'id {username} >/dev/null 2>&1')
        except:
            raise Exception(f'El usuario {username} ya existe en linux ...')

        try:
            subprocess.run(['userdel', '-r', username],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
        except:
            raise Exception(f'Error al eliminar el usuario {username} en el sistema linux ...')
                            



    def install_problem(self, username, problemNumber):
        src_path = get_problem_path(problemNumber)
        dst_path = "/home/" + username + "/problem_"
        dst_path += str(problemNumber) if problemNumber>=10 else ("0" + str(problemNumber))
        dst_path +="/"

        
        os.mkdir(dst_path)

        dst_file = dst_path + "enunciado.txt"
        with open(dst_file, "w") as dst:
            dst.write("\n ------ [ENUNCIADO] -----------------\n\n")

            info=src_path + "/info.txt"
            with open(info, "r") as fich:
                for l in fich:
                    dst.write(l)

            dst.write("\n\n")

            info=src_path + "/problem.txt"
            with open(info, "r") as fich:
                for l in fich:
                    dst.write(l)

            dst.write("\n\n")

            
            dst.write("\n ------ [INPUT] -----------------------\n\n")
            dst.write("$ ./program.sh ")
            in_args = src_path + "/public_testcase/in_arguments"
            with open(in_args, "r") as ina:
                for l in ina:
                    dst.write(l)

            dst.write("\n")
            in_std = src_path + "/public_testcase/in_stdin"
            with open(in_std, "r") as instd:
                for l in instd:
                    dst.write(l)
                
                
            dst.write("\n ------ [OUTPUT] -----------------------\n\n")
            out = src_path + "/public_testcase/out"
            with open(out, "r") as of:
                for l in of:
                    dst.write(l)

            dst.write("\n")

            dst.close()

        # A) ACL: make the user able to read,write and execute
        #         even he is not the owner of the folder            
        #shutil.chown(dst_path, user=username, group=username)
        subprocess.run(['setfacl', '-m', 'u:' + username + ':rwx', dst_path])

        # B) The rest, owner + permissons
        for root, dirs, files in os.walk(dst_path):
            for momo in dirs:
                #shutil.chown(op.join(root,momo), user=username, group=username)
                os.chmod(op.join(root,momo), 0o555)
                subprocess.run(['setfacl', '-m', 'u:' + username + ':rwx', op.join(root,momo)])

        
            for momo in files:
                #shutil.chown(op.join(root,momo), user=username, group=username)
                os.chmod(op.join(root,momo), 0o400)
                subprocess.run(['setfacl', '-m', 'u:' + username + ':rwx', op.join(root,momo)])


        return dst_path
    
