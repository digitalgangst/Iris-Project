#!/usr/bin/python3
# coding: utf-8
import snowboydecoder, pyttsx3, os.path, wave, requests, os
from time import gmtime, strftime
import speech_recognition as iris
from subprocess import call
from google_speech import Speech
from bs4 import BeautifulSoup
import threading

iris_voice = "~/"

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
recognizer = iris.Recognizer()
#

def func():
    master_name = open('master_name', 'r').read()
    lang = 'pt-br'

    if ('horas') in l:
        current_time = strftime('%H:%M', gmtime())
        Speech('Agora são {0}'.format(current_time), lang).play()
    if ('música') in l:
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
                    print('AQUI ESTA >{0}< TERMINO'.format(uri))
                    Speech('Ok, tocando.', lang).play()
                    class MyThread(threading.Thread):
                        def run(self):
                            os.system("spotify --uri='spotify:track:%s#0:0.01'" % (uri))
                            pass

                    thread = MyThread()
                    thread.daemon = True
                    thread.start()

            except Exception as e:
                print(e)
                


def listen():
    with iris.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language='pt-BR')
    except iris.UnknownValueError:
        print("Could not understand audio")
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
