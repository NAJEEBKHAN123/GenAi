from langchain_community.tools import tool, StructuredTool, BaseTool
from pydantic import BaseModel, Field
from typing import Type

#step 1
# def multiply(a, b):
#     """multiply two numbers"""
#     return a * b

# def multiply(a: int, b: int) -> int:
#     """multiply two numbers"""
#     return a * b


# @tool 

# def multiply(a: int, b: int) -> int:
#     """multiply two numbers"""
#     return a * b


# result = multiply.invoke({"a": 4, "b": 6})

# print(result)

# print(multiply.name)
# print(multiply.description)
# print(multiply.args)




### structure tools 

# class multiplyInput(BaseModel):
#     a: int = Field(required=True, description="Enter your first number")
#     b: int = Field(required=True, description="Enter your second number")

# def multiply_fun(a: int, b: int) -> int:
#     return a * b


# multiply_tools = StructuredTool.from_function(
#     func=multiply_fun,
#     name="multiply",
#     description="multiply two numbers",
#     args_schema=multiplyInput
# )

# result = multiply_tools.invoke({'a': 3, 'b': 6})
# # print(result)



###base tools

class multiplyInput(BaseModel):
    a: int = Field(required=True, description="Enter your first number")
    b: int = Field(required=True, description="Enter your second number")


class multiply_Tools(BaseTool):
    name: str = "multiply"
    description: str = 'multiply two numbers',
    args_schema: Type[BaseModel] = multiplyInput


    def _run(self, a: int, b: int) -> int:
       return a * b

multiply_tools = multiply_Tools()

result =  multiply_tools.invoke({'a': 5, 'b': 7})
print(result)



### custom toolkit

@tool

def addNum(a: int, b: int) -> int:
    """add two numbers"""
    return a + b


@tool

def multiply(a: int, b: int) -> int:
    """multiply two number"""
    return a * b


class MathToolkit:
    def get_tools(self):
        return [addNum, multiply]


toolkit = MathToolkit()
tools = toolkit.get_tools()

for tool in tools:
    print(tool.name, "=>", tool.description)