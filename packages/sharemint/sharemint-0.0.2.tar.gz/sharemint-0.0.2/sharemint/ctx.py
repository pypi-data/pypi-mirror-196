from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext
import sys


class CTX:

    def __init__(self, client_id:str, client_secret_key:str, site_url:str) -> None:
        try:
            _ = ClientContext(f'{site_url}').with_credentials(ClientCredential(f'{client_id}',f'{client_secret_key}'))
        except Exception:        
            raise AttributeError('Incorrect Parameters Passed! Please check Client ID/Client Secret Key/Site URL!!')
        self._client_id = client_id
        self._client_secret_key = client_secret_key
        self._site_url = site_url

    def get_ctx(self):
        try:
            client_credentials = ClientCredential(f'{self._client_id}',f'{self._client_secret_key}')
            ctx = ClientContext(f'{self._site_url}').with_credentials(client_credentials)
            return ctx
        except Exception as e:
            print(f"ClientContext Generation Failed! Please check Client ID/Client Secret Key/Site URL {e!r}", file=sys.stderr)
            return False
        