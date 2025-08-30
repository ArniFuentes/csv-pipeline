from tkinter import Tk
from tkinter.filedialog import askdirectory
import os
import pandas as pd
import auxiliary_functions as a_f


def select_folder() -> str:
    root = Tk()
    root.withdraw()
    excel_file_path = askdirectory(title='Select a folder with the data')
    return excel_file_path


def get_file_names(folder) -> list[str]:
    file_list = os.listdir(folder)
    test = [file for file in file_list if file.endswith(".csv")]
    return test


def export_csv_files(folder, transformed_files, files_name):
    for file_name, df in zip(files_name, transformed_files):
        output_file_name = f'{os.path.splitext(file_name)[0]}-transformed.csv'
        df.to_csv(os.path.join(folder, output_file_name), index=False)


def process_files(folder: str, files: list[str], csv_config) -> list[pd.DataFrame]:
    transformed_files = []

    for file in files:
        df = a_f.read_file(folder, file, csv_config.encodings,
                           csv_config.delimiters)

        print(f"Processing file: {file}")

        df = df.drop_duplicates()

        target_date = a_f.create_target_date(file)

        df = a_f.filter_by_date(df, target_date)

        df = df.rename(columns=csv_config.new_properties)

        stores = a_f.create_stores(df)

        df_list = a_f.create_dfs_list(stores, df, csv_config.prices)

        df = pd.concat(df_list, ignore_index=True)

        df = df[(df['SKU'] != 0) & (df['Stock'] == 'in_stock')]

        df = df.drop_duplicates()

        transformed_files.append(df)
    return transformed_files
