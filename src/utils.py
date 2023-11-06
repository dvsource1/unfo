def make_it_number(value):
  # print(f"Making it number: {value}")
  num_str = ''.join(filter(str.isdigit, value))
  return int(num_str) if num_str else 0
