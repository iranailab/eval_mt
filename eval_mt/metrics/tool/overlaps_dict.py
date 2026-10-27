def overlaps_dict(dict1, dict2):

  """ 
    To find commonalities of 2 dictionaries
    dict1 = {"a" : 3, "b" : 2, "c" : 7}
    dict2 = {"a" : 1, "b" : 5, "f" : 17}
    overlaps_dict(dict1, dict2)
    ---> {"a" : 1, "b" : 2}

  """

  overlaps = dict()
  for key in dict1:
    if key in dict2:
      _val_overlaps = min(dict1[key], dict2[key])
      overlaps.update({key : _val_overlaps})
  return overlaps