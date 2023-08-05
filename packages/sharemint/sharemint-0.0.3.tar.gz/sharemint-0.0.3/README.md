# sharemint
A Python Package to interact with SharePoint Folders &amp; Files

ShareMint is a Higher Level Package built on top of Office365-REST-Python-Client (https://github.com/vgrem/Office365-REST-Python-Client) with the aim of providing an easy Interaction with SharePoint Website Folders.

# Installation: 
pip install sharemint
(URL: https://pypi.org/project/sharemint/)

# Import: 
_from sharemint import ShareMint_


# Methods Supported Currently:
-------
1] file_exists(file_site_path) -> bool ( Tells if a file exists in SharePoint Folder ) 

2] download_file(file_site_path, save_folder_path) -> str ( Downloads file to local folder )

3] upload_file(device_file_path, sharepoint_folder_path) -> None ( Uploads File to a SharePoint Folder )

4] delete_file(file_path) -> None ( Deletes a file from a SharePoint Folder )

5] get_updated_files_path(created_datetime_utc: str|datetime ) -> list ( Return list of files created>=created_datetime_utc )

6] download_folder(self, site_folder_path:str, download_folder_path=str) -> str ( Downloads folder from sharepoint and returns the downloaded folder path )
