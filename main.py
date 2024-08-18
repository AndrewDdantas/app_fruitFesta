import streamlit as st
from time import sleep

st.set_page_config(
    page_title="Roterizador",
    page_icon="",
    layout="centered", 
    initial_sidebar_state="collapsed",
)

with st.form('LoginForm'):
    st.title('Bem Vindo, insira seu login:')
    col1, col2 = st.columns(2)
    col1.image('./logo.png')
    User = col2.text_input('Usuário')

    Pass = col2.text_input("Senha",type='password')

    login_button = col2.form_submit_button("Login")

    if login_button:
        if Pass == st.secrets['pass'] and User.lower() == st.secrets['user']:
            st.session_state['Usuário'] = User
            st.session_state['Login'] = 'Logado'
            st.warning('Login realizado com sucesso!')
            sleep(2)
            st.switch_page('./pages/Home_Page.py')
            
        else:
            st.error("Favor verificar os dados.")
