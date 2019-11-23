from os import makedirs

def create(folder_name, show_exceptions=False):

    try:

        makedirs(folder_name)

    except:

        if (show_exceptions == True):

            raise
        
    return(folder_name)
