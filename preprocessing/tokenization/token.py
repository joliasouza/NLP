import re
import pandas as pd

with open('texto.txt', 'r', encoding = 'utf-8') as file:
    texto = file.read()

def tokenize(txt):
    tokens = re.split('\W+', texto)
    return tokens

tokens = tokenize(texto)

data = pd.DataFrame({'tokens': tokens})

print(data)

data.head()

data.to_csv('output.csv', index = False)