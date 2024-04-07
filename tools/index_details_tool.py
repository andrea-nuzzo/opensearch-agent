from typing import Type, Optional
from pydantic import BaseModel, Field
from open_search_config import config
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool

class IndexDetailsInput(BaseModel):
    """Input for the list index details tool."""
    index_name: str = Field(..., description="The name of the index for which the details are to be retrieved")

class IndexDetailsTool(BaseTool):
    """Tool for getting information about a single OpenSearch index"""

    name = "opensearch_index_show_details"
    description = "Input is an index name, output is a JSON based string with the aliases, mappings containing the field names and settings of an index"

    def _run(
        self,
        index_name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Get all indices in the open search server ususally separated by a line break"""
        try:
            alias = config.client.indices.get_alias(index=index_name)
            field_mappings = config.client.indices.get_field_mapping(
                index=index_name, fields="*"
            )
            field_settings = config.client.indices.get_settings(index=index_name)
            return str(
                {
                    "alias": alias[index_name],
                    "field_mappings": field_mappings[index_name],
                    "settings": field_settings[index_name],
                }
            )
        except:
            return f"Could not fetch index information for {index_name}"

    async def _arun(
        self,
        index_name: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("IndexDetailsTool does not support async")

    args_schema: Optional[Type[BaseModel]] = IndexDetailsInput

