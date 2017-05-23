import redis
import random
Redis_Host = "52.163.48.238"
Redis_port = 10102
Redis_db = 1
pool = redis.ConnectionPool(host=Redis_Host,port=Redis_port,db=Redis_db)
client = redis.Redis(connection_pool=pool)
# redis_urls = client.hget(2240013,"movie_url")
# redis_crawled = client.hget(2240013,"crawled")
redisKeys = client.keys()
elem = random.choice(redisKeys)
# print redis_urls
# print redis_crawled
redis_urls = client.hget(elem,"movie_url")
redis_crawled = client.hget(elem,"crawled")
print len(redisKeys)
print elem
print redis_urls
print redis_crawled