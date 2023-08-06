#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : OpenAIEmbeddings
# @Time         : 2023/7/11 18:40
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import langchain
from langchain.embeddings import OpenAIEmbeddings as _OpenAIEmbeddings

from meutils.pipe import *
from chatllm.langchain.utils import get_openai_api_key_set


class OpenAIEmbeddings(_OpenAIEmbeddings):
    """多key多线程"""

    def embed_documents(
        self, texts: List[str], chunk_size: Optional[int] = 0
    ) -> List[List[float]]:

        openai_api_key_set = get_openai_api_key_set()
        max_workers = max(len(openai_api_key_set), 1)  # todo: 防止过大，维护key队列

        if max_workers > 1:
            embeddings_map = {}
            for i, openai_api_key in enumerate(openai_api_key_set):
                kwargs = self.dict()
                kwargs['openai_api_key'] = openai_api_key
                embeddings_map[i] = _OpenAIEmbeddings(**kwargs)

            if langchain.debug:
                logger.info([e.openai_api_key for e in embeddings_map.values()])
                logger.info(f"Maximum concurrency: {max_workers * self.chunk_size}")

            def __embed_documents(arg):
                idx, texts = arg
                embeddings = embeddings_map.get(idx % max_workers, 0)
                return embeddings.embed_documents(texts)

            return (
                texts | xgroup(self.chunk_size)
                | xenumerate
                | xThreadPoolExecutor(__embed_documents, max_workers)
                | xchain_
            )

        return super().embed_documents(texts)


if __name__ == '__main__':
    e = OpenAIEmbeddings()
    print(e.embed_documents(['x']))
