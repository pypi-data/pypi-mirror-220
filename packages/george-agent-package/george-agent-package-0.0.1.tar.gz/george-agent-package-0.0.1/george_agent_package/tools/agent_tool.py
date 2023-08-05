from promptflow import ToolProvider, tool
from promptflow.core.tools_manager import register_builtins
from langchain.agents import AgentType, initialize_agent
from george_agent_package.tools.utils import ToolAdapterUtils
from george_agent_package.tools.utils import ToolConfiguration
from promptflow.connections import AzureOpenAIConnection
from typing import Optional
from langchain.agents.agent import Agent
from langchain.memory import ConversationBufferMemory


class ZeroShotReactDescriptionAgent(ToolProvider):
    def __init__(
        self,
        llm_config: AzureOpenAIConnection,
    ):
        super().__init__()
        self.llm_config = llm_config

    @tool
    def run(
        self,
        query: str,
        tool1_config: ToolConfiguration,
        tool2_config: Optional[ToolConfiguration] = None,
        tool3_config: Optional[ToolConfiguration] = None,
        tool4_config: Optional[ToolConfiguration] = None,
        agent_type: Optional[AgentType] = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory: Optional[str] = "conversational-buffer-memory",
        prompt_template: Optional[str] = None,
    ):
        if not tool1_config:
            raise Exception("tool1_config is required")
        tool_configs = [tool1_config]
        if tool2_config:
            tool_configs.append(tool2_config)
        if tool3_config:
            tool_configs.append(tool3_config)
        if tool4_config:
            tool_configs.append(tool4_config)
        llm = ToolAdapterUtils.CreateAgentLLM(self.llm_config)
        tools = []
        for config in tool_configs:
            # Do something with the tool configuration
            createdtool = ToolAdapterUtils.CreateToolAdapter(config, llm)
            tools.append(createdtool)

        agent = initialize_agent(
            tools,
            llm,
            agent=agent_type,
            verbose=True,
        )
        output = agent.run(query)
        return output


register_builtins(ZeroShotReactDescriptionAgent)
