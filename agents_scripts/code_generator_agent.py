from langchain.agents import initialize_agent, AgentType, Tool
from langchain.memory import ConversationBufferMemory
from langgraph.graph import StateGraph
from langchain.chat_models import ChatOpenAI
from langchain_gigachat.chat_models import GigaChat
from langchain_gigachat.tools.giga_tool import giga_tool

from langchain.schema import HumanMessage, SystemMessage, Document, AIMessage
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.types import Command
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END, MessagesState, START
from typing import TypedDict, Optional, Literal, List, Dict
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

from pathlib import Path
import time
import datetime
import warnings
import os
import re

warnings.filterwarnings("ignore")
os.environ["GIGACHAT_CREDENTIALS"] = "Yjc1YWZhNTItMzYwYS00NmU4LTk4YjctZjU4YzAwMDIyMGJmOjJhNWE3YmVhLTAyYzctNGJhNy05NWE3LWEzY2YwNGQzYzZiNw=="

class SaveResult(BaseModel):
    status: str = Field(description="Статус сохранения файла")
    message: str = Field(description="Сообщение о результате сохранения в файл")

few_shot_examples_save = [
    {
        "request": "Можешь ли ты отправить сохранить строку 'Мама мыла раму' в файл по пути '/home/ts777/Code/agent4agents/test/test_msg.txt",
        "params": {"file_path": "/home/ts777/Code/agent4agents/test/test_msg.txt", "content": "Мама мыла раму"},
    }
]

@giga_tool(few_shot_examples=few_shot_examples_save)
def save_file(
    file_path: str = Field(description="Путь до файла, в который нужно сохранить содержимое."),
    content: str = Field(description="Информация, которую нужно сохранить в файл."),
) -> SaveResult:
    """Сохранить информацию в файл"""
    print(f"! save_file to {file_path}, content: {content}")
    try:
        match_python = re.search(r'```python\s*(.*?)\s*```', content, re.DOTALL)
        if match_python:
            content = match_python.group(1)
        with open(file_path, "w") as f:
            f.write(content)
        return SaveResult(status="OK", message="Файл успешно сохранен!")
    except Exception as e:
        return SaveResult(status="FAIL", message=f"Не удалось сохранить файл, ошибка: {e}")

class ReadResult(BaseModel):
    status: str = Field(description="Статус чтения файла")
    message: str = Field(description="Сообщение о результате чтения файла")
    result: str = Field(description="Содержимое файла")

few_shot_examples_read = [
    {
        "request": "Можешь ли ты порочитать содержимое файла '/home/ts777/Code/agent4agents/test/test_msg.txt",
        "params": {"file_path": "/home/ts777/Code/agent4agents/test/test_msg.txt"},
    }
]

@giga_tool(few_shot_examples=few_shot_examples_save)
def read_file(
    file_path: str = Field(description="Путь до файла, который нужно прочитать."),
) -> ReadResult:
    """Прочитать информацию из файла"""
    print(f"! read_file from {file_path}")
    try:
        with open(file_path, "r") as f:
            content = f.read()
        if file_path.endswith(".py"):
            content = (
                "```python\n"
                f"{content}"
                "\n```")
        return ReadResult(status="OK", message="Файл успешно прочитан!", result=content)
    except Exception as e:
        return ReadResult(status="FAIL", message=f"Не удалось прочитать файл, ошибка: {e}", result=None)

class MkdirResult(BaseModel):
    status: str = Field(description="Статус создания директории")
    message: str = Field(description="Сообщение о результате создания директории")

few_shot_examples_mkdir = [
    {
        "request": "Можешь ли ты создать директорию '/home/ts777/Code/agent4agents/test_dir",
        "params": {"path": "/home/ts777/Code/agent4agents/test/test_dir"},
    }
]

@giga_tool(few_shot_examples=few_shot_examples_mkdir)
def create_dir(
    path: str = Field(description="Путь до директории, которую нужно создать.")
) -> MkdirResult:
    """Создать директорию"""
    print(f"! create_dir {path}")
    try:
        if Path(path).exists():
            return MkdirResult(status="OK", message="Директория уже существует!")    
        Path(path).mkdir(parents=True, exist_ok=True)
        return MkdirResult(status="OK", message="Директория успешно создана!")
    except:
        return MkdirResult(status="FAIL", message="Не удалось создать директорию")

class PythonResult(BaseModel):
    status: str = Field(description="Статус запуска Python-кода")
    message: str = Field(description="Сообщение о результате запуска Python-кода.")

test_code = """```python
name = 'Ivan'
print(f'Hello, {name}!')
```python
"""

few_shot_examples_code = [
    {
        "request": f"Можешь ли ты запустить код {test_code}",
        "params": {"code_str": f"{test_code}"},
    }
]

@giga_tool(few_shot_examples=few_shot_examples_code)
def run_python_code(
    code_str: str = Field(description="Строка с Python-кодом, который нужно запустить.")
) -> PythonResult:
    """Сохранить информацию в файл"""
    print(f"! run_python_code {code_str}")
    try:
        match_python = re.search(r'```python\s*(.*?)\s*```', code_str, re.DOTALL)
        if match_python:
            code = match_python.group(1)
            result = exec(code)
        else:
            return PythonResult(status="FAIL", message="Не удалось выделить информацию из блока ```python[code]```.")
        return PythonResult(status="OK", message=f"Код успешно запущен! Результат: {result}")
    except Exception as e:
        return PythonResult(status="FAIL", message=f"Не удалось запустить код, ошибка: {e}")

with open("../sources/project_structure.md", "r") as f:
    project_structure = f.read()

with open("../sources/project_content.md", "r") as f:
    project_content = f.read()
    
with open("../tests/test_project_desc.md", "r") as f:
    project_task = f.read()


test_prompt_coder = f""" Ты - очень опытный Senior Python Developer. Ты обладаешь отличными навыками написания кода,
а также умеешь создавать директории, сохранять содержимое в файл, читать данные из файла, писать Python-код и запускать его.
Твоя рабочая директория - /home/ts777/TEST/. Работай только в ней.
Твоя задача - создать полноценное рабочее приложение для решения задачи {project_task}. 
Проверь, создан ли проект {project_name}. Если нет, то создай проект {project_name} и организуй его структуру с соответствии с этой структурой: {project_structure}.
Прочитай описание каждого раздела {project_content}. 
Выдели изменения, которые нужно внести в каждый раздел для того, чтобы он соответствовал поставленной задаче.
Составь план разработки проекта. 
Действуй шаг за шагом в соответствии с планом:
1. Выбери раздел.
2. Отредактируй код раздела в соответсвии с планом разработки.
3. Протестируй код, проверь, что он работает.
4. Запиши код в файл.
5. Переходи к следующему разделу.
6. Повторяй до тех пор, пока не заполнишь каждый раздел.
ВАЖНО: обрабатывай каждый файл последовательно, не нужно писать все сразу!
"""

llm = GigaChat(
    model="GigaChat-2-Max",
    verify_ssl_certs=False,
    profanity_check=False,
    streaming=False,
    max_tokens=8192,
    temperature=0.3,
    repetition_penalty=1.01,
    timeout=60
)

config = {"configurable": {"thread_id": "thread_id4"}}
message = {
    "messages": [HumanMessage(content=test_prompt_coder)]
}
functions = [save_file, read_file, create_dir, run_python_code]
llm_with_functions = llm.bind_tools(functions)
agent_executor = create_react_agent(llm_with_functions, 
                                    functions,
                                    checkpointer=MemorySaver()
                                   )
result = agent_executor.invoke(message, config=config)