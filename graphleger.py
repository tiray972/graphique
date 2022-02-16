import discord
import ftx
import pandas as pd
import json
import time
import ta
import matplotlib.pyplot as plt
from math import *
import os

def truncate(n, decimals=0):
    r = floor(float(n)*10**decimals)/10**decimals
    return str(r)

def getBalance(myclient, coin):
    jsonBalance = myclient.get_balances()
    if jsonBalance == []: 
        return 0
    pandaBalance = pd.DataFrame(jsonBalance)
    if pandaBalance.loc[pandaBalance['coin'] == coin].empty: 
        return 0
    else: 
        return float(pandaBalance.loc[pandaBalance['coin'] == coin]['free'])

# prerequi nom ect... (api)
pairSymbol = 'ETH/USD'
fiatSymbol = 'USD'
cryptoSymbol = 'ETH'
accountName = 'RAYROB'
goOn = True
myTruncate = 3
i = 9
j = 21


client = ftx.FtxClient(
    api_key='',
    api_secret='',
    subaccount_name=accountName
)
fiatAmount = getBalance(client, fiatSymbol)
cryptoAmount = getBalance(client, cryptoSymbol)

total=fiatAmount+cryptoAmount
result = client.get_balances()
# fontion pour montrer ceux que represente une hausse tant de pourcent
# pour une baisse il faut indiquer le moins
def pourecent(nombre,val):
    return nombre + (nombre * val / 100)

data = client.get_historical_data(
    market_name=pairSymbol,
    resolution=3600,
    limit=1000,
    start_time=float(round(time.time()))-3*3600,
    end_time=float(round(time.time())))
df=pd.DataFrame(data)
total=fiatAmount+(cryptoAmount*df['close'].iloc[-1])

def ajouterValeurFond(fichier):
	ajout=open(fichier,'+a')
	ajout.write(str(total)+'\n')

def ajouterValeurMarcher(fichier):
	ajout=open(fichier,'+a')
	ajout.write(str((df['close'].iloc[-1] * 0.011) + 2.06626061)+'\n')


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

token = ""
def recupdermessage():
	token = ""
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
	token = ""
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




def main():
	ajouterValeurMarcher('valeur.txt')
	ajouterValeurFond('valus.txt')
	if comparerderniermessage('!graphique eth'):
		os.system('python3 send.py')



main()





