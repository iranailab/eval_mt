from nltk.corpus import wordnet
from nltk.stem.porter import PorterStemmer


class meteor:
	def __init__(self):
		self.stemmer = PorterStemmer()

	def metor_score(self, refs, pred):
		return max([self._metor_single_refs_pred(ref, pred) for ref in refs])

	def _metor_single_refs_pred(self, ref, pred):
		ref_num_word = self._create_num(ref)
		pred_num_word = self._create_num(pred)

		#matching_word by word
		matching_word_by_word , ref_num_word , pred_num_word = self._matching_word_by_word(ref_num_word, pred_num_word)

		#stemmer matching word by word
		stemmer_matching_word_by_word , ref_num_word , pred_num_word = self._stemmer_matching_word_by_word(ref_num_word, pred_num_word)

		#synonymm atching word by word
		synonymm_matching_word_by_word , ref_num_word , pred_num_word = self._synonymm_matching_word_by_word(ref_num_word, pred_num_word)


		all_marches = sorted(matching_word_by_word + stemmer_matching_word_by_word + synonymm_matching_word_by_word, key=lambda element : element[0])

		ref_lenght = len(ref.split())
		pred_lenght = len(pred.split())
		matches_lenght = len(all_marches)
		try:
			precision = matches_lenght / pred_lenght
			recall = matches_lenght / ref_lenght
			fscore = (precision * recall * 10) / ((9 * precision) +  recall)
			chunk_count = self._chunks(all_marches)
			frag_frac = chunk_count / matches_lenght
		except ZeroDivisionError:
			return 0

		penalty = 0.5 * (frag_frac ** 3)
		return fscore * (1 - penalty)
	
	def _matching_word_by_word(self, ref_num_word, pred_num_word):
		matching_word_by_word = list()
		for index_pred in range(0 , len(pred_num_word))[::-1]:
			for index_ref in range(0, len(ref_num_word))[::-1]:
				if pred_num_word[index_pred][1] == ref_num_word[index_ref][1]:
					matching_word_by_word.append(tuple([pred_num_word[index_pred][0], ref_num_word[index_ref][0]]))
					ref_num_word.pop(index_ref)
					pred_num_word.pop(index_pred)
					break
		return matching_word_by_word , ref_num_word, pred_num_word

	def _stemmer_matching_word_by_word(self, ref_num_word, pred_num_word):
		ref_num_word = [tuple([element[0], self.stemmer.stem(element[1])]) for element in ref_num_word]
		pred_num_word = [tuple([element[0], self.stemmer.stem(element[1])]) for element in pred_num_word]
		return self._matching_word_by_word(ref_num_word, pred_num_word)		

	def _synonymm_matching_word_by_word(self, ref_num_word, pred_num_word):
		matching_word_by_word = []
		for index_pred in range(0, len(pred_num_word))[::-1]:
			word_synonymms= wordnet.synsets(pred_num_word[index_pred][1])
			pred_synonymm = [pred_num_word[index_pred][1]]

			for synonymm in word_synonymms:
				for lemma in synonymm.lemmas():
					if lemma.name().find("_") < 0:
						pred_synonymm.append(lemma.name())

			pred_synonymm = set(pred_synonymm)

			for index_ref in range(0, len(ref_num_word))[::-1]:
				if ref_num_word[index_ref][1] in pred_synonymm:
					matching_word_by_word.append(tuple([pred_num_word[index_pred][0], ref_num_word[index_ref][0]]))
					ref_num_word.pop(index_ref)
					pred_num_word.pop(index_pred)
					break
		return matching_word_by_word, ref_num_word, pred_num_word

	def _chunks(self, matches):
		index = 0
		chunk = 1

		while index < len(matches) - 1:
			if (matches[index + 1][0] == matches[index][0] + 1) and (matches[index + 1][1] == matches[index][1] + 1):
				index += 1
				continue

			chunk += 1
			index += 1
		return chunk
		
	def _create_num(self, text):
		text = text.lower()
		words = text.split()
		num_words = [tuple([index, words[index]]) for index in range(len(words))]
		return num_words



