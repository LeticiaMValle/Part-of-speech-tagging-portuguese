import pandas as pd

def getchar():
    a = input('').split(" ")[0]
    print(a)

filter_table = pd.read_csv('siconv_cgdad_v2.0_instrumentos.txt', sep="\t")
to_filter_table = pd.read_excel('AcaoOrcamentaria.xlsx')
result_final = pd.DataFrame(columns=to_filter_table.columns)

for id_proposta in filter_table['id_proposta']:
    append = pd.DataFrame(to_filter_table[to_filter_table['id_proposta'] == id_proposta].values,columns=to_filter_table.columns)
    
    if id_proposta not in result_final['id_proposta'].values:
        result_final = result_final.append(append,ignore_index=True)
        
result_final = result_final.drop_duplicates('id_proposta')
result_final.to_csv(r'csv_final.csv')
