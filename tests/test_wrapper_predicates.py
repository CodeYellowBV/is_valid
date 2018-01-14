from unittest import TestCase
import json

from is_valid import is_json_where, is_dict_where, is_list_of, is_bool,\
    is_str, is_int, is_optional, is_nullable

from .utils import json_data, incorrect_json_data, invalid_json_data


class TestJSON(TestCase):

    def setUp(self):
        self.pred = is_dict_where(
            foo=is_list_of(
                is_dict_where(
                    bar=is_bool,
                    baz=is_str
                )
            ),
            bar=is_int
        )
        self.json_pred = is_json_where(self.pred)

    def test_is_json_where(self):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                self.json_pred(json_data),
                self.json_pred.explain(json_data).valid
            )
        with self.subTest('pred correct'):
            self.assertTrue(self.json_pred(json_data))

    def test_is_json_where_incorrect(self):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                self.json_pred(incorrect_json_data),
                self.json_pred.explain(incorrect_json_data).valid
            )
        with self.subTest('pred correct'):
            self.assertFalse(self.json_pred(incorrect_json_data))

    def test_is_json_where_invalid(self):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                self.json_pred(invalid_json_data),
                self.json_pred.explain(invalid_json_data).valid
            )
        with self.subTest('pred correct'):
            self.assertFalse(self.json_pred(invalid_json_data))

    def test_is_json_where_failing_loader(self):
        def failing_loader(body):
            raise NotImplementedError()

        json_pred = is_json_where(self.pred, loader=failing_loader)
        with self.subTest('pred raises'):
            with self.assertRaises(NotImplementedError):
                json_pred(json_data)

    def test_is_json_on_non_pred(self):
        pred = is_json_where(json.loads(json_data))
        with self.subTest('valid data'):
            self.assertTrue(pred(json_data))
        with self.subTest('invalid json'):
            self.assertFalse(pred(incorrect_json_data))


class TestOptionalPredicates(TestCase):

    def test_is_optional(self):
        pred = is_optional(1)
        for value, expected in [(1, True), (None, True), (0, False)]:
            with self.subTest(
                'explain=True == explain=False; {}; {}'
                .format(value, expected)
            ):
                self.assertEqual(pred(value), pred.explain(value).valid)
            with self.subTest('pred correct; {}; {}'.format(value, expected)):
                self.assertEqual(pred(value), expected)

    def test_is_nullable(self):
        pred = is_nullable(1)
        for value, expected in [(1, True), (None, True), (0, False)]:
            with self.subTest(
                'explain=True == explain=False; {}; {}'
                .format(value, expected)
            ):
                self.assertEqual(pred(value), pred.explain(value).valid)
            with self.subTest('pred correct; {}; {}'.format(value, expected)):
                self.assertEqual(pred(value), expected)
