import streamlit as st

st.set_page_config(
    page_title="Roterizador",
    page_icon="", 
    layout='centered',
    initial_sidebar_state="collapsed",
)

try:
    log = st.session_state['Login']
except:
    st.switch_page('./main.py')
    
st.title("Bem-Vindo Roberto!")

st.subheader('O que você deseja fazer?')

col1, col2 = st.columns(2)

col1 = col1.container(height=150, border=True)
col1.subheader('Deseja gerar uma nova rota?')
col1.page_link('./pages/Roterizador.py')
col2 = col2.container(height=150, border=True)
col2.subheader('Romaneios')
col2.page_link('./pages/Package.py')