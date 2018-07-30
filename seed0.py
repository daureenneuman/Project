# Uses the Python client library.

from apiclient import errors
from apiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload
from quickstart import service
import requests
import json
import io
from quickstartgemail  import service_gemail
import base64
from email.mime.text import MIMEText


folder_id ='120NRhCavpKVm2oLn1S35-bQiiNh5LKP7'

# def insert_file(service, folder_id, name):
#     meta_data = {
#     'name': name,
#     'parents': [folder_id], 
#      'mimeType' : 'application/vnd.google-apps.document'
#     }
  
#   file = service.files().create(body=meta_data, fields='id').execute()

#     # Uncomment the following line to print the File ID
#   return file
# calling the function three times for all kids in the right age"

# alma_file = insert_file(service, folder_id, name='alma.txt')
# alma_id = alma_file["id"]
# alma_details = service.files().get(fileId=alma_id).execute()
# alma_file_name = alma_details["name"]

# ben_file = insert_file(service, folder_id, name='ben.txt')
# ben_id = ben_file["id"]
# ben_details = service.files().get(fileId=ben_id).execute()
# ben_file_name = ben_details["name"]

# goni_file = insert_file(service, folder_id, name='goni.txt')
# goni_id = goni_file["id"]
# goni_details = service.files().get(fileId=goni_id).execute()
# goni_file_name = goni_details["name"]

# elison_file = insert_file(service, folder_id, name='elison.txt')
# elison_id = elison_file["id"]
# elison_details = service.files().get(fileId=elison_id).execute()
# elison_file_name = elison_details["name"]


#
# updatingfileId=file['id'])

# content = "this is a test to see if the update workes " +'\n'+"new line"
# print(content)

# fh  = io.BytesIO(content.encode())
# media = MediaIoBaseUpload(fh, mimetype='text/plain')
# file_meta_data = {
#     'name': 'elison.txt',
    
#      'mimeType' : 'application/vnd.google-apps.document'
#     }

# updated_file = service.files().update(
#         body=file_meta_data,
#         #uploadType = 'media',
#         fileId='12jEha6W-BPVopjKStsnQmMa1o064Z-o3_jgttD934CA',
#         #fields = fileID,
#         media_body=media).execute()

# content_new = service.files().export(fileId='12jEha6W-BPVopjKStsnQmMa1o064Z-o3_jgttD934CA', mimeType='text/plain').execute()

#################################################


def create_message(sender, to, subject, message_text):

      message = MIMEText(message_text)
      message['to'] = to
      message['from'] = sender
      message['subject'] = subject
      return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):

    message = (service.users().messages().send(userId=user_id, body=message).execute())


# message = create_message(sender= 'daureenn@gmail.com', to = 'yoav.neuman@gmail.com', subject='test123',  message_text="Sent from my python program!!!")
# send_message(service=service_gemail, user_id='me', message=message)
