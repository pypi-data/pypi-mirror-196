from .ctx import CTX
import os
from office365.sharepoint.files.file import File
import traceback

class Folder(CTX):

    def __init__(self, client_id: str, client_secret_key: str, site_url: str) -> None:
        super().__init__(client_id, client_secret_key, site_url)


    def download_folder(self, site_folder_path, download_folder_path=None):
        """
        A Function which downloads SharePoint folder
        
    
        Params
        ------
        :site_folder_path:str - Folder path with respect to the Documents(Shared Documents) Folder in SharePoint Website

        :download_folder_path:str - Local Directory Folder Path where the SharePoint Folder will be downloaded
                                    Optional - If not passed, the folder will be downloaded in the Current Working Directory

                                    
        Returns
        -------
        :Local Path of the downloaded SharePoint Folder

        
        Example
        -------
        To download a folder named "XYZ" in the SharePoint Documents to local Desktop folder:
        
        :site_folder_path = "Shared Documents/XYZ"
        :download_folder_path = "C:\\Users\\MyName\\Desktop"
        """

        def save_file(file_site_path, save_folder_path):
            file_name = os.path.split(file_site_path)[-1]
            save_path = os.path.join(save_folder_path, file_name)
            response = File.open_binary(ctx, file_site_path)
            response.raise_for_status()
            with open(save_path, "wb") as local_file:
                local_file.write(response.content)


        def enum_folder(site_folder_obj, save_folder_path):
            site_folder_obj.expand(["Files", "Folders"]).get().execute_query()
            for file in site_folder_obj.files:
                save_file(file.properties['ServerRelativeUrl'],  save_folder_path)

            for child_folder in site_folder_obj.folders:
                save_folder_name = os.path.split(save_folder_path)[-1]
                folder_path = save_folder_path + child_folder.properties['ServerRelativeUrl'].split(save_folder_name)[-1]
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
                enum_folder(child_folder, save_folder_path)

        try:
            ctx = self.get_ctx()
            site_folder_obj = ctx.web.get_folder_by_server_relative_url(site_folder_path).get().execute_query()


            if download_folder_path is None:
                download_folder_path = os.getcwd()

            save_folder_path = os.path.join(download_folder_path, site_folder_path.split('/')[-1])

            if not os.path.exists(save_folder_path):
                os.mkdir(save_folder_path)

            enum_folder(site_folder_obj, save_folder_path)

            return save_folder_path

        except FileNotFoundError as e:
            print(f"Folder download failed! Please check if the folder exists. {e!r}")
            return None

        except Exception as e:
            print(f"Folder download failed! {e!r}")
            return None