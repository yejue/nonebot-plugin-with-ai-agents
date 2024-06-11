from typing import Union

from .base import BaseLLMModel
from .glm import GLMModel
from .dashscope import DashscopeModel
from .openai import OpenAIModel


LLM_TYPE = Union[BaseLLMModel, GLMModel, DashscopeModel, OpenAIModel]
