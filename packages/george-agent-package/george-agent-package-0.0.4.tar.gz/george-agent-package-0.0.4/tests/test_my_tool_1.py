import pytest
import unittest

from promptflow.connections import CustomConnection
from george_agent_package.tools.math_tool_adapter import MathToolAdapter
from george_agent_package.tools.utils import ToolConfiguration




class TestSubTools:
    def test_math_tool(self):
        tool = MathToolAdapter()
        result = tool.run("test tool")
        assert isinstance(result, ToolConfiguration)

# Run the unit tests
if __name__ == "__main__":
    unittest.main()
