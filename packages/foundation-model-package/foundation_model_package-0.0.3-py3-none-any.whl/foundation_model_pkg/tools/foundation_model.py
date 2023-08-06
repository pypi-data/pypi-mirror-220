from typing import List, Dict, Union, Optional
from enum import Enum

from promptflow import ToolProvider, tool
from promptflow.connections import CustomConnection
from promptflow.core.tools_manager import register_builtin_method, register_apis

from urllib.error import HTTPError
import random
import jinja2
import json
import time

try:
    from langchain.llms.azureml_endpoint import (
        AzureMLOnlineEndpoint,
        ContentFormatterBase,
        DollyContentFormatter,
        OSSContentFormatter
    )
except ImportError as e:
    raise ImportError(
        """Trouble importing langchain.
        To install, please run `pip install langchain`.
        Or upgrade to the most recent version by running `pip install langchain -U`"""
    )

def retry_with_exponential_backoff(
    func,
    initial_delay: float = 1,
    exponential_base: float = 2,
    jitter: bool = True,
    max_retries: int = 10,
    errors: tuple = (HTTPError,),
):
    """Retry a function with exponential backoff."""

    def wrapper(*args, **kwargs):
        num_retries = 0
        delay = initial_delay

        # Loop until a successful response or max_retries is hit or an exception is raised
        while True:
            try:
                return func(*args, **kwargs)

            # Retry on specific errors
            except errors as e:
                # Increment retries
                num_retries += 1

                # Check if max retries has been reached
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )

                # Increment the delay
                delay *= exponential_base * (1 + jitter * random.random())

                # Sleep for the delay
                time.sleep(delay)

            # Raise exceptions for any errors not specified
            except Exception as e:
                raise e

    return wrapper

class ModelFamily(str, Enum):
    LLAMA = "llama"
    DOLLY = "dolly"
    GPT2 = "gpt2"

class API(str, Enum):
    CHAT = "chat"
    COMPLETION = "completion"

class LlamaContentFormatter(ContentFormatterBase):

    def __init__(self, api: API, chat_history: Optional[List[Dict]] = []):
        super().__init__()
        self.api = api
        self.chat_history = chat_history

    def format_history(self, prompt: str) -> str:
        
        chat_list = []
        for interaction in self.chat_history:
            if "inputs" in interaction and "question" in interaction["inputs"]: 
                chat_list.append({"role": "user", "content": interaction["inputs"]["question"]})
            if "outputs" in interaction and "answer" in interaction["outputs"]:
                chat_list.append({"role": "assistant", "content": interaction["outputs"]["answer"]})
        
        chat_list.append({"role": "user", "content": f"\"{prompt}\""})

        return json.dumps(chat_list)
    
    def format_request_payload(self, prompt: str, model_kwargs: Dict) -> bytes:
        environment = jinja2.Environment()
        prompt=prompt.replace('"', '\\"').replace("\n","\\n")
        request_payload = ""
        
        if self.api == API.CHAT:
            history = self.format_history(prompt=prompt)
            template = environment.from_string(
                '{"input_data": {"input_string":{{history}},"parameters": {{model_kwargs}}}}'
                )
            request_payload = template.render(history=history, model_kwargs=json.dumps(model_kwargs))
        elif self.api == API.COMPLETION:
            template = environment.from_string(
                '{"input_data": {"input_string": ["{{prompt}}"], "parameters": {{model_kwargs}}}}'
            )
            request_payload= template.render(prompt=prompt, model_kwargs=json.dumps(model_kwargs))

        return str.encode(request_payload)
    
    def format_response_payload(self, output: bytes) -> str:
        return json.loads(output)["output"]

class ContentFormatterFactory:
    def get_content_formatter(model_family: ModelFamily, api: API, chat_history: Optional[List[Dict]] = []) -> ContentFormatterBase:
         
        if model_family == ModelFamily.LLAMA:
            return LlamaContentFormatter(chat_history=chat_history, api=api)
        elif model_family == ModelFamily.DOLLY:
            return DollyContentFormatter()
        elif model_family == ModelFamily.GPT2:
            return OSSContentFormatter()
        else:
            raise NotImplementedError(f"{model_family} Not Implemented Yet.")

class FoundationModel(ToolProvider):
    def __init__(self, connection: CustomConnection):
        super().__init__()
        self.connection = connection

    @staticmethod
    @retry_with_exponential_backoff
    def get_completion(llm: AzureMLOnlineEndpoint, prompt: str) -> str:
        return llm(prompt)
    
    @tool
    def foundation(
        self,
        model_family: ModelFamily,
        api: API,
        prompt: str,
        deployment_name: str,
        chat_history: Optional[List[Dict]] = [],
        model_kwargs: Optional[Dict] = {},
    ) -> str:
        
        content_formatter = ContentFormatterFactory.get_content_formatter(model_family=model_family,api=api,chat_history=chat_history)
        llm = AzureMLOnlineEndpoint(
            endpoint_url=self.connection.endpoint_url,
            endpoint_api_key=self.connection.endpoint_api_key,
            deployment_name=deployment_name,
            content_formatter=content_formatter,
            model_kwargs=model_kwargs,
        )

        return FoundationModel.get_completion(llm=llm, prompt=prompt)

register_apis(FoundationModel)

@tool
def foundation_model(
    connection: CustomConnection,
    model_family: ModelFamily,
    api: API,
    prompt: str,
    deployment_name: str,
    chat_history: Optional[List[Dict]] = [],
    model_kwargs: Optional[Dict] = {},
) -> str:
    return FoundationModel(connection).foundation(
        prompt=prompt,
        model_family=model_family,
        api=api,
        deployment_name=deployment_name,
        chat_history=chat_history,
        model_kwargs=model_kwargs
    )


register_builtin_method(foundation_model)