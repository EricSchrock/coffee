from argparse import ArgumentParser
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from regex import is_new_york, is_1900_to_1909, is_dollars


def load_data(dataset_path: str) -> pd.DataFrame:
    menu_df = pd.read_csv(f"{dataset_path}/Menu.csv")
    return menu_df

def explore_menu_table(menu_df: pd.DataFrame) -> None:
    place_ny    =  menu_df['place'].str.contains(is_new_york, na=False)
    place_other = ~menu_df['place'].str.contains(is_new_york, na=False) & menu_df['place'].notnull()
    place_null  =  menu_df['place'].isna()

    date_1900s =  menu_df['date'].str.contains(is_1900_to_1909, na=False)
    date_other = ~menu_df['date'].str.contains(is_1900_to_1909, na=False) & menu_df['date'].notnull()
    date_null  =  menu_df['date'].isna()

    currency_dollars =  menu_df['currency'].str.contains(is_dollars, na=False)
    currency_other   = ~menu_df['currency'].str.contains(is_dollars, na=False) & menu_df['currency'].notnull()
    currency_null    =  menu_df['currency'].isna()

    assert (menu_df[place_ny]['place'].size + menu_df[place_other]['place'].size + menu_df[place_null]['place'].size) == menu_df['place'].size, "Invalid place value assumptions"
    assert (menu_df[date_1900s]['date'].size + menu_df[date_other]['date'].size + menu_df[date_null]['date'].size) == menu_df['date'].size, "Invalid date value assumptions"
    assert (menu_df[currency_dollars]['currency'].size + menu_df[currency_other]['currency'].size + menu_df[currency_null]['currency'].size) == menu_df['currency'].size, "Invalid currency value assumptions"
    assert menu_df['place'].size == menu_df['date'].size == menu_df['currency'].size, "Invalid attribute length assumption"

    bar_df = pd.DataFrame({
            'Target value': [menu_df[currency_dollars]['currency'].size, menu_df[date_1900s]['date'].size, menu_df[place_ny]   ['place'].size],
            'Other value':  [menu_df[currency_other]  ['currency'].size, menu_df[date_other]['date'].size, menu_df[place_other]['place'].size],
            'No value':     [menu_df[currency_null]   ['currency'].size, menu_df[date_null] ['date'].size, menu_df[place_null] ['place'].size]
        },
        index=['currency', 'date', 'place']
    )

    sns.set_theme()
    bar_df.plot(kind='barh', stacked=True, color=['green', 'grey', 'lightgrey'], xlabel="Number of Records", title="Applicable Menu Table Attributes")
    plt.savefig("doc/menu-bar-chart.png", bbox_inches='tight')
    plt.clf()

    menu_df['year'] = pd.to_datetime(menu_df.date, errors='coerce').dt.year
    menu_df['decade'] = menu_df.year - (menu_df.year % 10)

    assert menu_df[menu_df['decade'] == 1900.0]['decade'].size == menu_df[date_1900s]['date'].size, "Invalid date range assumption"

    menu_df['decade'].plot(kind='hist', x='date', xlabel="Decade", ylabel="Count", title="Number of Menus By Decade", bins=range(1850, 2011, 10))
    plt.savefig("doc/menu-date-histogram.png", bbox_inches='tight')
    plt.clf()

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('dataset_path', help='Path to the directory of the dataset to run on')
    args = parser.parse_args()

    menu_df = load_data(args.dataset_path)

    explore_menu_table(menu_df)


if __name__ == "__main__":
    main()
