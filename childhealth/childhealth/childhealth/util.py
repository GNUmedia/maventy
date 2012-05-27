import random

# skip: il1o0, uppercase
_rchars = "abcdefghjkmnpqrstuvwxyz23456789"

def random_string(len):
  """Generate a user-friendly random string of the given length."""
  rstr = ''
  for dummy in range(len):
      rstr += random.choice(_rchars)
  return rstr

