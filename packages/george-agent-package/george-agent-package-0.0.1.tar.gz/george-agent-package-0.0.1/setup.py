from setuptools import find_packages, setup

setup(
    name="george-agent-package",
    version="0.0.1",
    description="This is my agent tools package",
    packages=find_packages(),
    entry_points={
        "package_tools": ["agent_tools = george_agent_package.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
)
