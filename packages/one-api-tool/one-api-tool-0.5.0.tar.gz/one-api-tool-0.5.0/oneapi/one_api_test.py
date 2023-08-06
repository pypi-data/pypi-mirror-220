# -*- coding: utf-8 -*-
import json
from typing import Optional, Sequence, List
import openai
import anthropic
from pydantic import BaseModel
from abc import ABC, abstractmethod
import sys
import os
from typing import Callable, Optional, Sequence, List
import tiktoken
import asyncio
import logging
from openai.openai_object import OpenAIObject
sys.path.append(os.path.normpath(f"{os.path.dirname(os.path.abspath(__file__))}/.."))
from oneapi.one_api import *


if __name__ == "__main__":
    claude_config = '../../ant/config/anthropic_config_personal.json'
    openai_config = '../../ant/config/openapi_official_chenghao.json'
    azure_config = '../../ant/config/openapi_azure_config_xiaoduo_dev.json'
    config_file = openai_config
    tool = OneAPITool.from_config_file(config_file)
    prompt = '今天天气不错？'
    
    res = asyncio.run(tool.asimple_chat(prompt, stream=False))
    print(res)