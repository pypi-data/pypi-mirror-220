from promptflow import ToolProvider, tool
from promptflow.core.tools_manager import register_builtins
from george_agent_package.tools.utils import ToolConfiguration, ToolType, Category
from promptflow.connections import CustomConnection

INPUT_SCHEMA_TEMPLATE = '{"prompt": "{prompt}"}'

class MirToolAdapter(ToolProvider): 
    def __init__(
        self,
        connection: CustomConnection,  # TODO: Update this to the correct type MirConnection
    ):
        super().__init__()
        if connection is None:
            raise Exception("connection is required")
        if connection.URL is None:
            raise Exception("connection.URL is required")
        if connection.KEY is None:
            raise Exception("connection.KEY is required")
        if connection.DEPLOYMENT is None:
            raise Exception("connection.DEPLOYMENT is required")
        self.connection = connection

    @tool
    def run(self, tool_name: str, tool_description: str, input_schema: str = INPUT_SCHEMA_TEMPLATE):
        # Do something with the tool configuration
        self.connection["input_schema"] = input_schema
        toolconfig = ToolConfiguration(
            name = tool_name,
            description = tool_description,
            tool_type = ToolType.BUILT_IN,
            category = Category.LANGCHAIN,
            connection = self.connection,
        )
        return toolconfig


register_builtins(MirToolAdapter)
