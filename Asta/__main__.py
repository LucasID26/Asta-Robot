from config import bot,prefix,own 
from pyrogram import filters
import subprocess
import sys
import os
import re 
import pickle

@bot.on_message(filters.command('restart',prefix) & filters.user(own[0]))
async def restart_plugins(client,m):
  msg = await m.reply_text("__Restarting BOT__. . .")
  with open("restart.pickle", "wb") as status:
    pickle.dump([m.chat.id, msg.id], status)
  restart_program() 

def restart():
  pesan = ""
  menulis_init()
  install = install_requirements()
  pesan += install
  pull = git()
  pesan += pull
  return pesan



async def restarting():
  if os.path.exists("restart.pickle"):
    with open('restart.pickle', 'rb') as status:
      chat_id, message_id = pickle.load(status)
      os.remove("restart.pickle")
      pesan = restart()
      await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"{pesan}\n\n`Restarting berhasil✅`")

def restart_program():
  os.system('git pull')
  os.execv(sys.executable, ['python', 'main.py']) #+ sys.argv)

   
def menulis_init():
  for file in os.listdir('Asta/plugins'):
    with open('Asta/plugins/__init__.py', 'r') as f:
      init_lines = f.readlines()
    if file.endswith('.py') and not file.startswith('__'):
      module_name = file[:-3]
      import_line = f"from . import {module_name}"
      if not re.search(fr"\b{re.escape(import_line)}\b", str(init_lines)):
        with open('Asta/plugins/__init__.py', 'a') as f:
          f.write("\n"+import_line)


def install_requirements():
  completed_process = subprocess.run(['pip', 'install', '-r', 'requirements.txt'], capture_output=True)
  
  result_dict = {}
  if completed_process.returncode == 0:
    result_dict['status'] = 'Berhasil✅'
    result_dict['message'] = 'Semua module berhasil diinstal'
  else:
    result_dict['status'] = 'Kegagalan❎'
    result_dict['message'] = 'Beberapa modul gagal diinstal'
    result_dict['failed_modules'] = []
    for line in completed_process.stderr.splitlines():
      line = line.decode('utf-8').strip()
      if line.startswith('ERROR: Could not find a version'):
        module_name = line.split()[6]
        result_dict['failed_modules'].append(module_name)
  pesan_install = f"**Install Requirements :**\n"
  if result_dict['status'] == 'Berhasil✅':
    pesan_install += f"**Status :** {result_dict['status']}\n**INFO :** {result_dict['message']}"
  else:
    module_gagal = '\n'.join(['  - ' + module for module in result_dict['failed_modules']]) 
    pesan_install += f"**Status :** {result_dict['status']}\n**INFO :** {result_dict['message']}\n**Module :** {module_gagal}"
  return pesan_install


def git():
  #subprocess.run(['git', 'pull'])
  git_diff = subprocess.Popen(['git', 'diff', '--name-status', 'HEAD@{1}..HEAD'], stdout=subprocess.PIPE)
  output_str = git_diff.communicate()[0].decode('utf-8')

  added_files = []
  modified_files = []
  deleted_files = []
  hasil = ""
  for line in output_str.split('\n'):
    if line.startswith('A'):
      added_files.append(line[2:])
    elif line.startswith('M'):
      modified_files.append(line[2:])
    elif line.startswith('D'):
      deleted_files.append(line[2:])
  if added_files:
    hasil += '**FILE BARU :**\n'
    for file in added_files:
      hasil += file+'\n'
    pass 
  if modified_files:
    hasil += '**FILE DI EDIT :**\n'
    for file in modified_files:
      hasil += file+'\n'
  if deleted_files:
    hasil += '**FILE DIHAPUS :**\n'
    for file in deleted_files:
      hasil += file+'\n'
  if not added_files and not modified_files and not deleted_files:
    hasil += "**UP TO DATE WITH MAIN**"
  return hasil
      
