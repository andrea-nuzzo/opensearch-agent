from typing import Type, Optional
from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field
from langchain.tools.base import BaseTool
from open_search_config import config


class IndexShowDataInput(BaseModel):
    """Input for the index show data tool."""
    index_name: str = Field(..., description="The name of the index for which the data is to be retrieved")

class IndexShowDataTool(BaseTool):
    """Tool for getting a list of entries from an OpenSearch index, helpful to figure out what data is available."""

    name = "opensearch_index_show_data"
    description = "Input is an index name, output is a JSON based string with and extract of the data of the index"

    def _run(
        self,
        index_name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Get all indices in the open search server ususally separated by a line break"""
        try:
            body = {
                "from": "0",
                "size": "5",
                "query": {"match_all": {}},
            }
            
            res = config.client.search( index=index_name, body=body)
            
            return str(res["hits"])
        except:
            return f"Could not fetch index data for {index_name}"

    args_schema: Optional[Type[BaseModel]] = IndexShowDataInput
    