import requests
import pandas as pd
from time import sleep
from os import chdir, getcwd, listdir, system
import sys
import json

initPath = getcwd()

with open("ativos.json", "r") as fin:
    ativos = json.load(fin)


def get_api_data(ativo, function = "TIME_SERIES_DAILY", formato="csv"):
    print("Pegando dados da API")
    p0 = "https://www.alphavantage.co/query?function={}&symbol={}"
    p1 = "&interval=1min&apikey=YSGOECP6DIVEJB8V&outputsize=full&datatype={}"
    url = (p0 + p1).format(function, ativo + ".sa", formato)
    with requests.Session() as s:
        dowload = s.get(url)
        data = dowload.content.decode('utf-8')
    return data


def create_csv(ativo, data):
    chdir("./data/")
    with open(ativo + ".csv", 'w') as fin:
        fin.write(data)
    chdir(initPath)
    print("------------------------------")
    print("Gerando o csv de " + ativo.upper())


def get_csv_data(ativo, function = "TIME_SERIES_DAILY"):
    chdir("./data/")
    with open(ativo + ".csv", 'r') as fout:
        df = pd.read_csv(fout)
    chdir(initPath)
    print("Extraindo dados com pandas")
    print("------------------------------")
    return df


def sleeper(num):
    for i in range(num):
        print("." * i)
        sys.stdout.write("\033[F") # Cursor up one line
        sleep(1)


def add_ativos(lista):
    for i in range(len(lista)):
        ativo = lista[i]
        create_csv(ativo,get_api_data(ativo))
        print("------------------------------")
        #print(get_csv_data(ativo).iloc[0])
        #print("------------------------------")
        if i < len(lista) - 1:
            print("Pausa para não sobrecarregar a API")
            sleeper(20)


def write_ativos():
    with open("ativos.json", "w") as fin:
        ativos.sort()
        outputData = json.dumps(ativos, indent=4)
        fin.write(outputData)


def clean_invalid_csv():
    chdir("./data/")
    f = listdir()
    for i in range(len(ativos)-1,0,-1): #Tirando os ativos que estão na lista mas não tem csv
        ativo = ativos[i]
        if ativo + ".csv" not in f:
            ativos.remove(ativo)
    error = 'Error Message": "Invalid API call.'
    for file in f: #Removendo ativos invalidos
        with open(file, "r") as csv_file:
            data = csv_file.read()
            if error in data:
                system("rm {}".format(file))
                ativos.remove(file[:-4])
    print(ativos)
    chdir(initPath)
    write_ativos()


while True:
    print(" Adicionar ativos ou atualizar dados de todos o ativos?")
    print("          1                  2")
    resposta = input(": ")
    if resposta == "1":
        print("Quais ativos? ")
        resposta = input(": ").lower().split(" ")
        if resposta != [""]:
            ativos.extend(resposta)
            ativos = list(set(ativos))
            try:
                add_ativos(resposta)
            except ValueError:
                pass
        else:
            print("Nenhum ativo adicionado ")
    elif resposta == "2":
        add_ativos(ativos)
    else:
        break

write_ativos()
clean_invalid_csv()

