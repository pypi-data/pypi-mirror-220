"""
reids连接池

实现增删改查功能

"""
import json
import time

from redis import Redis, ConnectionPool

from digiCore import Decorate


class RedisConnectionPool():

    def __init__(self,
                 host: str,
                 port: int,
                 password: str,
                 db: int):
        self.__pool__ = ConnectionPool(host=host,
                                       port=port,
                                       password=password,
                                       db=db,
                                       max_connections=100)

    def __call__(self):
        return Redis(connection_pool=self.__pool__)

    def __enter__(self):
        self.redis_conn = self()
        return self.redis_conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.redis_conn.connection_pool.disconnect()


class RedisDao:

    def __init__(self, host: str, port: int, password: str, db: int):
        self.conn = RedisConnectionPool(host, port, password, db)

    @Decorate.def_retry(msg="redis: 获取任务队列长度失败，正在重试连接！")
    def get_task_list_len(self, task_name: str):
        """
        获取任务列表长度
        :param task_name: 任务队列名称
        :return: int
        """
        with self.conn as redis_conn:
            return redis_conn.llen(task_name)

    @Decorate.def_retry(msg="redis: 设置redis运行标识失败，正在重试连接！")
    def setnx_run_sign(self, run_sign):
        """
        设置 run_sign 运行标识。
        如果标识 存在则返回  False
        如果标识 不存在则设置为 1，返回 True
        :param run_sign: 运行标识
        :return: bool
        """
        with self.conn as redis_conn:
            return redis_conn.setnx(run_sign, 1)

    @Decorate.def_retry(msg="redis: 删除redis运行标识失败，正在重试连接！")
    def delete_run_sign(self, run_sign):
        """
        删除分布式锁
        删除完成 或者 运行标识 不存在 返回 0
        :param run_sign: 运行标识
        :return: 0
        """
        with self.conn as redis_conn:
            return redis_conn.delete(run_sign)

    @Decorate.def_retry(msg="redis: 添加任务失败，正在重试连接！")
    def push_task(self, task_name: str, task_json: dict):
        """
        将任务添加到redis进行缓存
        :param task_name: 任务队列名称
        :param task_json: 任务实例
        :return: True
        """
        with self.conn as redis_conn:
            if not task_json:
                return None
            bson_data = json.dumps(task_json)
            return redis_conn.lpush(task_name, bson_data)

    @Decorate.def_retry(msg="redis: 弹出任务失败，正在重试连接！")
    def pop_task(self, task_name: str):
        """
        从任务队列中弹出一个任务实例

        队列存在数据的时候 返回 json格式数据
        队列不存在数据的时候，返回 None
        :param task_name: 任务队列名称
        :return: json/None
        """
        with self.conn as redis_conn:
            bson_data = redis_conn.rpop(task_name)
            if not bson_data:
                return None
            data_json = json.loads(bson_data)
            return data_json

    @Decorate.def_retry(msg="redis: hash添加数据失败，正在重试连接！")
    def hash_task(self, hash_name, hash_data):
        """
        将hash加密的数据缓存到redis。
        保存格式为 hash队列
        :param hash_name: hash队列的名称
        :param hash_data: hash加密之后的数据
        :return:
        """
        with self.conn as redis_conn:
            strTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            redis_conn.hset(hash_name, hash_data, strTime)

    @Decorate.def_retry(msg="redis: access_token获取失败，正在重试连接！")
    def get_lingxing_api_access_token(self):
        """
        获取领星API的token
        """
        AUTH_TOKEN = "common-lingxing-access-token:common:token"
        with self.conn as redis_conn:
            token = json.loads(redis_conn.get(AUTH_TOKEN))
            if token:
                return token.get("access_token")
            else:
                return None

    @Decorate.def_retry(msg="redis: auth_token获取失败，正在重试连接！")
    def get_lingxing_crawler_auth_token(self):
        """
        获取领星爬虫页面的token
        """
        AUTH_TOKEN = "common-lingxing-access-token:common:auth_tokens"
        with self.conn as redis_conn:
            token = redis_conn.srandmember(AUTH_TOKEN).decode()
            if token:
                return token
            else:
                return None

    @Decorate.def_retry(msg='redis: 数据设置失败！', error_type=False)
    def set_data(self, redis_key: str, redis_value: str):
        """
        设置键值
        :param redis_key: 键
        :param redis_value: 值
        """
        with self.conn as redis_conn:
            redis_conn.set(redis_key, redis_value)

    @Decorate.def_retry(msg='redis: 读取数据失败！', error_type=None)
    def get_data(self, redis_key: str):
        """
        读取redis数据
        :param redis_key: redis键名
        """
        with self.conn as redis_conn:
            data = redis_conn.get(redis_key)
            if data:
                return data.decode()
            else:
                return None
