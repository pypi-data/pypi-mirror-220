import os
import pandas as pd


def check_missing_exif(df, column):
    """
    Filter data frame for null values in column.

    Args:
        df (DataFrame): Data frame of EXIF data
        column (str): Name of column to filter for null values

    Returns:
        DataFrame
    """
    df = df[df[column].isnull()]
    return df


def count_images_by_columns(df, columns, sort=None):
    """
    Group images by column(s) and count images

    Args:
        df (DataFrame): Data frame of EXIF data
        columns (list): List of columns to group by
        sort (list): Optional list of columns for sorting returned data frame

    Returns:
        DataFrame
    """

    # group and count
    df = df.groupby(columns).size().reset_index()
    df = df.rename(columns={0: 'count'})

    # (optional) sort
    if sort is not None:
        df = df.sort_values(by=sort).reset_index(drop=True)

    return df


def get_column(df, column):
    """
    Extract column from data frame as list

    Args:
        df (DataFrame): Data frame of EXIF data
        column (str): Name of column to extract

    Returns:
        List
    """
    return df[column].to_list()


def filename2columns(df, filename_col, columns):
    """
    Split the filename column into individual columns.

    Args:
        df (DataFrame): Data frame of EXIF data
        filename_col (str): Name of column in data frame that contains the filenames of images
        columns (list): The filename_col will be split into individual columns using the OS file separator. List the
        names you would like to assign to each column from right to left in the filename. You do not need to assign a
        name to every column. Columns that aren't given names won't be added to the output data frame. For example,
        if the first filename in the filenames_col is
        '~/Documents/Samsung_phones/s20/s20_2/natural/wide/20230417_183817.jpg' and columns=['image', 'camera',
        'scene_type', 'phone', 'model'], an image column will be created with the first entry '20230417_183817.jpg',
        the first entry of the camera column will be 'wide', the first entry of the scene_type column will be
        'natural', the first entry of the phone column will be 's20_2', and the first entry of the model column will
        be 's20'. No columns will be created for 'Documents' or 'Samsung_phones'.

    Returns:
        DataFrame
    """

    for i in range(1, len(columns)+1):
        column = columns.pop()
        df.insert(0, column, df[filename_col].str.split(os.path.sep).str[-i])

    return df


def find_images(df, filter_dict, return_columns=None):
    """
    Use Pandas to filter the EXIF data frame for column(s) and column value(s) specified in filter_dict.

    Args:
        df (DataFrame): Data frame of EXIF data
        filter_dict (dict): Dictionary of column and column value pair(s). Example filter_dict={'phone':
        's21_1', 'Aperture': 2.2}
        return_columns (list): Optional list of columns to return if you don't want the entire data frame

    Returns:
        DataFrame
    """
    for k, v in filter_dict.items():
        df = df.query("`{0}` == @v".format(k)).reset_index(drop=True)

    if return_columns is not None:
        df = df[return_columns]

    return df


def read_exif(path, filename_col, encoding='utf-8'):
    """
    Load EXIF data from a csv file as a Pandas data frame and drop any images whose name starts with '.'

    Args:
        path (str): Absolute or relative file path and file name of the csv file containing EXIF data extracted using
        Phil Harvey's EXIFTool
        filename_col (str): The name of the column in the EXIF data that contains the images' filenames
        encoding (str): The encoding for Pandas to use when loading the csv file of EXIF data

    Returns:
        DataFrame
    """
    df = pd.read_csv(path, encoding=encoding)

    # drop file names that start with '.'
    files = get_column(df=df, column=filename_col)
    images = pd.Series([s.split('/')[-1].strip() for s in files])
    df = df[~images.str.startswith('.')]

    return df
