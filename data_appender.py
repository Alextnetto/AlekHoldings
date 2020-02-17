import pandas as pd
import numpy as np
import json
import seaborn as sb
import matplotlib.pyplot as plt
from os import listdir


filenames = listdir("./data")
filenames.sort()


def just_name(name):
    return name[:-4]

df_existente = pd.read_csv("final_data_revised.csv")

ativosList = list(map(just_name, filenames))


df_final = pd.DataFrame()

for ativo, file in zip(ativosList,filenames):
    print(ativo, file)
    try:
        df_ativo = pd.read_csv("./data/" + file)
        df_ativo["ativo"] = df_ativo.apply(lambda row: ativo, axis=1)
        df_ativo["variacaoDiaria"] = df_ativo.apply(lambda row: row.close - row.open, axis=1)
        df_ativo["variacaoIntra"] = df_ativo.apply(lambda row: row.high - row.low, axis=1)
        df_ativo["year"] = df_ativo.apply(lambda row: str(row.timestamp[:4]), axis=1)

        df_ativo["variacaoPercentual"] = df_ativo.apply(lambda row: 0, axis=1)
        for day in range(df_ativo.shape[0]-2, -1, -1):
            closeT0 = df_ativo["close"].iloc[day+1]
            closeT1 = df_ativo["close"].iloc[day]
            df_ativo["variacaoPercentual"].iloc[day] = (closeT1/closeT0) -  1

        indexClean = ["variacaoPercentual", "open", "close"]
        close = df_ativo["close"]
        year = [x for x in range(df_ativo.shape[0], 0, -1)]
        sb.lineplot(x=year, y=close)
        sb_plot = sb.lineplot(x=year, y=close)
        plt.savefig("./graphs/{}.png".format(ativo), dpi=260)
        plt.clf()
        df_final = df_final.append(df_ativo)
    except AttributeError:
        print("Erro!!")

columns = ["timestamp", "ativo", "open", "high", "low", "close", "volume", "variacaoPercentual", "variacaoDiaria", "variacaoIntra", "year"]
df_final = df_final[columns]
df_final = df_final.sort_values(["timestamp", "ativo"])

df_existente.append(df_final)
df_existente.drop_duplicates()

df_existente.to_csv("final_data.csv", index=False)