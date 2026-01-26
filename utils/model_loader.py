import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


class ConfigLoader:
    def __init__(self):
        load_dotenv()
        print("Loaded config.....")
        self.config = load_config()

        if "llm" not in self.config:
            raise ValueError("Missing 'llm' section in config.yaml")

    def __getitem__(self, key):
        return self.config[key]


class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        load_dotenv()
        self.config = ConfigLoader()

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        """Load and return the LLM model."""
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")

        llm_config = self.config["llm"]

        if self.model_provider == "groq":
            print("Loading LLM from Groq..............")

            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise EnvironmentError("GROQ_API_KEY is not set")

            if "groq" not in llm_config:
                raise ValueError("Missing 'groq' config in config.yaml")

            model_name = llm_config["groq"].get("model_name")
            if not model_name:
                raise ValueError("Missing groq.model_name in config.yaml")

            return ChatGroq(
                model=model_name,
                api_key=groq_api_key,
                temperature=0.2,
            )

        elif self.model_provider == "openai":
            print("Loading LLM from OpenAI..............")

            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise EnvironmentError("OPENAI_API_KEY is not set")

            if "openai" not in llm_config:
                raise ValueError("Missing 'openai' config in config.yaml")

            model_name = llm_config["openai"].get("model_name")
            if not model_name:
                raise ValueError("Missing openai.model_name in config.yaml")

            return ChatOpenAI(
                model=model_name,
                api_key=openai_api_key,
                temperature=0.2,
            )

        else:
            raise ValueError(
                f"Unsupported model_provider '{self.model_provider}'. "
                f"Supported: groq, openai"
            )
