import pandas as pd
import os
from itertools import product


def filter_by_date(df, target_date) -> pd.DataFrame:
    df['Update date and time Store A'] = pd.to_datetime(
        df['Update date and time Store A'])
    df['Update date and time Store A'] = df['Update date and time Store A'].dt.date
    return df[df['Update date and time Store A'] == target_date]


def create_stores(df) -> list[str]:
    df_columns = list(df.columns)
    stores = [string[4:] for string in df_columns if 'SKU' in string]
    return stores


def read_file(folder, file, encodings, delimiters) -> pd.DataFrame:
    filepath = os.path.join(folder, file)

    for enc, deli in product(encodings, delimiters):
        try:
            df = pd.read_csv(filepath, delimiter=deli, encoding=enc)
            return df
        except:
            print(f"Failed with encoding={enc}, delimiter={deli}")

    raise ValueError(
        "The file could not be read with the defined encodings/delimiters.")


def create_target_date(file):
    date = file[-12:-4]
    year = date[:4]
    month = date[-4:-2]
    day = date[-2:]
    target_date = pd.to_datetime(f'{year}-{month}-{day}').date()
    return target_date


def create_dfs_list(stores, df, prices) -> list[pd.DataFrame]:
    df_list = []

    for store in stores:
        for price_type, col_pattern in prices:
            col = col_pattern.format(store)
            tienda_df = pd.DataFrame({
                'SKU': df[f'SKU {store}'],
                'Category': df['Category'],
                'Brand': df['Brand'],
                'Name': df['Name'],
                'Price': df[col],
                'Price type': price_type,
                'Stock': df[f'Stock {store}'],
                'Store': store,
                'Date': df['Update date and time Store A']
            })

            df_list.append(tienda_df)
    return df_list
