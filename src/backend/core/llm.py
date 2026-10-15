from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
load_dotenv()
class LLMFactory:
    _llm = None
    @classmethod
    def create(cls):
        if cls._llm is None:
            cls._llm = ChatOpenAI(
                model= os.getenv("MODEL"),
                openai_api_key= os.getenv("OPENAI_API_KEY"),
                openai_api_base= os.getenv("OPENAI_API_BASE")
            )
        return cls._llm

    # GPT OOS 120b

    @staticmethod
    def llm_text_invoker(system_prompt: str, user_prompt: str):
        llm = LLMFactory.create()
        # Use literal message objects instead of a PromptTemplate 
        # to prevent LangChain from parsing `{}` as variables.
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        try:
            raw_response = llm.invoke(messages)
            
            return str(getattr(raw_response, "content", raw_response))
        except Exception as e:
            return f"LLM invocation error: {str(e)}"