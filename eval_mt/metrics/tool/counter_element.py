def counter_element(temp):


  """

    This function is used to count the elements in n_grams
    temp = [1, 2, 3, 2, 1, 1, 1]
    counter_element(temp)
    ---> {1 : 4, 2 : 2, 3 : 1}

  """

  counter = {}
  for element in temp:
    counter[element] = counter[element] + 1 if element in counter else 1
  return counter
