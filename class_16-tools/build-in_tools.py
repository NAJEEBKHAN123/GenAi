from langchain_community.tools import DuckDuckGoSearchRun, ShellTool


#DuckDuckGoSearchRun tool

searchs = DuckDuckGoSearchRun()

result = searchs.invoke("Pak v Wi 2nd test live")

# print(result)


#ShellTool tool

shell_tool = ShellTool()
result = shell_tool.invoke("ls -l")
print(result)