import yaml
import os
from pathlib import Path
from enum import Enum
from typing import Optional
from promptflow.connections import CustomConnection, SerpConnection
import urllib.error
import json
import ssl
import openai
from promptflow.connections import (
    AzureOpenAIConnection,
    SerpConnection,
    CustomConnection,
)
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import Tool
from langchain.chat_models import AzureChatOpenAI
from serpapi import GoogleSearch
from langchain.schema import BaseLanguageModel


def collect_tools_from_directory(base_dir) -> dict:
    tools = {}
    for f in Path(base_dir).glob("**/*.yaml"):
        with open(f, "r") as f:
            tools_in_file = yaml.safe_load(f)
            for identifier, tool in tools_in_file.items():
                tools[identifier] = tool
    return tools


def list_package_tools():
    """List package tools"""
    yaml_dir = Path(__file__).parents[1] / "yamls"
    return collect_tools_from_directory(yaml_dir)


class Category(Enum):
    LANGCHAIN = "langchain"
    AZUREML = "azureml"


class ToolType(Enum):
    BUILT_IN = "built-in"


class ToolConfiguration:
    def __init__(
        self,
        name: str,
        description: str,
        tool_type: ToolType,
        category: Category,
        connection = None,
    ):
        self.name = name
        self.description = description
        self.tool_type = tool_type
        self.category = category
        self.connection = connection

class ToolAdapterUtils:
    @staticmethod
    def substitute_prompt(json_template: str, prompt: str) -> str:
        # Load the JSON template
        template_data = json.loads(json_template)
        
        # Substitute the {prompt} placeholder with the value
        substituted_data = json.dumps(template_data).replace("{prompt}", str(prompt))
        
        return substituted_data

    

    @staticmethod
    def CreateAgentLLM(config: AzureOpenAIConnection, temperature: float = 0.7, model_name: str = "gpt-35-turbo") -> BaseLanguageModel:
        openai.api_base = config.api_base
        openai.api_type = config.api_type
        openai.api_version = config.api_version
        # todo: parameterize model_name and temperature
        llm = AzureChatOpenAI(client=openai.ChatCompletion,
                              temperature= temperature, 
                              deployment_name=model_name,
                              model_name=model_name, 
                              openai_api_key=config.api_key,
                              openai_api_base=config.api_base,
                              openai_api_type=config.api_type,
                              openai_api_version=config.api_version)
        return llm
    
    @staticmethod
    def CreateToolAdapter(config: ToolConfiguration, llm: BaseLanguageModel):
        if config.tool_type == ToolType.BUILT_IN:
            # Switch case on the NAME property
            if config.name == "serp-api":
                if not isinstance(config.connection, SerpConnection):
                    raise Exception(
                        "Connection type for Serp Tool Adapter must be SerpConnection"
                    )
                run = SerpAPIWrapper(search_engine = GoogleSearch, serpapi_api_key=config.connection.api_key).run
                tool = Tool(
                    name=config.name, func=run, description=config.description
                )
                return tool
            elif config.name == "llm-math":
                run = LLMMathChain(llm=llm, verbose=True).run
                tool = Tool(
                    name=config.name, func=run, description=config.description
                )
                return tool
            else:
                return ToolAdapterUtils.generate_mir_tool(config)
        else:
            raise Exception("Unknown tool.")

    @staticmethod
    def generate_mir_tool(config):
        def allowSelfSignedHttps(allowed):
            # bypass the server certificate verification on client side
            if (
                allowed
                and not os.environ.get("PYTHONHTTPSVERIFY", "")
                and getattr(ssl, "_create_unverified_context", None)
            ):
                ssl._create_default_https_context = ssl._create_unverified_context
        if not isinstance(config.connection, CustomConnection):
            raise Exception(
                "Connection type for MIR tool type must be CustomConnection"
            )
        url = config.connection.URL
        key = config.connection.KEY
        deployment = config.connection.DEPLOYMENT

        def func(prompt: str) -> str:
            allowSelfSignedHttps(True)
            data = ToolAdapterUtils.substitute_prompt(json_template=config.connection.input_schema, prompt=prompt)
            #data = {"prompt": prompt}
            body = str.encode(data)
            if not key:
                raise Exception("A key should be provided to invoke the endpoint")
            headers = {
                "Content-Type": "application/json",
                "Authorization": ("Bearer " + key),
                "azureml-model-deployment": deployment,
            }
            req = urllib.request.Request(url, body, headers)
            try:
                response = urllib.request.urlopen(req)
                result = response.read()
            except urllib.error.HTTPError as error:
                print("The request failed with status code: " + str(error.code))

                # Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure
                print(error.info())
                print(error.read().decode("utf8", "ignore"))
                raise error
            final_response = json.loads(result)
            return json.dumps(final_response)

        tool = Tool(
            name=config.name,
            func=func,
            description=config.description,
        )
        return tool