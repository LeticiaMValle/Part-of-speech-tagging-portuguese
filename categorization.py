#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:56:46 2019

@author: LeticiaValle_Mac
"""

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
from nltk.tokenize import RegexpTokenizer

from Stopwords import stopwords as sw

nltk.download('punkt')


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def pre_process(df_descricao):
    df_descricao = df_descricao.str.lower()            # letra minuscula 
    df_descricao = df_descricao.apply(remove_accents)  # remove acento
    tokenizer = RegexpTokenizer(r'\w+')
    
    for n in range(len(df_descricao)):
        df_descricao[n] = tokenizer.tokenize(df_descricao[n])   # tokeniza
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
    
    #tolenika cada comentario
    descricao_tokens = pre_process(df_descricao)


 ####################################################
    #Exemplo : linha 161 do csvsiconv_cgdad_v2.0_instrumentos.txt
    print('Texto original:', df_descricao[161])
    print('Tokens:', descricao_tokens[161])
    
    #Monta um cluster de palavras que representa a categoria
    # Construção de Quadra Poliesportiva
    #Construção, Quadra, Poliesportiva, esporte
    
    CM_Edu_Obras_Cons_QE = 0 
    CM_Edu_Obras_Ref_QE = 0 
    CM_Edu_Obras_Mod_QE = 0 
    
    cluster_Edu_Obras_Cons_QE = ['construcao', 'quadra', 'poliesportiva', 'esporte']
    cluster_Edu_Obras_Ref_QE = ['reforma', 'quadra', 'poliesportiva', 'esporte']
    cluster_Edu_Obras_Mod_QE = ['modernizacao', 'quadra', 'poliesportiva', 'esporte']
    
    for w in descricao_tokens[161]: 
        if w in cluster_Edu_Obras_Cons_QE:
            CM_Edu_Obras_Cons_QE =  CM_Edu_Obras_Cons_QE + 1
            
        if w in cluster_Edu_Obras_Ref_QE:
            CM_Edu_Obras_Ref_QE =  CM_Edu_Obras_Ref_QE + 1
        
        if w in cluster_Edu_Obras_Mod_QE:
            CM_Edu_Obras_Mod_QE =  CM_Edu_Obras_Mod_QE + 1
    
    
    list_edu_obras =  ['CM_Edu_Obras_Cons_QE', 'CM_Edu_Obras_Ref_QE', 'CM_Edu_Obras_Mod_QE']
    dictionary_edu_obras = {name: val for name, val in locals().items() if name in list_edu_obras}

    print('Dicionario:',dictionary_edu_obras)
    
    print('Categoria:', max(dictionary_edu_obras, key=dictionary_edu_obras.get))
    
    
    