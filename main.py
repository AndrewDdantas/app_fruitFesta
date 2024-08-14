import streamlit as st
from time import sleep

st.title("Bem vindo ao APP FruitFesta")

with st.form('LoginForm'):
    User = st.text_input('Usuário')

    Pass = st.text_input("Senha",type='password')

    login_button = st.form_submit_button("Login")

    if login_button:
        if Pass == st.secrets['pass'] and User == st.secrets['user']:
            st.session_state['Usuário'] = User
            st.session_state['Login'] = 'Logado'
            st.warning('Login realizado com sucesso!')
            sleep(2)
            st.switch_page('./pages/Roterizador.py')
            
        else:
            st.error("Favor verificar os dados.")