
# -*- coding: utf-8 -*-
import pandas as pd
import morfeusz2
import pickle

morf = morfeusz2.Morfeusz()
data = pd.read_excel("wykaz_miejscowosci.xlsx")

values = data[u'Nazwa miejscowości '].values.tolist()
values_lexical = []

for value in values:
    try:
        value = value.lower()
        lexical = morf.analyse(value)
        lst_word = -1
        name = []
        
        for i in lexical:
            if i[0] == lst_word:
                continue

            lst_word = i[0]
            v = i[2][1]
            v = v.split(":")[0]
            v = v.lower()
            name.append(v)

        name = " ".join(name)
        if u"góra" in name:
            print(name)
        values_lexical.append(name)
    except:
        print("błąd")
        continue

lexical_set = set(values_lexical)

with open("cities.pickle", "w") as f:
    pickle.dump(lexical_set, f)

