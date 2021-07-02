import xml.etree.ElementTree as ET
import streamlit as st
import pandas as pd
import json

tree = ET.parse('tri.xml')
root = tree.getroot()


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
