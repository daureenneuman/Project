# Uses the Python client library.

from apiclient import errors
from apiclient.http import MediaFileUpload
from quickstart import service

def insert_file(service, title, description, parent_id, mime_type, filename):
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
  # media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
  body = {
    'name': title,
    'description': description,
    'mimeType': mime_type
  }
  # Set the parent folder.
  if parent_id:
    body['parents'] = [{'id': parent_id}]

  try:
    file = service.files().create(
        body=body,
        ).execute()

    # Uncomment the following line to print the File ID
    # print 'File ID: %s' % file['id']

    return file
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)
    return None

insert_file(service, "try", "try", "0Bw0ZnNgr3knbY0NfVlIyNFlHRlk", "application/vnd.google-apps.document", "try")