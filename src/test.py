from unittest import TestCase

from regex import IS_1900_TO_1909, IS_NEW_YORK


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

        self.assertRegex("Albany, NY", IS_NEW_YORK)
        self.assertRegex("Some random place in New York", IS_NEW_YORK)
        self.assertRegex("New York? Maybe?", IS_NEW_YORK)
        self.assertRegex("Fancy Restaurant [NY]", IS_NEW_YORK)

    def test_regex_is_1900_to_1909(self):
        self.assertRegex("1900", IS_1900_TO_1909)
        self.assertRegex("1909", IS_1900_TO_1909)

        self.assertNotRegex("1899", IS_1900_TO_1909)
        self.assertNotRegex("1910", IS_1900_TO_1909)

        self.assertRegex("1900-01-01", IS_1900_TO_1909)
        self.assertRegex("1909-12-31", IS_1900_TO_1909)

        self.assertNotRegex("1899-12-31", IS_1900_TO_1909)
        self.assertNotRegex("1910-01-01", IS_1900_TO_1909)

        self.assertNotRegex("12/05/1905", IS_1900_TO_1909)

class TestMain(TestCase):
    def test(self):
        pass

class TestBonus(TestCase):
    def test(self):
        pass
