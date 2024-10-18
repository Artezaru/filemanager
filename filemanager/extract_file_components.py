from typing import Tuple
import os

def extract_file_components(filepath: str) -> Tuple[str]:
    """
    extract_file_components extracts from a filepath the 3 components:
        - path
        - name
        - extension
    
    Parameters
    ----------
    filepath : str
        The filepath of a file.

    Returns
    -------
    path : str
        The path of the filepath.
    name : str 
        The name of the filepath.
    extension : str 
        The extension of the filepath.

    Raises
    ------
    TypeError : If the given argument is not str.

    Examples
    --------
    Basic usage of `extract_file_components`:

    >>> extract_file_components("C:\\my\\super\\path\\name.txt")
    ('C:\\my\\super\\path', 'name', '.txt')

    >>> extract_file_components("name.txt")
    ('', 'name', '.txt')

    >>> extract_file_components("C:\\my\\super\\path\\name")
    ('C:\\my\\super\\path', 'name', '')
    """
    if not isinstance(filepath, str):
        raise TypeError('Parameter filepath is not string.')
    path, filename_with_ext = os.path.split(filepath)
    filename, extension = os.path.splitext(filename_with_ext)
    return path, filename, extension


def main():
    print("See test_extract_file_components.py")
    
if __name__ == '__main__':
    main()