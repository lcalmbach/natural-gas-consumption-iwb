import streamlit as st
import json
from io import BytesIO
import os
import socket
import string
import csv
import zipfile
import random
import logging


def download_button(data, download_filename, button_text):
    """
    Function to create a download button for a given object.

    Parameters:
    - object_to_download: The object to be downloaded.
    - download_filename: The name of the file to be downloaded.
    - button_text: The text to be displayed on the download button.
    """
    # Create a BytesIO buffer
    json_bytes = json.dumps(data).encode("utf-8")
    buffer = BytesIO(json_bytes)

    # Set the appropriate headers for the browser to recognize the download
    st.set_option("deprecation.showfileUploaderEncoding", False)
    st.download_button(
        label=button_text,
        data=buffer,
        file_name=download_filename,
        mime="application/json",
    )


def is_valid_json(json_str):
    try:
        json.loads(json_str)
        return True
    except ValueError:
        return False


def get_hostname():
    return socket.gethostname().lower()


def get_var(varname: str) -> str:
    """
    Retrieves the value of a given environment variable or secret from the Streamlit configuration.

    If the current host is the local machine (according to the hostname), the environment variable is looked up in the system's environment variables.
    Otherwise, the secret value is fetched from Streamlit's secrets dictionary.

    Args:
        varname (str): The name of the environment variable or secret to retrieve.

    Returns:
        The value of the environment variable or secret, as a string.

    Raises:
        KeyError: If the environment variable or secret is not defined.
    """
    if socket.gethostname().lower() == LOCAL_HOST:
        return os.environ[varname]
    else:
        return st.secrets[varname]


def get_random_word(length=5) -> str:
    """
    Generate a random word of a given length.

    This function generates a random word by choosing `length` number of random letters from ASCII letters.

    Parameters:
    length (int): The length of the random word to generate. Default is 5.

    Returns:
    str: The generated random word.
    """
    # Choose `length` random letters from ascii_letters
    letters = string.ascii_letters
    return "".join(random.choice(letters) for _ in range(length))


def create_file(file_name: str, columns: list) -> None:
    """
    Creates a new file and writes the columns list to the file.

    Parameters:
    file_name (str): The name of the file to be created.
    columns (list): The list of columns to be written to the file.

    Returns:
    None
    """
    with open(file_name, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(columns)
        print(f"File {file_name} created.")


def append_row(file_name: str, row: list) -> None:
    """
    Appends a row to a CSV file.

    Args:
        file_name (str): The name of the CSV file to append to.
        row (list): The row to append to the CSV file.

    Returns:
        None
    """
    with open(file_name, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(row)


def zip_files(file_names: list, target_file: str):
    """
    Compresses a list of files into a zip file. The zip file will be
    downloaded to the user's computer if download button is clicked.

    :return: None
    """

    # Create a new zip file and add files to it
    with zipfile.ZipFile(target_file, "w") as zipf:
        for file in file_names:
            # Add file to the zip file
            # The arcname parameter avoids storing the full path in the zip file
            zipf.write(file, arcname=os.path.basename(file))


def init_logging(name, filename, console_level=logging.DEBUG, file_level=logging.ERROR):
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(min(console_level, file_level))  # Set to the lower of the two levels

    # Create a file handler and set level
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(file_level)

    # Create a console handler and set level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)

    # Create a formatter with a custom time format (excluding milliseconds)
    time_format = "%Y-%m-%d %H:%M:%S"  # Custom time format
    formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt=time_format)

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

LOCAL_HOST = "liestal"
