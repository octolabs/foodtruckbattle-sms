# code source - http://appengine-cookbook.appspot.com/recipe/high-concurrency-counters-without-sharding/
import logging

from google.appengine.api import memcache
from google.appengine.ext import db

class CounterModel(db.Model):
    counter = db.IntegerProperty()

def incrementCounter(key, delta=1, update_interval=10):
    """Increments a memcached counter.
    Args:
      key: The key of a datastore entity that contains the counter.
      delta: Non-negative integer value (int or long) to increment key by, defaulting to 1.
      update_interval: Minimum interval between updates.
    """
    lock_key  = "counter_lock:%s" % (key,)
    count_key = "counter_val:%s" % (key,)

    if memcache.add(lock_key, None, time=update_interval):
        # Time to update the DB
        prev_count = int(memcache.get(count_key) or 0)
        new_count = prev_count + delta

        def tx():
            entity = CounterModel.get_by_key_name(key)
            entity.counter += new_count
            entity.put()

        try:
            db.run_in_transaction(tx)
            if prev_count>0 and memcache.decr(count_key, delta=prev_count) is None:
                logging.warn("counter %s could not be decremented (will double-count): %d" % (key, prev_count))
        except Exception, e:
            # db failed to update: we'll try again later; just add delta to memcache like usual for now
            memcache.incr(count_key, delta, initial_value=0)
    else:
        # Just update memcache
        memcache.incr(count_key, delta, initial_value=0)