
# general `uses()` function to check if `find_*()` finds results based on queries
def uses(function, *args, **kwargs):
  return len(function(*args, **kwargs).elements) > 0