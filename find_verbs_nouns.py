#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 10:05:57 2019

@author: LeticiaValle_Mac
"""

import pandas as pd
import nltk
from collections import Counter

#Approach usando a metodologia de "part of speech tagging"

def tagger(texto):

    #separa o texto em tokens de palavras
    tokens_texto = nltk.word_tokenize(texto)
        
    #usando o etiquetador para classificar os tokens do texto
    classificacao = etiquetador_unigram.tag( tokens_texto )

    return (classificacao)


if __name__ == '__main__':
    
    list_verbs = []
    list_nouns = []
    clas_list = []
    
    #definos um texto a ser classificado
    #texto = "Ja chegou o disco voador!"
    df = pd.read_csv('siconv_cgdad_v2.0_instrumentos.txt', sep="\t")
    df_descricao = df['descricao_proposta']
    
    
    #obtendo as sentenas etiquetadas do corpus mac_morpho
    sentencas_etiquetadas = nltk.corpus.mac_morpho.tagged_sents()
    
    #instanciamos um etiquetador unigram e o treinamos com as sentencas etiquetadas
    etiquetador_unigram = nltk.tag.UnigramTagger( sentencas_etiquetadas )
    
    #chama a funcao que vai dar os tags
    for n in range(0,len(df_descricao)):
        clas_list.append(tagger(df_descricao[n])) 
    
    #separa os verbos e substantivos em listas
    for row in range (len(clas_list)):
        for n in range (len(clas_list[row])):
            if ((clas_list[row][n][1] == 'V') == True):
                list_verbs.append(clas_list[row][n][0])
            
            if ((clas_list[row][n][1] == 'N') == True):
                list_nouns.append(clas_list[row][n][0])
        
    # conta a frequencia dos verbos e pega os 100 mais comuns
    counter_verbs = Counter(list_verbs).most_common(100)
    counter_nouns = Counter(list_nouns).most_common(200)
        
    print("Verbos frequentes:", counter_verbs)
    print("\n")
    print("Substantivos frequentes:", counter_nouns)
    
    #salva o conteudo em arquivo txt
    with open('verbs.txt', 'w') as f:
        for item in counter_verbs:
            string = str(item[0]) + " : "+ str(item[1])
            f.write(string)
            f.write("\n")

    with open('nouns.txt', 'w') as f:
        for item in counter_nouns:
            string = str(item[0]) + " : "+ str(item[1])
            f.write(string)
            f.write("\n")

    
        
        
