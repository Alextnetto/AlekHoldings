import json
from os import listdir, system, chdir

with open("ativos.json", "r") as fin:
    ativo = json.load(fin)

chdir("./data")
files = listdir()

print(len(files))

for file in files:
    if file[:-4] not in ativo:
        system("rm " + file)
