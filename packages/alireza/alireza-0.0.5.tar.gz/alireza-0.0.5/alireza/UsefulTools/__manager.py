__all__ = ['random_string','format_finder','string_validator']





import secrets
import string
from urllib.parse import quote
from alireza.DjangoTools import rename_file
from typing import Iterable
from alireza.UsefulTools.__Error_Handler import _ErrorHandling
import re




def random_string(length:int=15,url_safe:bool=False,regex:str=False,only_letters:bool=False,only_digits:bool=False,
                  only_lowercase:bool=False,only_uppercase:bool=False,*args,**kwargs) -> str:
    """
    Generate a random String .
    You can only choose one between regex and only_letters and only_digits .
    Regex must be a string.
    Example:
    >>> regex='AaBbCc123#'
    """
    if regex:
        regex = regex.replace(' ','')
    _ErrorHandling._random_string_error_handler(length,url_safe,regex,only_letters,only_digits,only_lowercase,only_uppercase)
    #characters
    
    if not regex:
        #only letters or digits or both
        if only_letters == True:
            characters = string.ascii_letters
        elif only_digits == True:
            characters = string.digits
        else:
            characters = string.hexdigits
    else:
        characters = regex


    generated_string = "".join([secrets.choice(characters) for _ in range(length)])
    

    #url safe
    if url_safe:
        generated_string = quote(generated_string)


    #lower & upper
    if only_lowercase:
        generated_string = generated_string.lower()
    elif only_uppercase:
        generated_string = generated_string.upper()

    return generated_string





def format_finder(filenames:Iterable[str],customformats:Iterable[str]|None=None,find_formats:Iterable[str]|None=None,
                  no_dot_filename:bool |None=False,rename_files:str|None=None,*args,**kwargs) -> str:
    """
    Extract the format from given filenames and return it as a tuple of (filename, ext). 
    Specify a custom format using customformat=['custom.format'], and if that format exists in the filenames, it will be extracted.
    You can also search for a specific format using find_format. If none of the given formats are found, it will return None.
    To remove all dots in the filename, use no_dot_filename.
    Additionally, you can rename the filename with rename_files using a provided string."
    """
    
    _ErrorHandling._format_finder_error_handler(filenames,customformats,find_formats,no_dot_filename,rename_files)
    result = []
    custom_formats = ['tar.gz']
    if customformats is not None:
        custom_formats += customformats


    for filename in filenames:
        filename_and_extention = None
        splited_filename = [i for i in filename.split('.') if len(i)>0] 
        if len(splited_filename) < 2:
            continue  
        elif len(splited_filename) == 2:
            filename = "".join(splited_filename[:-1])
            ext = splited_filename[-1]
            filename_and_extention = (filename,ext)
        else:
            for format in custom_formats:
                ext = filename[-len(format):]
                if ext == format:
                    filename_and_extention = (filename[:-len(format)-1],ext)
                


        if filename_and_extention is None:
            filename_and_extention = (".".join(splited_filename[:-1]),splited_filename[-1])

        if no_dot_filename is True:
            filename_and_extention = filename_and_extention[0].replace('.',''),filename_and_extention[1]
            result.append(filename_and_extention)
        else:
            result.append(filename_and_extention)

    if find_formats is not None:
        founded_results = []
        for files in result:
            if files[1] in find_formats:
                founded_results.append(files)
        if founded_results:
            result = founded_results
        else:
            return None
    if rename_files is not None:
        renamed_result = []
        for filename in result:
            renamed_file = rename_file('',f"{filename[0]}.{filename[1]}",customformats=custom_formats,filenamemethod=rename_files)
            renamed_result.append(renamed_file)
        return renamed_result



    return result




def string_validator(input_string:str,filter_characters:str,is_allowed:bool=True) -> bool:
    """
        *Validates a string based on the filter_characters and is_allowed.*
        
        Args:
        Input_string: The string to be validated.
        Filter_characters: The set of characters that used to validate the string.
        is_allowed: Determines the validation behavior.
            >>> if is_allowed is True -> only allows strings that contain the filter_characters.
            >>> if is_allowed is False -> only allows strings that does not contain the filter_characters.
    """
    _ErrorHandling._string_validator_error_handler(input_string,filter_characters,is_allowed)

    input_string = repr(input_string)[1:-1]
    filter_characters = repr(filter_characters)[1:-1]


    #is allowed
    if is_allowed:
        # Define a regular expression pattern for allowed characters
        pattern = f'^[{re.escape(filter_characters)}]+$'
        # Check if the input_string matches the pattern
        if re.match(pattern, input_string):
            return True
        else:
            return False
    

    #is disallowed
    elif not is_allowed:
        # Define a regular expression pattern for disallowed characters
        pattern = f'[{re.escape(filter_characters)}]'
        # Check if the input_string matches the pattern
        if re.search(pattern, input_string):
            return False
        else:
            return True
