from abc import ABC, abstractmethod


class BaseEmbedding(ABC):
    """Interface for embedding models."""

    # 检查模型是否可用
    def check_model_active(self, **kwargs) -> bool:
        """
                检查模型是否可用。

                参数:
                    自定义

                返回:
                    bool: 如果模型可用，则返回 True；否则，返回 False。
        """
        pass

    # 将字符串转为向量
    def embed_string(self, text: str, **kwargs):
        """
                将字符串转换为向量。

                参数:
                    text (str): 要转换的文本。
                    自定义

                返回:
                    list: 文本的嵌入向量。
        """
        pass
