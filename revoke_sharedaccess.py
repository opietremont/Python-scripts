#!/usr/local/bin/python3
"""This script prompts a user to revoke user in gdrive shared file
 bla bla bla"""

import os
import shutil
import subprocess
import tkinter as tk
import tkinter.filedialog
import re

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

if shutil.which("gdrive") is None:
	print("\nRequire:")
	print("\n- homebrew: /usr/bin/ruby -e '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)'")
	print("\n- gdrive: brew install gdrive\nelse https://github.com/prasmussen/gdrive\n")
	print("\nInit Google Token:")
	print("\n- gdrive: gdrive list\nand follow instructions then execute again script")
	exit(1)

while True:
	try:
		root = tk.Tk()
		root.withdraw()
		root.update()
		EMAIL_FILE = tk.filedialog.askopenfilename()
		root.destroy()
		if os.stat(EMAIL_FILE).st_size > 0 and os.path.isfile(EMAIL_FILE) and os.access(EMAIL_FILE, os.R_OK):
			break
	except OSError:
		pass
	print("\nempty file or unreadable file, please choose correct one")




def get_driveidfilelist(email):
	""" Fonction qui recupere l'ID des fichiers d'un utilisateur present en tant que lecteur."""
	cmd = ["gdrive", "list", "-m", "100000", "--query", f" '{email}' in readers ", "--no-header"]
	p_gdrive = subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding="utf-8")
	id_file_r = p_gdrive.communicate()[0].split('\n')
	return id_file_r

def get_drivefilepath(idfile):
	""" Fonction qui recupere le chemin Google Drive d'un fichier a partir de son ID."""
	cmd_stdin = ["gdrive", "info", f"{idfile}"]
	cmd_stdout = ["grep", "Path:"]
	p_gdrive = subprocess.Popen(cmd_stdin, stdout=subprocess.PIPE)
	p_grep = subprocess.Popen(cmd_stdout, stdin=p_gdrive.stdout, stdout=subprocess.PIPE, encoding="utf-8")
	result = p_grep.communicate()[0].split('\n')
	for file_path in result:
		return file_path

def get_drivepermissionid(idfile, email):
	""" Fonction qui recupere le permissionID d'un utilisateur
	à partir de l'ID d'un fichier dont il a acces et de son email."""
	cmd_stdin = ["gdrive", "share", "list", f"{idfile}"]
	cmd_stdout = ["grep", f"{email}"]
	p_gdrive = subprocess.Popen(cmd_stdin, stdout=subprocess.PIPE)
	p_grep = subprocess.Popen(cmd_stdout, stdin=p_gdrive.stdout, stdout=subprocess.PIPE, encoding="utf-8")
	result = p_grep.communicate()[0].split('\n')
	for permission_data in result:
		permission_id = permission_data.split(None, 1)[0]
		return permission_id

def revoke_drivesharedaccess(idpermission, idfile):
	""" Fonction qui revoque les droits d'acces d'un utilisateur
	a partir de l'ID d'un fichier et de son ID de permission."""
	cmd = ["gdrive", "share", "revoke", f"{idfile}", f"{idpermission}"]
	p_gdrive = subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding="utf-8")
	result = p_gdrive .communicate()[0].split('\n')
	return result

with open(EMAIL_FILE, "r") as file_obj:
	for line in file_obj:
		# regex format email
		regex = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
		if regex.match(str(line.rstrip('\n'))) is None:
			print("email file contain wrong data: " + line.rstrip('\n'))
			continue

		# On considere que l'utilisateur writer est aussi reader
		id_file_list = get_driveidfilelist(line.rstrip('\n'))
		nb_file_list = len(id_file_list) - 1
		if (nb_file_list) == 0:
			print("no shared access found: " + line.rstrip('\n'))
			continue

		list_path_file = DIR_PATH + "/" + line.rstrip('\n') +".txt"

		print("\nuser: " + line.rstrip('\n'))
		print("number of files: " + str(nb_file_list))

		while True:
			try:
				access_answer = str(input("Voulez vous récupérer la liste des fichiers accessibles ? y/n: "))
				if (access_answer.lower() == "y") or (access_answer.lower() == "n"):
					break
			except ValueError:
				pass
			print('\nIncorrect input, try again')

		if access_answer.lower() == "y":
			listpath_f = open(list_path_file, "a")
			print('\nLoading data, please wait')
			for item in id_file_list:
				try:
					id_file = item.split(None, 1)[0]
					print(get_drivefilepath(id_file)[6:].rstrip('\n') + " R")
					listpath_f.write(get_drivefilepath(id_file)[6:].rstrip('\n') + "\n")
				except IndexError:
					pass
				continue
			listpath_f.close()

		perm_id = get_drivepermissionid(id_file_list[0].split(None, 1)[0], line.rstrip('\n'))
		print("permission ID: " + perm_id)

		while True:
			try:
				doit_answer = input("Voulez vous revoquer les droits des utilisateurs concernés ? y/n: ")
				if (doit_answer.lower() == "y") or (doit_answer.lower() == "n"):
					break
			except ValueError:
				pass
			print('\nIncorrect input, try again')

		if doit_answer.lower() == "y":
			print('\nLoading data, please wait')
			for id_file in id_file_list:
				try:
					# print("cmd : gdrive share revoke " + id_file.split(None, 1)[0] + " " + perm_id)
					status = revoke_drivesharedaccess(perm_id, id_file.split(None, 1)[0])
					print(status[0])
				except IndexError:
					pass