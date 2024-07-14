from unittest import TestCase

from regex import IS_NEW_YORK


class TestRegex(TestCase):
    def test_regex_is_new_york(self):
        self.assertRegex("New York", IS_NEW_YORK)
        self.assertRegex("new york", IS_NEW_YORK)
        self.assertRegex("NEW YORK", IS_NEW_YORK)
        self.assertRegex("NeW yOrK", IS_NEW_YORK)

        self.assertNotRegex("newyork", IS_NEW_YORK)
        self.assertNotRegex("new-york", IS_NEW_YORK)
        self.assertNotRegex("new yorkie", IS_NEW_YORK)
        self.assertNotRegex("york", IS_NEW_YORK)
        self.assertNotRegex("new mexico", IS_NEW_YORK)
        self.assertNotRegex("newer york", IS_NEW_YORK)

        self.assertRegex("NY", IS_NEW_YORK)
        self.assertRegex("N.Y.", IS_NEW_YORK)
        self.assertRegex("NYC", IS_NEW_YORK)
        self.assertRegex("N.Y.C", IS_NEW_YORK)

        self.assertNotRegex("many", IS_NEW_YORK)

        self.assertRegex("new yorker", IS_NEW_YORK)
        self.assertRegex("new yorkers", IS_NEW_YORK)

class TestMain(TestCase):
    def test(self):
        pass

class TestBonus(TestCase):
    def test(self):
        pass
