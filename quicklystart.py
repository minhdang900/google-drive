from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES='https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'
FOLDER_ID='1rBksB-fgUf_C_v8PXQcv5Iej_cFPuda6'

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    # upload file to drive
    writeToGDrive(service, 'upload_test', '/Users/dangtran/Documents/Workspace/google-drive/upload_test.xlsx', FOLDER_ID)
    # Call the Drive v3 API
    # results = service.files().list(
    #     pageSize=10, fields="nextPageToken, files(id, name)").execute()
    # items = results.get('files', [])

    # if not items:
    #     print('No files found.')
    # else:
    #     print('Files:')
    #     for item in items:
    #         print(u'{0} ({1})'.format(item['name'], item['id']))

def writeToGDrive(service, filename,source,folder_id):
    file_metadata = {'name': filename,'parents': [folder_id],
    'mimeType': 'application/vnd.google-apps.spreadsheet'}
    media = MediaFileUpload(source,
                            mimetype='application/vnd.ms-excel', resumable=True)
    fileID = fileInGDrive(service, filename)
    if(not fileID):
        file = service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print('Upload Success!')
        print('File ID:', file.get('id'))
        return file.get('id')
    else:
        print('File ID', fileID)
        file_metadata = {'name': filename,
            'mimeType': 'application/vnd.google-apps.spreadsheet'}
        file = service.files().update(body=file_metadata,
                                            media_body=media,
                                            fileId=fileID).execute()


def fileInGDrive(service, filename):
    results = service.files().list(q="mimeType='application/vnd.google-apps.spreadsheet' and name='"+filename+"' and trashed = false and parents in '"+FOLDER_ID+"'",fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if items:
        return items[-1]['id']
    else:
        return False

if __name__ == '__main__':
    main()