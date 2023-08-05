from promptflow import ToolProvider, tool
from promptflow.core.tools_manager import register_builtins
from george_agent_package.tools.utils import ToolConfiguration, ToolType, Category
from promptflow.connections import SerpConnection

class SerpToolAdapter(ToolProvider):
    def __init__(
        self,
        connection: SerpConnection,
    ):
        super().__init__()
        if connection is None:
            raise Exception("connection is required")
        if connection.api_key is None:
            raise Exception("connection.api_key is required")
        self.connection = connection

    @tool #Todo: Parameterize all inputs to serp-api wrapper
    def run(self, description: str = "Search Engine Results Page API"):
        toolconfig = ToolConfiguration(
            name="serp-api",
            description = description,
            tool_type = ToolType.BUILT_IN,
            category = Category.LANGCHAIN,
            connection = self.connection,
        )
        return toolconfig


register_builtins(SerpToolAdapter)
