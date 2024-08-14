import streamlit as st
from time import sleep

with st.form('LoginForm'):
    col1, col2 = st.columns(2)
    col1.image('./logo.png')
    col2.title('Bem Vindo, insira seu login e senha.')
    User = col2.text_input('Usuário')

    Pass = col2.text_input("Senha",type='password')

    login_button = col2.form_submit_button("Login")

    if login_button:
        if Pass == st.secrets['pass'] and User == st.secrets['user']:
            st.session_state['Usuário'] = User
            st.session_state['Login'] = 'Logado'
            st.warning('Login realizado com sucesso!')
            sleep(2)
            st.switch_page('./pages/Roterizador.py')
            
        else:
            st.error("Favor verificar os dados.")
