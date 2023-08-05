import warnings
import math

class _ErrorHandling:

    @staticmethod
    def __type_finder(var):
        type_var = type(var)
        return "".join(str(type_var).split("'")[1:-1])
    
    @staticmethod
    def _random_string_error_handler(length,url_safe,regex,only_letters,only_digits,only_lowercase,only_uppercase):
        #length
        if type(length) is not int:
            error = "Value must be int not {}".format(_ErrorHandling.__type_finder(length))
            raise ValueError(error)
        elif length<1:
            error = f"Length must be greater than 0. The Given length {length} is {int(math.fabs(length))+1} short."
            raise IndexError(error)
        #end length



        ##############
        #regex
        elif regex and type(regex) is not str :
            error = "Regex must be a string. example: 'AaBb123#$' "
            raise ValueError(error)
        #end regex

        #only letters or digits
        elif type(only_letters) is not bool:
            error = "Value for only_letters must be boolean not {}".format(_ErrorHandling.__type_finder(only_letters))
            raise ValueError(error)
        elif type(only_digits) is not bool:
            error = "Value for only_digits must be boolean not {}".format(_ErrorHandling.__type_finder(only_digits))
            raise ValueError(error)
        
        #Disallowing from using regex and only_letters and only_digits at the same time.
        elif sum([bool(regex),only_letters,only_digits]) > 1:
            values = {'regex':bool(regex),'only_letters':only_letters,'only_digits':only_digits}
            variable_names = " and ".join([variable for variable,value in values.items() if value==True])
            error = f"can't use {variable_names} at the same time."
            raise TypeError(error)

        ##############

        #url_safe
        elif type(url_safe) is not bool:
            error = "Value for url_safe must be boolean not {}".format(_ErrorHandling.__type_finder(url_safe))
            raise ValueError(error)
        elif (bool(regex) is False) and (url_safe is True):
            warning = "You should Use url_safe with regex since it's useless by itself."
            warnings.warn(warning,category=Warning)


        #upper and lower
        if type(only_lowercase) is not bool:
            error = "Value for only_lowercase must be boolean not {}".format(_ErrorHandling.__type_finder(only_lowercase))
            raise ValueError(error)
        elif type(only_uppercase)is not bool:
            error = "Value for only_uppercase must be boolean not {}".format(_ErrorHandling.__type_finder(only_uppercase))
            raise ValueError(error)
        if only_digits is True and (only_lowercase or only_uppercase):
            warning = "Using only_lowercase or only_uppercase with only_digits it's useless and won't do anything."
            warnings.warn(warning,category=Warning)
        if only_lowercase and only_uppercase:
            error = "Can't use both only_lowercase and only_uppercase at the same time."
            raise ValueError(error)
        
    
        
    @staticmethod
    def _format_finder_error_handler(filenames,customformats,find_formats,no_dot_filename,rename_files):
        #filenames
        _ErrorHandling.__find_format_errors(filenames,'filenames')
    
        #customformats
        _ErrorHandling.__find_format_errors(customformats,'customformats')
        
        #find_formats
        _ErrorHandling.__find_format_errors(find_formats,'find_formats')
        
        #no_dot_filename
        if no_dot_filename is not None:
            if type(no_dot_filename) is not bool:
                error = """Invalid argument type. Expected a boolean value, but received {}.
                Please provide a boolean value (True or False) as the argument.""".format(_ErrorHandling.__type_finder(no_dot_filename))
                raise TypeError(error)


        #rename_files
        if rename_files is not None:
            if type(rename_files) is not str:
                error = """Invalid argument type. Expected a string, but received {}. 
                Please provide a value of type string as the argument.""".format(_ErrorHandling.__type_finder(rename_files))
                raise TypeError(error)


    @staticmethod
    def __is_iterable(obj):
        try:
            iter(obj)
            return True
        except TypeError:
            return False
        
    @staticmethod
    def __find_format_errors(param,param_name):
        if param is not None:
            if type(param) is str or  not _ErrorHandling.__is_iterable(param) :
                error = f"{param_name} must be an array with strings inside it."
                raise TypeError(error)
            elif not all(tuple(map(lambda item: isinstance(item,str),param))):
                error = "The array contains non-string elements."
                raise TypeError(error)
            elif not all(tuple(map(lambda item:'.' in item,param))):
                error = "The array contains non-file elements."
                raise ValueError(error)
            elif type(param) is dict:
                error = "Only lists, tuples, and sets are supported. Dictionaries cannot be used as an array."
                raise ValueError(error)
            


    @staticmethod
    def _string_validator_error_handler(input_string,filter_characters,is_allowed):
        if type(input_string) is not str:
            error = "input_string Value must be a String not {}.".format(_ErrorHandling.__type_finder(input_string))
            raise TypeError(error)
        elif type(filter_characters) is not str:
            error = "filter_characters Value must be a String not {}.".format(_ErrorHandling.__type_finder(filter_characters))
            raise TypeError(error)
        elif type(is_allowed) is not bool:
            error = "is_allowed Value must be a bool not {}.".format(_ErrorHandling.__type_finder(is_allowed))
            raise TypeError(error)
        
        elif len(input_string) < 1:
            error = "input_string must have at least 1 character."
            raise ValueError(error)
        elif len(filter_characters) < 1:
            error = "filter_characters must have at least 1 character."
            raise ValueError(error)
    