import os

import pandas as pd
import tabula as tb
from django.conf import settings

from .models import BalanceSheet


def splitter(row):
    """using function to split 2016 particulars (year particulars) column

    :param column to split
    :return two splitted columns
    """

    if pd.isnull(row):
        return None, None
    try:
        splitted = row.split(' ')
        num = splitted[0]
        rest = ' '.join(splitted[1:])
    except:
        return None, None
    return num, rest


def convert_pdf_to_csv(path):
    """
    Takes as input a pdf file, converts to csv and returns dataframe

    :param path to pdf
    :return: dataframe
    """
    # reading the pdf file into dataframe

    try:
        df = tb.read_pdf(path)

        # getting column names into a list and extracting year from them

        col = df.columns.values.tolist()
        # ['Particulars', '2015', '2016 Particulars', 'Unnamed: 3', 'Unnamed: 4', '2015.1', '2016']

        year1 = col[1]  # 2015
        year2 = col[2][:4]  # 2016
        year1_dup = col[5]  # 2015.1
        year2_dup = col[6] + ".1"  # 2016.1  rename last column
        particulars_dup = col[2][5:] + ".1"  # rename duplicate particulars column
        # applying the function on 2016 Particulars (year2 particulars) column

        # rename 2016 last column
        df[year2_dup] = df[col[6]]

        # split 2016 particulars column
        df[year2], df[particulars_dup] = zip(*df[col[2]].apply(splitter))

        # rename Unnamed column
        df.rename(columns={col[4]: ''}, inplace=True)

        # delete '2016 Particulars', 'Unnamed: 3'
        del df[col[2]], df[col[3]]

        # ordering/ rearrange  as it was in pdf
        df = df[[col[0], year1, year2, particulars_dup, '', year1_dup, year2_dup]]

        # replacing nan values with spaces
        df.fillna('', inplace=True)

    except:
        return None, None

    if not df.shape[0]:
        return None, None

    try:
        # converting dataframe to csv file
        csv_file_name = year1 + "-" + year2
        csv_file_path = os.path.join(settings.MEDIA_ROOT, csv_file_name)
        df.to_csv(csv_file_path, index=False)
    except:
        return df, None

    return df, csv_file_name


def save_dataframe_to_db(df):
    variable, variable2 = df.columns[0], df.columns[3]
    year1, year1_dup = df.columns[1], df.columns[5]
    year2, year2_dup = df.columns[2], df.columns[6]

    for index, row in df.iterrows():
        if row[variable] is None or row[variable].strip() == "":
            continue

        BalanceSheet.objects.update_or_create(variable=row[variable],
                                              year=int(year1), value=row[year1])
        BalanceSheet.objects.update_or_create(variable=row[variable],
                                              year=int(year2), value=row[year2])

    for index, row in df.iterrows():
        if row[variable2] is None or row[variable2].strip() == "":
            continue
        BalanceSheet.objects.update_or_create(variable=row[variable2],
                                              year=int(year1),
                                              value=row[year1_dup])
        BalanceSheet.objects.update_or_create(variable=row[variable2],
                                              year=int(year2),
                                              value=row[year2_dup])
