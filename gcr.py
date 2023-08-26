from __future__ import print_function
import os.path
import sys
import io
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly', 'https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly', 'https://www.googleapis.com/auth/drive.readonly']

def get_course_ids_and_names(creds, course_names=None):
    try:
        service = build('classroom', 'v1', credentials=creds)

        results = service.courses().list(courseStates=['ACTIVE']).execute()
        courses = results.get('courses', [])

        if not courses:
            print('No courses found.')
            return
        
        course_ids = []
        course_names_2 = []

        if not course_names:
            return [course['id'] for course in courses], [course['name'] for course in courses]
        else: 
            for course_name in course_names:
                for course in courses:
                    if course['name'] == course_name:
                        course_ids.append(course['id'])
                        course_names_2.append(course['name'])
            
            return course_ids, course_names_2
                    
    except HttpError as error:
        print('An error occurred: %s' % error)

def get_materials(creds, course_ids):

    try:
        service = build('classroom', 'v1', credentials=creds)

        course_materials = {}

        for course_id in course_ids:
            results = service.courses().courseWorkMaterials().list(courseId=course_id).execute()
            
            for courseWorkMaterial in results.get('courseWorkMaterial', []):
                for material in courseWorkMaterial['materials']:
                    drive_file = material['driveFile']['driveFile']
                    file_id = drive_file['id']
                    file_name = drive_file['title']
                    if not course_materials.get(course_id, None):
                        course_materials[course_id] = []
                    course_materials[course_id].append({file_id: file_name})

        return course_materials

    except HttpError as error:
        print('An error occurred: %s' % error)

def download_files(creds, materials, folders, path='./'):

    if not path:
        path = './'

    try:
        service = build('drive', 'v3', credentials=creds)

        for i, course_id in enumerate(materials):
            for material in materials[course_id]:
                for file_id, file_name in material.items():
                    request = service.files().get_media(fileId=file_id)
                    file = io.BytesIO()
                    downloader = MediaIoBaseDownload(file, request)
                    done = False
                    print(f'Downloading {file_name}...')
                    while done is False:
                        status, done = downloader.next_chunk()
                        print(F'Status: {int(status.progress() * 100)}.')
                        
                    with open(f'{path}/{folders[i]}/{file_name}', 'wb') as f:
                        f.write(file.getvalue())

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.getvalue()

def create_folder(folders, path='./'):

    if not path:
        path = './'
        
    folders_2 = []

    for folder in folders:
        folder = '_'.join([word for word in folder.split(' ') if word.isalnum()])
        folders_2.append(folder)
        if not os.path.exists(f'{path}/{folder}'):
            os.makedirs(f'{path}/{folder}')
    
    return folders_2


def main():
    parser = argparse.ArgumentParser(description="Download courses.")

    parser.add_argument("--courses", help="Path to the courses.txt file")
    parser.add_argument("--download-path", help="Path to the download destination")
    parser.add_argument("--course", help="Course name")

    args = parser.parse_args()

    course = args.course
    courses_path = args.courses
    download_path = args.download_path

    if courses_path and not os.path.exists(courses_path):
        print(f"File {courses_path} does not exist.")
        sys.exit(1)
    elif download_path and not os.path.exists(download_path):
        print(f"Path {download_path} does not exist.")
        sys.exit(1)

    courses = []

    if courses_path:
        with open(courses_path, "r") as f:
            courses = f.readlines()

        courses = [course.strip() for course in courses]
    elif course:
        courses.append(course)

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    course_ids_and_names = get_course_ids_and_names(creds, courses)
    course_ids = course_ids_and_names[0]
    course_names = course_ids_and_names[1]

    materials = get_materials(creds, course_ids)
    folders = create_folder(course_names, download_path)
    download_files(creds, materials, folders, download_path)
    
if __name__ == '__main__': 
    main()
