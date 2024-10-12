def validate_number(input: str, type: str, range: bool) -> bool:
  if type.lower() == "int":
    try:
      value = int(input)
      return value >= 0
    except ValueError:
      return False
  elif type.lower() == "float":
    try:
      value = float(input)
      if range == True:
        return (0.0 <= value and value <= 1.0)
      else:
        return value >= 0.0
    except ValueError:
      return False