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

import json
import unicodedata
import re
from collections import Counter
from nltk.tokenize import word_tokenize
import nltk 
from nltk.tokenize import RegexpTokenizer

from Stopwords import stopwords as sw

nltk.download('punkt')

def getchar():
    a = input('').split(" ")[0]
    print(a)

def getValue(item):
    return item[1]

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

    # TODO json to dictionary
    with open('Clusters/base.json', 'r') as f:
        clusters = json.load(f)

    results = dict()
    categorias_name = []
    rows = []

    # TODO para cada linha saber quantas palavras da categoria especifica bate, ou seja,
    # iterar para cada palavra em todas as categorias e somar 1 nas posições das categorias.
    # Na proxima palvra da mesma linha, ao iterar, somar 1 à mesma posição 

    for i,row in enumerate(descricao_tokens,start=0): # iteração por linha]
        rows.append("{}:{}".format(i+2,row))
        results[i] = dict()
        #results[i]["tuple"] = j
        for word in row: # iteração por palavra na linha
            for cat_obj in clusters: # categorias gerais
                for cat_arr_str in cat_obj:
                    cat_arr = cat_obj[cat_arr_str]

                    for cat2_obj in cat_arr: # sub categorias
                        for cat2_arr_str in cat2_obj:
                            cat2_arr = cat2_obj[cat2_arr_str]

                            for cat3_obj in cat2_arr: # categoria especifica
                                for cat3_arr_str in cat3_obj:
                                    cat3_arr = cat3_obj[cat3_arr_str]

                                    for cat4_obj in cat3_arr: # palavras da categoria
                                        for cat4_arr_str in cat4_obj:
                                            cat4_arr = cat4_obj[cat4_arr_str]

                                            catname = cat_arr_str + '->' + cat2_arr_str
                                            if cat3_arr_str != 'value':
                                                catname += '->' + cat3_arr_str
                                            if cat4_arr_str != 'value':
                                                catname += '->' + cat4_arr_str

                                            if catname not in categorias_name:
                                                categorias_name.append(catname)

                                            if catname not in results[i]:
                                                results[i][catname] = 0

                                            for cat4_arr_arr in cat4_arr:
                                                if word == cat4_arr_arr[0] :
                                                    results[i][catname] += cat4_arr_arr[1]

                                            #if word in cat4_arr:
                                            #    results[i][catname] += 1

results_final = dict()
result_final_duplicated = dict()

for dict_results_final_row_index in results:
    dict_results_final_row = results.get(dict_results_final_row_index)
    row_tuple_list = dict_results_final_row.items()

    row_result = "" 
    sorted_row_result = sorted(row_tuple_list,key=getValue,reverse=True)

    if sorted_row_result[0][1] == 0:
        row_result = "outros"
        results_final[rows[dict_results_final_row_index]] = row_result
    else :
        row_result = sorted_row_result[0][0]
        i = 0
        duplicated = False
        while sorted_row_result[i][1] == sorted_row_result[i + 1][1] :
            row_result += " | " + sorted_row_result[i + 1][0]
            i += 1
            duplicated = True
        if duplicated :
            result_final_duplicated[rows[dict_results_final_row_index]] = row_result
        else :
            results_final[rows[dict_results_final_row_index]] = row_result

jsonO = json.dumps(result_final_duplicated)
print(jsonO)
'''
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
'''