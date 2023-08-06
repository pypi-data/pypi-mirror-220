from transwarp_embedding_hub.openai import *
from transwarp_embedding_hub.pulse import *


class EmbeddingHub:
    """Factory for embedding strategy."""

    def __init__(self, model_name):
        self.model_name = model_name

    #根据参数 获取embedding策略
    def get_strategy(self):

        Strategy = {
            'openai': OpenAI(),
            'TranswarpVectorPulse': TranswarpVectorPulse()
        }.get(self.model_name)


        # 如果没有匹配的类型，则返回 'no match model'
        if not Strategy:
            raise ValueError('no match model')
        else:
            return Strategy
