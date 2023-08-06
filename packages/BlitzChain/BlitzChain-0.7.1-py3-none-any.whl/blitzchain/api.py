"""The API behind BlitzChain
"""
import json
import base64
import requests
import time
from typing import List, Dict, Any
from .splitter import WordSplitter
from .utils import chunk_documents


def get_json_response(response):
    try:
        return response.json()
    except Exception as e:
        return response.content


class Client:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://app.twilix.io/api/v1/"

    def Collection(self, collection_name: str):
        return Collection(api_key=self.api_key, collection_name=collection_name)

    def list_collections(self):
        response = requests.get(
            url=self.base_url + "collection/list",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key,
            },
        )
        return get_json_response(response)


class Collection:
    def __init__(self, api_key: str, collection_name: str):
        self.collection_name = collection_name
        self.api_key = api_key
        self.base_url = "https://app.twilix.io/api/v1/"

    def insert_objects(
        self,
        objects: list,
        fields_for_vectorization: list = None,
        split_on_field: str = None,
        wait_to_finish=True,
    ):
        if wait_to_finish:
            url = self.base_url + "collection/bulk-insert"
        else:
            raise NotImplementedError
            # url = self.base_url + "collection/async-bulk-insert"

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key,
            },
            json={
                "collection": self.collection_name,
                "objects": objects,
                "fieldsForVectorization": fields_for_vectorization,
                "splitOnField": split_on_field,
            },
        )
        if not wait_to_finish:
            return (
                response.status_code == 200,
                "Request failed - please make sure parameters are correct.",
            )
        return get_json_response(response)

    def insert_pdf(self, url: str):
        api_url = self.base_url + "collection/insert-pdf"
        print(api_url)
        response = requests.post(
            api_url,
            headers={
                # "Content-Type": "application/json",
                "Authorization": "Bearer "
                + self.api_key
            },
            json={"collection": self.collection_name, "url": url},
        )
        return get_json_response(response)

    def update_object(self, object: Dict):
        """Update an object"""
        api_url = self.base_url + "object/update"
        response = requests.post(
            api_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key,
            },
            json={"collection": self.collection_name, "object": object},
        )
        return get_json_response(response)

    def update_objects(self, objects: List[Dict], autochunk: bool=True, chunksize: int=20):
        """Update objects"""
        if autochunk:
            print("Automatically chunking updating to avoid overloading the server.")
            for chunk in chunk_documents(objects=objects, chunksize=chunksize):
                api_url = self.base_url + "collection/bulk-update"
                response = requests.post(
                    api_url,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + self.api_key,
                    },
                    json={"collection": self.collection_name, "objects": chunk},
                )
                print(get_json_response(response))
                time.sleep(3)
            return
        else:
            raise ValueError("Autochunk needs to be set to `true` for now.")
        # api_url = self.base_url + "collection/bulk-update"
        # response = requests.post(
        #     api_url,
        #     headers={
        #         "Content-Type": "application/json",
        #         "Authorization": "Bearer " + self.api_key,
        #     },
        #     json={"collection": self.collection_name, "objects": objects},
        # )
        # return get_json_response(response)

    def insert_html(self, html: str, metadata: dict = None):
        api_url = self.base_url + "collection/insert-html"
        response = requests.post(
            api_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key,
            },
            json={
                "collection": self.collection_name,
                "html": html,
                "metadata": metadata,
            },
        )
        return get_json_response(response)

    def generative_qa(
        self,
        user_input: str,
        prompt_fields: list,
        conversation_id: str = None,
        limit: int = 5,
        fields: list = None,
        include_rerank: bool = False,
        minimum_rerank_score: float = 0.7,
        include_moderation: bool = False,
    ):
        """Get an answer based on a question that you ask."""
        url = self.base_url + "collection/generative-qa"
        print(url)
        data = {
            "collection": self.collection_name,
            "userInput": user_input,
            "promptFields": prompt_fields,
            "limit": limit,
            "fields": fields,
            "includeRerank": include_rerank,
            "minimumRerankScore": minimum_rerank_score,
            "include_moderation": include_moderation,
        }
        if conversation_id:
            data["conversationID"] = conversation_id
        print(data)
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key,
            },
            json=data,
        )
        return get_json_response(response)

    def copilot(
        self,
        user_input: str,
        prompt_fields: list,
        conversation_id: str = None,
        limit: int = 5,
        fields: list = None,
        include_rerank: bool = False,
        minimum_rerank_score: float = 0.7,
        include_moderation: bool = False,
    ):
        """Get an answer based on a question that you ask."""
        url = self.base_url + "collection/generative-code-qa"
        print(url)
        data = {
            "collection": self.collection_name,
            "userInput": user_input,
            "promptFields": prompt_fields,
            "limit": limit,
            "fields": fields,
            "includeRerank": include_rerank,
            "minimumRerankScore": minimum_rerank_score,
            "includeModeration": include_moderation,
        }
        if conversation_id:
            data["conversationID"] = conversation_id
        print(data)
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key,
            },
            json=data,
        )
        return get_json_response(response)

    def list_objects(
        self,
        limit: int = 5,
        offset: int = 0,
        fields: list = None,
        where=None,
        sort: list = None,
    ):
        api_url = self.base_url + "object/list"
        print(api_url)
        response = requests.post(
            api_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key,
            },
            json={
                "collection": self.collection_name,
                "limit": limit,
                "offset": offset,
                "fields": fields,
                "where": where,
                "sort": sort,
            },
        )
        return get_json_response(response)

    def count(self):
        api_url = self.base_url + "object/count"
        response = requests.get(
            api_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key,
            },
            params={
                "collection": self.collection_name,
            },
        )
        return get_json_response(response)

    def launch_dashboard(
        self, name: str, description: str, prompt_fields: List[str] = None
    ):
        """Launch Dashboard"""
        if prompt_fields is None:
            prompt_fields = ["autoGen_content"]
        encoding = base64.urlsafe_b64encode(
            json.dumps(
                {
                    "path": "graph-weaver",
                    "name": name,
                    "collection": self.collection_name,
                    "promptFields": prompt_fields,
                    "apiKey": self.api_key,
                    "description": description,
                }
            ).encode()
        )
        token = encoding.decode()
        link = "https://ask.twilix.io/custom?token=" + token
        print(link)
