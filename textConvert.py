"""
This module converts a message into numbers to prepare it for encryption
Trying out unit testing.
"""

import unittest

conversion_key = {
	  ' ': '55',
	  '1': '91',
	  '0': '88',
	  '3': '93',
	  '2': '92',
	  '5': '95',
	  '4': '94',
	  '7': '97',
	  '6': '96',
	  '9': '99',
	  '8': '98',
	  'a': '11',
	  'c': '13',
	  'b': '12',
	  'e': '15',
	  'd': '14',
	  'g': '17',
	  'f': '16',
	  'i': '19',
	  'h': '18',
	  'k': '22',
	  'j': '21',
	  'm': '24',
	  'l': '23',
	  'o': '26',
	  'n': '25',
	  'q': '28',
	  'p': '27',
	  's': '31',
	  'r': '29',
	  'u': '33',
	  't': '32',
	  'w': '35',
	  'v': '34',
	  'y': '37',
	  'x': '36',
	  'z': '38'
}

message = "word1 word2 word3"


class MyTest(unittest.TestCase):
	def test_split_by_n(self):
		self.assertEqual(split_by_n("123456789", 3), ["123", "456", "789"])
		self.assertEqual(split_by_n("123456789", 9), ["123456789"])
		self.assertEqual(split_by_n("123", 1), ["1", "2", "3"])
	def test_convert_to_numerals(self):
		self.assertEqual(convert_to_numerals('123'), "919293")
		self.assertEqual(convert_to_numerals('abc'), "111213")
		self.assertEqual(convert_to_numerals('123abc'), "919293111213")
		self.assertEqual(convert_to_numerals('123 abc'), "91929300111213")
	def test_convert_to_alpha(self):
		self.assertEqual(convert_to_alpha('919293'), "123")
		self.assertEqual(convert_to_alpha('111213'), "abc")
		self.assertEqual(convert_to_alpha('919293111213'), "123abc")
		self.assertEqual(convert_to_alpha('91929300111213'), "123 abc")
	def test_reverse_dict_keys_values(self):
		self.assertEqual(next(reverse_dict_keys_values({'a': '1', 'b': '2'})), {'1': 'a', '2': 'b'})

def reverse_dict_keys_values(dict_input):
	#flip the keys and values in a dictionary
	yield {v: k for k, v in dict_input.iteritems()}

def convert_long_list_to_string_list(long_list):
	return [str(x) for x in long_list]

def split_by_n_generator(sequence, n):
	#generator splits a sequence by n
    while sequence:
        yield sequence[:n]
        sequence = sequence[n:]

def split_by_n(sequence, n):
	#returns a full list rather than interator for split_by_n_generator
	return [x for x in split_by_n_generator(sequence, n)]

def convert_to_numerals(str_input):
	#converts string to numerals base on the conversion key
	split_input = split_by_n(str_input, 1) 
	for i in range(len(split_input)):
		split_input[i] = conversion_key[split_input[i]]
	return ''.join(split_input)

def convert_to_alpha(int_input):
	#converts a numeral sequence to alphabetical characters based on the conversion key
	reverse_conversion_key = next(reverse_dict_keys_values(conversion_key))
	split_input = split_by_n(int_input, 2)
	for i in range(len(split_input)):
		split_input[i] = reverse_conversion_key[split_input[i]]
	return ''.join(split_input)

if __name__ == '__main__':
	unittest.main()







