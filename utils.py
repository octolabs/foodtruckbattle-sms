import models
from google.appengine.ext import db
from google.appengine.api import memcache

""" returns sms message body with top 3 food trucks/votes """
def getTop3():
	top3 = db.GqlQuery("SELECT * FROM Truck ORDER BY counter DESC LIMIT 3")

	msg="Thanks for voting! Leaderboard: "
	for truck in top3:
		msg=msg+truck.name+" - "+str(truck.counter)+" votes | "

	return msg


""" incerement counter for defined food truck, based on foodtruck handle"""	
def incrementCounter(key, update_interval=10):
  """Increments a memcached counter.
  Args:
    key: The key of a datastore entity that contains the counter.
    update_interval: Minimum interval between updates.
  """
  lock_key = "counter_lock:%s" % (key,)
  count_key = "counter_value:%s" % (key,)
  if memcache.add(lock_key, None, time=update_interval):
    # Time to update the DB
    count = int(memcache.get(count_key) or 0) + 1
    def tx():
      entity = models.Truck.get_by_key_name(key)
      entity.counter += count
      entity.put()
    db.run_in_transaction(tx)
    memcache.delete(count_key)
  else:
    # Just update memcache
    memcache.incr(count_key, initial_value=0)

