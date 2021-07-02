import xml.etree.ElementTree as ET
import streamlit as st
import pandas as pd
import os

# Pasta com os arquivox XML
folder_name = 'data/'

# Lista a pasta
file_list = os.listdir(folder_name)

# Cria a barra lateral com a opcao para escolher o arquivo
equity = st.sidebar.selectbox('Qual fundo?', file_list)

# Abre o arquivo XML escolhido
tree = ET.parse(folder_name + equity)
# parse do arquivo
root = tree.getroot()

# Cria as variaveis que serao usadas ao longo do codigo
tmp_dict = {}
tmp_list = []
# Titulo
for elem in root.iter('NomeFundo'):
    st.title(elem.text)

# Quantidade de Imoveis
st.header("Imoveis")

# Imoveis tem mais campos do que esses, mas no momento so esses interessam
field_list = [
    'Nome', 'NumUnidades', 'OutrasCaractRelevantes', 'PercentVacancia', 'PercentInadimplencia', 'PercentReceitasFII'
]
# iterando todos os imoveis prontos
for elem in root.iter('LstImovRendaAcabados'):
    for subelem in elem:
        # Zerando a lista temporaria e o dictionario
        tmp_dict = {}
        tmp_inquilino_list = []
        # Para cada informacao de imovel que tiver no XML vamos criar um campo no dicionario
        for imovel in subelem:
            if imovel.tag in field_list:
                tmp_dict[imovel.tag] = imovel.text
        # assim q o dicionario estiver ok, vamos adicionar ele em uma lista para ser consumida pelo pandas
        # Cada imovel gera um dicionario, e essa lista tera todos eles
        tmp_list.append(tmp_dict)

# criacao do dataframe
df_imoveis = pd.DataFrame(data=tmp_list, columns=field_list)
# Convertendo campos para numero, para somar no vinal
df_imoveis['PercentVacancia'] = pd.to_numeric(df_imoveis['PercentVacancia'])
df_imoveis['PercentInadimplencia'] = pd.to_numeric(
    df_imoveis['PercentInadimplencia'])
df_imoveis['PercentReceitasFII'] = pd.to_numeric(
    df_imoveis['PercentReceitasFII'])

# Somando os campos anteriores
df_imoveis.loc['Total'] = df_imoveis.iloc[:, 3:].sum()
# Cosmetico: preenchedo os nan com string vazia
df_imoveis = df_imoveis.fillna("")
# Plotando o grafico
st.table(df_imoveis)


# AtivosFinanceiros
st.header("Outros ativos financeiros")
# Reiniciando as variaveis
ativos_lista = []
tmp_list = []

# esperamos que o XML nao mude, mas caso ele mude, vamos sempre pegar os tipos
# de ativos financeiros diponiveis nele
for elem in root.findall('.//AtivosFinanceiros'):
    for subelem in elem:
        ativos_lista.append(subelem.tag)

# Agora vamos em todos os Ativos Financeiros e criar uma lista de dicionarios
for ativo in ativos_lista:
    for elem in root.findall('.//' + ativo + '/Emissor'):
        # zera o dicionario temporario
        tmp_dict = {}
        # Adiciona campo com o tipo do ativo financeiro
        tmp_dict['Tipo'] = ativo
        # Para cada informacao de ativo que tiver no XML vamos criar um campo no dicionario
        for subelem in elem:
            tmp_dict[subelem.tag] = subelem.text
        # assim q o dicionario estiver ok, vamos adicionar ele em uma lista para ser consumida pelo pandas
        tmp_list.append(tmp_dict)

# Criando o dataframe
df_af = pd.DataFrame(data=tmp_list)
# Cosmetico: preenchedo os nan com string vazia
df_af = df_af.fillna("")
# Dependendo do tipo do ativo ele pode ser de um Fundo ou de uma Sociedade
# Entao vamos juntar as duas informacoes em uma coluna e dropar as anteriores
if "Fundo" in df_af and "Sociedade" in df_af:
    df_af["Fundo/Sociedade"] = df_af["Fundo"] + df_af["Sociedade"]
    del df_af["Fundo"]
    del df_af["Sociedade"]
# Plot
st.table(df_af)

# Vencimento
st.header("Vencimento dos contratos")
columns = [
    'percentReceitaImovel', 'percentReceitasFII']
# Zerando o dictionario
tmp_dict = {}
# Itera a lista de vencimento de contratos
for elem in root.iter('DistrContratosPrazo'):
    for subelem in elem:
        # Se contem informacao ela será consumida, caso contratio adiciona 0
        if len(subelem.attrib) != 0:
            tmp_dict[subelem.tag] = subelem.attrib
        else:
            tmp_dict[subelem.tag] = 0
# Cria dataframe
df = pd.DataFrame(data=tmp_dict)
# Plot
st.table(df.T)

# Fim
