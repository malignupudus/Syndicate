from urllib.parse import unquote_plus

def extract(data):

    data = data.decode()
    
    if (len(data) == 0):
        
        return({})
    
    try:
        
        post_data_dict = {}
        data = data.split('&')
        
        for _ in data:

            data = _.split('=')

            post_data_dict[data[0]] = unquote_plus(data[1])

        return(post_data_dict)

    except:

        return({})
