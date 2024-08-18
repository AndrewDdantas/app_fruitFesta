import streamlit as st
import services.google_connect as gcf

st.set_page_config(
    page_title="Roterizador",
    page_icon="", 
    layout='wide',
    initial_sidebar_state='expanded',
)

try:
    log = st.session_state['Login']
except:
    st.switch_page('./main.py')

st.title('Romaneios')
st.subheader('Aqui você pode visualizar todos os romaneios gerados, atualizar o motorista e visualizar o arquivo novamente.',)

st.sidebar.image('./logo.png')
st.sidebar.page_link('./pages/Home_Page.py')
st.sidebar.page_link('./pages/Roterizador.py')

with st.spinner('Atualizando'):
    df = gcf.get_package()
    data = st.data_editor(df, hide_index=True)
    gcf.update_package(data)