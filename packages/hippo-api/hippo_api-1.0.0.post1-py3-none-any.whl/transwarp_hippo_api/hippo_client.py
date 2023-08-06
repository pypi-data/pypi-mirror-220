import json
from pickle import EMPTY_DICT

import requests
from dataclasses import dataclass, asdict, field
from types import MappingProxyType
from typing import Optional

from requests import Response
from urllib.parse import urlparse

from transwarp_hippo_api.conn_mgr import globalConnManager, ConnState, check_hippo_host_port_alive
from transwarp_hippo_api.hippo_type import *


def EMPTY_DICT():
    return {}


''' 定义HippoField数据类用于存储字段信息'''


@dataclass
class HippoField:
    name: str  # 字段名
    is_primary_key: bool  # 是否为主键
    data_type: HippoType  # 数据类型
    type_params: dict = field(default_factory=EMPTY_DICT)  # 类型参数，使用EMPTY_DICT作为默认工厂函数


''' 定义HippoConn类用于管理和操作Hippo连接 '''


class HippoConn:
    def __init__(self, hippo_host_ports: list[str], username: str = 'shiva', pwd: str = 'shiva'):
        # parsed_url = urlparse(hippo_url)
        # hippo_host_port = f"{parsed_url.scheme}://{parsed_url.netloc}"
        self.hippo_host_ports = hippo_host_ports  # 初始化连接的host和port
        for hp in self.hippo_host_ports:  # 检查每一个host和port的状态，如果连接正常则加入到全局连接管理器中
            if check_hippo_host_port_alive(hp):
                globalConnManager.add_conn(hp, ConnState.ACTIVE)
            else:
                globalConnManager.add_conn(hp, ConnState.FAILED)

        self.username = username  # 设置用户名
        self.pwd = pwd  # 设置密码

    # 定义默认的json请求头，只包含内容类型为'application/json'
    default_json_header = MappingProxyType({
        'Content-Type': 'application/json',
    })

    # 定义一个方法，用于生成hippo的URL
    def make_hippo_url(self, conn_host_port: str):
        return conn_host_port + "/hippo/v1"

    # 定义一个put请求的方法，用于发送put请求到hippo服务器
    def put(self, component_url, js_data: str, headers=default_json_header):
        url_base = "http://" + globalConnManager.get_available_conn_from_view(self.hippo_host_ports)
        url = self.make_hippo_url(url_base) + component_url
        return requests.put(url, auth=(self.username, self.pwd), headers=headers, json=js_data)

    # 定义一个delete请求的方法，用于发送delete请求到hippo服务器
    def delete(self, component_url, js_data: str, headers=default_json_header):
        url_base = "http://" + globalConnManager.get_available_conn_from_view(self.hippo_host_ports)
        url = self.make_hippo_url(url_base) + component_url
        return requests.delete(url, auth=(self.username, self.pwd), headers=headers, json=js_data)

    # 定义一个get请求的方法，用于发送get请求到hippo服务器，此处实现了简单的重试逻辑
    def get(self, component_url, js_data: str, headers=default_json_header, retry_max: int = 3):
        retry_max_count = retry_max
        while retry_max_count > 0:
            this_available_host_port = None
            try:
                this_available_host_port = globalConnManager.get_available_conn_from_view(self.hippo_host_ports)
                url_base = "http://" + this_available_host_port
                url = self.make_hippo_url(url_base) + component_url
                return requests.get(url, auth=(self.username, self.pwd), headers=headers, json=js_data)
            except requests.exceptions.ConnectionError as ce:
                # 对于get请求，做一个简单的重试
                if this_available_host_port is not None:
                    globalConnManager.mark_conn_state(this_available_host_port, ConnState.FAILED)
                retry_max_count -= 1
                if retry_max_count == 0:
                    raise ce

    # 定义一个post请求的方法，用于发送post请求到hippo服务器
    def post(self, component_url, js_data: str, headers=default_json_header):
        url_base = "http://" + globalConnManager.get_available_conn_from_view(self.hippo_host_ports)
        url = self.make_hippo_url(url_base) + component_url
        return requests.post(url, auth=(self.username, self.pwd), headers=headers, json=js_data)

    # 定义一个静态方法，用于处理json响应，如果响应状态码200，则返回json数据，否则抛出异常
    @staticmethod
    def handle_json_resp(resp: Response) -> dict:
        if resp.status_code == 200:
            s = resp.content
            return json.loads(s)
        else:
            js = resp.json()
            r = js["error"]["reason"]
            raise ValueError(r)


''' 定义HippoTableMeta数据类用于存储表的元数据信息 '''


@dataclass
class HippoTableMeta:
    tbl_name: str  # 表名
    schema: list[HippoField]  # 表结构，包含多个字段
    n_replicas: int  # 副本数量
    n_shards: int  # 分片数量
    db_name: str  # 数据库名


''' 定义HippoTable类用于管理和操作Hippo表 '''


class HippoTable:
    def __init__(self, hippo_conn: HippoConn, tbl_meta: HippoTableMeta):
        self.hippo_conn = hippo_conn  # Hippo连接对象
        self.tbl_meta = tbl_meta  # 表的元数据对象
        self.tbl_name = tbl_meta.tbl_name  # 表名
        self.schema = tbl_meta.schema  # 表结构

    # 定义__str__方法，用于打印HippoTable对象时显示表名和字段信息
    def __str__(self):
        if self.schema is None:
            return f"HippoTable({self.tbl_name}, fields: N/A)"
        else:
            return f"HippoTable({self.tbl_name}, fields: [{','.join([f'{f.name}:{f.data_type.value}' for f in self.schema])}])"

    # 定义一个内部方法用于处理对表的数据操作，包括插入、更新、删除等
    def _manipulate_rows(self, cols_like, op_type: str = "insert"):

        """
                用于处理对表的数据操作，包括插入、更新、删除等。

                参数:
                cols_like: 列数据列表，每个元素是一个列表，表示一列的所有数据。
                op_type: 操作类型，可以是 "insert"、"update"、"upsert" 或 "delete"。

                返回值:
                如果操作成功，返回 True。否则，抛出 ValueError 异常。
        """
        assert len(cols_like) == len(
            self.schema), f"to insert data columns({len(cols_like)}) does not match cols in schema({len(self.schema)})"
        fields_data = []

        rows_num = -1
        for idx, col in enumerate(cols_like):
            col_name = self.schema[idx].name

            # TODO: 可以插入数据的类型和表里的数据类型

            data = cols_like[idx]
            if not isinstance(data, list):
                raise TypeError(f"to insert data column {idx} is not a list")
            col_len = len(data)
            if rows_num != -1 and rows_num != col_len:
                raise ValueError(f"to insert data column rows {col_len} does not match previous row number {rows_num}")
            rows_num = col_len

            this_field_data = {
                "field_name": col_name,
                "field": data,
            }
            fields_data.append(this_field_data)

        req_data = {
            "fields_data": fields_data,
            "num_rows": rows_num,
        }
        if op_type != "insert":
            req_data["op_type"] = op_type

        js = json.dumps(req_data)
        js = json.loads(js)
        resp = self.hippo_conn.put(f"/{self.tbl_name}/_bulk?database_name={self.tbl_meta.db_name}&pretty", js_data=js)
        if resp.status_code == 200:
            return True
        else:
            raise ValueError(resp.content)

    # 定义插入行的方法，内部调用_manipulate_rows方法
    def insert_rows(self, cols_like):

        """
                插入行数据。

                参数:
                cols_like: 列数据列表，每个元素是一个列表，表示一列的所有数据。

                返回值:
                如果插入成功，返回 True。否则，抛出 ValueError 异常。
        """
        return self._manipulate_rows(cols_like, "insert")

    # 定义更新行的方法，内部调用_manipulate_rows方法
    def update_rows(self, cols_like):

        """
                更新行数据。

                参数:
                cols_like: 列数据列表，每个元素是一个列表，表示一列的所有数据。

                返回值:
                如果更新成功，返回 True。否则，抛出 ValueError 异常。
        """
        return self._manipulate_rows(cols_like, "update")

    # 定义插入或更新行的方法，内部调用_manipulate_rows方法
    def upsert_rows(self, cols_like):

        """
                插入或更新行数据。

                参数:
                cols_like: 列数据列表，每个元素是一个列表，表示一列的所有数据。

                返回值:
                如果操作成功，返回 True。否则，抛出 ValueError 异常。
        """
        return self._manipulate_rows(cols_like, "upsert")

    # 定义删除行的方法，内部调用_manipulate_rows方法
    def delete_rows(self, cols_like):

        """
                删除行数据。

                参数:
                cols_like: 列数据列表，每个元素是一个列表，表示一列的所有数据。

                返回值:
                如果删除成功，返回 True。否则，抛出 ValueError 异常。
        """
        return self._manipulate_rows(cols_like, "delete")

    # 批量删除数据。expr 参数用于指定要删除的行的条件。例如，"age > 18"。
    def delete_rows_by_query(self, expr: str = "",
                            wait_for_competion=True, timeout: str = "2m"):

        """
                批量删除数据。expr 参数用于指定要删除的行的条件。例如，"age > 18"。

                参数:
                expr: 删除条件表达式。
                wait_for_competion: 是否等待删除完成，默认为True。
                timeout: 超时时间，默认为"2m"。

                返回值:
                如果删除成功，返回作业状态。否则，抛出 ValueError 异常。
        """

        data = {
            "database_name": self.tbl_meta.db_name,
            "table_name": self.tbl_name,
            "expr": expr,
            "wait_for_completion": wait_for_competion,
            "timeout": timeout
        }
        js = json.dumps(data)
        js = json.loads(js)
        print(js)
        resp = self.hippo_conn.post(f"/_delete_by_query?pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        st = r["job_status"]
        if st is not None and st == HippoJobStatus.HIPPO_JOB_SUCCESS.value:
            return st
        else:
            error = r.get("errors")
            raise ValueError(f"cannot delete rows due to return error:{error}")

    # 创建索引。该方法用于在指定的字段上创建索引，可以加快查询速度。
    def create_index(self, field_name: str, index_name: str, index_type: IndexType, metric_type: MetricType, **kwargs):

        """
                在指定的字段上创建索引。

                参数:
                field_name: 要创建索引的字段名。
                index_name: 新创建的索引的名称。
                index_type: 索引类型，应为 IndexType 枚举的一个值。
                metric_type: 度量类型，应为 MetricType 枚举的一个值。
                **kwargs: 其他可选参数，用于指定创建索引时的额外设置。

                返回值:
                如果创建成功，返回 True。否则，抛出 ValueError 异常。
        """
        req = {
            "field_name": field_name,
            "index_name": index_name,
            "metric_type": metric_type.value,
            "index_type": index_type.value,
            "params": kwargs
        }

        js = json.dumps(req)
        js = json.loads(js)

        resp = self.hippo_conn.put(
            f"/{self.tbl_name}/_create_embedding_index?database_name={self.tbl_meta.db_name}&pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        if r["acknowledged"]:
            return True
        else:
            raise ValueError("cannot create index due to return error.")

    #  创建标量索引。用于在指定的字段上创建标量索引。
    def create_scalar_index(self, field_names: list[str], index_name: str):

        """
                在指定的字段上创建标量索引。

                参数:
                field_names: 要创建索引的字段名列表。
                index_name: 新创建的索引的名称。

                返回值:
                如果创建成功，返回True。否则，抛出ValueError异常。
        """

        data = {
            "index_name": index_name,
            "field_names": field_names
        }

        js = json.dumps(data)
        js = json.loads(js)

        resp = self.hippo_conn.put(
            f"/{self.tbl_name}/_create_scalar_index?database_name={self.tbl_meta.db_name}&pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        if r["acknowledged"]:
            return True
        else:
            raise ValueError("cannot create index due to return error.")

    # 删除标量索引。通过索引名称删除对应的标量索引。
    def delete_scalar_index(self, index_name: str):

        """
                通过索引名称删除对应的标量索引。

                参数:
                index_name: 要删除的索引的名称。

                返回值:
                如果删除成功，返回True。否则，抛出ValueError异常。
        """

        data = {
            "index_name": index_name
        }

        js = json.dumps(data)
        js = json.loads(js)

        resp = self.hippo_conn.delete(
            f"/{self.tbl_name}/_drop_scalar_index?database_name={self.tbl_meta.db_name}&pretty", js_data=js)
        print(resp.status_code)
        r = HippoConn.handle_json_resp(resp)
        if r["acknowledged"]:
            return True
        else:
            raise ValueError("cannot create index due to return error.")

    # 删除索引。通过索引名称删除对应的索引
    def drop_index(self, index_name: str):

        """
                通过索引名称删除对应的索引。

                参数:
                index_name: 要删除的索引的名称。

                返回值:
                如果删除成功，返回True。否则，抛出ValueError异常。
        """
        assert isinstance(index_name, str)
        return self.drop_indexes([index_name])

    # 删除多个索引。可以同时删除多个索引。
    def drop_indexes(self, index_names: list[str]):

        """
                可以同时删除多个索引。

                参数:
                index_names: 要删除的索引的名称列表。

                返回值:
                如果删除成功，返回True。否则，抛出ValueError异常。
        """
        assert all(',' not in ind_name for ind_name in index_names), "index name should not contains ','"
        req = {
            "index_name": ','.join(index_names),
        }

        js = json.dumps(req)
        js = json.loads(js)

        resp = self.hippo_conn.delete(
            f"/{self.tbl_name}/_drop_embedding_index?database_name={self.tbl_meta.db_name}&pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        if r["acknowledged"]:
            return True
        else:
            raise ValueError("cannot create index due to return error.")

    # 激活索引。通过索引名称激活对应的索引。
    def activate_index(self, index_name: str, wait_for_completion: bool = True, hippo_timeout_secs: int = 120):

        """
                通过索引名称激活对应的索引。

                参数:
                index_name: 要激活的索引的名称。
                wait_for_completion: 是否等待激活完成，默认为True。
                hippo_timeout_secs: 超时时间，以秒为单位，默认为120秒。

                返回值:
                如果激活成功，返回作业状态。否则，抛出ValueError异常。
        """
        req = {
            "index_name": index_name,
            "wait_for_completion": wait_for_completion,
            "timeout": hippo_timeout_secs,
        }

        js = json.dumps(req)
        js = json.loads(js)

        resp = self.hippo_conn.post(
            f"/{self.tbl_name}/_activate_embedding_index?database_name={self.tbl_meta.db_name}&pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        st = r.get("job_status")
        if st is not None and st == HippoJobStatus.HIPPO_JOB_SUCCESS.value:
            return st
        else:
            error_info = None
            try:
                error_info = r.get("errors")
            except:
                pass
            raise ValueError(f"build index return status: {st}, error info: {error_info}")

    def build_index(self, index_name: str, wait_for_completion: bool = True, hippo_timeout_secs: int = 120):

        """
            构建指定的索引。

            参数:
            index_name: 要构建的索引的名称。
            timeout: 超时时间，默认为"1m"。

            返回值:
            如果构建成功，返回True。否则，抛出Exception异常。
        """

        req = {
            "index_name": index_name,
            "wait_for_completion": wait_for_completion,
            "timeout": hippo_timeout_secs,
        }

        js = json.dumps(req)
        js = json.loads(js)

        resp = self.hippo_conn.post(
            f"/{self.tbl_name}/_rebuild_embedding_index?database_name={self.tbl_meta.db_name}&pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        st = r.get("job_status")
        if st is not None and st == HippoJobStatus.HIPPO_JOB_SUCCESS.value:
            return st
        else:
            error_info = None
            try:
                error_info = r.get("errors")
            except:
                pass
            raise ValueError(f"build index return status: {st}, error info: {error_info}")

    # 释放索引。通过索引名称释放对应的索引。
    def release_index(self, index_name: str, wait_for_completion: bool = True, hippo_timeout_secs: int = 120):

        """
                释放指定的索引。

                参数:
                index_name: 要释放的索引的名称。
                wait_for_completion: 是否等待释放完成，默认为True。
                hippo_timeout_secs: 超时时间，以秒为单位，默认为120秒。

                返回值:
                如果释放成功，返回作业状态。否则，抛出ValueError异常。
        """
        req = {
            "index_name": index_name,
            "wait_for_completion": wait_for_completion,
            "timeout": hippo_timeout_secs,
        }

        js = json.dumps(req)
        js = json.loads(js)

        resp = self.hippo_conn.post(
            f"/{self.tbl_name}/_release_embedding_index?database_name={self.tbl_meta.db_name}&pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        st = r.get("job_status")
        if st is not None and st == HippoJobStatus.HIPPO_JOB_SUCCESS.value:
            return st
        else:
            raise ValueError(f"build index return status: {st}")

    # 加载索引。加载指定的索引以便进行查询。
    def load_index(self, index_name: str, wait_for_completion: bool = True, hippo_timeout_secs: int = 120):

        """
            加载指定的索引。

            参数:
            index_name: 要加载的索引的名称。
            timeout: 超时时间，默认为"1m"。

            返回值:
            如果加载成功，返回True。否则，抛出Exception异常。
        """
        req = {
            "index_name": index_name,
            "wait_for_completion": wait_for_completion,
            "timeout": hippo_timeout_secs,
        }

        js = json.dumps(req)
        js = json.loads(js)

        resp = self.hippo_conn.post(
            f"/{self.tbl_name}/_load_embedding_index?database_name={self.tbl_meta.db_name}&pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        st = r.get("job_status")
        if st is not None and st == HippoJobStatus.HIPPO_JOB_SUCCESS.value:
            return st
        else:
            raise ValueError(f"build index return status: {st}")

    # 获取索引。获取当前表中所有的索引。
    def get_index(self):

        """
                获取当前表中所有的索引。

                返回值:
                返回一个包含所有索引的字典。
        """
        resp = self.hippo_conn.get(
            f"/{self.tbl_name}/_get_embedding_index?database_name={self.tbl_meta.db_name}&pretty", js_data=None)
        r = HippoConn.handle_json_resp(resp)
        return r

    # 获取设置。获取当前表的设置信息。
    def get_settings(self) -> dict:

        """
                获取当前表的设置信息。

                返回值:
                返回一个包含所有设置的字典。
        """
        resp = self.hippo_conn.get(f"/{self.tbl_name}/_settings?database_name={self.tbl_meta.db_name}&pretty",
                                   js_data=None)
        r = HippoConn.handle_json_resp(resp)
        return r

    # 更新设置。更新当前表的设置信息。
    def update_settings(self, **kwargs):
        """
                更新当前表的设置信息。

                参数:
                **kwargs: 包含要更新的设置的字典。

                返回值:
                如果更新成功，返回True。否则，返回False。
        """
        req = kwargs
        js = json.dumps(req)
        js = json.loads(js)

        resp = self.hippo_conn.put(f"/{self.tbl_name}/_settings?database_name={self.tbl_meta.db_name}&pretty",
                                   js_data=js)
        r = HippoConn.handle_json_resp(resp)
        if 'acknowledged' in r and r['acknowledged'] == True:
            return True
        else:
            return False

    # 查询标量。按照指定的输出字段和表达式对表进行查询。
    def query_scalar(self,
                     output_fields: list[str],
                     expr: str,
                     ):

        """
                按照指定的输出字段和表达式对表进行查询。

                参数:
                output_fields: 输出字段的列表。
                expr: 查询表达式。

                返回值:
                返回一个包含查询结果的字典。
        """
        req = {
            "output_fields": output_fields,
            "expr": expr,
        }
        js = json.dumps(req)
        js = json.loads(js)

        resp = self.hippo_conn.get(f"/{self.tbl_name}/_query?database_name={self.tbl_meta.db_name}&pretty", js_data=js)
        result = HippoConn.handle_json_resp(resp)

        this_query_result = result.get("fields_data")

        this_query_ret_result = {}

        for col_data in this_query_result:
            field_name = col_data.get("field_name")
            field_values = col_data.get("field_values", [])
            this_query_ret_result[field_name] = field_values

        return this_query_ret_result

    # 查询。按照指定的查询参数对表进行查询，并返回结果。
    def query(self,
              search_field: str,
              vectors: list[list[float]],
              output_fields: list[str],
              topk: int,
              metric_type: str = 'l2',
              dsl: str = None,
              **params,
              ) -> list[HippoResult]:

        """
                按照指定的查询参数对表进行查询，并返回结果。

                参数:
                search_field: 搜索字段的名称。
                vectors: 向量列表，用于搜索。
                output_fields: 输出字段的列表。
                topk: 返回的最多的结果数量。
                metric_type: 度量类型，默认为'l2'。
                dsl: 指定的领域特定语言（可选）。
                **params: 其他查询参数。

                返回值:
                返回一个包含查询结果的列表。
        """
        req = {
            "output_fields": output_fields,
            "search_params": {
                "anns_field": search_field,
                "topk": topk,
                "params": params,
                "metric_type": metric_type,
            },
            "vectors": vectors,
        }

        if dsl is not None:
            req["dsl"] = dsl

        js = json.dumps(req)
        js = json.loads(js)
        resp = self.hippo_conn.get(f"/{self.tbl_name}/_search?database_name={self.tbl_meta.db_name}&pretty", js_data=js)
        result = HippoConn.handle_json_resp(resp)

        try:
            if result.get("num_queries") != len(vectors):
                raise RuntimeError(
                    f"internal error, return query number({result.get('num_queries')}) not equal to input query number({len(vectors)}).")

            query_results = result.get("results")
            assert query_results is not None, "internal error, result should not be None."

            total_result = []

            for qr in query_results:
                total_result.append(None)

            for qr in query_results:
                query_id = qr.get("query")
                this_query_result = qr.get("fields_data")

                this_query_ret_result = {}

                for col_data in this_query_result:
                    field_name = col_data.get("field_name")
                    field_values = col_data.get("field_values", [])

                    # 当前结果不够的时候，无法保障topk条，我们先不检查了 TODO
                    # assert dsl is not None or len(field_values) == topk, f"return values number({len(field_values)}) mismatch with topk({topk})"
                    # assert dsl is not None or len(scores) == topk, f"return scores number({len(field_values)}) mismatch with topk({topk})"

                    scores = col_data.get("scores", [])

                    this_query_ret_result[field_name] = field_values
                    this_query_ret_result[field_name + "%scores"] = scores

                total_result[query_id] = this_query_ret_result
        except BaseException as e:
            raise ValueError(f"error during process result, exception -> is {e}. \nreturn json is {resp.json()}")

        return total_result


# 定义了一个函数，用于处理类型字符串，返回相应的HippoType枚举值或None
def _handle_type_str(type_str: str) -> Optional[HippoType]:
    lower_type_name = type_str.lower()
    for m in HippoType.__members__.values():
        if m.value == lower_type_name:
            return m
    for k, v in HippoTypeAliases.items():
        for alias in v:
            if lower_type_name == alias:
                return k
    return None


# 定义了一个函数，用于处理字段模式，返回一个HippoField对象或None
def _handle_field_schema(dd: dict) -> Optional[HippoField]:
    field_name = dd["name"]
    is_primary_key = dd["is_primary_key"]
    data_type = _handle_type_str(dd["data_type"])
    if data_type is None:
        raise ValueError(f"value for data type error: {dd['data_type']}")
    return HippoField(name=field_name, is_primary_key=is_primary_key, data_type=data_type)


''' 定义了一个HippoClient类 '''


class HippoClient:
    # 初始化方法，参数包括主机名、用户名和密码
    def __init__(self, host_port: str | list[str], username: str = 'shiva', pwd: str = 'shiva'):
        if isinstance(host_port, str):
            xx = [host_port]
        elif isinstance(host_port, list):
            xx = host_port
        else:
            raise TypeError("host_port should be str or list[str")
        self.hippo_conn = HippoConn(xx, username, pwd)

    # 定义了一个方法，用于处理表字典，返回一个HippoTable对象或None
    def _handle_tbl_dict(self, tbl_name: str, dd: dict) -> Optional[HippoTable]:

        fields = [_handle_field_schema(x) for x in dd["schema"]["fields"]]

        print(dd)
        meta = HippoTableMeta(
            tbl_name=tbl_name,
            schema=fields,
            n_shards=dd["settings"]["number_of_shards"],
            n_replicas=dd["settings"]["number_of_shards"],
            db_name=dd["database_name"]
        )

        return HippoTable(self.hippo_conn, meta)

    # 定义了一个方法，用于检查表名
    def __check_single_tbl_name(self, tbl_name: str):
        assert '*' not in tbl_name, "table name should not contains *"

    # 定义了一个方法，用于检查数据库名
    def __check_single_database_name(self, database_name: str):
        assert '*' not in database_name, "database name should not contains *"

    # 定义了一个方法，用于复制表
    def copy_table(self, source_table_name: str, dest_table_name: str,
                   source_database_name: str = "default", dest_database_name: str = "default",
                   remote_info: dict = None, fields: list = None, fields_projection: list = None,
                   expr: str = None, op_type: str = "insert", wait_for_completion=True, timeout: str = "2m"):

        """
            复制指定数据库中的表。

            参数:
            source_table_name: 源表名。
            dest_table_name: 目标表名。
            source_database_name: 源数据库名，默认为"default"。
            dest_database_name: 目标数据库名，默认为"default"。
            remote_info: 远程信息的字典，用于指定远程源（可选）。
            fields: 要复制的字段列表（可选）。
            fields_projection: 字段投影列表，用于修改复制的字段（可选）。
            expr: 表达式，用于过滤要复制的数据（可选）。
            op_type: 操作类型，默认为"insert"，可以是"insert"、"update"或"upsert"。
            wait_for_completion: 是否等待复制完成，默认为True。
            timeout: 超时时间，默认为"2m"。

            返回值:
            如果复制成功，返回作业状态。否则，抛出ValueError异常。
        """

        source_table = {
            "database_name": source_database_name,
            "table_name": source_table_name
        }

        if remote_info is not None:
            source_table["remote_info"] = remote_info

        dest_table = {
            "database_name": dest_database_name,
            "table_name": dest_table_name
        }

        data = {
            "source_table": source_table,
            "dest_table": dest_table,
            "op_type": op_type,
            "wait_for_completion": wait_for_completion,
            "timeout": timeout
        }

        if fields is not None:
            data["fields"] = fields

        if fields_projection is not None:
            data["fields_projection"] = fields_projection

        if expr is not None:
            data["expr"] = expr

        js = json.dumps(data, cls=HippoTypesEncoder)
        js = json.loads(js)

        resp = self.hippo_conn.post(f"/_copy_by_query?pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        st = r.get("job_status")
        if st is not None and st == HippoJobStatus.HIPPO_JOB_SUCCESS.value:
            return st
        else:
            error = r.get("errors")
            raise ValueError(f"cannot copy table due to return error:{error}")

    # 定义了一个方法，用于获取表
    def get_table(self, tbl_name: str, database_name: str = "default") -> Optional[HippoTable]:

        """
            获取指定的表。

            参数:
            tbl_name: 表名。
            database_name: 数据库名，默认为"default"。

            返回值:
            如果找到，返回HippoTable实例。否则，返回None。
        """
        self.__check_single_tbl_name(tbl_name)
        resp = self.hippo_conn.get(f"/{tbl_name}?database_name={database_name}&pretty", js_data=None)
        r = HippoConn.handle_json_resp(resp)
        if len(r) < 1:
            return None
        else:
            for k, v in r.items():
                if k == tbl_name:
                    return self._handle_tbl_dict(k, v)
            return None

    # 定义了一个方法，用于获取表信息
    def get_table_info(self, tbl_name: str, database_name: str = "default"):

        """
            获取指定表的信息。

            参数:
            tbl_name: 表名。
            database_name: 数据库名，默认为"default"。

            返回值:
            返回一个包含表信息的字典。如果出现错误，抛出ValueError异常。
        """
        resp = self.hippo_conn.get(f"/{tbl_name}?database_name={database_name}&pretty", js_data="")
        try:
            r = HippoConn.handle_json_resp(resp)
            return r
        except:
            raise ValueError(HippoConn.handle_json_resp(resp))

    # 定义了一个方法，用于获取表结构
    def get_table_schema(self, tbl_name: str, database_name: str = "default"):

        """
            获取指定表的结构。

            参数:
            tbl_name: 表名。
            database_name: 数据库名，默认为"default"。

            返回值:
            返回一个包含表结构的字典。
        """
        info = self.get_table_info(tbl_name, database_name)
        table_info = info.get(tbl_name, {})
        return table_info.get('schema', None)

    # 定义了一个方法，用于获取表的向量索引
    def get_table_indexes(self, tbl_name: str, database_name: str = "default"):

        """
            获取指定表的向量索引。

            参数:
            tbl_name: 表名。
            database_name: 数据库名，默认为"default"。

            返回值:
            返回一个包含向量索引信息的字典。
        """
        info = self.get_table_info(tbl_name, database_name)
        embedding_index_info = info.get(tbl_name, {})
        return embedding_index_info.get('embedding_indexes', None)

    # 定义了一个方法，用于获取表配置
    def get_table_config(self, table_name: str = None, database_name: str = "default"):

        """
            获取指定表的配置。

            参数:
            table_name: 表名，如果不提供，则获取所有表的配置。
            database_name: 数据库名，默认为"default"。

            返回值:
            返回一个包含表配置的字典。如果找不到配置，抛出ValueError异常。
        """
        resp = None
        if table_name is None:
            resp = self.hippo_conn.get(f"/_settings?database_name={database_name}&pretty", js_data="")
        else:
            resp = self.hippo_conn.get(f"/{table_name}/_settings?database_name={database_name}&pretty", js_data="")
        r = HippoConn.handle_json_resp(resp)
        if resp.status_code == 200:
            config_key = f"{database_name}#{table_name}"
            if config_key in r:
                return {table_name: r[config_key]}
            else:
                raise ValueError(f"No configuration found for table {table_name} in database {database_name}")
        else:
            raise ValueError(resp.content)

    # 定义了一个方法，用于更新表配置
    def update_table_config(self, table_name: str, number_of_replicas: int = None, data_center: str = None,
                            tag: str = None,
                            embedding_segment_max_deletion_proportion: float = 0.1,
                            embedding_segment_seal_proportion: float = 0.2, embedding_segment_max_size_mb: int = 512,
                            tag_clear=True, disaster_preparedness=True, scatter_replica=True, dc_affinity=True,
                            database_name: str = "default"):

        """
            更新指定表的配置。

            参数:
            table_name: 表名。
            number_of_replicas, data_center, tag, embedding_segment_max_deletion_proportion, embedding_segment_seal_proportion, embedding_segment_max_size_mb, tag_clear, disaster_preparedness, scatter_replica, dc_affinity: 配置选项。
            database_name: 数据库名，默认为"default"。

            返回值:
            如果更新成功，返回True。否则，抛出ValueError异常。
        """

        data = {
            "disaster_preparedness": disaster_preparedness,
            "scatter_replica": scatter_replica,
            "dc_affinity": dc_affinity,
            "tag.clear": tag_clear,
            "embedding.segment.max_size_mb": embedding_segment_max_size_mb,
            "embedding.segment.seal_proportion": embedding_segment_seal_proportion,
            "embedding.segment.max_deletion_proportion": embedding_segment_max_deletion_proportion
        }
        if number_of_replicas is not None:
            data["number_of_replicas"] = number_of_replicas
        if data_center is not None:
            data["data_center"] = data_center
        if tag is not None:
            data["tag"] = tag

        js = json.dumps(data, cls=HippoTypesEncoder)
        js = json.loads(js)

        resp = self.hippo_conn.put(f"/{table_name}/_settings?database_name={database_name}&pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        if resp.status_code == 200 and r.get("acknowledged") is True:
            return True
        else:
            raise ValueError(HippoConn.handle_json_resp(resp))

    # 为指定数据库中的给定表创建别名
    def create_alias(self, table_name: str, alise_name: str, database_name: str = "default"):

        """
            为指定数据库中的给定表创建别名。

            参数:
            table_name: 表名。
            alias_name: 别名。
            database_name: 数据库名，默认为"default"。

            返回值:
            如果创建成功，返回True。否则，抛出ValueError异常。
        """

        actions = {
            "type": "Add",
            "database_name": database_name,
            "alias_name": alise_name,
            "table_name": table_name
        }

        data = {
            'actions': [actions]
        }

        js = json.dumps(data, cls=HippoTypesEncoder)
        js = json.loads(js)
        resp = self.hippo_conn.post(f"/_aliases?pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        if resp.status_code == 200 and r.get("acknowledged") is True:
            return True
        else:
            raise ValueError(resp.content)

    # 删除指定数据库中的别名。
    def delete_alias(self, alias_name: str, database_name: str = "default"):

        """
            删除指定数据库中的别名。

            参数:
            alias_name: 别名。
            database_name: 数据库名，默认为"default"。

            返回值:
            如果删除成功，返回True。否则，抛出ValueError异常。
        """
        resp = self.hippo_conn.delete(f"/_aliases/{alias_name}?database_name={database_name}&pretty", js_data="")
        r = HippoConn.handle_json_resp(resp)
        if resp.status_code == 200 and r.get("acknowledged") is True:
            return True
        else:
            raise ValueError(resp.content)

    # 创建新的数据库。
    def create_database(self,
                        name: str) -> bool:

        """
            创建新的数据库。

            参数:
            name: 数据库的名称。

            返回值:
            如果创建成功，返回True。否则，抛出ValueError异常。
        """

        data = {
            'database_name': name
        }

        js = json.dumps(data, cls=HippoTypesEncoder)
        js = json.loads(js)

        resp = self.hippo_conn.put(f"/_database?pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        if resp.status_code == 200 and r.get("acknowledged") is True:
            return True
        else:
            raise ValueError(resp.content)

    # 列出所有的数据库
    def list_databases(self):
        """
            列出所有的数据库。

            返回值:
            返回一个包含所有数据库的列表。
        """

        resp = self.hippo_conn.get(f"/_database?pretty", js_data="")
        r = HippoConn.handle_json_resp(resp)
        return r

    # 删除指定的数据库
    def delete_database(self,
                        name: str) -> bool:
        """
            删除指定的数据库。

            参数:
            name: 数据库的名称。

            返回值:
            如果删除成功，返回True。否则，抛出ValueError异常。
        """
        self.__check_single_database_name(name)
        data = {
            'database_name': name
        }
        js = json.dumps(data, cls=HippoTypesEncoder)
        js = json.loads(js)
        resp = self.hippo_conn.delete(f"/_database?pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        if 'acknowledged' in r and r['acknowledged'] == True:
            return True
        else:
            raise ValueError(resp.content)

    # 列出指定数据库中的数据分片（如果提供了表名，则仅列出该表的分片）
    def list_shards(self, table_name: str = None, database_name: str = "default"):

        """
            列出指定数据库中的数据分片。如果提供了表名，则仅列出该表的分片。

            参数:
            table_name: 表名，如果不提供，则列出所有表的分片。
            database_name: 数据库名，默认为"default"。

            返回值:
            返回一个字典，其中包含了分片的信息。
        """

        resp = None
        if table_name is None:
            resp = self.hippo_conn.get(f"/_cat/shards?database_name={database_name}&v", js_data="")
        else:
            resp = self.hippo_conn.get(f"/_cat/shards/{table_name}?database_name={database_name}&v", js_data="")

        if resp.status_code == 200:
            s = resp.content
            s_decoded = s.decode('utf-8')
            lines = s_decoded.split('\n')  # 将数据分成行
            headers = lines[0].split()  # 将第一行分成标题

            shards_data = {header: [] for header in headers}  # 创建一个空字典，每个标题作为键

            for line in lines[1:]:  # 对于剩余的每一行
                values = line.split()  # 将行分成值
                for header, value in zip(headers, values):  # 对于每一对标题和值
                    shards_data[header].append(value)  # 将值添加到相应的列表
            return shards_data
        else:
            raise ValueError(HippoConn.handle_json_resp(resp))

    # 检查指定的数据库是否包含指定的表。
    def check_table_exists(self, table_name: str, database_name: str = "default"):

        """
            检查指定的数据库是否包含指定的表。

            参数:
            table_name: 表名。
            database_name: 数据库名，默认为"default"。

            返回值:
            如果存在，返回True。否则，返回False。
        """
        data = {
            'database_name': database_name,
            'table_name': table_name
        }

        js = json.dumps(data, cls=HippoTypesEncoder)
        js = json.loads(js)

        resp = self.hippo_conn.get(f"/_check_table_existence?pretty", js_data=js)

        try:
            r = HippoConn.handle_json_resp(resp)
            if resp.status_code == 200:
                if r.get("acknowledged"):
                    return True
                else:
                    return False
        except ValueError as e:
            if str(e) == f"table {table_name} not exist in database {database_name}, get table id from database failed":
                return False
            else:
                raise e

    # 指定的数据库中创建新的表
    def create_table(self,
                     name: str,
                     fields: list[HippoField],
                     database_name: str = "default",
                     number_of_shards: int = 1,
                     number_of_replicas: int = 1) -> Optional[HippoTable]:

        """
            在指定的数据库中创建新的表。

            参数:
            name: 表名。
            fields: 一个HippoField对象的列表，每个对象代表一个字段。
            database_name: 数据库名，默认为"default"。
            number_of_shards: 分片数，默认为1。
            number_of_replicas: 复制数，默认为1。

            返回值:
            如果创建成功，返回一个HippoTable对象。否则，抛出ValueError异常。
        """
        fields_for_req = [asdict(f) for f in fields]

        data = {
            'settings': {
                'number_of_shards': number_of_shards,
                'number_of_replicas': number_of_replicas,
            },
            'schema': {
                'fields': fields_for_req,
            }
        }

        js = json.dumps(data, cls=HippoTypesEncoder)
        js = json.loads(js)

        # print("BODY:", js)

        resp = self.hippo_conn.put(f"/{name}?database_name={database_name}&pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        if resp.status_code == 200 and r.get("acknowledged") is True:
            meta = HippoTableMeta(tbl_name=name, schema=fields, n_replicas=number_of_replicas,
                                  n_shards=number_of_shards, db_name=database_name)
            return HippoTable(hippo_conn=self.hippo_conn, tbl_meta=meta)
        else:
            raise ValueError(resp.content)

    # 重命名指定数据库中的表
    def rename_table(self, old_table_name: str, new_table_name: str, database_name: str = "default"):

        """
            重命名指定数据库中的表。

            参数:
            old_table_name: 旧的表名。
            new_table_name: 新的表名。
            database_name: 数据库名，默认为"default"。

            返回值:
            如果重命名成功，返回True。否则，抛出ValueError异常。
        """
        data = {
            "database_name": database_name,
            "table_name": old_table_name,
            "new_table_name": new_table_name
        }

        js = json.dumps(data, cls=HippoTypesEncoder)
        js = json.loads(js)

        resp = self.hippo_conn.put(f"/_rename_table?pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)

        if resp.status_code == 200 and r.get("acknowledged") is True:
            return True
        else:
            raise ValueError(resp.content)

    # 删除指定数据库中的表
    def delete_table(self, tbl_name: str, database_name: str = "default"):

        """
            删除指定数据库中的表。

            参数:
            tbl_name: 需要删除的表名。
            database_name: 数据库名，默认为"default"。

            返回值:
            如果删除成功，返回True。否则，抛出ValueError异常。
        """
        self.__check_single_tbl_name(tbl_name)
        resp = self.hippo_conn.delete(f"/{tbl_name}?database_name={database_name}&pretty", js_data=None, headers=None)
        r = HippoConn.handle_json_resp(resp)
        if 'acknowledged' in r and r['acknowledged'] == True:
            return True
        else:
            raise ValueError(resp.content)

    # 列出指定数据库中的所有表
    def list_tables(self, database_name: str = "default", pattern: str = "*", ignore_aliases=True):

        """
            列出指定数据库中的所有表。

            参数:
            database_name: 数据库名，默认为"default"。
            pattern: 表名的匹配模式，默认为"*"，匹配所有表。
            ignore_aliases: 是否忽略别名，默认为True。

            返回值:
            一个字典，其中包含了匹配模式的所有表的信息。
        """
        ignore_aliases = str(ignore_aliases).lower()
        if pattern == "*":
            print(database_name)
            resp = self.hippo_conn.get(f"/_cat/tables?database_name={database_name}&v&ignore_aliases={ignore_aliases}",
                                       js_data="")
        else:
            resp = self.hippo_conn.get(
                f"/_cat/tables/{pattern}?database_name={database_name}&v&ignore_aliases={ignore_aliases}", js_data="")

        if resp.status_code == 200:
            s = resp.content
            s_decoded = s.decode('utf-8')
            lines = s_decoded.split('\n')  # 将数据分成行
            headers = lines[0].split()  # 将第一行分成标题
            table_data = {header: [] for header in headers}  # 创建一个空字典，每个标题作为键

            for line in lines[1:]:  # 对于剩余的每一行
                values = line.split()  # 将行分成值
                for header, value in zip(headers, values):  # 对于每一对标题和值
                    table_data[header].append(value)  # 将值添加到相应的列表
            return table_data
        else:
            raise ValueError(HippoConn.handle_json_resp(resp))


    # 此方法用于创建新的用户。你可以通过参数指定用户名、密码，并设置用户是否具有超级用户权限、是否可以创建角色和数据库
    def create_user(self, user_name: str,
                    pwd: str,
                    is_super: bool = False,
                    can_create_role: bool = False,
                    can_create_db: bool = False) -> bool:

        """
            创建新的用户。

            参数:
            user_name: 用户名。
            pwd: 用户密码。
            is_super: 是否为超级用户，默认为False。
            can_create_role: 用户是否可以创建角色，默认为False。
            can_create_db: 用户是否可以创建数据库，默认为False。

            返回值:
            一个布尔值，表示操作是否成功。
        """

        data = {
            "password": pwd,
            "metadata": {
                "is_super": is_super,
                "can_create_role": can_create_role,
                "can_create_db": can_create_db
            }
        }

        js = json.dumps(data, cls=HippoTypesEncoder)
        js = json.loads(js)

        resp = self.hippo_conn.put(f"/_security/user/{user_name}?pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        if r.get("created"):
            return True
        else:
            raise ValueError(r)

    # 删除指定的用户
    def delete_user(self, user_name: str):
        """
            删除指定的用户。

            参数:
            user_name: 需要删除的用户名。

            返回值:
            一个布尔值，表示操作是否成功。
        """

        resp = self.hippo_conn.delete(f"/_security/user/{user_name}?pretty",js_data="")
        r = HippoConn.handle_json_resp(resp)
        if r.get("found"):
            return True
        else:
            raise ValueError(r)

    # 获取指定用户的信息
    def get_user_info(self, user_name: str):
        """
            获取指定用户的信息。

            参数:
            user_name: 用户名。

            返回值:
            一个字典，其中包含了用户的信息。
        """

        resp = self.hippo_conn.get(f"/_security/user/{user_name}?pretty", js_data="")
        r = HippoConn.handle_json_resp(resp)
        return r

    # 更改指定用户的信息，包括密码和元数据（如是否为超级用户、是否可以创建角色和数据库）。你可以选择是否更改元数据。
    def change_user_info(self, user_name: str,
                         pwd: str,
                         change_meta: bool = False,
                         is_super: bool = False,
                         can_create_role: bool = False,
                         can_create_db: bool = False):
        """
            更改指定用户的信息，包括密码和元数据（如是否为超级用户、是否可以创建角色和数据库）。

            参数:
            user_name: 用户名。
            pwd: 新的用户密码。
            change_meta: 是否更改元数据，默认为False。
            is_super: 是否为超级用户，默认为False。
            can_create_role: 用户是否可以创建角色，默认为False。
            can_create_db: 用户是否可以创建数据库，默认为False。

            返回值:
            一个布尔值，表示操作是否成功。
        """

        data = {
            "password": pwd,
            "metadata": {
                "is_super": is_super,
                "can_create_role": can_create_role,
                "can_create_db": can_create_db
            }
        }
        if not change_meta:
            del data["metadata"]

        js = json.dumps(data, cls=HippoTypesEncoder)
        js = json.loads(js)
        print(js)

        resp = self.hippo_conn.put(f"/_security/user/{user_name}/_alter?pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        if r.get("acknowledged"):
            return True
        else:
            raise ValueError(r)

    # 用于更改指定用户的密码。如果没有提供用户名，那么将改变当前用户的密码
    def change_password(self, new_password: str, user_name: str = None):
        """
            更改指定用户的密码。如果没有提供用户名，那么将改变当前用户的密码。

            参数:
            new_password: 新的密码。
            user_name: 用户名，如果为None，则表示改变当前用户的密码。

            返回值:
            一个布尔值，表示操作是否成功。
        """

        if user_name is None:
            return self.change_user_info(self.hippo_conn.username, new_password)
        else:
            return self.change_user_info(user_name, new_password)

    # 给指定用户授予在特定数据库或表上的权限。
    def grant_user_permission(self, user_name: str, privileges: list[str], table_name: str = None,
                              database_name: str = "default"):

        """
            为指定用户授予对特定数据库或表的权限。

            参数:
            user_name: 用户名。
            privileges: 权限列表。
            table_name: 表名，默认为None，表示对整个数据库授予权限。
            database_name: 数据库名称，默认为"default"。

            返回值:
            一个布尔值，表示操作是否成功。
        """

        data = None
        if table_name is None:
            data = {
                "database_name": database_name,
                "privileges": privileges
            }
        else:
            data = {
                "table_name": table_name,
                "database_name": database_name,
                "privileges": privileges
            }
        js = json.dumps(data, cls=HippoTypesEncoder)
        js = json.loads(js)

        resp = self.hippo_conn.post(f"/_security/acl/{user_name}?pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        if r.get("acknowledged"):
            return True
        else:
            raise ValueError(r)

    # 删除指定用户在特定数据库或表上的权限。
    def delete_user_permission(self, user_name: str, privileges: list[str], table_name: str = None,
                               database_name: str = "default"):

        """
            删除指定用户在特定数据库或表上的权限。

            参数:
            user_name: 用户名。
            privileges: 权限列表。
            table_name: 表名，默认为None，表示对整个数据库删除权限。
            database_name: 数据库名称，默认为"default"。

            返回值:
            一个布尔值，表示操作是否成功。
        """

        data = None
        if table_name is None:
            data = {
                "database_name": database_name,
                "privileges": privileges
            }
        else:
            data = {
                "table_name": table_name,
                "database_name": database_name,
                "privileges": privileges
            }
        js = json.dumps(data, cls=HippoTypesEncoder)
        js = json.loads(js)
        resp = self.hippo_conn.delete(f"/_security/acl/{user_name}?pretty", js_data=js)
        r = HippoConn.handle_json_resp(resp)
        if r.get("acknowledged"):
            return True
        else:
            raise ValueError(r)

    # 用于查看指定用户的权限
    def view_user_permission(self, user_name: str):
        """
            查看指定用户的权限。

            参数:
            user_name: 用户名。

            返回值:
            一个字典，其中包含了用户的权限信息。
        """

        resp = self.hippo_conn.get(f"/_security/user/_privileges/{user_name}?pretty", js_data="")
        if resp.status_code == 200:
            r = HippoConn.handle_json_resp(resp)
            return r
        else:
            raise ValueError(HippoConn.handle_json_resp(resp))

    # 用于查看指定表的权限
    def view_table_permission(self, table_name: str, database_name: str = "default"):
        """
            查看指定表的权限。

            参数:
            table_name: 表名。
            database_name: 数据库名称，默认为"default"。

            返回值:
            一个字典，其中包含了表的权限信息。
        """

        resp = self.hippo_conn.get(f"/_security/tables/{table_name}?database_name={database_name}&pretty", js_data="")
        if resp.status_code == 200:
            r = HippoConn.handle_json_resp(resp)
            return r
        else:
            raise ValueError(HippoConn.handle_json_resp(resp))

    # 列出所有的表
    def list_all_tables(self) -> list[HippoTable]:
        """
            列出所有的表。

            返回值:
            一个HippoTable对象的列表，每个HippoTable对象代表一个表。
        """
        resp = self.hippo_conn.get("/_settings?pretty", js_data=None)
        r = HippoConn.handle_json_resp(resp)
        ret = []
        for db_tbl_name, content in r.items():
            xx = db_tbl_name.split("#")
            db, tbl = xx[0], xx[1]
            tbl_meta = HippoTableMeta(tbl, None, int(content["number_of_replicas"]), int(content["number_of_shards"]),
                                      db_name=db)
            ret.append(HippoTable(self.hippo_conn, tbl_meta))
        return ret

    # 用于获取任务。你可以通过参数指定任务 ID 和操作模式。
    def get_job(self, job_ids: list[str] = None, action_patterns=None):
        """
            获取符合指定动作模式并且在给定任务ID列表中的任务。

            参数:
            job_ids: 指定的任务ID列表，默认为None，表示获取所有任务。
            action_patterns: 指定的动作模式，默认为["hippo*"]。

            返回值:
            一个字典，其中包含了获取到的任务的信息。
        """

        if action_patterns is None:
            action_patterns = ["hippo*"]

        data = {
            "action_patterns": action_patterns
        }

        if job_ids is not None:
            data["job_jds"] = job_ids

        js = json.dumps(data, cls=HippoTypesEncoder)
        js = json.loads(js)

        resp = self.hippo_conn.get("/_jobs?pretty", js_data=js)

        if resp.status_code == 200:
            return HippoConn.handle_json_resp(resp)
        else:
            raise ValueError(HippoConn.handle_json_resp(resp))

    # 删除指定的任务。
    def delete_job(self, job_id: str):
        """
            删除指定ID的任务。

            参数:
            job_id: 需要删除的任务的ID。

            返回值:
            一个布尔值，表示操作是否成功。
        """

        resp = self.hippo_conn.delete(f"/_jobs/{job_id}?pretty", js_data="")
        r = HippoConn.handle_json_resp(resp)
        if r.get("acknowledged"):
            return True
        else:
            raise ValueError(r)

    # 查看回收站中的表
    def view_tables_in_trash(self, database_name: str = "default"):
        """
                查询并返回指定数据库中回收站中的表的信息。

                参数:
                database_name: 数据库名称，默认为"default"。

                返回值:
                一个字典，其中键是表的属性，值是属性对应的列表。
        """

        resp = self.hippo_conn.get(f"/_cat/trash?database_name={database_name}&v", js_data="")
        if resp.status_code == 200:
            s = resp.content
            s_decoded = s.decode('utf-8')
            lines = s_decoded.split('\n')  # 将数据分成行
            headers = lines[0].split()  # 将第一行分成标题

            table_data = {header: [] for header in headers}  # 创建一个空字典，每个标题作为键

            for line in lines[1:]:  # 对于剩余的每一行
                values = line.split()  # 将行分成值
                for header, value in zip(headers, values):  # 对于每一对标题和值
                    table_data[header].append(value)  # 将值添加到相应的列表
            return table_data
        else:
            raise ValueError(HippoConn.handle_json_resp(resp))

    # 从回收站中删除指定的表
    def delete_table_in_trash(self, table_name: str, database_name: str = "default"):
        """
                从指定数据库的回收站中删除指定的表。

                参数:
                table_name: 需要删除的表名。
                database_name: 数据库名称，默认为"default"。

                返回值:
                一个布尔值，表示操作是否成功。
        """
        resp = self.hippo_conn.delete(f"/_trash/{table_name}?database_name={database_name}&pretty", js_data="")
        r = HippoConn.handle_json_resp(resp)
        if r.get("acknowledged"):
            return True
        else:
            raise ValueError(r)
