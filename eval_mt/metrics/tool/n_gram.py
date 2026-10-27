def ngrams(text, n, ignore_split = False):



  if ignore_split:

    """
      model = n_grams()
      model.fit_grams("alireza", 3, True)
      --->[("ali"), ("lir"), ("ire"), ("rez"), ("eza")]
    """
    return [tuple(text[index : index + n]) for index in range(0, len(text) - n + 1)]


  else:
    """
      model = n_grams()
      model.fit_grams("this is a ball", 2)
      --->[('this', 'is'), ('is', 'a'), ('a', 'ball')]
    """

    text = text.lower()
    words = text.split()
    return [tuple(words[index : index + n]) for index in range(0, len(words) - n + 1)]