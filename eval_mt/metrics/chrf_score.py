import string

from .tool.counter_element import counter_element
from .tool.n_gram import ngrams
from .tool.overlaps_dict import overlaps_dict


class chrf:
	"""
		we calcute chrf score
		ref = "this is a blue ball"
		pred = "this iss a blue bal"
		model = chrf_score()
		model.fit(pred, ref)
			--- > 0.7657370407370406
		
	"""

	def __init__(self, min_size_ngram = 1, max_size_ngram = 6):

		"""
  			the standard CHR F with β = 1 i.e. the harmonic mean of precision and recall, 
			as well as CHR F3 where β = 3, i.e. the recall has three times more weight. 
			The number 3 has been taken arbitraly as a preliminary value, 
			and the CHR F3 is tested only on WMT 14 data – more systematic experiments in this direction should be carried out in the future work.

			β is a parameter which assigns β times more
			importance to recall than to precision – if β = 1,
			they have the same importance.


			As a first step, we carried out several experiments regarding n-gram length.
			Since the optimal n for word-based measures is shown to be n = 4,  
			MTERATER used up to 10-gram and BEER up to 6-gram, we investigated those three variants. 
			In addition, we investigated a dynamic n calculated for each sentence as the average word length. 
			The best correlations are obtained for 6-gram, there- fore we carried out further experiments only on them.
		"""
		self.min_size_ngram = min_size_ngram
		self.max_size_ngram = max_size_ngram
		self.beta = 3 # chrf3

	def chrf_score(self, ref, pred):
		"""
			we calcute precision recall 
			and we calcute  chrf : ((1 + beta ** 2) * (recall * precision)) / (beat ** 2 * recall + precision) for each n (grams)
		"""
		ref = self._preprocess(ref)
		pred = self._preprocess(pred)

		chrf_scores = list()
		for n in range(self.min_size_ngram, self.max_size_ngram + 1):
			ref_ngrams = ngrams(ref, n, True)
			pred_ngrams = ngrams(pred, n, True)

			Precision_recall = self._precision_recall(ref_ngrams, pred_ngrams)
			chrf = None
			try:
				chrf = ((1 + self.beta ** 2) * Precision_recall["precision"] * Precision_recall["recall"]) / (self.beta ** 2 * Precision_recall["precision"] + Precision_recall["recall"])
			except ZeroDivisionError:
				chrf = 0
			chrf_scores.append(chrf)

		return sum(chrf_scores) / len(chrf_scores)

	def _precision_recall(self, ref_ngram, predict_ngram):

	  """
		    this is based on confusion matrix
		    tp :  
		      The common members in the reference sentence and the sentence translated by the sentence, 
		      which means the ones that are predicted correctly (considered as correct translation) 
		      and are really correct because they are shared with the reference sentence.

		    tp + fp : 
		      In the sentence translated by machines, 
		      those that are translated correctly and are really correct and those that are considered correct but are wrong

		    tp + fn : 
		      In the reference sentence, there are those that are translated correctly and are really correct, 
		      and those that are considered as wrong translations but are correct.

		  precision = tp / tpfp
		  recall = tp / tpfn

	  """
	  ref_ngram_count = counter_element(ref_ngram)
	  predict_ngram_count = counter_element(predict_ngram)

	  tp = sum(overlaps_dict(ref_ngram_count, predict_ngram_count).values())
	  tpfp = sum(predict_ngram_count.values())
	  tpfn = sum(ref_ngram_count.values())
	  precision = tp / tpfp
	  recall = tp / tpfn

	  return {
	    "precision" : precision,
	    "recall" : recall
	  }

	def _preprocess(self, text):
		"""
			In this model, we have to ignore the distances and remove 
		"""
		translator = str.maketrans('', '',string.punctuation)
		text = text.translate(translator)
		return "".join([char for char in text if char != " "])



