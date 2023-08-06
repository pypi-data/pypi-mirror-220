import sys

from transwarp_hippo_api.hippo_client import *
from transwarp_hippo_api.hippo_type import *
import logging
from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.base import VectorStore, VST
from typing import Any, Iterable, List, Optional, Tuple
import random

logger = logging.getLogger(__name__)

# 默认连接
DEFAULT_HIPPO_CONNECTION = {
    "host": "172.18.128.48",
    "port": "8922",
}


class Hippo(VectorStore):
    def __init__(
            self,
            embedding_function: Embeddings,
            table_name: str = "zdc_test_langchain01",
            database_name: str = "default",
            connection_args: Optional[dict[str, Any]] = None,
            index_params: Optional[dict] = None,
            drop_old: Optional[bool] = False,
    ):

        # TODO hippo 暂时不需要 default_search_params

        # self.default_search_params = {
        #     "IVF_FLAT": {"metric_type": "L2", "params": {"nprobe": 10}},
        #     "IVF_SQ8": {"metric_type": "L2", "params": {"nprobe": 10}},
        #     "IVF_PQ": {"metric_type": "L2", "params": {"nprobe": 10}},
        #     "HNSW": {"metric_type": "L2", "params": {"ef": 10}},
        #     "RHNSW_FLAT": {"metric_type": "L2", "params": {"ef": 10}},
        #     "RHNSW_SQ": {"metric_type": "L2", "params": {"ef": 10}},
        #     "RHNSW_PQ": {"metric_type": "L2", "params": {"ef": 10}},
        #     "IVF_HNSW": {"metric_type": "L2", "params": {"nprobe": 10, "ef": 10}},
        #     "ANNOY": {"metric_type": "L2", "params": {"search_k": 10}},
        #     "AUTOINDEX": {"metric_type": "L2", "params": {}},
        # }

        self.embedding_func = embedding_function
        self.table_name = table_name
        self.database_name = database_name
        self.index_params = index_params

        # In order for a collection to be compatible, pk needs to be auto'id and int
        self._primary_field = "pk"
        # In order for compatiblility, the text field will need to be called "text"
        self._text_field = "text"
        # In order for compatbility, the vector field needs to be called "vector"
        self._vector_field = "vector"
        self.fields: list[str] = []
        # Create the connection to the server
        if connection_args is None:
            connection_args = DEFAULT_HIPPO_CONNECTION
        self.hc = self._create_connection_alias(connection_args)
        self.col = Optional[HippoTable]

        # print(f"database_name: {self.database_name}")

        # 如果collection存在则删除
        try:
            if self.hc.get_table(self.table_name, self.database_name) and drop_old:
                self.hc.delete_table(self.table_name, self.database_name)
        except:
            pass

        try:
            if self.hc.get_table(self.table_name, self.database_name):
                self.col = self.hc.get_table(self.table_name, self.database_name)
        except:
            pass

        # 初始化向量数据库
        self._init()

    def _create_connection_alias(self, connection_args: dict) -> HippoClient:
        """Create the connection to the Hippo server."""
        # Grab the connection arguments that are used for checking existing connection
        host: str = connection_args.get("host", None)
        port: int = connection_args.get("port", None)

        # Order of use is host/port, uri, address
        if host is not None and port is not None:
            if "," in host:
                hosts = host.split(',')
                given_address = ','.join([f'{h}:{port}' for h in hosts])
            else:
                given_address = str(host) + ":" + str(port)
        else:
            logger.debug("Missing standard address type for reuse atttempt")

        try:
            logger.info(f"create HippoClient[{given_address}]")
            return HippoClient([given_address])
        except Exception as e:
            logger.error("Failed to create new connection")
            raise e

    def _init(
            self, embeddings: Optional[list] = None, metadatas: Optional[list[dict]] = None
    ) -> None:
        logger.info(f"init ...")
        # print(f"init...{self.database_name}")
        if embeddings is not None:
            logger.info(f"create collection")
            self._create_collection(embeddings, metadatas)
        self._extract_fields()
        self._create_index()
        # self._create_search_params()

    def _create_collection(
            self, embeddings: list, metadatas: Optional[list[dict]] = None
    ) -> None:

        # Determine embedding dim
        dim = len(embeddings[0])
        logger.debug(f"[_create_collection] dim: {dim}")
        fields = []

        # Create the primary key field
        fields.append(
            HippoField(self._primary_field, True, HippoType.INT64)
        )

        # Create the text field

        fields.append(
            HippoField(self._text_field, False, HippoType.STRING)
        )

        # Create the vector field, supports binary or float vectors
        # TODO 二进制向量类型待开发
        fields.append(
            HippoField(self._vector_field, False, HippoType.FLOAT_VECTOR, type_params={"dimension": dim})
        )
        # TODO Determine metadata schema hippo中没有类似于 milvus 中 infer_dtype_bydata 数据类型推断的方法,所以目前将非向量类型的数据均转化为string类型。

        if metadatas:
            #     # Create FieldSchema for each entry in metadata.
            for key, value in metadatas[0].items():
                #         # Infer the corresponding datatype of the metadata
                if isinstance(value, list):
                    value_dim = len(value)
                    fields.append(HippoField(key, False, HippoType.FLOAT_VECTOR, type_params={"dimension": value_dim}))
                else:
                    fields.append(HippoField(key, False, HippoType.STRING))

        logger.debug(f"[_create_collection] fields: {fields}")

        # Create the collection
        # TODO number_of_shards, number_of_replicas 参数调整方式待开发 默认均为1
        self.hc.create_table(name=self.table_name, fields=fields, database_name=self.database_name, number_of_shards=1,
                             number_of_replicas=1)
        # print(f"create_collection:{self.table_name},{self.database_name}")
        self.col = self.hc.get_table(self.table_name, self.database_name)
        logger.info(f"[_create_collection] : create table {self.table_name} in {self.database_name} successfully")
        # print(f"[_create_collection] : create table {self.table_name} in {self.database_name} successfully")

    def _extract_fields(self) -> None:
        """Grab the existing fields from the Collection"""
        if isinstance(self.col, HippoTable):
            schema: list[HippoField] = self.col.schema
            logger.debug(f"[_extract_fields] schema:{schema}")
            for x in schema:
                self.fields.append(x.name)
            logger.debug(f"04 [_extract_fields] fields:{self.fields}")
            # print(f"04 [_extract_fields] fields:{self.fields}")

    # TODO 目前只针对列名为 vector 的字段（自动创建的向量字段）进行索引校验，其他向量类型的列需要自行创建索引
    def _get_index(self) -> Optional[dict[str, Any]]:
        """Return the vector index information if it exists"""
        if isinstance(self.col, HippoTable):
            table_info = self.hc.get_table_info(self.table_name, self.database_name).get(self.table_name, {})
            embedding_indexes = table_info.get('embedding_indexes', None)
            if embedding_indexes is None:
                return None
            else:
                for x in self.hc.get_table_info(self.table_name, self.database_name)[self.table_name][
                    'embedding_indexes']:
                    logger.debug(f"[_get_index] embedding_indexes {embedding_indexes}")
                    if x['column'] == self._vector_field:
                        return x

    # TODO 只能为self._vector_field 字段创建索引
    def _create_index(self) -> None:
        """Create a index on the collection"""

        if isinstance(self.col, HippoTable) and self._get_index() is None:
            if self._get_index() is None:
                if self.index_params is None:
                    self.index_params = {
                        "index_name": "langchain_auto_create",
                        "metric_type": MetricType.L2,
                        "index_type": IndexType.IVF_FLAT,
                        "nlist": 10,
                    }

                    # print(self.col.tbl_meta)
                    # print(self.col.schema)

                    print(self.col.create_index(
                        self._vector_field,
                        self.index_params['index_name'],
                        self.index_params['index_type'],
                        self.index_params['metric_type'],
                        nlist=self.index_params['nlist'],
                    ))
                    logger.debug(self.col.activate_index(self.index_params['index_name']))
                    logger.info("create index successfully")

    # TODO hippo暂时不需要

    # def _create_search_params(self) -> None:
    #     """Generate search params based on the current index type"""
    #     index_type = IndexType.IVF_FLAT
    #     metric_type = MetricType.L2
    #     self.search_params["index_type"] = index_type
    #     self.search_params["metric_type"] = metric_type
    #     print(f"[_create_search_params] search_params:{self.search_params}")

    # TODO hippo 不支持load方法

    # def _load(self) -> None:
    #     """Load the collection if available."""
    #     from pymilvus import Collection
    #
    #     if isinstance(self.col, Collection) and self._get_index() is not None:
    #         self.col.load()

    def add_texts(
            self,
            texts: Iterable[str],
            metadatas: Optional[List[dict]] = None,
            timeout: Optional[int] = None,
            batch_size: int = 1000,
            **kwargs: Any,
    ) -> List[str]:

        """
                添加文本到集合。

                参数:
                texts: 一个可迭代对象，包含要添加的文本。
                metadatas: 一个可选的字典列表，每个字典包含与一个文本相关联的元数据。
                timeout: 可选的超时时间，以秒为单位。
                batch_size: 每批插入的文本数量，默认为1000。
                **kwargs: 其他可选参数。

                返回值:
                一个字符串列表，包含已插入文本的唯一标识符。

                注意:
                如果集合尚未创建，此方法将创建一个新的集合。
        """

        if texts == "":
            logger.debug("Nothing to insert, skipping.")
            return []
        texts = list(texts)

        logger.debug(f"[add_texts] texts: {texts}")

        try:
            embeddings = self.embedding_func.embed_documents(texts)
        except NotImplementedError:
            embeddings = [self.embedding_func.embed_query(x) for x in texts]

        if len(embeddings) == 0:
            logger.debug("Nothing to insert, skipping.")
            return []

        logger.debug(f"[add_texts] len_embeddings:{len(embeddings)}")

        # 如果还没有创建collection则创建collection
        if not isinstance(self.col, HippoTable):
            self._init(embeddings, metadatas)

        # Dict to hold all insert columns
        # TODO hippo不支持自增类型的主键，索引在这里只能选择生成随机数的方式来生成主键，有风险
        insert_dict: dict[str, list] = {
            self._primary_field: [random.randint(0, sys.maxsize) for _ in range(len(embeddings))],
            self._text_field: texts,
            self._vector_field: embeddings,
        }
        # print(f"[add_texts] insert_dict:{insert_dict}")
        logger.debug(f"[add_texts] metadatas:{metadatas}")
        logger.debug(f"[add_texts] fields:{self.fields}")
        if metadatas is not None:
            for d in metadatas:
                for key, value in d.items():
                    if key in self.fields:
                        insert_dict.setdefault(key, []).append(value)

        logger.debug(insert_dict[self._primary_field])
        logger.debug(insert_dict[self._text_field])

        # Total insert count
        vectors: list = insert_dict[self._vector_field]
        total_count = len(vectors)

        logger.debug(f"[add_texts] total_count:{total_count}")
        for i in range(0, total_count, batch_size):
            # Grab end index
            end = min(i + batch_size, total_count)
            # Convert dict to list of lists batch for insertion
            insert_list = [insert_dict[x][i:end] for x in self.fields]
            try:
                res = self.col.insert_rows(insert_list)
                logger.info(f"05 [add_texts] insert {res}")
            except Exception as e:
                logger.error(
                    "Failed to insert batch starting at entity: %s/%s", i, total_count
                )
                raise e
        return [""]


    def similarity_search(
            self,
            query: str,
            k: int = 4,
            param: Optional[dict] = None,
            expr: Optional[str] = None,
            timeout: Optional[int] = None,
            **kwargs: Any,
    ) -> list[HippoResult]:

        """
        在查询字符串上执行相似度搜索。

        参数:
        query (str): 要搜索的文本。
        k (int, optional): 要返回的结果数量。 默认为4。
        param (dict, optional): 指定索引的搜索参数。默认为无。
        expr (str, optional): 过滤表达式。默认为无。
        timeout (int, optional): 超时错误前的等待时间。 默认为无。
        kwargs: Collection.search() 的关键字参数。

        返回值:
        List[Document]: 搜索的文档结果。
        """
        if self.col is None:
            logger.debug("No existing collection to search.")
            return []
        res = self.similarity_search_with_score(
            query=query, k=k, param=param, expr=expr, timeout=timeout, **kwargs
        )
        return [doc for doc, _ in res]

    def similarity_search_with_score(
            self,
            query: str,
            k: int = 4,
            param: Optional[dict] = None,
            expr: Optional[str] = None,
            timeout: Optional[int] = None,
            **kwargs: Any,
    ) -> List[Tuple[Document, float]]:

        """
        在查询字符串上执行搜索，并返回带有分数的结果。

        参数:
        query (str): 正在搜索的文本。
        k (int, optional): 要返回的结果数量。 默认为4。
        param (dict): 指定索引的搜索参数。默认为无。
        expr (str, optional): 过滤表达式。默认为无。
        timeout (int, optional): 超时错误前的等待时间。 默认为无。
        kwargs: Collection.search() 的关键字参数。

        返回值:
        List[float], List[Tuple[Document, any, any]]:
        """
        if self.col is None:
            logger.debug("No existing collection to search.")
            return []

        # Embed the query text.
        embedding = self.embedding_func.embed_query(query)

        ret = self.similarity_search_with_score_by_vector(
            embedding=embedding, k=k, param=param, expr=expr, timeout=timeout, **kwargs
        )
        return ret

    # TODO hippo暂时不需要 parm这个参数，等待后续开发
    def similarity_search_with_score_by_vector(
            self,
            embedding: List[float],
            k: int = 4,
            param: Optional[dict] = None,
            expr: Optional[str] = None,
            timeout: Optional[int] = None,
            **kwargs: Any,
    ) -> List[Tuple[Document, float]]:

        """
        在查询字符串上执行搜索，并返回带有分数的结果。

        参数:
        embedding (List[float]): 正在搜索的嵌入向量。
        k (int, optional): 要返回的结果数量。 默认为4。
        param (dict): 指定索引的搜索参数。默认为无。
        expr (str, optional): 过滤表达式。默认为无。
        timeout (int, optional): 超时错误前的等待时间。 默认为无。
        kwargs: Collection.search() 的关键字参数。

        返回值:
        List[Tuple[Document, float]]: 结果文档和分数。
        """
        if self.col is None:
            logger.debug("No existing collection to search.")
            return []

        # if param is None:
        #     param = self.search_params

        # Determine result metadata fields.
        output_fields = self.fields[:]
        output_fields.remove(self._vector_field)

        # Perform the search.
        logger.debug(f"search_field:{self._vector_field}")
        logger.debug(f"vectors:{[embedding]}")
        logger.debug(f"output_fields:{output_fields}")
        logger.debug(f"topk:{k}")
        logger.debug(f"dsl:{expr}")

        res = self.col.query(
            search_field=self._vector_field,
            vectors=[embedding],
            output_fields=output_fields,
            topk=k,
            dsl=expr
        )
        # Organize results.
        logger.debug(f"[similarity_search_with_score_by_vector] res:{res}")
        score_col = self._text_field + "%scores"
        ret = []
        count = 0
        for items in zip(*[res[0][field] for field in output_fields]):
            # 使用字典推导从字段名和对应的值创建元数据字典
            meta = {field: value for field, value in zip(output_fields, items)}
            # 创建 Document 对象，并从元数据字典中移除文本字段
            doc = Document(page_content=meta.pop(self._text_field), metadata=meta)
            # 获取对应的分数
            logger.debug(f"[similarity_search_with_score_by_vector] res[0][score_col]:{res[0][score_col]}")
            score = res[0][score_col][count]
            count += 1
            # 创建元组并添加到结果列表
            ret.append((doc, score))

        return ret

    @classmethod
    def from_texts(
            cls,
            texts: List[str],
            embedding: Embeddings,
            metadatas: Optional[List[dict]] = None,
            table_name: str = "default",
            database_name: str = "default",
            connection_args: dict[str, Any] = DEFAULT_HIPPO_CONNECTION,
            index_params: dict = None,
            search_params: dict = {},
            drop_old: bool = False,
            **kwargs: Any) -> VST:

        """
                从给定的文本创建一个 VST 类的实例。

                参数:
                texts (List[str]): 要添加的文本列表。
                embedding (Embeddings): 用于文本的嵌入模型。
                metadatas (List[dict], optional): 每个文本的元数据字典列表。默认为无。
                table_name (str): 表名。默认为 "zdc_test_langchain01"。
                database_name (str): 数据库名。默认为 "default"。
                connection_args (dict[str, Any]): 连接参数。默认为 DEFAULT_HIPPO_CONNECTION。
                index_params (dict): 索引参数。默认为无。
                search_params (dict): 搜索参数。默认为空字典。
                drop_old (bool): 是否丢弃旧的集合。默认为 False。
                kwargs: 其他参数。

                返回值:
                VST: VST 类的实例。
        """



        logger.info("00 [from_texts] init the class of Hippo")
        # 创建vector_db
        vector_db = cls(
            embedding_function=embedding,
            table_name=table_name,
            database_name=database_name,
            connection_args=connection_args,
            index_params=index_params,
            drop_old=drop_old,
            **kwargs,
        )
        logger.debug(f"[from_texts] texts:{texts}")
        logger.debug(f"[from_texts] metadatas:{metadatas}")
        # 向vector_db插入文本
        vector_db.add_texts(texts=texts, metadatas=metadatas)
        return vector_db
