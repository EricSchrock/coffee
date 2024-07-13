import re
import sqlite3
from argparse import ArgumentParser
from typing import List, Tuple

import pandas as pd

from main import clean_data, load_data, timer
from regex import IS_CUP_OF_COFFEE, IS_NEW_YORK


@timer
def query_data(menu_df: pd.DataFrame, page_df: pd.DataFrame, item_df: pd.DataFrame, dish_df: pd.DataFrame) -> List[Tuple[float, float]]:
    menu_df['year'] = pd.to_datetime(menu_df.date, errors='coerce').dt.year

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
        SELECT menu.year, item.price FROM item
        INNER JOIN dish ON item.dish_id = dish.id
        INNER JOIN page ON item.menu_page_id = page.id
        INNER JOIN menu ON page.menu_id = menu.id
        WHERE dish.name IS NOT NULL AND dish.name REGEXP ?
        AND menu.place IS NOT NULL AND menu.place REGEXP ?
        AND menu.currency = "Dollars"
        AND item.price IS NOT NULL AND item.price < 1;
        """, [IS_CUP_OF_COFFEE, IS_NEW_YORK]).fetchall()

    con.close()

    return results

@timer
def save_query_results(dirty: List[Tuple[float, float]], clean: List[Tuple[float, float]]) -> None:
    pass #todo: plot median price by year (add to README results section?)

@timer
def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('dataset_path', help='Path to the directory of the dataset to run on')
    args = parser.parse_args()

    menu_df, page_df, item_df, dish_df = load_data(args.dataset_path)

    results_dirty = query_data(menu_df, page_df, item_df, dish_df)

    clean_data(menu_df, page_df, item_df, dish_df)

    results_clean = query_data(menu_df, page_df, item_df, dish_df)

    save_query_results(results_dirty, results_clean)


if __name__ == "__main__":
    main()
