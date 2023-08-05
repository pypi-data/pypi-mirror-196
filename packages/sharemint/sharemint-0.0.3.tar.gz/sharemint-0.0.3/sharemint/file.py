from .ctx import CTX
from .errors import UnknownErrorOccured
import os
import sys
import traceback
from requests.exceptions import HTTPError
from dateutil import parser
from datetime import datetime
from dateutil.parser import ParserError
import logging


class File(CTX):

    def __init__(self, client_id: str, client_secret_key: str, site_url: str) -> None:
        super().__init__(client_id, client_secret_key, site_url)


    def file_exists(self, file_site_path:str) -> bool:
        """
        A Function to check if a file exists in SharePoint   
    
        Params
        ------
        :file_site_path:str - File Path with respect to the Documents(Shared Documents) Folder in SharePoint Website

                                    
        Returns
        -------
        :True(if file exits) or False

        
        Example
        -------
        To check if a file named "myfile.txt" exists in "Test" folder which is present in SharePoint Documents Folder:
        
        :file_site_path = "Shared Documents/Test/myfile.txt"
        """

        try:
            ctx = self.get_ctx()
            if not ctx:
                raise UnknownErrorOccured()
            file_url = f"{ self._site_url.split('.com')[-1] }/{file_site_path}"
            try:
                _ = ctx.web.get_file_by_server_relative_path(file_url).get().execute_query()
            except:
                return False
            return True
        except UnknownErrorOccured:
            logging.error('ClientContext Generation Failed!')
            return False
        except Exception as e:
            logging.error(f'Unknown Error Occured! {e!r}')
            return False
        

    def download_file(self, file_site_path:str, save_folder_path:str=None):
        """
        A Function to download file from a SharePoint Folder   
    
        Params
        ------
        :file_site_path:str - File Path with respect to the Documents(Shared Documents) Folder in SharePoint Website
        
        :save_folder_path:str - Local Device Folder path where the file will be downloaded
                                Optional - If not passed the file will be downloaded in the Current Working Directory

                                                            
        Returns
        -------
        :Downloaded File Local Path

        
        Example
        -------
        To download a file named "myfile.txt" from "Test" folder which is present in SharePoint Documents Folder to Desktop:
        
        :file_site_path = "Shared Documents/Test/myfile.txt"
        :save_folder_path = "C:\\Users\\MyName\\Desktop"
        """

        try:

            file_name = os.path.split(file_site_path)[-1]
            
            save_path = os.path.join(save_folder_path, file_name) if save_folder_path else os.path.join('.', file_name)

            ctx = self.get_ctx()
            if ctx:
                pass
            else:
                raise Exception('ClientContext Generation Failed! Please check Client ID/Client Secret Key/Site URL')
            
            file_url = f"{ self._site_url.split('.com')[-1] }/{file_site_path}"

            with open(save_path, "wb") as local_file:
                _ = ctx.web.get_file_by_server_relative_path(file_url).download(local_file).execute_query()
            return save_path
        except FileNotFoundError:
            logging.error('Download Failed, Please check if the Folder Exists!')
            traceback.print_exc()
        except HTTPError:
            logging.error('Download Failed, Please check the SharePoint file path. The path should be relative to SharePoint Documents Folder, E.g. Shared Documents/Folder/myfile.txt')
            traceback.print_exc()
        except Exception as e:
            logging.error(f"Download Failed, {e!r}", file=sys.stderr)
            traceback.print_exc()
            logging.debug(traceback.format_exc())
        finally:
            return None


    def upload_file(self, device_file_path:str, sharepoint_folder_path:str):
        """
        A Function to upload file to a SharePoint Folder   
    
        Params
        ------
        :device_file_path:str - Local File Path of the file which is to be Uploaded
        
        :sharepoint_folder_path:str - SharePoint Folder path where the file will be uploaded
                                                            
        Returns
        -------
        :None

        
        Example
        -------
        To upload a file named "myfile.txt" from local Desktop folder to SharePoint Documents Folder named "Test":
        
        :device_file_path = "C:\\Users\\MyName\\Desktop\\myfile.txt"
        :sharepoint_folder_path = "Shared Documents/Test"
        """

        try:
            
            file_name = os.path.split(device_file_path)[-1]
            upload_folder_path = sharepoint_folder_path + '/' + file_name

            with open(device_file_path, 'rb') as content_file:
                file_content = content_file.read()

            dir, name = os.path.split(upload_folder_path)
            ctx = self.get_ctx()
            _ = ctx.web.get_folder_by_server_relative_url(dir).upload_file(name, file_content).execute_query()

            try:
                site_file_path = sharepoint_folder_path + '/' + file_name
                status = self.file_exists(site_file_path)
                if not status:
                    raise UnknownErrorOccured()
            except Exception:
                raise UnknownErrorOccured()
            logging.info('File Uploaded Successfully!')
        except FileNotFoundError:
            logging.error('File Upload Failed, Please check the File Path!')
            traceback.print_exc()
        except HTTPError:
            logging.error('File Upload Failed, Please check the SharePoint Folder path. The path should be relative to SharePoint Documents Folder, E.g. Shared Documents/Folder')
            traceback.print_exc()
        except UnknownErrorOccured:
            logging.error('File Upload Failed, Something Went Wrong... Please try after some time!')
        except Exception as e:
            logging.error('Check if the Folder exists in SharePoint!')
            logging.error(f"File Upload Failed, {e!r}", file=sys.stderr)


    def delete_file(self, file_path:str):
        """
        A Function to delete a file to a SharePoint Folder   
    
        Params
        ------
        :file_path:str - Local File Path of the file which is to be Uploaded
                                                                    
        Returns
        -------
        :None
        

        Example
        -------
        To delete a file named "myfile.txt" from SharePoint Documents Folder named "Test":
        
        :file_path = "Shared Documents/Test/myfile.txt"
        """

        try:
            file_site_path = f"{self._site_url.split('.com')[-1]}/{file_path}"
            if not self.file_exists(file_path):
                raise UnknownErrorOccured()

            ctx = self.get_ctx()
            file = ctx.web.get_file_by_server_relative_url(file_site_path)
            file.delete_object().execute_query()
            logging.info('File Deleted Successfully!')
        except UnknownErrorOccured:
            logging.error('File Delete Failed, Please check if File Exists!!')
        except Exception as e:
            logging.error(f"File Delete Failed, {e!r}", file=sys.stderr)
            


    def get_updated_files_path(self, created_datetime_utc=None):
        """
        A Function to get a list of SharePoint Relative file path of all the files in Sharepoint Documents Folder
    
        
        Params
        ------
        :created_datetime_utc:str|datetime - Optional: If passed, path of all the files created after created_datetime_utc will be returned 
                                             Note: Filter will be applied based on UTC TimeZone

                                                                                                    
        Returns
        -------
        :List of SharePoint Files (Server Relative URL Path)
        

        Example
        -------        
        :created_datetime_utc = "2023-01-01 00:00:01"
        """
        try:
            date_string_iso = None
            iso_string_format = "%Y-%m-%dT%H:%M:%SZ"
            if created_datetime_utc is not None:
                if isinstance(created_datetime_utc, str):
                    date_string_iso = parser.parse(created_datetime_utc, fuzzy=True).strftime(iso_string_format)
                elif isinstance(created_datetime_utc, datetime):
                    date_string_iso = parser.parse(created_datetime_utc, fuzzy=True).strftime(iso_string_format)
            
            ctx = self.get_ctx()
            if not ctx:
                raise UnknownErrorOccured('ClientContext Generation Failed! Please check Client ID/Client Secret Key/Site URL')
                
            file_path_list = []
            lib_title = "Documents"
            lib = ctx.web.lists.get_by_title(lib_title)
            if date_string_iso:
                site_items = lib.items.order_by("Created desc").filter(f"Created ge datetime'{date_string_iso}'").select(["FileRef", 'FileSystemObjectType']).get().execute_query()
            else:
                site_items = lib.items.select(["FileRef", 'FileSystemObjectType']).get().execute_query()

            for item in site_items:
                file_url, item_type = item.properties.get("FileRef"), item.properties.get("FileSystemObjectType")
                if item_type == 0:
                    file_path_list+=['/'.join(file_url.split('/')[3:])]
            return file_path_list
        except ParserError as e:
            logging.error(f"Operation Failed! Date String Passed doesn't contain valid DateTime {e!r}")
            traceback.print_exc()
        except UnknownErrorOccured as e:
            logging.error(f"Operation Failed! {e!r}")
            traceback.print_exc()
        except Exception as e:
            logging.error(f"Operation Failed! Got Unknown Error {e!r}")
            traceback.print_exc()
        return []