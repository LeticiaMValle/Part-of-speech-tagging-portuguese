#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 13:46:57 2019

@author: LeticiaValle_Mac
"""
import pandas as pd
#from tf_idf_pt import get_stop_words

import unicodedata
import re
from collections import Counter
from nltk.tokenize import word_tokenize
import nltk 

from Stopwords import stopwords as sw

nltk.download('punkt')


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def pre_process(df_descricao):
    df_descricao = df_descricao.str.lower()            # letra minuscula 
    df_descricao = df_descricao.apply(remove_accents)  # remove acento
    df_descricao = df_descricao.apply(word_tokenize)   # tokeniza
    
    for n in range(len(df_descricao)):
        for w in df_descricao[n]:
            if w not in stopwords:
                descricao_tokens[n].append(w)
    
    
    return (descricao_tokens)

if __name__ == '__main__':
    
    list_words = []
    
    stopwords = sw.get_stop_words()     # Carrega as stop-words
    
    df = pd.read_csv('siconv_cgdad_v2.0_instrumentos.txt', sep="\t")
    df_descricao = df['descricao_proposta']

    descricao_tokens = [[] for _ in range(len(df_descricao))]
    
    descricao_tokens = pre_process(df_descricao)

    # para as palavras-chave de cada comentario, procurar as palavras
    # terminadas em AR/ER/IR/OR/UR, AO ou ENTO 
    
    regex = r"\w+(?:cao|ar|er|ir|ento)\b"
    verbs = re.findall(regex, str(descricao_tokens))
    
    # conta a frequencia dos verbos e pega os 150 mais comuns
    counter = Counter(verbs).most_common(50)

    with open('file_verbs.txt', 'w') as f:
        for item in counter:
            string = str(item[0]) + " : "+ str(item[1])
            f.write(string)
            f.write("\n")

    
    