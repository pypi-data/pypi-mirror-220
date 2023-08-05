__all__= ['rename_file',]


from uuid import uuid4
from alireza.DjangoTools.__Error_Handler import _ErrorHandling





def __format_finder(all_formats,filename):
    finded=False
    for format in all_formats:
        formats = format.split('.')
        len_format = len(formats) 
        if filename[-len_format:] == formats and len_format<len(filename):
                finded = True
                return {'status':finded,'format':format}
    
    return{'status':finded,'format':''}


def rename_file(instance,filename,customformats:list[str]|None=[],filenamemethod:str|None=uuid4(),hardpath:str|None=False,accept:list[str]|None=[],*args,**kwargs) -> str :
    """
    This function is originally made for Django, but you can use it anywhere depending on your needs.
    
    This function will return you a string containing the name and format of the file and you should use this function in upload_file in Django models.
    The files are stored in the MEDIA_ROOT path in your settings.py.
    If you want to use customformat or filenametype or other things in Django models.py , create a separate function in models.py and put the following codes in it.

    def created_function(instance,filename):
        return rename_file(instance,filename,customformats=[give formats here],filenamemethod=give your method for naming files here,hardpath=give path here)

    In your model:
    image = models.ImageField(upload_to=created_function)

    Customformats should be a list of strings like -> customformats=['cs.fo','cstm.frmt'] and not like ['.cs.fo','cstm.frmt']
    If you want to save the files in another Directory in your MEDIA_ROOT you can give a path to hard path and it will save file in that path .
    
    Example: 

    def created_function(instance,filename):
        return rename_file(instance,filename,hardpath='profiles') -> file saves in -> MEDIA_ROOT/profiles/image.png


    When using the 'accept' parameter, it will only save files that are included in the given list. If a file format is not found in the 'accept' list,
    an empty string (not saving the file) will be returned instead of saving the file.


    """

    _ErrorHandling._rename_file_error_handler(instance,filename,customformats,filenamemethod,hardpath,accept)
    custom_format = customformats + ['tar.gz']
    splited_filename = [i for i in filename.split('.') if len(i)>0] 
    if len(splited_filename) < 2:
        return ''   
    elif len(splited_filename) == 2:
        ext = splited_filename[-1]
    else:
        format_finder = __format_finder(custom_format,splited_filename)
        if format_finder['status']:
            ext=format_finder['format']

    #accept 
    if accept:
        if __format_finder(accept,splited_filename)['status'] is False:
            return ''
                

    
    
    #returning path
    if hardpath == False:
        try:
            return '%s.%s' % (filenamemethod,ext)
        except UnboundLocalError:
            return '%s.%s' % (filenamemethod,splited_filename[-1])
    #hardpath
    else:
        while hardpath[-1] == '/':
            hardpath = hardpath[:-1]
        try:
            return '%s/%s.%s' % (hardpath,filenamemethod,ext)
        except UnboundLocalError:
            return '%s/%s.%s' % (hardpath,filenamemethod,splited_filename[-1])
            



