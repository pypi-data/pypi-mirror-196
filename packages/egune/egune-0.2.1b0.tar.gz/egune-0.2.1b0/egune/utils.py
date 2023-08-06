import redis
from json import dumps, loads
import requests


def normalize_user_id(user_id):
    return user_id.split(":")[0]


class Cache(object):
    def __init__(self, config):
        self.redis = redis.Redis(host=config["host"], port=config["port"], db=0)
        self.ttl = config["ttl"]
        self.prefix = config["prefix"] + ":"

    def __contains__(self, key):
        return self.redis.exists(self.prefix + str(key))

    def __getitem__(self, key):
        return loads(self.redis.get(self.prefix + str(key)))

    def __setitem__(self, key, value):
        self.redis.set(self.prefix + str(key), dumps(value), ex=self.ttl)

    def __delitem__(self, key):
        return self.redis.delete(self.prefix + str(key))

    def clear(self):
        return self.redis.flushall()


class Module:
    def __init__(self, config):
        self.name = config["name"]
        if "cache" in config:
            self.cache = Cache(config["cache"])
        self.use_cache = "cache" in config
        self.address = f"http://{config['host']}:{config['port']}/"
        self.config = config

    def post(self, endpoint, *args):
        try:
            resp = requests.post(self.address + endpoint, json={"__args__": args})
            return resp.json()["data"]
        except Exception as e:
            print(f"ERROR: {self.name}", args, flush=True)
            print(e, flush=True)
