from __future__ import annotations

import logging
from typing import (
    Any,
    List,
)

from pydantic import BaseModel

from transwarp_embedding_hub.embedding_hub import *

from langchain.embeddings.base import Embeddings

logger = logging.getLogger(__name__)


class TranswarpEmbeddingHub(BaseModel, Embeddings):
    """embedding hub intergration hippo_with_langchain"""

    model: str
    strategy: Any

    # 根据模型名称初始化策略
    def __init__(self, **data: Any):
        super().__init__(**data)
        self.strategy = EmbeddingHub(self.model).get_strategy()

    # 检查模型是否可用
    def check_model_active(self):
        try:
            self.embed_query("你好")
            return True  # 如果没有发生异常，说明模型可用
        except Exception as e:
            print(f"Model not available. Error: {e}")
            return False  # 如果发生了异常，说明模型不可用

    # 将文档转为一组向量
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        list = []
        for text in texts:
            list.append(self.strategy.embed_string(text))
        return list

    # 将字符串转为向量
    def embed_query(self, text: str) -> List[float]:
        return self.strategy.embed_string(text)
