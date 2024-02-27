# coding = utf-8
# @Time    : 2024-02-27  09:15:30
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: Redis utils.

import redis
import json
import cfg

# Redis连接池, decode_responses=True表示将返回的byte类型数据解码为str类型
# 读取cfg制定的redis配置
pool = redis.ConnectionPool(host=cfg.REDIS_HOST, port=cfg.REDIS_PORT, db=cfg.REDIS_DB, decode_responses=True)
r = redis.Redis(connection_pool=pool)

# 保存数据到Redis，如果存在则更新
def save_to_redis(key, value):
    r.set(key, json.dumps(value))

# 从Redis中获取数据
def get_from_redis(key,default_value):
    value = r.get(key)
    print(f"Get Value: {value}")
    if value is not None:
        return json.loads(value)
    else:
        return default_value
    
# 从Redis中删除数据
def delete_from_redis(key):
    r.delete(key)

# 从Redis中获取所有的key
def get_all_keys_from_redis():
    return r.keys()

if __name__ == "__main__":
    # 测试
    save_to_redis("test", "test value")
    print(get_from_redis("test"))
    delete_from_redis("test")
    print(get_from_redis("test"))
    print(get_all_keys_from_redis())