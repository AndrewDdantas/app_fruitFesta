import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'] 
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    './credentials.json', scope)
client = gs.authorize(credentials)
drive_service = build('drive', 'v3', credentials=credentials)

worksheet = client.open_by_key('1k_KoUupNSWdSG8ExFtxR-LnTSJ0Dr8c_XDks1SowL7Q')

route_sheet = worksheet.worksheet('ROTAS')
packing_sheet = worksheet.worksheet('ROMANEIOS')
driver_sheet = worksheet.worksheet('MOTORISTAS')


def get_drivers():
    return driver_sheet.get_values('a2:b')

def upload_arquivo(documento, nome):


    # Configura os metadados do arquivo para o upload no Google Drive
    file_metadata = {'name': documento}
    media = MediaFileUpload(documento, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    
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

def upload_data_package(routes):
    try:
        rotas = routes[['OV','ClienteDesc','localização']]
        rotas['KEY'] = int(packing_sheet.get_values('a2:d')[-1][0])+1
        rotas = rotas[['KEY','OV','ClienteDesc','localização']]
        rotas.loc[len(rotas)-1,'ClienteDesc'] = 'FruitFesta'
        packing_sheet.update([[int(packing_sheet.get_values('a2:d')[-1][0])+1, rotas['OV'].nunique(), '', 'andrewdantas15@gmail.com']],f'a{len(packing_sheet.get_values('a1:a'))+1}')
        route_sheet.update(rotas.values.tolist() , f'a{len(route_sheet.get_values('a1:a'))+1}')
        return len(route_sheet.get_values('a1:a'))+1
    except:
        return Exception
