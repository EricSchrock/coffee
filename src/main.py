from argparse import ArgumentParser
import functools
import matplotlib.pyplot as plt
from matplotlib_venn import venn3_unweighted
import pandas as pd
import re
import seaborn as sns
import sqlite3
from statistics import mean, median
from time import time
from typing import Callable, List, Tuple

from regex import is_new_york, is_1900_to_1909, is_dollars, is_cup_of_coffee


def remove_leading_and_trailing_whitespace(menu_df: pd.DataFrame, page_df: pd.DataFrame, item_df: pd.DataFrame, dish_df: pd.DataFrame) -> None:
    menu_df['date'] = menu_df['date'].apply(lambda x: x.strip() if type(x) == str else x)
    menu_df['call_number'] = menu_df['call_number'].apply(lambda x: x.strip() if type(x) == str else x)
    menu_df['place'] = menu_df['place'].apply(lambda x: x.strip() if type(x) == str else x)
    menu_df['currency'] = menu_df['currency'].apply(lambda x: x.strip() if type(x) == str else x)
    item_df['price'] = item_df['price'].apply(lambda x: x.strip() if type(x) == str else x)
    dish_df['name'] = dish_df['name'].apply(lambda x: x.strip() if type(x) == str else x)

def repair_menu_date_from_call_number(menu_df: pd.DataFrame, page_df: pd.DataFrame, item_df: pd.DataFrame, dish_df: pd.DataFrame) -> None:
    regex = r"^[0-9][0-9][0-9][0-9]-.*"
    menu_df.loc[menu_df['date'].isna() & menu_df['call_number'].str.contains(regex, na=False), 'date'] = menu_df['call_number'].str[:4]

def repair_menu_date_outside_expected_range(menu_df: pd.DataFrame, page_df: pd.DataFrame, item_df: pd.DataFrame, dish_df: pd.DataFrame) -> None:
    menu_df['date'] = menu_df['date'].str.replace(r"^0190", "1900", regex=True) # Typos observed in manual data exploration
    menu_df['date'] = menu_df['date'].str.replace(r"^1091", "1901", regex=True)
    menu_df['date'] = menu_df['date'].str.replace(r"^2928", "1928", regex=True)

def repair_menu_place_new_york_spelling(menu_df: pd.DataFrame, page_df: pd.DataFrame, item_df: pd.DataFrame, dish_df: pd.DataFrame) -> None:
    regex = r"(?i)enw york|nwe york|ne wyork|newy ork|new yrok|new yokr|\bew york|nw york|ne york|newyork|new ork|new yrk|new yok|new yor\b|[^n]ew york|n[^e]w york|ne[^w] york|new[^ ]york|new [^y]ork|new y[^o]rk|new yo[^r]k|new yor[^k]"
    menu_df['place'] = menu_df['place'].str.replace(regex, 'NEW YORK', regex=True)

def repair_menu_currency_dollars_spelling(menu_df: pd.DataFrame, page_df: pd.DataFrame, item_df: pd.DataFrame, dish_df: pd.DataFrame) -> None:
    regex = r"(?i)^(?:odllars|dlolars|dolalrs|dollras|dollasr|ollars|dllars|dolars|dollrs|dollas|dollar|[^d]ollars|d[^o]llars|do[^l]lars|dol[^l]ars|doll[^a]rs|dolla[^r]s|dollar[^s])$"
    menu_df['currency'] = menu_df['currency'].str.replace(regex, 'Dollars', regex=True)

def repair_menu_currency_convert_cents_to_dollars(menu_df: pd.DataFrame, page_df: pd.DataFrame, item_df: pd.DataFrame, dish_df: pd.DataFrame) -> None:
    menu_ids = menu_df.loc[menu_df['currency'] == 'Cents', 'id']
    menu_df.loc[menu_df['currency'] == 'Cents', 'currency'] = "Dollars"
    page_ids = page_df.loc[page_df['menu_id'].isin(menu_ids), 'id']
    item_df.loc[item_df['menu_page_id'].isin(page_ids) & item_df['price'].notnull(), 'price'] /= 100

def repair_dish_name_coffee_spelling(menu_df: pd.DataFrame, page_df: pd.DataFrame, item_df: pd.DataFrame, dish_df: pd.DataFrame) -> None:
    regex = r"(?i)\b(?:ocffee|cfofee|cofefe|offee|cffee|cofee|coffe|[^ct]offee|c[^o]ffee|co[^f]fee|cof[^f]ee|coff[^e]e|coffe[^e])\b"
    dish_df['name'] = dish_df['name'].str.replace(regex, 'Coffee', regex=True)

def timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        value = func(*args, **kwargs)
        runtime = time() - start
        print(f"Finished {func.__name__:20} in {(runtime):7.3f} secs")
        return value
    return wrapper

@timer
def load_data(dataset_path: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    menu_df = pd.read_csv(f"{dataset_path}/Menu.csv")
    page_df = pd.read_csv(f"{dataset_path}/MenuPage.csv")
    item_df = pd.read_csv(f"{dataset_path}/MenuItem.csv")
    dish_df = pd.read_csv(f"{dataset_path}/Dish.csv")
    return menu_df, page_df, item_df, dish_df

@timer
def profile_menu_data(menu_df: pd.DataFrame) -> List[int]:
    place_ny         =  menu_df['place']   .str.contains(is_new_york,     na=False)
    date_1900s       =  menu_df['date']    .str.contains(is_1900_to_1909, na=False)
    currency_dollars =  menu_df['currency'].str.contains(is_dollars,      na=False)

    return [
        menu_df[ place_ny & ~date_1900s & ~currency_dollars]['id'].size,
        menu_df[~place_ny &  date_1900s & ~currency_dollars]['id'].size,
        menu_df[ place_ny &  date_1900s & ~currency_dollars]['id'].size,
        menu_df[~place_ny & ~date_1900s &  currency_dollars]['id'].size,
        menu_df[ place_ny & ~date_1900s &  currency_dollars]['id'].size,
        menu_df[~place_ny &  date_1900s &  currency_dollars]['id'].size,
        menu_df[ place_ny &  date_1900s &  currency_dollars]['id'].size
    ]

@timer
def profile_dish_data(dish_df: pd.DataFrame) -> int:
    return dish_df[dish_df['name'].str.contains(is_cup_of_coffee, na=False)].size

@timer
def query_data(menu_df: pd.DataFrame, page_df: pd.DataFrame, item_df: pd.DataFrame, dish_df: pd.DataFrame) -> List[float]:
    def regexp(expr, item):
        regex = re.compile(expr, re.IGNORECASE)
        return bool(regex.search(item))

    con = sqlite3.connect(":memory:")
    con.create_function("REGEXP", 2, regexp)
    cur = con.cursor()

    menu_df.to_sql("Menu", con, if_exists='replace', index=False, method='multi', chunksize=10_000)
    page_df.to_sql("Page", con, if_exists='replace', index=False, method='multi', chunksize=10_000)
    item_df.to_sql("Item", con, if_exists='replace', index=False, method='multi', chunksize=10_000)
    dish_df.to_sql("Dish", con, if_exists='replace', index=False, method='multi', chunksize=10_000)

    results = cur.execute("""
        SELECT price FROM item
        WHERE menu_page_id IN (
            SELECT id FROM page
            WHERE menu_id IN (
                SELECT id FROM menu
                WHERE menu.place IS NOT NULL AND menu.place REGEXP ?
                AND date BETWEEN 1900 AND 1909
                AND currency = "Dollars"))
        AND dish_id IN (SELECT id FROM dish WHERE dish.name IS NOT NULL AND dish.name REGEXP ?)
        AND price IS NOT NULL
        AND price < 1;
        """, [is_new_york, is_cup_of_coffee]).fetchall()

    con.close()

    prices = [ result[0] for result in results ]

    return prices

@timer
def clean_data(menu_df: pd.DataFrame, page_df: pd.DataFrame, item_df: pd.DataFrame, dish_df: pd.DataFrame) -> None:
    cleaning_routines = [
        remove_leading_and_trailing_whitespace,
        repair_menu_date_from_call_number,
        repair_menu_date_outside_expected_range,
        repair_menu_place_new_york_spelling,
        repair_menu_currency_dollars_spelling,
        repair_menu_currency_convert_cents_to_dollars,
        repair_dish_name_coffee_spelling,
    ]

    for cleaning_routine in cleaning_routines:
        cleaning_routine(menu_df, page_df, item_df, dish_df)

@timer
def save_menu_profile(dirty: List[int], clean: List[int]) -> None:
    labels = ["New York", "1900 - 1909", "Dollars"]
    colors = ['teal', 'purple', 'blue']
    sns.set_theme()
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    venn3_unweighted(subsets=dirty, set_labels=labels, set_colors=colors)
    plt.title("Menus With Target Values (dirty data)")
    plt.subplot(1, 2, 2)
    venn3_unweighted(subsets=clean, set_labels=labels, set_colors=colors)
    plt.title("Menus With Target Values (clean data)")
    plt.tight_layout()
    plt.savefig("doc/menu-venn-diagram.png", bbox_inches='tight')
    plt.close()

@timer
def save_dish_profile(dirty: int, clean: int) -> None:
    sns.set_theme()
    plt.bar(x=['Dirty Data', 'Clean Data'], height=[dirty, clean], alpha=0.75)
    plt.title('Dishes Matching the "is_cup_of_coffee" Regex')
    plt.savefig("doc/dish-name-coffee-bar-chart.png", bbox_inches='tight')
    plt.close()

@timer
def save_query_result(dirty: List[float], clean: List[float]) -> None:
    sns.set_theme()
    plt.hist([dirty, clean], color=['r','b'], alpha=0.75)
    plt.title("Price of a Cup of Coffee in New York State (1900 - 1909)")
    plt.xlabel("Price ($)")
    plt.ylabel("Menu Appearances (count)")
    plt.legend(loc="upper right", labels=['Dirty', 'Clean'])
    plt.axvline(mean(dirty),   color='r', linestyle='dashed', linewidth=1, alpha=0.75)
    plt.axvline(median(dirty), color='r', linestyle='dashed', linewidth=1, alpha=0.75)
    plt.axvline(mean(clean),   color='b', linestyle='dashed', linewidth=1, alpha=0.75)
    plt.axvline(median(clean), color='b', linestyle='dashed', linewidth=1, alpha=0.75)
    x = max([mean(dirty), median(dirty), mean(clean), median(clean)]) * 1.5
    _, y = plt.ylim()
    font = plt.rcParams['font.family']
    plt.rcParams['font.family'] = 'monospace'
    plt.text(x, y * 0.90, f"Count:  {len(dirty):4}",      color='r', alpha=0.75)
    plt.text(x, y * 0.85, f"Max:    {max(dirty):.2f}",    color='r', alpha=0.75)
    plt.text(x, y * 0.80, f"Mean:   {mean(dirty):.2f}",   color='r', alpha=0.75)
    plt.text(x, y * 0.75, f"Median: {median(dirty):.2f}", color='r', alpha=0.75)
    plt.text(x, y * 0.65, f"Count:  {len(clean):4}",      color='b', alpha=0.75)
    plt.text(x, y * 0.60, f"Max:    {max(clean):.2f}",    color='b', alpha=0.75)
    plt.text(x, y * 0.55, f"Mean:   {mean(clean):.2f}",   color='b', alpha=0.75)
    plt.text(x, y * 0.50, f"Median: {median(clean):.2f}", color='b', alpha=0.75)
    plt.rcParams['font.family'] = font
    plt.savefig(f"doc/coffee-price-histogram.png", bbox_inches='tight')
    plt.close()

@timer
def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('dataset_path', help='Path to the directory of the dataset to run on')
    args = parser.parse_args()

    menu_df, page_df, item_df, dish_df = load_data(args.dataset_path)

    menu_profile_dirty = profile_menu_data(menu_df)
    dish_profile_dirty = profile_dish_data(dish_df)
    prices_dirty = query_data(menu_df, page_df, item_df, dish_df)

    clean_data(menu_df, page_df, item_df, dish_df)

    menu_profile_clean = profile_menu_data(menu_df)
    dish_profile_clean = profile_dish_data(dish_df)
    prices_clean = query_data(menu_df, page_df, item_df, dish_df)

    save_menu_profile(menu_profile_dirty, menu_profile_clean)
    save_dish_profile(dish_profile_dirty, dish_profile_clean)
    save_query_result(prices_dirty, prices_clean)


if __name__ == "__main__":
    main()
