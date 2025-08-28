import pandas as pd
import os


def filter_by_date(df, target_date) -> pd.DataFrame:
    df['Update date and time Store A'] = pd.to_datetime(
        df['Update date and time Store A'])
    df['Update date and time Store A'] = df['Update date and time Store A'].dt.date
    return df[df['Update date and time Store A'] == target_date]


def rename_properties(df) -> pd.DataFrame:
    new_properties = {
        "Regular price": "Regular price Store A",
        "Card price": "Card price Store A",
        "SKU": "SKU Store A",
        "URL": "URL Store A",
        "Has stock": "Stock Store A",
    }

    # rename properties
    return df.rename(columns=new_properties)


def create_stores(df) -> list[str]:
    df_columns = list(df.columns)
    stores = [string[4:] for string in df_columns if 'SKU' in string]
    return stores


def read_file(folder, file) -> pd.DataFrame:
    encodings = ["Windows-1252", "utf-8", "utf-8-sig", "latin-1", "cp1252"]
    delimiters = [";", "|", ","]
    for enc in encodings:
        try:
            for deli in delimiters:
                try:
                    df = pd.read_csv(os.path.join(folder, file),
                                     delimiter=deli, encoding=enc)
                except:
                    print(f'Try another delimiter')

            if isinstance(df, pd.DataFrame):
                break
        except:
            print(f"Try another encoding")
    return df


def create_target_date(file):
    date = file[-12:-4]
    year = date[:4]
    month = date[-4:-2]
    day = date[-2:]
    target_date = pd.to_datetime(f'{year}-{month}-{day}').date()
    return target_date


def create_dfs_list(stores, df) -> list[pd.DataFrame]:
    prices = [("Regular price", "Regular price {}"),
              ("Card price", "Card price {}")]
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
