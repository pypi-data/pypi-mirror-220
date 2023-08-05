from promptflow import tool, ToolProvider
from promptflow.core.tools_manager import register_builtins
from george_agent_package.tools.utils import ToolConfiguration
from george_agent_package.tools.utils import ToolType, Category


class MathToolAdapter(ToolProvider):
    def __init__(self):
        super().__init__()

    @tool
    def run(self, description: str = "useful in solving math problems"):
        # Do something with the tool configuration
        toolconfig = ToolConfiguration(
            name="llm-math",
            description=description,
            tool_type=ToolType.BUILT_IN,
            category=Category.LANGCHAIN,
        )
        return toolconfig


register_builtins(MathToolAdapter)
