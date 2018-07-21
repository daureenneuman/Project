# Uses the Python client library.

from apiclient import errors
from apiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload
from quickstart import service
import requests
import json
import io
folder_id ='120NRhCavpKVm2oLn1S35-bQiiNh5LKP7'

def insert_file(service, folder_id, name):
  """Insert new file.

  Args:
    service: Drive API service instance.
    title: Title of the file to insert, including the extension.
    description: Description of the file to insert.
    parent_id: Parent folder's ID.
    mime_type: MIME type of the file to insert.
    filename: Filename of the file to insert.
  Returns:
    Inserted file metadata if successful, None otherwise.
  """
  
  meta_data = {
    'name': name,
    'parents': [folder_id], 
     'mimeType' : 'application/vnd.google-apps.document'
    }
  
  file = service.files().create(body=meta_data, fields='id').execute()

    # Uncomment the following line to print the File ID
  return file
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

content = "thios is a test to see of this fucken shit update workes who who who" +'\n'+"hjhkjhkhj"
print(content)

fh  = io.BytesIO(content.encode())
media = MediaIoBaseUpload(fh, mimetype='text/plain')
file_meta_data = {
    'name': 'elison.txt',
    
     'mimeType' : 'application/vnd.google-apps.document'
    }

updated_file = service.files().update(
        body=file_meta_data,
        #uploadType = 'media',
        fileId='12jEha6W-BPVopjKStsnQmMa1o064Z-o3_jgttD934CA',
        #fields = fileID,
        media_body=media).execute()

content_new = service.files().export(fileId='12jEha6W-BPVopjKStsnQmMa1o064Z-o3_jgttD934CA', mimeType='text/plain').execute()

