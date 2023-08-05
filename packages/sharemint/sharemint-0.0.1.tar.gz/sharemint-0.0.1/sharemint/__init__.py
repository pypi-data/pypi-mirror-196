from sharemint.file import File
from sharemint.folder import Folder


class ShareMint(File, Folder):
    """
    A Simple Class which helps to interact with Files and Folders stored in a SharePoint Website
    
    
    Attributes
    ----------
    :client_id:str = Client ID of the SharePoint Website

    :client_secret_key:str = Client Secret Key of the SharePoint Website
    
    :site_url:str = SharePoint Website URL


    Example
    -------
    :site_url = "https://mydomainnamexyz.sharepoint.com/sites/website_name"
    

    Client Credentials
    -----------------
    How to create Client ID and Client Secret Key for a SharePoint Website: 
    URL: https://faun.pub/quick-etl-with-python-part-1-download-files-from-sharepoint-online-40bf23711662?gi=2037ff9a2528

    
    Methods
    -------
    :file_exists(file_site_path) -> bool ( Tells if a file exists in SharePoint Folder )
    
    :download_file(file_site_path, save_folder_path) -> str ( Downloads file to local folder )

    :upload_file(device_file_path, sharepoint_folder_path) -> None ( Uploads File to a SharePoint Folder )
       
    :delete_file(file_path) -> None ( Deletes a file from a SharePoint Folder )
    
    :get_updated_files_path(created_datetime_utc: str|datetime ) -> list ( Return list of files created>=created_datetime_utc )

    :download_folder(self, site_folder_path:str, download_folder_path=str) -> str ( Downloads folder from sharepoint and returns the downloaded folder path )
    """

    def __init__(self, client_id: str, client_secret_key: str, site_url: str) -> None:
        super().__init__(client_id, client_secret_key, site_url)

    def __str__(self) -> str:
        return f"SharePoint Site - {self._site_url}"