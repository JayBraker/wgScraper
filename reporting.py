#!/home/jaybraker/wgSuche/bin/python
from bs4 import BeautifulSoup
import telegram
import requests
import random
import json
import re

getNumber = re.compile('.\d*.html')
getDesc = re.compile('freitext_\d_content')
clean1 = re.compile('<.*?>')
whiteSpcs = re.compile('\s+')
clean2 = re.compile('\n+')

def htmlClean(strin):
	strin = re.sub(clean1, '', str(strin))
	strin = strin.strip('[')
	strin = strin.strip(']')
	strin = re.sub(whiteSpcs, ' ', strin)
	strin = re.sub(clean2, '\n', strin)
	return strin

def main():
	f = []
	with open('/home/jaybraker/wgSuche/agents.txt') as filla:
		f = json.load(filla)
	header = {}
	header['User-Agent']=random.choice(f)
	print("Verwendeter Agent:")
	print(header['User-Agent'])
	r = requests.get("https://www.wg-gesucht.de/wg-zimmer-und-1-zimmer-wohnungen-in-Aachen.1.0+1.1.0.html?offer_filter=1&city_id=1&noDeact=1&categories%5B%5D=0&categories%5B%5D=1&rent_types%5B%5D=2&sMin=20&rMax=350",headers=header)
	print(r.status_code)
	soup = BeautifulSoup(r.content, 'html.parser')
	soupWGs = soup.find_all('div', {"id" : re.compile('liste-details-ad-\d*')})

	me = {}
	with open('/home/jaybraker/wgSuche/reportTo.json') as otto:
		me = json.load(otto)
	bot = telegram.Bot(me['token'])
	f = open('/home/jaybraker/wgSuche/test.html','w')
	f.write(str(soupWGs))
	f.close()
	f = open('/home/jaybraker/wgSuche/test.html','r')
	print('loaded')
	soup = BeautifulSoup(f, "html.parser")
	imgs = []
	facts = None
	for e in soup.find_all('a'):
		entry={}
		if e.get('style') != None:
			url = "https://www.wg-gesucht.de/"+e['href']
			entry['url']=url
			temp = requests.get(url)
			print(temp)
			tSoup = BeautifulSoup(temp.content, "html.parser")
			desc = tSoup.find_all("p", {"id":getDesc})
			desc = htmlClean(desc)
			facts = tSoup.find_all("h2", class_='headline headline-key-facts')
			facts = htmlClean(facts)
			entry['desc'] = desc
			entry['facts'] = facts
			#print(desc)
			#print(facts)

		i = ""
		i = e.get('style')
		if i:
			res = getNumber.search(str(e))
			res = str(res.group(0)).strip('.')
			res = str(res).strip('.html')
			print(res)
			i = i.strip("background-image: url(")
			i = i.strip(");")
			i = i.replace(".sized", ".large")
			i = i.replace(".small", ".large")
			entry['id']=id
			entry['img_url']=i

			imgs.append(entry)
	for e in imgs:
		msg = "<a href=\""+e['url']+"\">"+e['facts']+"</a>"
		#msg = "["+e['facts']+"]\("+e['url']+"\)"+e['desc']+"[\.]\("+e['img_url']+"\)"
		print(msg)
		#msg = e['desc'] +" "+ e['img_url']
		if msg:
			bot.send_message(chat_id=me['chat_id'],text=msg,parse_mode=telegram.ParseMode.HTML)

if __name__ == '__main__':
	main()
