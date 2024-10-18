from typing import Tuple, List, Optional, Union, Sequence, Callable
import os
import re
from .extract_file_components import extract_file_components

def search_files(*,
                 include_directory: Optional[Union[str, Sequence[str]]] = None,
                 include_pattern: Optional[Union[str, Sequence[str]]] = None,
                 include_start: Optional[Union[str, Sequence[str]]] = None,
                 include_content: Optional[Union[str, Sequence[str]]] = None,
                 include_end: Optional[Union[str, Sequence[str]]] = None,
                 include_extension: Optional[Union[str, Sequence[str]]] = None,
                 include_filter: Optional[Callable[[str], bool]] = None,
                 exclude_subdirectory: Optional[Union[str, Sequence[str]]] = None,
                 exclude_pattern: Optional[Union[str, Sequence[str]]] = None,
                 exclude_start: Optional[Union[str, Sequence[str]]] = None,
                 exclude_content: Optional[Union[str, Sequence[str]]] = None,
                 exclude_end: Optional[Union[str, Sequence[str]]] = None,
                 exclude_extension: Optional[Union[str, Sequence[str]]] = None,
                 exclude_filter: Optional[Callable[[str], bool]] = None,
                 ) -> List[str]:
    """
    search_files allows you to search for files by applying different filters
    based on file location, file name, and extension. The function returns 
    a list containing the absolute path of files that match the filters.

    .. note::
        Type Optional[Union[str, Sequence[str]]] means that input data must be 
        ``None``, ``str``, ``Tuple[str]``, or ``List[str]``.

    .. note::
        The function works by exclusion priority. This means that a file will only
        be returned by the function if it checks all the ``include`` filters. 
        However, if a file which checks all the ``include`` filters 
        checks at least one of the ``exclude`` filters, then it will not be returned.

    Parameters
    ----------
    include_directory : Optional[Union[str, Sequence[str]]]
        The absolute path(s) of the parent directory(ies) in which to search for files. 
        If several directories are provided, the function will search in all of them.
        Including a directory and one of its sub-directories is not useful and takes longer 
        to compute, as the function will search twice in this sub-directory. 
        
        Default: None, means that the search directory will be the current folder using `os.getcwd()`.

    include_pattern : Optional[Union[str, Sequence[str]]]
        Only files whose name (without path or extension) conforms to at least one of the patterns 
        given as input will be returned by the function. A pattern is a character string describing a 
        regular expression (see https://docs.python.org/3/library/re.html). 
        
        The `re.match(pattern, filename)` method will be applied to the name (without path or extension) of the files. 
        
        Default: None, means that no pattern filter will be applied.

    include_start : Optional[Union[str, Sequence[str]]]
        Only files whose name (without path or extension) begins with at least one of the input strings 
        will be returned by the function. 

        Default: None, means that no filter on the beginning of the file name will be applied.

    include_content : Optional[Union[str, Sequence[str]]]
        Only files whose name (without path or extension) contains at least one of the input strings 
        will be returned by the function. 

        Default: None, means that no filter on the content of the file name will be applied.

    include_end : Optional[Union[str, Sequence[str]]]
        Only files whose name (without path or extension) ends with at least one of the input strings 
        will be returned by the function. 

        Default: None, means that no filter on the ending of the file name will be applied.

    include_extension : Optional[Union[str, Sequence[str]]]
        Only files whose extension is in the input strings will be returned by the function. Note that
        the given extensions must contain the dot, for example `“.txt”`.

        Default: None, means that no filter on the extension of the file will be applied.

    include_filter : Optional[Callable[[str], bool]]
        Adds a custom filter to apply on the filepath (path/name.extension) of a file and returns 
        a boolean. Only files that check the filter (True) will be returned by the function.  

        Default: None, means that no external filter on the filepath of the file will be applied.

        Warning: The type of include_filter and any errors introduced are not handled by the function.

    exclude_subdirectory : Optional[Union[str, Sequence[str]]]
        Files contained in one of the supplied sub-folders will not be returned by the function.

        Default: None, means that no sub-folders in `include_directory`` will be excluded from the search.

    exclude_pattern : Optional[Union[str, Sequence[str]]]
        Files matched with at least one of given patterns will not be returned by the function. 

        Default: None, means that no exclusion pattern filter will be applied.

    exclude_start : Optional[Union[str, Sequence[str]]]
        Files started with at least one of given strings will not be returned by the function. 

        Default: None, means that no exclusion filter on the beginning of the file name will be applied.

    exclude_content : Optional[Union[str, Sequence[str]]]
        Files contained at least one of given strings will not be returned by the function. 

        Default: None, means that no exclusion filter on the content of the file name will be applied.

    exclude_end : Optional[Union[str, Sequence[str]]]
        Files ended with at least one of given strings will not be returned by the function. 

        Default: None, means that no exclusion filter on the ending of the file name will be applied.

    exclude_extension : Optional[Union[str, Sequence[str]]]
        Files with at least one of given extensions will not be returned by the function. 

        Default: None, means that no exclusion filter on the extension of the file will be applied.

    exclude_filter : Optional[Callable[[str], bool]]
        Adds a custom filter to apply on the filepath (path/name.extension) of a file and returns 
        a boolean. Files that check the filter (True) will not be returned by the function. 

        Default: None, means that no external exclusion filter on the filepath of the file will be applied.

        Warning: The type of include_filter and any errors introduced are not handled by the function. 

    Returns
    -------
    list_filepath : List[str]
        The list containing the filepaths found checking all the filters.

    Raises
    ------
    TypeError : If a given argument is not Optional[Union[str, Sequence[str]]].

    FileNotFoundError : If a given 'include_directory' can't be found.

    Examples
    --------
    Basic usage of `search_files`:

        .. code-block:: python

            from FileManager import search_files

            # Searching python and text files in the 'C:\\path\\to\\start' directory (but not in the 'nohere' sub-directory whose file name begins with 'mydata'.
            list_filepaths = search_files(
                include_directory='C:\\path\\to\\start', 
                include_start='mydata',
                include_extension=['.py', '.txt'],
                exclude_subdirectory=['nohere']
            )
            
            if len(list_filepaths) == 0:
                print("No file checks the filters")
            else:
                for filepath in list_filepath:
                    print(filepath)
    """
    def check_type_union(obj: Optional[Union[str, Sequence[str]]]) -> bool:
        """ is instance(obj, Optional[Union[str, Sequence[str]]]) """
        if obj is None:
            return True
        if isinstance(obj, str):
            return True
        if isinstance(obj, Sequence):
            return all(isinstance(element, str) for element in obj)
        return False
    
    def data_to_list(obj: Optional[Union[str, Sequence[str]]]) -> List[str]:
        if obj is None:
            return []
        if isinstance(obj, str):
            return [obj]
        return obj
    
    def matches_criteria(filepath: str, patterns: List[str], starts: List[str], contains: List[str], ends: List[str], exts: List[str], filter: Optional[Callable[[str], bool]]) -> bool:
        path, filename, extension = extract_file_components(filepath) 
        return (
            (not starts or any(filename.startswith(s) for s in starts)) and
            (not contains or any(c in filename for c in contains)) and
            (not ends or any(filename.endswith(e) for e in ends)) and
            (not exts or any(extension == e for e in exts)) and
            (not patterns or any(re.match(p, filename) for p in patterns)) and 
            ((filter is None) or filter(filepath))
        )

    def matches_exclusion_criteria(filepath: str, patterns: List[str], starts: List[str], contains: List[str], ends: List[str], exts: List[str], filter: Optional[Callable[[str], bool]]) -> bool:
        path, filename, extension = extract_file_components(filepath)
        return (
            (starts and any(filename.startswith(s) for s in starts)) or
            (contains and any(c in filename for c in contains)) or
            (ends and any(filename.endswith(e) for e in ends)) or
            (exts and any(extension == e for e in exts)) or
            (patterns and any(re.match(p, filename) for p in patterns)) or
            ((filter is not None) and filter(filepath))
        )
    
    # Parameter Check
    for param in [include_directory, include_pattern, include_start, include_content, include_end, include_extension,
                  exclude_subdirectory, exclude_pattern, exclude_start, exclude_content, exclude_end, exclude_extension]:
        if not check_type_union(param):
            raise TypeError('A Parameter is of the wrong type.')

    # Parameter Conversion -> all convert in List[str] to simplify the rest of the function.
    include_directory = data_to_list(include_directory)
    include_pattern = data_to_list(include_pattern)
    include_start = data_to_list(include_start)
    include_content = data_to_list(include_content)
    include_end = data_to_list(include_end)
    include_extension = data_to_list(include_extension)
    exclude_subdirectory = data_to_list(exclude_subdirectory)
    exclude_pattern = data_to_list(exclude_pattern)
    exclude_start = data_to_list(exclude_start)
    exclude_content = data_to_list(exclude_content)
    exclude_end = data_to_list(exclude_end)
    exclude_extension = data_to_list(exclude_extension)

    # If include_directory = [] -> add os.getcwd() , ie Default value
    if len(include_directory) == 0:
        include_directory.append(os.getcwd())

    # Checking the directories
    for directory in include_directory:
        if not os.path.isdir(directory):
            raise FileNotFoundError(f'The {directory=} is not found.')
    
    # Seacking the files
    list_filepaths = []
    for directory in include_directory:
        for root, dirs, files in os.walk(directory):
            # Skip excluded subdirectories
            if exclude_subdirectory and any(excluded in root for excluded in exclude_subdirectory):
                continue
            for file in files:
                filepath = os.path.join(root, file)
                if matches_criteria(filepath, include_pattern, include_start, include_content, include_end, include_extension, include_filter) and \
                   not matches_exclusion_criteria(filepath, exclude_pattern, exclude_start, exclude_content, exclude_end, exclude_extension, exclude_filter):
                    list_filepaths.append(filepath)
    return list_filepaths
    

def main():
    print("See test_search_files.py")
    
if __name__ == '__main__':
    main()