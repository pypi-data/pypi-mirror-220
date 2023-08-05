import warnings



class _ErrorHandling():

    @staticmethod
    def _rename_file_error_handler(instance,filename,customformats,filenamemethod,hardpath,accept):
        if (cf_type:=type(customformats)) is not list:
            error = "customformats Must be a list not {}.".format("".join(str(cf_type).split("'")[1:-1]))
            raise ValueError(error)
        elif (accept_type:=type(accept)) is not list:
            error = "accept Must be a list not {}.".format("".join(str(accept_type).split("'")[1:-1]))
            raise ValueError(error)
        elif any(not isinstance(item, str) for item in customformats):
            error = "customformats should be a list of strings."
            raise ValueError(error)
        elif any(not isinstance(item, str) for item in accept):
            error = "accept should be a list of strings."
            raise ValueError(error)
        elif any(item.startswith('.') or item.endswith('.') for item in customformats):
            error = """Wrong format syntax. make sure that there is no (.) in start or end of your format. your input should look like this:
            customformats=['custom.format'] and your output is -> filename.custom.format"""
            raise ValueError(error)
        elif any(item.startswith('.') or item.endswith('.') for item in accept):
            error = """Wrong format syntax. make sure that there is no (.) in start or end of your format. your input should look like this:
            accept=['custom.format'] and your output is -> filename.custom.format"""
            raise ValueError(error)
        