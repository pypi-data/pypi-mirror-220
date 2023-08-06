from azure.identity import DefaultAzureCredential, ManagedIdentityCredential, VisualStudioCodeCredential, AzureCliCredential, ChainedTokenCredential
from azure.core.credentials import AccessToken
from azure.core.exceptions import ClientAuthenticationError
from typing import Any, Protocol, Union, List


class MSCredential(Protocol):
    def get_token(self, *scopes: str, **kwargs: Any) -> AccessToken:
        ...

    def close(self) -> None:
        ...


class WrappedCredential:
    """Wrapper for Azure credentials. Uses ChainedTokenCredential to chain multiple credentials.
    options with default values:
            def_credential:bool = False - (don't) use DefaultAzureCredential
            mi_credential:bool = True - use ManagedIdentityCredential
            ac_credential:bool = True - use AzureCliCredential
            vs_credential:bool = True - use VisualStudioCodeCredential"""

    def __init__(
            self,
            def_credential: bool = False,
            mi_credential: bool = True,
            ac_credential: bool = True,
            vs_credential: bool = True,
    ) -> None:
        """Initialize WrappedCredential object"""
        self.credential: Union[ChainedTokenCredential, None] = []
        self.cred_list: List[MSCredential] = []

        if def_credential:
            self.cred_list.append(DefaultAzureCredential())
        if mi_credential:
            self.cred_list.append(ManagedIdentityCredential())
        if ac_credential:
            self.cred_list.append(AzureCliCredential())
        if vs_credential:
            self.cred_list.append(VisualStudioCodeCredential())

        if len(self.cred_list) > 0:
            self.credential = ChainedTokenCredential(*self.cred_list)

    def get_token(self, *scopes: str, **kwargs: Any) -> AccessToken:
        """Get token from credential"""
        if self.credential:
            return self.credential.get_token(*scopes, **kwargs)
        else:
            raise ClientAuthenticationError("No credentials available")

    def close(self) -> None:
        """Close credential"""
        if self.credentials:
            self.credential.close()
            self.credential = None


class Az_login:
    """Performs login, Executes a query to a single or multiple workspaces, returns resultset """

    def __init__(self) -> None:
        self.creds = None

    def login(self):
        try:
            if self.creds == None:
                micredential = ManagedIdentityCredential()  # DefaultAzureCredential()
                azcredential = AzureCliCredential()
                vscredential = VisualStudioCodeCredential()
                self.creds = ChainedTokenCredential(
                    azcredential, micredential, vscredential)
        finally:
            if (self.creds == None):
                raise Exception('Unable to perform login to azure')
            return self.creds
