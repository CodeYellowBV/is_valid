from .base import Predicate
from .is_eq import is_eq
from .is_fixed import is_fixed


is_no_match = is_fixed(False, 'no_match', 'None of the conditions match.')


def identity(data):
    return data


class is_cond(Predicate):
    """
    Generates a predicate that given pairs of condition and validation
    predicates (represented as 2-tuples) returns the result of the validation
    predicate that corresponds to the first condition predicate that holds
    for the given data. If none of the condition predicates hold the predicate
    with the ``default`` keyword argument will be used. By default this will
    always consider the data invalid with the explanation that the data matches
    none of the conditions.
    """

    def __init__(
        self, *conditions,
        cond_trans=identity, pred_trans=identity,
        default=is_no_match
    ):
        self._conditions = [
            (c if callable(c) else is_eq(c), p if callable(p) else is_eq(p))
            for c, p in conditions
        ]
        self._cond_trans = cond_trans
        self._pred_trans = pred_trans
        self._default = default if callable(default) else is_eq(default)

    def _evaluate(self, data, explain, context):
        cond_data = self._cond_trans(data)
        pred_data = self._pred_trans(data)
        for condition, predicate in self._conditions:
            if condition(cond_data, context=context):
                return predicate(pred_data, explain, context)
        return self._default(pred_data, explain, context)
