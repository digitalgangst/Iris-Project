#!/usr/bin/python3
# coding: utf-8

###IMPORT

import snowboydecoder, pyttsx3, os.path, wave, requests, os
import pyowm, time
import threading, re, wikipedia, json, pyowm
import speech_recognition as iris
from subprocess import call
from google_speech import Speech
from bs4 import BeautifulSoup
from newsapi.newsapi_client import NewsApiClient
from pynput.keyboard import Key, Controller
from urllib.request import urlopen
from time import gmtime, strftime, time

###Configs

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
speech_engine.setProperty('rate', 50) # noise config
print('[*] Ajustando ruído de fundo.')
recognizer = iris.Recognizer()
with iris.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)
print('[+] OK./n')
# key pressing config
keyboard = Controller()
#API Keys
newsapi = NewsApiClient(api_key='f88b2cec4f5d4e46a511706325e756de')
climaAPI = ('c5743b7436f81e619263925dca22e064')

def func():
    master_name = open('master_name', 'r').read()
    lang = 'pt-br'

    music_w = ['Toque', 'toque', 'Tocar', 'tocar', 'música', 'som']
    music_y = ['Recomenda', 'recomenda', 'Recomende', 'recomende', 'Recomendação', 'recomendação']
    wiki_w = ['Quem é', 'quem é', 'Quem foi', 'quem foi', 'O que é', 'o que é']
    news_w = ['Noticias', 'noticias', 'Notícias', 'notícias', 'Notícia', 'notícia']
    wheater_w = ['Clima', 'Previsão', 'Tempo', 'Temperatura', 'clima', 'previsão', 'tempo', 'temperatura']
    price_quote_w = ['Cotação', 'cotação', 'Valor', 'valor', 'Preço', 'preço']

    if any(x in l for x in price_quote_w):
        def search_currency(currency):
            with open('./json/moedas.json') as crrncy:
                data = json.load(crrncy)
                data = data[currency]
                def api_price(data):
                    request_api = requests.get("https://economia.awesomeapi.com.br/all")
                    price = json.loads(request_api.text)
                    price_quote = 'A cotação atual é de R$ '+price[data]['bid'][:4]
                    Speech(price_quote, lang).play()
                api_price(data)
        try:
            l = l.lower()
            currency = re.findall(r'\w+$', l)[0]
            search_currency(currency)
        except:
            error = ("Erro na API, tente novamente mais tarde.")
            print(error)
            Speech(error, lang).play()

    if any(x in l for x in wheater_w):
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        data = json.load(response)
        city1 = data['city']

        print(city1)

        
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
        current_time = strftime('%H:%M', gmtime())
        Speech('Agora são {0}'.format(current_time), lang).play()

    if any(x in l for x in music_w):
        if ('Pausar') in l or ('pausar') in l:
            keyboard.press(Key.space)
            keyboard.release(Key.space)
            Speech('Música pausada.', lang).play()
        elif ('Retomar') in l or ('retomar') in l or ('Continuar') in l or ('continuar' in l):
            Speech('Retomando música.', lang).play()
            keyboard.press(Key.space)
            keyboard.release(Key.space)
        elif ('Parar') in l or ('parar') in l:
            call(["killall", 'tizonia'])
            Speech('Música interrompida.', lang).play()
        elif any(y in l for y in music_y):
            Speech('Qual gênero de música você deseja?', lang).play()
            with iris.Microphone() as source:
                audio = recognizer.listen(source)
                try:
                    genre = recognizer.recognize_google(audio)
                    print(genre)

                    class Spotify(threading.Thread):
                        def run(self):
                            os.system("tizonia --spotify-recommendations-by-genre '%s'" % (genre))
                            pass
                    thread = Spotify()
                    thread.daemon = True
                    Speech('Ok, tocando músicas recomendadas do gênero {0}.'.format(genre), lang).play()
                    thread.start()

                except Exception as e:
                    print(e)
                    Speech('Desculpe, não consegui encontrar.', lang).play()

        else:
            try:
                s = os.system("pgrep tizonia")
                if s == 0:
                    print('Processo ativo.')
                    os.system('killall tizonia')
                    Speech('Já estou com um processo de reprodução de música ativo. Irei terminar-lo.', lang).play()
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
                                    os.system("tizonia --spotify-track-id %s" % (uri))
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
    print('[+] Listening...')
    call(["play", "beep-07.wav", "-q"])
    l = listen()
    print(l)

    if l != '':
        func()




detector = snowboydecoder.HotwordDetector("Iris.pmdl", sensitivity=0.5, audio_gain=1)
detector.start(detected_callback)
