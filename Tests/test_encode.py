import collections
import unittest

import pytest

import bencode2
from bencode2 import BencodeEncodeError


class EncodeTestCase(unittest.TestCase):
    def test_exception_when_strict(self):
        invalid_obj = None
        with self.assertRaises(BencodeEncodeError):
            bencode2.bencode(invalid_obj)

    def test_encode_str(self):
        coded = bencode2.bencode("ThisIsAString")
        self.assertEqual(
            coded, b"13:ThisIsAString", msg="Failed to encode string from str."
        )

    def test_encode_int(self):
        coded = bencode2.bencode(42)
        self.assertEqual(coded, b"i42e", msg="Failed to encode integer from int.")

    def test_encode_bytes(self):
        pass
        b = b"TheseAreSomeBytes"
        coded = bencode2.bencode(b)
        s = bytes(str(len(b)), "utf-8")
        self.assertEqual(coded, s + b":" + b, msg="Failed to encode string from bytes.")

    def test_encode_list(self):
        s = ["a", "b", 3]
        coded = bencode2.bencode(s)
        self.assertEqual(coded, b"l1:a1:bi3ee", msg="Failed to encode list from list.")

    def test_encode_tuple(self):
        t = ("a", "b", 3)
        coded = bencode2.bencode(t)
        self.assertEqual(coded, b"l1:a1:bi3ee", msg="Failed to encode list from tuple.")

    def test_encode_dict(self):
        od = collections.OrderedDict()
        od["ka"] = "va"
        od["kb"] = 2
        coded = bencode2.bencode(od)
        self.assertEqual(
            coded, b"d2:ka2:va2:kbi2ee", msg="Failed to encode dictionary from dict."
        )

    def test_encode_complex(self):
        od = collections.OrderedDict()
        od["KeyA"] = ["listitemA", {"k": "v"}, 3]
        od["KeyB"] = {"k": "v"}
        od["KeyC"] = 3
        od["KeyD"] = "AString"
        expected_result = (
            b"d4:KeyAl9:listitemAd1:k1:vei3ee4:KeyBd1:k1:ve4:KeyCi3e4:KeyD7:AStringe"
        )
        coded = bencode2.bencode(od)
        self.assertEqual(coded, expected_result, msg="Failed to encode complex object.")
        pass


data = {
    "_id": "5973782bdb9a930533b05cb2",
    "isActive": True,
    "balance": "$1,446.35",
    "age": 32,
    "eyeColor": "green",
    "name": "Logan Keller",
    "gender": "male",
    "company": "ARTIQ",
    "email": "logankeller@artiq.com",
    "phone": "+1 (952) 533-2258",
    "friends": [
        {"id": 0, "name": "Colon Salazar"},
        {"id": 1, "name": "French Mcneil"},
        {"id": 2, "name": "Carol Martin"},
    ],
    "favoriteFruit": "banana",
}


def test_encode():
    bencode2.bencode(data)


def test_duplicated_type_keys():
    with pytest.raises(BencodeEncodeError):
        bencode2.bencode({"string_key": 1, b"string_key": 2})
