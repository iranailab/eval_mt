from .tool.counter_element import counter_element
from .tool.n_gram import ngrams
from .tool.overlaps_dict import overlaps_dict


class gleu:
    def __init__(self, min_n_gram = 1, max_n_gram = 4):
        self.min_n_gram = min_n_gram
        self.max_n_gram = max_n_gram


    def gleu_score(self, refs, pred):
        pred_all_gram = (self._all_gram(pred))
        tp_fp = sum(counter_element(pred_all_gram).values())

        scores = []
        for ref in refs:
            ref_all_gram = self._all_gram(ref)
            tp_fn = sum(counter_element(ref_all_gram).values())
            tp = sum(overlaps_dict(counter_element(ref_all_gram), counter_element(pred_all_gram)).values())
            """
                precision = tp / tp_fp
                recall = tp / tp_fn

                glue = min(precision, recall) <-----> max(tp_fp, tp_fn)

            """
            precision = tp / tp_fp
            recall = tp / tp_fn
            scores.append(min(precision, recall))
        return max(scores)

    def _all_gram(self, text, is_list = False):
        result = []
        for n in range(self.min_n_gram, self.max_n_gram + 1):
            result.extend(ngrams(text, n))
        return result

