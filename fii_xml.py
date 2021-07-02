import xml.etree.ElementTree as ET
import streamlit as st
import pandas as pd

tree = ET.parse('tri.xml')

root = tree.getroot()

tmp_dict = {}
tmp_list = []
# Titulo
for elem in root.iter('NomeFundo'):
    st.title(elem.text)

# Quantidade de Imoveis
st.header("Imoveis")
field_list = [
    'Nome', 'NumUnidades', 'OutrasCaractRelevantes', 'PercentVacancia', 'PercentInadimplencia', 'PercentReceitasFII'
]

for elem in root.iter('LstImovRendaAcabados'):
    for subelem in elem:
        # Reset dictionary
        tmp_dict = {}
        tmp_inquilino_list = []
        for imovel in subelem:
            if imovel.tag in field_list:
                tmp_dict[imovel.tag] = imovel.text

        tmp_list.append(tmp_dict)
df_imoveis = pd.DataFrame(data=tmp_list, columns=field_list)
df_imoveis['PercentVacancia'] = pd.to_numeric(df_imoveis['PercentVacancia'])
df_imoveis['PercentInadimplencia'] = pd.to_numeric(
    df_imoveis['PercentInadimplencia'])
df_imoveis['PercentReceitasFII'] = pd.to_numeric(
    df_imoveis['PercentReceitasFII'])


df_imoveis.loc['Total'] = df_imoveis.iloc[:, 3:].sum()
df_imoveis = df_imoveis.fillna("")
st.table(df_imoveis)


# AtivosFinanceiros
st.header("Outros ativos financeiros")
ativos_lista = []

tmp_list = []
for elem in root.findall('.//AtivosFinanceiros'):
    for subelem in elem:
        ativos_lista.append(subelem.tag)

for ativo in ativos_lista:
    for elem in root.findall('.//' + ativo + '/Emissor'):
        tmp_dict = {}
        tmp_dict['Tipo'] = ativo
        for subelem in elem:
            tmp_dict[subelem.tag] = subelem.text

        tmp_list.append(tmp_dict)

df_af = pd.DataFrame(data=tmp_list)
df_af = df_af.fillna("")
df_af["Fundo/Sociedade"] = df_af["Fundo"] + df_af["Sociedade"]
del df_af["Fundo"]
del df_af["Sociedade"]
st.table(df_af)

# Vencimento
st.header("Vencimento dos contratos")
columns = [
    'percentReceitaImovel', 'percentReceitasFII']
# Reset dictionary
tmp_dict = {}
for elem in root.iter('DistrContratosPrazo'):
    for subelem in elem:
        if len(subelem.attrib) != 0:
            tmp_dict[subelem.tag] = subelem.attrib
        else:
            tmp_dict[subelem.tag] = 0

df = pd.DataFrame(data=tmp_dict)
st.table(df.T)
