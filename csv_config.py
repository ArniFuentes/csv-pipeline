from dataclasses import dataclass


@dataclass
class CSVConfig:
    new_properties: dict
    encodings: list
    delimiters: list
    prices: list


csv_config = CSVConfig(
    new_properties={
        "Regular price": "Regular price Store A",
        "Card price": "Card price Store A",
        "SKU": "SKU Store A",
        "URL": "URL Store A",
        "Has stock": "Stock Store A",
    },
    encodings=["Windows-1252", "utf-8", "utf-8-sig", "latin-1", "cp1252"],
    delimiters=[";", "|", ","],
    prices=[("Regular price", "Regular price {}"), ("Card price", "Card price {}")]
)


