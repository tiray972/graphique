import discord
import ftx
import pandas as pd
import json
import time
import ta
import matplotlib.pyplot as plt
from math import *
import os


def pourecent(nombre,val):
    return nombre + (nombre * val / 100)

def extract_num_intexFileToListe(fichier):
	file=open(fichier,'+r')
	u=file.read()
	l=[]
	val=''
	for n in u:
		if n!='\n':
			val+=n
		else:
			l.append(float(val))
			val=''
	return l

token = "OTEyNDg2ODc2NDEyMjc2Nzc3.YZwpoA.0c2fmEWpAz6YHLrWfskBY2WOiKk"
def recupdermessage():
	token = "OTEyNDg2ODc2NDEyMjc2Nzc3.YZwpoA.0c2fmEWpAz6YHLrWfskBY2WOiKk"
	client = discord.Client()
	@client.event
	async def on_ready():
		print(f'{client.user} has connected to Discord!')
		mes=open('message.txt','+w')
		channel = client.get_channel(912495325997064193)
		message = await channel.fetch_message(channel.last_message_id)
		mes.write(message.content)
		user = await client.fetch_user(711967096820465777)
		await client.close()
		time.sleep(1)
	client.run(token)
	mes=open('message.txt','+r')
	
	return mes.read()



def sendmessage(message,nb):#envoyer message ou graph sur discord 
	token = "OTEyNDg2ODc2NDEyMjc2Nzc3.YZwpoA.0c2fmEWpAz6YHLrWfskBY2WOiKk"
	client = discord.Client()
	if nb==0:
		@client.event
		async def on_ready():
			
			print(f'{client.user} has connected to Discord!')
			channel = client.get_channel(912495325997064193)
			await channel.send(message)
			
			user = await client.fetch_user(711967096820465777)
			await user.send(message)
			
			await client.close()
			time.sleep(1)
	if nb==1:
		@client.event
		async def on_ready():
			
			print(f'{client.user} has connected to Discord!')
			channel = client.get_channel(912495325997064193)
			
			await channel.send(file=discord.File(message))
			user = await client.fetch_user(711967096820465777)
			await user.send('graph envoyer')
			
			await client.close()
			time.sleep(1)
	client.run(token)

#sendmessage('test3',0)0 pour message normal 1 pour un graph ex:sendmessage('graph.png',1)

def comparerderniermessage(motsAttendu):#
	if recupdermessage()==motsAttendu:
		return True
	else:
		return False



plt.figure()
plt.plot(extract_num_intexFileToListe('valeur.txt'),label='hold')
plt.plot(extract_num_intexFileToListe('valus.txt'),label='solde')
plt.xlabel('temp avec interval de 15min')
plt.ylabel('montant en $')
plt.legend()
plt.savefig('graph.png')
sendmessage('graph.png',1)
