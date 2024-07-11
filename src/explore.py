from argparse import ArgumentParser
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from typing import Tuple

from regex import is_new_york, is_1900_to_1909, is_dollars


def load_data(dataset_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    menu_df = pd.read_csv(f"{dataset_path}/Menu.csv")
    dish_df = pd.read_csv(f"{dataset_path}/Dish.csv")
    return menu_df, dish_df

def explore_menu_table(menu_df: pd.DataFrame) -> None:
    menus_with_no_place       = menu_df[ menu_df['place'].isna()]
    menus_from_new_york       = menu_df[ menu_df['place'].str.contains(is_new_york, na=False)]
    menus_from_other_places   = menu_df[~menu_df['place'].str.contains(is_new_york, na=False) & menu_df['place'].notnull()]

    menus_with_no_date        = menu_df[ menu_df['date'].isna()]
    menus_from_1900_to_1909   = menu_df[ menu_df['date'].str.contains(is_1900_to_1909, na=False)]
    menus_from_other_dates    = menu_df[~menu_df['date'].str.contains(is_1900_to_1909, na=False) & menu_df['date'].notnull()]

    menus_with_no_currency    = menu_df[ menu_df['currency'].isna()]
    menus_in_dollars          = menu_df[ menu_df['currency'].str.contains(is_dollars, na=False)]
    menus_in_other_currencies = menu_df[~menu_df['currency'].str.contains(is_dollars, na=False) & menu_df['currency'].notnull()]

    assert (menus_with_no_place['place'].size + menus_from_new_york['place'].size + menus_from_other_places['place'].size) == menu_df['place'].size, "Invalid place value assumptions"
    assert (menus_with_no_date['date'].size + menus_from_1900_to_1909['date'].size + menus_from_other_dates['date'].size) == menu_df['date'].size, "Invalid date value assumptions"
    assert (menus_with_no_currency['currency'].size + menus_in_dollars['currency'].size + menus_in_other_currencies['currency'].size) == menu_df['currency'].size, "Invalid currency value assumptions"
    assert menu_df['place'].size == menu_df['date'].size == menu_df['currency'].size, "Invalid attribute length assumption"

    target = [menus_in_dollars['currency'].size, menus_from_1900_to_1909['date'].size, menus_from_new_york['place'].size]
    other = [menus_in_other_currencies['currency'].size, menus_from_other_dates['date'].size, menus_from_other_places['place'].size]
    empty = [menus_with_no_currency['currency'].size, menus_with_no_date['date'].size, menus_with_no_place['place'].size]

    sns.set_theme()

    bar_df = pd.DataFrame({'In target range': target, 'Other value': other, 'No value': empty}, index=['currency', 'date', 'place'])
    bar_df.plot(kind='barh', stacked=True, color=['green', 'grey', 'lightgrey'], xlabel="Number of records", title="Applicable Menu Table Attributes")
    plt.savefig("doc/menu-bar-chart.png", bbox_inches='tight')

    #todo: Histogram of menus per decade
    #todo: Venn diagram of menus in NY, from 1900-1909, and in Dollars
        #todo: https://stackoverflow.com/questions/18079563/finding-the-intersection-between-two-series-in-pandas
        #todo: matplotlib_venn (get help from chatGPT)

def explore_dish_table(dish_df: pd.DataFrame) -> None:
    pass #todo: create "is_cup_of_coffee" regex and plot "name" attribute stacked bar chart (coffee, other, no value)

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('dataset_path', help='Path to the directory of the dataset to run on')
    args = parser.parse_args()

    menu_df, dish_df = load_data(args.dataset_path)

    explore_menu_table(menu_df)
    explore_dish_table(dish_df)


if __name__ == "__main__":
    main()
