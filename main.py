from utilities import (select_folder, get_file_names,
                       process_files, export_csv_files)


def main():
    folder = select_folder()

    files_name = get_file_names(folder)

    processed_csv_files = process_files(folder, files_name)
    print("process_files terminado")

    export_csv_files(folder, processed_csv_files, files_name)


if __name__ == "__main__":
    main()
