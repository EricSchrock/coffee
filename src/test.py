from math import isnan
from unittest import TestCase

import pandas as pd

from main import (profile_dish_data, profile_menu_data,
                  remove_leading_and_trailing_whitespace,
                  repair_dish_name_coffee_spelling,
                  repair_menu_currency_convert_cents_to_dollars,
                  repair_menu_currency_dollars_spelling,
                  repair_menu_date_from_call_number,
                  repair_menu_date_outside_expected_range,
                  repair_menu_place_new_york_spelling)
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
    def test_remove_leading_and_trailing_whitespace(self):
        menu_df = pd.DataFrame({'date': ["1900\n"], 'call_number': ["  1900-123  "], 'place': ["   Albany, NY"], 'currency': ["\tDollars\r\n"]})
        page_df = pd.DataFrame()
        item_df = pd.DataFrame({'price': [0.25]})
        dish_df = pd.DataFrame({'name': ["  Cup of Coffee"]})

        remove_leading_and_trailing_whitespace(menu_df, page_df, item_df, dish_df)

        self.assertEqual(menu_df['date'].iloc[0], "1900")
        self.assertEqual(menu_df['call_number'].iloc[0], "1900-123")
        self.assertEqual(menu_df['place'].iloc[0], "Albany, NY")
        self.assertEqual(menu_df['currency'].iloc[0], "Dollars")
        self.assertEqual(item_df['price'].iloc[0], 0.25)
        self.assertEqual(dish_df['name'].iloc[0], "Cup of Coffee")

    def test_repair_menu_date_from_call_number(self):
        menu_df = pd.DataFrame({'date': ["1900", float("nan"), float("nan"), float("nan"), float("nan")], 'call_number': ["1899-01", "1899-02", "Other", "", float("nan")]})
        page_df = pd.DataFrame()
        item_df = pd.DataFrame()
        dish_df = pd.DataFrame()

        repair_menu_date_from_call_number(menu_df, page_df, item_df, dish_df)

        self.assertEqual(menu_df['date'].iloc[0], "1900")
        self.assertEqual(menu_df['date'].iloc[1], "1899")

        self.assertTrue(isnan(menu_df['date'].iloc[2]))
        self.assertTrue(isnan(menu_df['date'].iloc[3]))
        self.assertTrue(isnan(menu_df['date'].iloc[4]))

    def test_repair_menu_date_outside_expected_range(self):
        menu_df = pd.DataFrame({'date': ["0190-01-01", "1091-05-05", "2928-12-31", "12/31/2928"]})
        page_df = pd.DataFrame()
        item_df = pd.DataFrame()
        dish_df = pd.DataFrame()

        repair_menu_date_outside_expected_range(menu_df, page_df, item_df, dish_df)

        self.assertEqual(menu_df['date'].iloc[0], "1900-01-01")
        self.assertEqual(menu_df['date'].iloc[1], "1901-05-05")
        self.assertEqual(menu_df['date'].iloc[2], "1928-12-31")
        self.assertEqual(menu_df['date'].iloc[3], "12/31/2928")

    def test_repair_menu_place_new_york_spelling(self):
        menu_df = pd.DataFrame({'place': ["Now Yurk", "New Y0rk", "Ne York", "Nwe York"]})
        page_df = pd.DataFrame()
        item_df = pd.DataFrame()
        dish_df = pd.DataFrame()

        repair_menu_place_new_york_spelling(menu_df, page_df, item_df, dish_df)

        self.assertEqual(menu_df['place'].iloc[0], "Now Yurk")
        self.assertEqual(menu_df['place'].iloc[1], "New York")
        self.assertEqual(menu_df['place'].iloc[2], "New York")
        self.assertEqual(menu_df['place'].iloc[3], "New York")

    def test_repair_menu_currency_dollars_spelling(self):
        menu_df = pd.DataFrame({'currency': ["Doller", "Dollers", "Dollar", "Dolalrs"]})
        page_df = pd.DataFrame()
        item_df = pd.DataFrame()
        dish_df = pd.DataFrame()

        repair_menu_currency_dollars_spelling(menu_df, page_df, item_df, dish_df)

        self.assertEqual(menu_df['currency'].iloc[0], "Doller")
        self.assertEqual(menu_df['currency'].iloc[1], "Dollars")
        self.assertEqual(menu_df['currency'].iloc[2], "Dollars")
        self.assertEqual(menu_df['currency'].iloc[3], "Dollars")

    def test_repair_menu_currency_convert_cents_to_dollars(self):
        menu_df = pd.DataFrame({'id': [1], 'currency': ["Cents"]})
        page_df = pd.DataFrame({'id': [2], 'menu_id': [1]})
        item_df = pd.DataFrame({'menu_page_id': [2], 'price': [10.0]})
        dish_df = pd.DataFrame()

        repair_menu_currency_convert_cents_to_dollars(menu_df, page_df, item_df, dish_df)

        self.assertEqual(menu_df['currency'].iloc[0], "Dollars")
        self.assertEqual(item_df['price'].iloc[0], 0.1)

    def test_repair_dish_name_coffee_spelling(self):
        menu_df = pd.DataFrame()
        page_df = pd.DataFrame()
        item_df = pd.DataFrame()
        dish_df = pd.DataFrame({'name': ["Caffe", "Caffee", "Coffe", "Cofefe"]})

        repair_dish_name_coffee_spelling(menu_df, page_df, item_df, dish_df)

        self.assertEqual(dish_df['name'].iloc[0], "Caffe")
        self.assertEqual(dish_df['name'].iloc[1], "Coffee")
        self.assertEqual(dish_df['name'].iloc[2], "Coffee")
        self.assertEqual(dish_df['name'].iloc[3], "Coffee")

    def test_profile_menu_data(self):
        menu_df = pd.DataFrame({
            'id':       [1,         2,         3,      4,         5,    6,         7,      8,         9 ],
            'place':    ["NY",      "NY",      "NY",   "NY",      "NY", "",        "",     "",        ""],
            'date':     ["1900",    "1900",    "1900", "",        "",   "1900",    "1900", "",        ""],
            'currency': ["Dollars", "Dollars", "",     "Dollars", "",   "Dollars", "",     "Dollars", ""],
        })

        profile = profile_menu_data.__wrapped__(menu_df)

        self.assertListEqual(profile, [1,1,1,1,1,1,2])

    def test_profile_dish_data(self):
        dish_df = pd.DataFrame({
            'id':   [1,        2,        3,        4,  5 ],
            'name': ["Coffee", "Coffee", "Coffee", "", ""],
        })

        profile = profile_dish_data.__wrapped__(dish_df)

        self.assertEqual(profile, 3)

    def test_query_data(self):
        pass

    def test_clean_data(self):
        pass
