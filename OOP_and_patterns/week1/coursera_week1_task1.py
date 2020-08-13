def factorize(x):
    """ Factorize positive integer and return its factors.
        :type x: int,>=0
        :rtype: tuple[N],N>0
    """
    pass

class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        case = ['string', 1.5]
        for x in case:
            with self.subTest(x=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        case = [-1, -10, -100]
        for x in case:
            with self.subTest(x=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        case = [0, 1]
        for x in case:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), (x,))

    def test_simple_numbers(self):
        case = [3, 13, 29]
        for x in case:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), (x,))

    def test_two_simple_multipliers(self):
        case = {6: (2, 3), 26: (2, 13), 121: (11, 11)}
        for x in case:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), case[x])

    def test_many_multipliers(self):
        cases = [(1001, (7,11,13)), (9699690, (2,3,5,7,11,13,17,19))]
        for x, res in cases:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), res)
