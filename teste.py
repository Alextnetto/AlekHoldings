import subprocess
import json
from os import system
from time import sleep

with open("ativos.json", "r") as fin:
    ativos = json.load(fin)


#Usar para saber o ID das janelas
#while True:
#    system('xdotool getmouselocation')
#    sleep(3)

chromeID = '35651624'
nautilusID = '31457287'

for ativo in ativos:
    system('xdotool windowactivate {}'.format(chromeID))
    sleep(1)
    system('xdotool key "F2"')
    sleep(2)
    system('xdotool type --delay 215 "{}" '.format(ativo))#Pesquisa o ativo
    sleep(1)
    system('xdotool key "KP_Enter"')
    sleep(1)
    system('xdotool mousemove 1746 109')
    sleep(1)
    system('xdotool click 1')#Fez dowload
    sleep(10)
    system('xdotool windowactivate {}'.format(nautilusID))#Vai para os dowloads
    system('xdotool mousemove 700 130')
    system('xdotool click 1')
    system('xdotool key "F2"')
    sleep(0.25)
    system('xdotool type --delay 215 "{}" '.format(ativo))#Renomeia
    system('xdotool key "KP_Enter"')
    sleep(5)
