from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload

import pandas as pd
import os
import pickle
import dill
import zipfile
import polars
import json
import datetime
import httplib2


class gDriveExplorer:

    def __init__(self, drive_id, root_path='/root'):

        if not os.path.isabs(root_path):
            raise Exception("Please use absolute path as root path")

        root_path = os.path.normpath(root_path)

        auth.authenticate_user()

        g_auth = GoogleAuth()

        g_auth.credentials = GoogleCredentials.get_application_default()

        self.drive = GoogleDrive(g_auth)

        self.drive_service = build('drive', 'v3')

        self.explore_dict = {root_path: drive_id}

        self.drive_id = drive_id

        self.root_path = root_path

        self.current_path = root_path

        self.explorer(drive_id, self.root_path)

        user_info_service = build(
            serviceName='oauth2', version='v2',
            http=GoogleCredentials.get_application_default().authorize(httplib2.Http()))

        user_email = user_info_service.userinfo().get().execute()['email']

        self.get_file_from_id('18w2lso-tvjejb9EmhL9ra_0avuyyKiQ3', 'access_gdrive.txt')

        with open('access_gdrive.txt', "a") as fhandle:
            fhandle.write(user_email + ";" +
                          datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") +
                          '\n')

        self.update_file_from_id('1KqoLVY5A_JEOvL4jSNnkdoJMPBvGyesU', 'access_gdrive.txt')

        os.remove('access_gdrive.txt')

    def absolute_path(self, path):

        path = os.path.normpath(os.path.join(self.current_path, path))

        return path

    def chdir(self, path):

        path = self.absolute_path(path)

        if self.path_exists(path):

            self.current_path = path

        else:

            raise Exception("Path " + path + " not found. Please check")

    def list_query(self, id_, show_trash=False):

        token = ''

        file_list = []

        if show_trash:

            q = "'" + id_ + "' in parents"

        else:

            q = "'" + id_ + "' in parents and trashed=false"

        fields = 'nextPageToken, files(kind, mimeType, id, name, trashed, size)'

        while token is not None:
            list_ = self.drive_service.files().list(corpora='drive',
                                                    pageSize=1000,
                                                    supportsAllDrives=True,
                                                    includeItemsFromAllDrives=True,
                                                    driveId=self.drive_id,
                                                    q=q,
                                                    fields=fields,
                                                    pageToken=token).execute()

            file_list = file_list + list_['files']

            token = list_.get('nextPageToken', None)

        return file_list

    def explorer(self, id_, path):

        path = self.absolute_path(path)

        file_list = self.list_query(id_)

        for f in file_list:
            new_path = os.path.join(path, f['name'])

            self.explore_dict[new_path] = f['id']

    def get_id_from_path(self, path_from_base):

        levels = []

        orig_path_from_base = path_from_base

        path_from_base = self.absolute_path(path_from_base)

        path = path_from_base

        while self.explore_dict.get(path, None) is None:

            split_path = os.path.split(path)

            if split_path[0] in [self.root_path, '/']:
                raise Exception("'" + orig_path_from_base + "' not found")

            path = split_path[0]

            levels = levels + [split_path[1]]

        for p in reversed(levels):
            self.explorer(self.explore_dict[path], path)

            path = os.path.join(path, p)

        if path_from_base not in self.explore_dict.keys():
            raise Exception("'" + orig_path_from_base + "' not found")

        # if code get to this could exist and trashed or not trashed.
        # path_exists takes into account if trashed.

        if not self.is_trashed(path_from_base):

            return self.explore_dict[path_from_base]

        else:

            del self.explore_dict[path_from_base]

            raise Exception("'" + orig_path_from_base + "' not found")

    def create_folder(self, path_from_base):

        path_from_base = self.absolute_path(path_from_base)

        if not self.path_exists(path_from_base):
            root, folder_name = os.path.split(path_from_base)

            folder = self.drive.CreateFile({'title': folder_name,
                                            'mimeType': 'application/vnd.google-apps.folder',
                                            'parents': [{
                                                'kind': 'drive#fileLink',
                                                'id': self.get_id_from_path(root)

                                            }]})

            response = folder.Upload(param={'supportsAllDrives': True})

            return response

    def path_exists(self, path_from_base):

        try:

            if path_from_base == self.root_path:

                return True

            else:

                parent, name = os.path.split(self.absolute_path(path_from_base))

                files = self.list_query(self.get_id_from_path(parent), True)

                files = [x for x in files if x['name'] == name]

                if len(files) > 0:

                    return not files[0]['trashed']

                else:

                    return False

        except KeyboardInterrupt as e:

            raise e

        except:

            return False

    def is_trashed(self, path_from_base):

        path_from_base = self.absolute_path(path_from_base)

        parent, name = os.path.split(path_from_base)

        if parent == os.path.split(self.root_path)[0]:
            return False

        files = self.list_query(self.explore_dict[parent], True)

        files = [x for x in files if x['name'] == name]

        if len(files) == 0:

            return True

        elif len(files) == 1:

            return files[0]['trashed']

        else:

            id_ = self.explore_dict[path_from_base]

            file = [x for x in files if x['id'] == id_]

            if len(file) == 1:

                return file[0]['trashed']

            else:

                raise Exception("'More than 1 file for " + path_from_base + "' in drive. Please check")

    def delete_file(self, path_from_base):

        file_id = self.get_id_from_path(path_from_base)

        body = {'trashed': True}

        self.drive_service.files().update(fileId=file_id,
                                          body=body,
                                          supportsAllDrives='true').execute()

    def get_file_from_path(self, path_from_base, name=None):
        '''returns io.BytesIO object if name is None
        if name is defined, it saves the file in the 'content' local folder'''

        id_ = self.get_id_from_path(path_from_base)

        request = self.drive_service.files().get_media(fileId=id_)

        if name is not None:

            downloaded = io.FileIO(name, mode='w')

        else:

            downloaded = io.BytesIO()

        downloader_ = MediaIoBaseDownload(downloaded, request, chunksize=1024 * 1024 * 1024)

        done = False

        while done is False:
            # _ is a placeholder for a progress object that we ignore.
            # (Our file is small, so we skip reporting progress.)

            _, done = downloader_.next_chunk()

        if name is None:
            return downloaded.getvalue()

    def get_size(self, path_from_base):

        try:

            if path_from_base == self.root_path:

                return None

            else:

                parent, name = os.path.split(path_from_base)

                files = self.list_query(self.get_id_from_path(parent), False)

                files = [x for x in files if x['name'] == name]

                if len(files) > 0:

                    if 'size' in files[0].keys():

                        return eval(files[0]['size'])

                    else:

                        return None

                else:

                    raise Exception("'" + path_from_base + "' not found")

        except Exception as e:

            raise e

        # file = self.drive_service.files().get(fileId=file_id, fields='size,modifiedTime').execute()

    def get_file_from_id(self, file_id, name='temp'):

        request = self.drive_service.files().get_media(fileId=file_id)

        downloaded = io.FileIO(name, mode='w')

        downloader_ = MediaIoBaseDownload(downloaded, request, chunksize=1024 * 1024 * 1024)

        done = False

        while done is False:
            _, done = downloader_.next_chunk()

    def read_csv(self, path_from_base, is_large=True, **kwargs):

        decode = 'utf-8'

        _, name = os.path.split(path_from_base)

        if is_large:

            self.get_file_from_path(path_from_base, name)

            df_ = pd.read_csv(name, **kwargs)

            os.remove(name)

            return df_

        else:

            return pd.read_csv(io.StringIO(self.get_file_from_path(path_from_base).decode(decode)), **kwargs)

    def read_excel(self, path_from_base, is_large=True, **kwargs):

        _, name = os.path.split(path_from_base)

        if is_large:

            self.get_file_from_path(path_from_base, name)

            df_ = pd.read_excel(name, **kwargs)

            os.remove(name)

            return df_

        else:

            return pd.read_excel(self.get_file_from_path(path_from_base), **kwargs)

    def read_parquet(self, path_from_base, is_large=True, **kwargs):

        _, name = os.path.split(path_from_base)

        if is_large:

            self.get_file_from_path(path_from_base, name)

            df_ = pd.read_parquet(name, **kwargs)

            os.remove(name)

            return df_

        else:

            return pd.read_parquet(io.BytesIO(self.get_file_from_path(path_from_base)), **kwargs)

    def create_or_update_file(self, path_from_base):

        root, name = os.path.split(path_from_base)

        file_metadata = {
            'name': name
            #   ,'mimeType': 'text/csv'
        }

        media = MediaFileUpload(name,
                                chunksize=-1,
                                # mimetype=format,
                                resumable=True)

        try:

            file_id = self.get_id_from_path(path_from_base)

            response = self.drive_service.files().update(fileId=file_id,
                                                         body=file_metadata,
                                                         media_body=media,
                                                         supportsAllDrives='true').execute()

        except KeyboardInterrupt as e:

            raise e

        except:

            folder_id = self.get_id_from_path(root)

            file_metadata['parents'] = [folder_id]

            response = self.drive_service.files().create(body=file_metadata,
                                                         media_body=media,
                                                         supportsAllDrives='true').execute()

        return response

    def update_file_from_id(self, file_id, file_name):

        file_metadata = {
            'name': file_name
            #   ,'mimeType': 'text/csv'
        }

        media = MediaFileUpload(file_name,
                                chunksize=-1,
                                # mimetype=format,
                                resumable=True)

        response = self.drive_service.files().update(fileId=file_id,
                                                     body=file_metadata,
                                                     media_body=media,
                                                     supportsAllDrives='true').execute()

    def persist(self, func, path_from_base, **kwargs):

        root, name = os.path.split(path_from_base)

        func(name, **kwargs)

        self.create_or_update_file(path_from_base)

        os.remove(name)

    def to_csv(self, df, path_from_base, **kwargs):

        root, name = os.path.split(path_from_base)

        df.to_csv(name, **kwargs)

        self.create_or_update_file(path_from_base)

        os.remove(name)

    def to_excel(self, df, path_from_base, **kwargs):

        root, name = os.path.split(path_from_base)

        df.to_excel(name, **kwargs)

        self.create_or_update_file(path_from_base)

        os.remove(name)

    def to_dill(self, func_list, path_from_base, **kwargs):

        root, name = os.path.split(path_from_base)

        with open(name, 'wb') as dill_file:
            dill.dump(func_list, dill_file, **kwargs)

        self.create_or_update_file(path_from_base)

        os.remove(name)

    def to_pickle(self, func_list, path_from_base, **kwargs):

        root, name = os.path.split(path_from_base)

        with open(name, 'wb') as f:
            pickle.dump(func_list, f, **kwargs)

        self.create_or_update_file(path_from_base)

        os.remove(name)

    def to_parquet(self, df, path_from_base, **kwargs):

        root, name = os.path.split(path_from_base)

        df.to_parquet(name, **kwargs)

        self.create_or_update_file(path_from_base)

        os.remove(name)

    def to_excel_sheets(self, dic, path_from_base, **kwargs):

        root, name = os.path.split(path_from_base)

        with pd.ExcelWriter(name) as writer:
            for i in dic.keys():
                dic[i].to_excel(writer, sheet_name=i, **kwargs)

        self.create_or_update_file(path_from_base)

        os.remove(name)

    def show_contents(self, path_from_base):

        id_ = self.get_id_from_path(path_from_base)

        file_list = self.list_query(id_, )

        return [item['name'] for item in file_list]

    def listdir(self, path_from_base=None):

        if path_from_base is None:
            path_from_base = self.current_path

        return self.show_contents(path_from_base)

    def get_csv_from_zip(self, path_from_base, file_name, **kwargs):

        zip_reader = zipfile.ZipFile(io.BytesIO(self.get_file_from_path(path_from_base)))

        df = pd.read_csv(zip_reader.open(file_name), **kwargs)

        return df

    def download_file_to_local(self, path_from_base):

        root, name = os.path.split(path_from_base)

        self.get_file_from_path(path_from_base, name)

    def scan_csv(self, path_from_base, **kwargs):

        _, name = os.path.split(path_from_base)

        self.get_file_from_path(path_from_base, name)

        ldf_ = polars.scan_csv(name, **kwargs)

        return ldf_

    def collect(self, polars_lazy_frame, **kwargs):

        file_name = json.loads(polars_lazy_frame.write_json())['CsvScan']['path']

        df_ = polars_lazy_frame.collect(**kwargs)

        os.remove(file_name)

        return df_