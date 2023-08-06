import os
import sys
import json
import requests
from urllib.parse import quote
import aiohttp
from . import SalesIntel, FactCheck

class Brainchain:
    def __init__(self, env: str = "prod", api_key: str = os.environ["BRAINCHAIN_API_KEY"],
                 service_url="https://brainchain--agent.modal.run/", salesintel_api_key=os.environ[
                "SALESINTEL_API_KEY"]):
        self.api_key = api_key
        self.env = env
        self.fact_check_instance = FactCheck(environment=env)
        self.sales_intel_client = SalesIntel(salesintel_api_key)
        self.environments = ["prod", "dev"]
        self.services = {
            "agent": {
                "prod": "https://brainchain--agent.modal.run/",
                "dev": "https://brainchain--agent-dev.modal.run/"
            },
            "agent-service": {
                "agent": "https://brainchain--agent-service.modal.run/agent"
            },
            "prompt-completion-service": {
                "prompting": "https://brainchain--prompt-completion-service-fastapi-app.modal.run/prompting",
                "get_pdf_title": "https://brainchain--prompt-completion-service-fastapi-app.modal.run/get_pdf_title",
                "get_pdf_authors": "https://brainchain--prompt-completion-service-fastapi-app.modal.run/get_pdf_authors"
            },
            "search": {
                "prod": "https://brainchain--search.modal.run/",
                "dev":  "https://brainchain--search-dev.modal.run/"
            },
            "electrolaser": {
                "prod": "https://brainchain--electrolaser.modal.run/",
                "dev": "https://brainchain--electrolaser-dev.modal.run/"
            },
            "weaviate_ingestion": {
                "ingest": "https://brainchain--weaviate-ingestion-fastapi-app.modal.run/ingest/",
                "query": "https://brainchain--weaviate-ingestion-fastapi-app.modal.run/query/",
                "retrieve": "https://brainchain--weaviate-ingestion-fastapi-app.modal.run/retrieve/",
                "preview": "https://brainchain--weaviate-ingestion-fastapi-app.modal.run/preview/"
            }
        }

    def fact_check(self, statement):
        return self.fact_check_instance.fact_check(statement)

    def search(self, query):
        endpoint = self.services["search"][self.env]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"query": query}
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def search_results(self, query: str, additional_pages: int = 10):
        return self.electrolaser(query, additional_pages=additional_pages)

    def electrolaser(self, query: str, additional_pages: int = 50):
        endpoint = self.services["electrolaser"][self.env]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"query": query, "additional_pages": additional_pages}
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def bullet_point_summarizer(self, text: str, prompt=""):
        endpoint = self.services["electrolaser"][self.env]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"query": query, "additional_pages": additional_pages}
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def prompt(self, q, history=[], top_p=0.0, system="You are a multi-disciplinary research assistant who formulates, validates, and figures out correct answers. Your insights are ferocious and undeniable. You expand and digest new concepts and relate them to what you already know.", model="gpt-3.5-turbo-16k", presence_penalty=0.0, frequency_penalty=0.0, n=1):
        endpoint = self.services["prompt-completion-service"]["prompting"]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"user_prompt": q, "history": history, "system_prompt": system, "model": model, "presence_penalty": float(
            presence_penalty), "frequency_penalty": float(frequency_penalty), "top_p": float(top_p)}
        response = requests.post(endpoint, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def ingest(self, url: str):
        """
        Ingest a document into Weaviate, via URL. For now, this only works with PDFs. URL has to be publicly
        accessible and point directly to the document, e.g. https://www.example.com/document.pdf.

        Note: if you want to monitor the status of your doc's ingestion, look at the Modal logs for the
        "weaviate-ingestion" app.

        :param url: URL of document to ingest.
        """
        endpoint = self.services["weaviate_ingestion"]["ingest"]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {'url': url}
        response = requests.post(endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def preview(self, class_name: str) -> dict:
        """
        Preview a Weaviate class/collection. By default, 3 items are returned (all possible fields in schema are
        returned per item).

        :param class_name: Name of class you want to preview.
        :return: Dictionary containing metadata about the class + an `objects` list containing the items.
        """
        endpoint = self.services["weaviate_ingestion"]["preview"]
        endpoint += class_name
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def query(self, concept: str, fields: str = 'title') -> dict[dict[list[dict[str, str]]]]:
        """
        Query Weaviate IngestDocs collection. By default, only titles are returned. If you want to add fields,
        simply add them as a comma-separated string. For example, fields='title,authors,chunk'.

        Example use:
        ```
        from brainchain import Brainchain
        bc = Brainchain()
        results = bc.query('water', fields='title,authors,chunk')
        ```

        :param concept: Query you want to send to Weaviate.
        :param fields: Fields you want returned from Weaviate.
        :return: Weaviate response.
        """
        endpoint = self.services["weaviate_ingestion"]["query"]
        endpoint += concept

        headers = {"Authorization": f"Bearer {self.api_key}"}
        if fields:
            endpoint += f'?fields={fields}'
            response = requests.get(endpoint, headers=headers)
        else:
            response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def retrieve(self, doc_uuid: str):
        """
        Retrieve a document from Weaviate IngestDocs collection, as stored in Amazon S3, via `doc_uuid`.

        Example use:
        ```
        from brainchain import Brainchain
        bc = Brainchain()
        bc.retrieve(doc_uuid='ed2535defea94c03b1f5bb2e7486bb17')
        >>> 'Congrats, you have downloaded your file locally!'
        ```

        :param doc_uuid: Document UUID as stored in Weaviate.
        """
        endpoint = self.services["weaviate_ingestion"]["retrieve"]
        endpoint += doc_uuid
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def obtain_title(self, text_first_page: str = None):
        endpoint = self.services["prompt-completion-service"]["get_pdf_title"]
        payload = {}

        if text_first_page:
            payload["document_text"] = text_first_page
    
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(endpoint, headers=headers, json=payload)
        content = response.content.decode('utf-8')
        return json.loads(content)

    def obtain_authors(self, text_first_page: str = None):
        endpoint =  self.services["prompt-completion-service"]["get_pdf_authors"]
        payload = {}

        if text_first_page:
            payload["document_text"] = text_first_page

        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(endpoint, headers=headers, json=payload)
        content = response.content.decode('utf-8')
        return json.loads(content)

    def summon(self, prompt, agent_type="OAMF", model="gpt-4-0613", max_tokens=2048, temperature=0, top_p=0, top_k=0.0, presence_penalty=0.0, frequency_penalty=0.0, chat_history: list = []):
        endpoint = self.services["agent-service"]["agent"]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {
            "prompt": prompt,
            "env": self.env,
            "agent_type": agent_type,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "chat_history": chat_history
        }
        response = requests.post(endpoint, headers=headers, json=params)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    async def asummon(self, prompt, agent_type="OAMF", model="gpt-4-0613", max_tokens=2048, temperature=0, top_p=0, top_k=0.0, presence_penalty=0.0, frequency_penalty=0.0, chat_history: list = []):
        endpoint = self.services["agent-service"]["agent"]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {
            "prompt": prompt,
            "env": self.env,
            "agent_type": agent_type,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "chat_history": chat_history
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, headers=headers, json=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    response.raise_for_status()

    def get_company(self, **kwargs):
        return self.sales_intel_client.get_company(**kwargs)

    def get_people(self, **kwargs):
        return self.sales_intel_client.get_people(**kwargs)

    def get_technologies(self, **kwargs):
        return self.sales_intel_client.get_technologies(**kwargs)

    def get_news(self, **kwargs):
        return self.sales_intel_client.get_news(**kwargs)
