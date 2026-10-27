import math

from .tool.counter_element import counter_element
from .tool.n_gram import ngrams
from .tool.overlaps_dict import overlaps_dict


class nist:
  def __init__(self, n = 5):
    self.number_n_grams = n

  def nist_score(self, refs, pred):
    pred_ngrams = [ngrams(pred, n) for n in range(1 , self.number_n_grams + 1)]
    refs_ngrams = [[ngrams(ref, n) for n in range(1, self.number_n_grams + 1)] for ref in refs]

    refs_ngrams_freq ,refs_total_words = dict() , 0
    for index in range(0, len(refs)):
      refs_total_words += len(refs[index].split())
      for num_gram in range(0, self.number_n_grams):
        count_ngrams = counter_element(refs_ngrams[index][num_gram])
        for element in count_ngrams:
          refs_ngrams_freq[element] = (refs_ngrams_freq[element] + count_ngrams[element]) if element in refs_ngrams_freq else 1

    info = self._info(refs_ngrams_freq, refs_total_words)

    nist_score , pred_lenght, ref_lenght = [], len(pred.split()), 0
    for n in range(0, self.number_n_grams):

      nist_precisions = list()
      for index_ref in range(0, len(refs)):
        ref_count_gram = counter_element(refs_ngrams[index_ref][n])
        pred_coumt_gram = counter_element(pred_ngrams[n])
        overlaps_ngram = overlaps_dict(ref_count_gram, pred_coumt_gram)
        numerator = sum([info[n_gram] * count for n_gram, count in overlaps_ngram.items()])
        denominator = sum(pred_coumt_gram.values())
        nist_precisions.append(numerator / denominator if denominator else 0)
      nist_score.append(max(nist_precisions))
      ref_lenght += len(refs[nist_precisions.index(max(nist_precisions))].split())

    return sum(nist_score) * self._length_penalty((ref_lenght / self.number_n_grams), pred_lenght)




  def _info(self, refs_ngrams_freq, refs_total_words):
    info = dict()
    for grams_1n in refs_ngrams_freq:
      grams_1m = grams_1n[ : -1] #w1, w2, ... wn-1
      occurrence = refs_ngrams_freq[grams_1m] if grams_1m and grams_1m in refs_ngrams_freq else refs_total_words
      info[grams_1n] = math.log(occurrence / refs_ngrams_freq[grams_1n], 2)
    return info



  def _length_penalty(self, refs_lenght, pred_lenght):
    ratio = pred_lenght / refs_lenght
    if 0 < ratio < 1:
        beta = math.log(0.5) / math.log(1.5) ** 2
        return math.exp(beta * math.log(ratio) ** 2)
    else:
        return 1
