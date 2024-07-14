from unittest import TestCase

from regex import IS_1900_TO_1909, IS_CUP_OF_COFFEE, IS_DOLLARS, IS_NEW_YORK


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

    def test_regex_is_dollars(self):
        self.assertRegex("Dollars", IS_DOLLARS)
        self.assertRegex("dollars", IS_DOLLARS)
        self.assertRegex("DOLLARS", IS_DOLLARS)
        self.assertRegex("dOlLaRs", IS_DOLLARS)

        self.assertNotRegex("Canadian Dollars", IS_DOLLARS)
        self.assertNotRegex("Australian Dollars", IS_DOLLARS)
        self.assertNotRegex("Dollars and Cents", IS_DOLLARS)

    def test_regex_is_cup_of_coffee(self):
        self.assertRegex("Coffee", IS_CUP_OF_COFFEE)
        self.assertRegex("coffee", IS_CUP_OF_COFFEE)
        self.assertRegex("COFFEE", IS_CUP_OF_COFFEE)
        self.assertRegex("cOFFEe", IS_CUP_OF_COFFEE)

        self.assertNotRegex("toffee", IS_CUP_OF_COFFEE)

        self.assertRegex("Cup of coffee", IS_CUP_OF_COFFEE)
        self.assertRegex("Black coffee", IS_CUP_OF_COFFEE)
        self.assertRegex("Goblet of coffee", IS_CUP_OF_COFFEE)
        self.assertRegex("Coffee, mug", IS_CUP_OF_COFFEE)
        self.assertRegex("Glass of fine coffee", IS_CUP_OF_COFFEE)
        self.assertRegex("Our best coffee, size demi-tasse", IS_CUP_OF_COFFEE)

        self.assertNotRegex("A gigantic pot of coffee", IS_CUP_OF_COFFEE)
        self.assertNotRegex("Coffee by the pound", IS_CUP_OF_COFFEE)
        self.assertNotRegex("Coffee, all you can drink", IS_CUP_OF_COFFEE)
        self.assertNotRegex("Cups of coffee for two", IS_CUP_OF_COFFEE)

        self.assertNotRegex("Coffee with cream", IS_CUP_OF_COFFEE)
        self.assertNotRegex("Iced Coffee", IS_CUP_OF_COFFEE)
        self.assertNotRegex("Cup of coffee with milk", IS_CUP_OF_COFFEE)

        self.assertNotRegex("Coffee cake", IS_CUP_OF_COFFEE)
        self.assertNotRegex("Coffee beans", IS_CUP_OF_COFFEE)
        self.assertNotRegex("Coffee buns", IS_CUP_OF_COFFEE)

class TestMain(TestCase):
    def test(self):
        pass

class TestBonus(TestCase):
    def test(self):
        pass
