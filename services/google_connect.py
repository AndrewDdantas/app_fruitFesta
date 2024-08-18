import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import streamlit as st

json = {
    "type": "service_account",
    "project_id": st.secrets['project_id'],
    "private_key_id": st.secrets['KEY'],
    "private_key": st.secrets['private_key'],
    "client_email": st.secrets['client_email'],
    "client_id": st.secrets['client_id'],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/case-693%40digital-layout-402513.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }

scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'] 
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    json, scope)
client = gs.authorize(credentials)
drive_service = build('drive', 'v3', credentials=credentials)

worksheet = client.open_by_key(st.secrets['sheet'])

route_sheet = worksheet.worksheet('ROTAS')
packing_sheet = worksheet.worksheet('ROMANEIOS')
driver_sheet = worksheet.worksheet('MOTORISTAS')


def get_drivers():
    return driver_sheet.get_values('a2:b')

def get_last_row():
    return  int(packing_sheet.get_values('a2:d')[-1][0])+1
    

def upload_arquivo(documento, nome):
    nome = str(nome)
    caminho_arquivo = f"{nome}.docx"
    
    # Salva o documento localmente
    documento.save(caminho_arquivo)

    # Configura os metadados do arquivo para o upload no Google Drive
    file_metadata = {'name': caminho_arquivo}
    media = MediaFileUpload(caminho_arquivo, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    
    # Faz o upload do arquivo
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Define as permissões de compartilhamento
    drive_service.permissions().create(
        fileId=file['id'],
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()
    
    # Gera o link de compartilhamento
    file_id = file.get('id')
    file_link = f'https://drive.google.com/file/d/{file_id}/view?usp=sharing'
    
    return file_link

def upload_data_package(routes, link):
    last_row = int(packing_sheet.get_values('a2:d')[-1][0])+1
    rotas = routes[['OV','ClienteDesc','localização']]
    rotas['KEY'] = int(packing_sheet.get_values('a2:d')[-1][0])+1
    rotas = rotas[['KEY','OV','ClienteDesc','localização']]
    rotas.loc[len(rotas)-1,'ClienteDesc'] = 'FruitFesta'
    packing_sheet.update([[int(packing_sheet.get_values('a2:d')[-1][0])+1, rotas['OV'].nunique(), '', 'andrewdantas15@gmail.com',link]],f'a{len(packing_sheet.get_values('a1:a'))+1}')
    route_sheet.update(rotas.values.tolist() , f'a{len(route_sheet.get_values('a1:a'))+1}')
