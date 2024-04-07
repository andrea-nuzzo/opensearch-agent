import json
from pydantic.v1 import BaseModel, Field
import tiktoken
from langchain.tools import StructuredTool
from open_search_config import config

class SearchToolInput(BaseModel):
    """Input for the index show data tool."""

    index_name: str = Field(
        ..., description="The name of the index for which the data is to be retrieved"
    )
    query: str = Field(..., description="The ElasticSearch JSON query used to filter all hits. Should use the _source field if possible to specify required fields.")
    from_: int = Field(
        ..., description="The record index from which the query will start"
    )
    size: int = Field(
        ...,
        description="How many records will be retrieved from the ElasticSearch query",
    )


def open_search(
    index_name: str,
    query: str,
    from_: int = 0,
    size: int = 5,
):
    """Executes a specific query on an ElasticSearch index and returns all hits or aggregation results"""
    size = min(50, size)
    encoding = tiktoken.encoding_for_model("gpt-4-0125-preview")
    try:
        full_dict: dict = json.loads(query)
        query_dict = None
        aggs_dict = None
        sort_dict = None
        if "query" in full_dict:
            query_dict = full_dict["query"]
        if "aggs" in full_dict:
            aggs_dict = full_dict["aggs"]
        if "sort" in full_dict:
            sort_dict = full_dict["sort"]
        if query_dict is None and aggs_dict is None and sort_dict is None:
            query_dict = full_dict
        if query_dict is None and aggs_dict is not None:
            size = 200

        final_res = ""
        retries = 0
        
        body = {
        }

        if query_dict is not None:
            body["query"] = query_dict
        if aggs_dict is not None:
            body["aggs"] = aggs_dict
        if sort_dict is not None:
            body["sort"] = sort_dict
                
        while retries < 100:
            print("Attempt number:", retries + 1)
            try:
                res = config.client.search(
                    index=index_name,
                    from_=from_,
                    size=size,
                    body=body
                )
            except Exception as e:
                print("Error message:", str(e))

            if query_dict is None and aggs_dict is not None:
                final_res = str(res['aggregations'])
            else:
                final_res = str(res['hits'])
            tokens = encoding.encode(final_res)
            retries += 1
            if len(tokens) > 6000:
                size -= 1
            else:
                return final_res
            
    except Exception as e:        
        msg = str(e)
        print("Error message:", msg)
        return msg

def create_search_tool():
    return StructuredTool.from_function(open_search, name="opensearch_index_search_tool", args_schema=SearchToolInput)

