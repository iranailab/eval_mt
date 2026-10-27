import math

from .tool.counter_element import counter_element
from .tool.n_gram import ngrams


class bleu:
	def __init__(self, min_n_gram = 1, max_n_gram = 4):
		self.min_n_gram = min_n_gram
		self.max_n_gram = max_n_gram

	def bleu_score(self, refs, pred):
		pred_ngram_count = [counter_element(ngrams(pred, n)) for n in range(self.min_n_gram, self.max_n_gram + 1)]
		pred_lenght = len(pred.split())

		refs_lenght = [len(ref.split()) for ref in refs]
		refs_ngram_count = list()
		for n in range(self.min_n_gram, self.max_n_gram + 1):
			result = [counter_element(ngrams(ref, n)) for ref in refs]
			refs_ngram_count.append(result)

		clipped_precision = list()
		for n in range(0, self.max_n_gram):
			clipped_count = self._clipped_count(refs_ngram_count[n], pred_ngram_count[n])
			total = sum(pred_ngram_count[n].values())
			clipped_precision.append(clipped_count / total if total else 0)


		db = 0
		for cp in clipped_precision:
			if cp == 0:
				db += math.log(1e-15) * (0.25)
			else :
				db += math.log(cp) * (0.25)

		return math.exp(db) * self._brevity_penalty(self._get_closest_ref_lenght(refs_lenght, pred_lenght), pred_lenght)
	

	def _clipped_count(self, refs_ngram, pred_ngram):
		score = 0
		for p_gram in pred_ngram:
			pred_ngram_count = pred_ngram[p_gram]
			max_gram_refs = 0
			for ref_ngram in refs_ngram:
				if p_gram in ref_ngram:
					max_gram_refs = max(max_gram_refs, ref_ngram[p_gram])

			score += min(max_gram_refs, pred_ngram_count)
		return score


	def _brevity_penalty(self, ref_lenght, pred_lenght):
		if pred_lenght > ref_lenght:
			return 1

		else:
			return math.exp(1 - ref_lenght / pred_lenght)

	def _get_closest_ref_lenght(self, refs_lenght, pred_lenght):
		return min(refs_lenght, key=lambda ref_lenght : abs(ref_lenght - pred_lenght))


