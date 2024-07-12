from argparse import ArgumentParser
import functools
import matplotlib.pyplot as plt
from matplotlib_venn import venn3_unweighted
import pandas as pd
import re
import seaborn as sns
from time import time
from typing import Callable, List, Tuple

from regex import is_new_york, is_1900_to_1909, is_dollars


def repair_menu_date_from_call_number(menu_df, page_df, item_df, dish_df) -> None:
    regex = re.compile(r"^[0-9][0-9][0-9][0-9]-.*")
    menu_df.loc[menu_df['date'].isna() & menu_df['call_number'].str.contains(regex, na=False), 'date'] = menu_df['call_number'].str[:4]

def repair_menu_date_outside_expected_range(menu_df, page_df, item_df, dish_df) -> None:
    menu_df['date'] = menu_df['date'].str.replace(r"^0190", "1900", regex=True) # Typos observed in manual data exploration
    menu_df['date'] = menu_df['date'].str.replace(r"^1091", "1901", regex=True)
    menu_df['date'] = menu_df['date'].str.replace(r"^2928", "1928", regex=True)

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
def profile_data(menu_df: pd.DataFrame) -> List[int]:
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
def clean_data(menu_df: pd.DataFrame, page_df: pd.DataFrame, item_df: pd.DataFrame, dish_df: pd.DataFrame) -> None:
    cleaning_routines = [
        repair_menu_date_from_call_number,
        repair_menu_date_outside_expected_range,
    ]

    for cleaning_routine in cleaning_routines:
        cleaning_routine(menu_df, page_df, item_df, dish_df)

@timer
def save_profile(dirty: List[int], clean: List[int]) -> None:
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
    plt.clf()

@timer
def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('dataset_path', help='Path to the directory of the dataset to run on')
    args = parser.parse_args()

    menu_df, page_df, item_df, dish_df = load_data(args.dataset_path)

    profile_dirty = profile_data(menu_df)

    clean_data(menu_df, page_df, item_df, dish_df)

    profile_clean = profile_data(menu_df)

    save_profile(profile_dirty, profile_clean)


if __name__ == "__main__":
    main()
