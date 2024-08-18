import streamlit as st
import pandas as pd
import services.connect as func
import services.google_connect as gcf
from io import BytesIO

st.set_page_config(
    page_title="Roterizador",
    page_icon="",
    layout="wide", 
    initial_sidebar_state="collapsed",
)

try:
    log = st.session_state['Login']
except:
    st.switch_page('./main.py')


if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

arq_st = st.empty()
arquivo = arq_st.file_uploader("Favor inserir arquivo.")

df_amostra = st.empty()

if arquivo or st.session_state.uploaded_file:
    st.session_state.uploaded_file = arquivo or st.session_state.uploaded_file

    aggDF = pd.read_excel(st.session_state.uploaded_file).groupby(['ClienteDesc','Geolocalização']).agg({
            'OV': lambda x: ', '.join(map(str, x)), 
            'Nota': lambda x: ', '.join(map(str, x)),
        'Volumes': 'sum',
        'TOTAL': 'sum'
    }).reset_index()

    aggDF['Geolocalização'] = aggDF['Geolocalização'].apply(func.ajustar_cord)
    aggDF['Geolocalização'] = aggDF['Geolocalização'].replace(r'\s+', '', regex=True)
    aggDF['Geolocalização'] = aggDF['Geolocalização'].replace('\n', '', regex=False)

    waypoints = aggDF['Geolocalização'].values.tolist()
    dist = pd.DataFrame(func.gerar_endereco(waypoints=waypoints))

    aggDF = pd.merge(aggDF, dist, 'left', left_on='Geolocalização', right_on=1)
    aggDF = aggDF.sort_values(2, ascending=False) 
    df_visu = aggDF[['OV', 'Nota', 'ClienteDesc', 'Geolocalização', 0, 2, 'Volumes', 'TOTAL']]
    df_visu.columns = ['Ordem Venda', 'Notas', 'Cliente', 'Localização', 'Endereço', 'Distância', 'Volumes', 'Total']
    df_visu['Distância'] = df_visu['Distância'].apply(lambda x: f'{int(x/1000)} Km'.replace(',','.'))
    df_visu['Volumes'] = df_visu['Volumes'].apply(lambda x: "{:,.0f}".format(x).replace(',', 'X').replace('.', ',').replace('X', '.'))
    df_visu['Total'] = df_visu['Total'].apply(lambda x: "{:,.0f}".format(x).replace(',', 'X').replace('.', ',').replace('X', '.'))

    df_amostra.dataframe(df_visu, hide_index=True)
    driver = st.selectbox('Qual motorista irá fazer a rota?', gcf.get_drivers())
    button = st.button('Gerar Romaneio')

    if button:
        df_amostra.empty()
        rotas = func.divide_em_blocos(aggDF['Geolocalização'].values.tolist(), 20)
        aggDF = aggDF[['Nota', 'OV', 'ClienteDesc', 'Volumes', 'TOTAL', 0]]
        merge = pd.merge(aggDF, pd.DataFrame(func.gerar_rota(rotas=rotas)), 'right', left_on=0, right_on='endereço')
        rotas_df = merge[['OV','ClienteDesc','localização']].fillna(0)
        last_row = gcf.get_last_row()
        merge = merge[['Nota', 'OV', 'endereço', 'distância', 'duração', 'ClienteDesc', 'Volumes', 'TOTAL']].fillna(0)

        volumes = "{:,.0f}".format(merge['Volumes'].sum()).replace(',', 'X').replace('.', ',').replace('X', '.')
        duracao = func.converter_segundos(merge['duração'].sum())
        distancia = f'{int(merge['distância'].sum()/1000)} Km'.replace(',','.')
        merge['distância'] = merge['distância'].apply(lambda x: f'{int(x/1000)} Km'.replace(',','.'))        
        merge['duração'] = merge['duração'].apply(func.converter_segundos)
        doc = func.criar_romaneio(merge, volumes, duracao, distancia,last_row)
        st.text('Romaneio gerado com sucesso, clique para baixar.')

        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        file_link = gcf.upload_arquivo(doc, f'Romaneio_{last_row}.docx')
        gcf.upload_data_package(rotas_df,file_link,driver)
        st.text(file_link)
        st.download_button(
            label="Baixar Romaneio",
            data=buffer,
            file_name=f"Romaneio_{last_row}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        arq_st.empty()
        st.session_state.uploaded_file = None
        df_amostra.empty()
        st.session_state.uploaded_file = None
