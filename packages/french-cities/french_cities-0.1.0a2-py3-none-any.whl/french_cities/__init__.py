# -*- coding: utf-8 -*-

from dotenv import load_dotenv

from french_cities.city_finder import find_city
from french_cities.departement_finder import find_departements
from french_cities.vintage import set_vintage

load_dotenv()

__version__ = "0.1.0a1"


__all__ = [
    "find_city",
    "find_departements",
    "set_vintage",
]


if __name__ == "__main__":
    import pandas as pd

    url = r"C:\Winpython\WinPython-64bit-3.9.2.0\notebooks\test-french-cities\test_french_cities\sample_pnttd.xlsx"
    df = pd.read_excel(url)
    df = df.rename(
        {
            "département du dossier": "dep",
            "commune de l'installation de traitement": "city",
        },
        axis=1,
    )
    df["dep"] = df["dep"].map(
        {
            "Nord": "59",
            "Aisne": "02",
            "Pas-de-Calais": "62",
            "Somme": "80",
            "Oise": "60",
        }
    )
    df2 = find_city(df)
    df2.to_excel("test_sample.xlsx")
