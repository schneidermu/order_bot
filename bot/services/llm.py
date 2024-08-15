from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama


llm = ChatOllama(
    model="llama3.1",
    temperature=0.1,
    base_url="http://0.0.0.0:11434",
    keep_alive=-1,
    num_thread=8,
)

system_prompt = """Ты полезный ассистент анализирующий текстовые заметки и \
формирующий из них поручения для сотрудников.

Заметки:

{input}

Поручения:"""

prompt = PromptTemplate.from_template(system_prompt)

chain = prompt | llm
