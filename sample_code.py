    #  """Sample code for returning time zone for an IP address
    #  Args:
    #      input (dict): dictionary containing input field(s) supplied in the recipe step
    #  Returns:
    #      dict: dictionary with keys matching the output schema
    #  """
    #  ip_address = input["ip_address"]
    #  response = requests.get("https://worldtimeapi.org/api/ip/{}".format(ip_address))
    #  if response.status_code != 200:
    #    raise ConnectionError(response.json()["error"])
    #  timezone = response.json()["timezone"]
    #  return {'timezone': timezone}