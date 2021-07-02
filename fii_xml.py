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
    'Nome', 'NumUnidades', 'OutrasCaractRelevantes', 'PercentVacancia', 'PercentInadimplencia', 'PercentReceitasFII',
]
for elem in root.iter('LstImovRendaAcabados'):
    for subelem in elem:
        # Reset dictionary
        tmp_dict = {}
        for imovel in subelem:
            if imovel.tag in field_list:
                tmp_dict[imovel.tag] = imovel.text
        # add to the list
        tmp_list.append(tmp_dict)

df_imoveis = pd.DataFrame(data=tmp_list, columns=field_list)
st.table(df_imoveis)


# Vencimento
st.header("Vencimento dos contratos")
columns = [
    'percentReceitaImovel', 'percentReceitasFII']
tmp_dict = {}
for elem in root.iter('DistrContratosPrazo'):
    for subelem in elem:
        if len(subelem.attrib) != 0:
            tmp_dict[subelem.tag] = subelem.attrib
        else:
            tmp_dict[subelem.tag] = 0

df = pd.DataFrame(data=tmp_dict)
st.table(df.T)
