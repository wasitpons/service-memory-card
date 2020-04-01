# ranking.py
from redis import Redis, RedisError
redis = Redis(host='redis', port=6379, charset="utf-8", decode_responses=True)

def find():
  global_ranking = redis.get('global_ranking')
  if global_ranking is None:
    return '0'
  return global_ranking

def getCurrentRanking(clicked):
  global_ranking = find()
  ranking = global_ranking.split(',')
  for count, item in enumerate(ranking, start=0):
    if clicked == int(item):
      return {
        'globalRanking': count+1
      }
  raise Exception('You ranking not found')

def save(clicked):
  global_ranking = find()
  if global_ranking == 0:
    ranking = 1
    redis.set('global_ranking', clicked)
    return {
      'globalRanking': ranking
    }
  else:
    ranking = global_ranking.split(',')
    for count, item in enumerate(ranking, start=0):
      if clicked <= int(item):
        ranking.insert(count, str(clicked))
        redis.set('global_ranking', ','.join(ranking))
        return getCurrentRanking(clicked)
    ranking.append(str(clicked))
    redis.set('global_ranking', ','.join(ranking))
    return getCurrentRanking(clicked)


def reset():
  redis.delete('global_ranking')