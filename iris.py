#!/usr/bin/python3
# coding: utf-8

###IMPORT

import snowboydecoder, pyttsx3, os.path, wave, requests, os
from datetime import datetime, date
import speech_recognition as iris
from subprocess import call
from google_speech import Speech
from bs4 import BeautifulSoup
import threading, re, wikipedia, json, pyowm
from newsapi.newsapi_client import NewsApiClient
from urllib.request import urlopen


### Blank Screen / active powersave mode
class blackscreen(threading.Thread):
    def run(self):
        os.system("eog --fullscreen iris_blank/black.jpg")
        pass
thread0 = blackscreen()
thread0.daemon = True
thread0.start()

logo = ('''


██╗    ██████╗     ██╗    ███████╗
██║    ██╔══██╗    ██║    ██╔════╝
██║    ██████╔╝    ██║    ███████╗
██║    ██╔══██╗    ██║    ╚════██║
██║    ██║  ██║    ██║    ███████║
╚═╝    ╚═╝  ╚═╝    ╚═╝    ╚══════╝


''')

isfile = os.path.isfile('master_name')
if isfile == True:
    pass
else:
    master_name = input(str('Como você gostaria de ser chamado?: '))
    f = open('master_name','a+')
    f.write('{0}'.format(master_name))
    f.close()

# speech config
speech_engine = pyttsx3.init()
speech_engine.setProperty('rate', 150) # noise config
print('[*] Ajustando ruído de fundo.')
recognizer = iris.Recognizer()
with iris.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)
call(['clear'])
print(logo)
print('[+] Ruídos ajustados.')
# key pressing config
keyboard = Controller()
#API Keys
newsapi = NewsApiClient(api_key='f88b2cec4f5d4e46a511706325e756de')
climaAPI = ('c5743b7436f81e619263925dca22e064')

def func():

    master_name = open('master_name', 'r').read()
    lang = 'pt-br'

    ### know commands
    music_w = ['Toque', 'toque', 'Tocar', 'tocar', 'música', 'som']
    wiki_w = ['Quem é', 'quem é', 'Quem foi', 'quem foi', 'O que é', 'o que é']
    news_w = ['Noticias', 'noticias', 'Notícias', 'notícias', 'Notícia', 'notícia']
    wheater_w = ['Clima', 'Previsão', 'Tempo', 'Temperatura', 'clima', 'previsão', 'tempo', 'temperatura']
    funcs = ['Fazer', 'Funções', 'Comandos', 'fazer', 'funções', 'comandos' ]
    disp_w = ['Manter', 'Mantenha', 'Ligada', 'manter', 'mantenha', 'ligada']
    disp_o_w = ['Desligar', 'Escurecer', 'desligar', 'escurecer']
    price_quote_w = ['Cotação', 'cotação', 'Valor', 'valor', 'Preço', 'preço']

    if any(x in l for x in price_quote_w):
        def search_currency(currency):
            with open('~/json/moedas.json') as crrncy:
                data = json.load(crrncy)
                data = data[currency]
                def api_price(data):
                    request_api = requests.get("https://economia.awesomeapi.com.br/all")
                    price = json.loads(request_api.text)
                    price_quote = 'A cotação atual é de R$ '+price[data]['bid'][:4]
                    Speech(price_quote, lang).play()
                api_price(data)

    if any(x in l for x in disp_o_w):
        class blackscreen1(threading.Thread):
            def run(self):
                os.system("eog --fullscreen iris_blank/black.jpg")
                pass
        thread1 = blackscreen1()
        thread1.daemon = True
        thread1.start()
        Speech('Entendido.', lang).play()
    if any(x in l for x in disp_w):
        call(["killall", "eog"])
        Speech('Entendido.', lang).play()

    if any (x in l for x in funcs):
        Speech('Posso te informar a previsão do tempo, as horas, as ultimas notícias, tocar e recomendar músicas de acordo como gênero desejado e também fazer pesquisas usando o wikipédia.',lang).play()
    if any(x in l for x in wheater_w):
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        data = json.load(response)
        city1 = data['city']

        print(city1)

        import pyowm, time
        owm = pyowm.OWM(climaAPI)
        city = owm.weather_at_place('{0}, BR'.format(city1))
        weather = city.get_weather()
        temp = weather.get_temperature('celsius')['temp']
        city2 = owm.three_hours_forecast('{0}, BR'.format(city1))
        chuvas = city2.will_have_rain()

        if chuvas == True:
            response_x = ('Está previsto chuvas para hoje.')
        else:
            response_x = ('Não está previsto chuvas para hoje.')

        response = ('A temperatura em %s é de %d°' % (city1, temp))

        Speech(response, lang).play()
        time.sleep(0.5)
        Speech(response_x, lang).play()

    if any(x in l for x in wiki_w):
        wikipedia.set_lang('pt')
        search = wikipedia.summary(l, sentences=2)
        print(search)
        Speech(search, lang).play()

    if any(x in l for x in news_w):
        top_headlines = newsapi.get_top_headlines(country='br')
        for news in top_headlines['articles'][:4]:
            text = (news['title'])
            Speech(text, lang).play()

    if ('horas') in l:
        now = datetime.now()
        h = now.hour
        m = now.minute
        d = now.day
        mm = now.month
        y = now.year

        DIAS = [
        'Segunda-feira',
        'Terça-feira',
        'Quarta-feira',
        'Quinta-Feira',
        'Sexta-feira',
        'Sábado',
        'Domingo'
        ]

        MESES = {1:'Janeiro', 2:'Fevereiro', 3:'Março', 4:'Abril',
                5:'Maio', 6:'Junho', 7:'Julho', 8:'Agosto',
                9:'Setembro', 10:'Outubro', 11:'Novembro', 12:'Dezembro'}

        data = date(year=y, month=m, day=d)
        indice_da_semana = data.weekday()
        dia_da_semana = DIAS[indice_da_semana]

        mes1 = MESES.get(m)
        dia = ('%s, %d de %s' % (dia_da_semana, d, mes1))
        
        Speech('Agora são %d:%d. Hoje é %s.' % (h, m, dia), lang).play()

    if any(x in l for x in music_w):
        if ('Pausar') in l or ('pausar') in l:
            call(["spotifycli", "--pause"])
            Speech('Música pausada.', lang).play()
        elif ('Retomar') in l or ('retomar') in l or ('Continuar') in l or ('continuar' in l):
            Speech('Retomando música.', lang).play()
            call(["spotifycli", "--play"])
        elif ('Parar') in l or ('parar') in l:
            call(["killall", 'spotify'])
            Speech('Música interrompida.', lang).play()

        else:
            try:
                s = os.system("pgrep spotify")
                if s == 0:
                    print('Processo ativo.')
                    os.system('killall spotify >/dev/null 2>/dev/null')
                    Speech('Música interrompida.', lang).play()
                else:
                    Speech('Qual música gostaria de ouvir?', lang).play()
                    with iris.Microphone() as source:
                        audio = recognizer.listen(source)
                    try:
                        song = recognizer.recognize_google(audio)
                        search = ('%s spotify' % (song))
                        page = requests.get("https://www.google.com/search?q={}&num=1".format(search))
                        soup = BeautifulSoup(page.content, features='html')
                        links = soup.findAll('a')
                        payload = ''

                        for link in links:
                            link_href = link.get('href')
                            if "url?q=" in link_href and not "webcache" in link_href:
                                payload+='Link: `'+link.get('href').split("?q=")[1].split("&sa=U")[0]+'`\n'
                        if payload:
                            uri = (payload.split('/')[4])
                            uri = uri.replace('`\nLink: `https:', '')
                            print(uri)

                            class Spotify(threading.Thread):
                                def run(self):
                                    os.system("spotify --uri='spotify:track:%s#0:01' & xdotool search --sync --onlyvisible --class 'spotify' windowminimize" % (uri))
                                    os.system("spotifycli --pause && spotifycli --play") # show in mirror
                                    pass
                            thread = Spotify()
                            thread.daemon = True
                            Speech('Ok, tocando.', lang).play()
                            thread.start()

                    except Exception as e:
                        print(e)
                        pass
            except:
                pass
def listen():
    with iris.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language='pt-BR')
    except iris.UnknownValueError:
        print("Could not understand audio")
        master_name = open('master_name', 'r').read()
        Speech('Desculpe {0}, não entendi.'.format(master_name), 'pt-br').play()
    except iris.RequestError as e:
        print("Recog Error; {0}".format(e))
    return ""

def detected_callback():
    global l
    os.system("killall eog >/dev/null 2>/dev/null") # screen on
    print('[+] Listening...')
    call(["play", "beep-07.wav", "-q"])
    l = listen()
    print(l)

    if l != '':
        func()
        call(['clear'])
        print(logo)

detector = snowboydecoder.HotwordDetector("Iris.pmdl", sensitivity=0.5, audio_gain=1)
detector.start(detected_callback)
