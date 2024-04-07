from typing import Type, Optional, List
from opensearchpy import OpenSearch
from pydantic import BaseModel, Field

class OpenSearchConfig(BaseModel):
    hosts: List[str] = Field(..., description="List of hosts for OpenSearch cluster")
    http_auth: Optional[tuple] = Field(None, description="Optional HTTP auth credentials (username, password)")
    use_ssl: bool = Field(False, description="Use SSL for connection")
    verify_certs: bool = Field(False, description="Verify SSL certificates")

    @property
    def client(self) -> OpenSearch:
        """Creates and returns an instance of the OpenSearch client."""
        return OpenSearch(
            hosts=self.hosts,
            http_auth=self.http_auth,
            use_ssl=self.use_ssl,
            verify_certs=self.verify_certs,
        )

config = OpenSearchConfig(
    hosts=["https://localhost:9200"],
    http_auth=("admin", "admin"),
    use_ssl=True,
    verify_certs=False,
)