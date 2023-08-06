try:
	import requests
except ImportError:
	raise "Requests @2.28.2 could not be imported."

class LOTR:
    """ SDK for the-one-api """
    #Methods not to be directly accessed
    def __init__(self, key=None, base_url='https://the-one-api.dev/v2'):
        self.base_url = base_url
        if key is not None:
            self.res = self.create_context(key)
        else:
            raise Exception("No API key given.")
            # self.res = requests 

    def create_context(self, key):
        """Creating the headers for API"""
        context = requests.session()
        context.headers = {'authorization': f'Bearer {key}'}
        return context
    
    def params(self, limit, page, offset, sort, filter):
        """ Helper function formats url params. """
        all_params = f'limit={limit}' if limit != '' else ''
        if all_params and page != '':
            all_params = f'{all_params}&page={page}'

        if all_params and offset != '':
            all_params = f'{all_params}&offset={offset}'

        if all_params and sort != '':
            all_params = f'{all_params}&sort={sort}'

        if all_params and filter != '':
            all_params = f'{all_params}&{filter}'

        all_params = f'?{all_params}' if all_params != '' else all_params
        return all_params
    
    def request(self, path, _id=None, extra_path='', limit='', page='', offset='', sort='', filter='', *args, **kwargs):
        """ creates the request"""
        all_params = self.params(limit, page, offset, sort, filter)
        if _id is None:
            # if movie and name is None:
            url = f'{self.base_url}/{path}{all_params}'
            req = self.res.get(url, *args, **kwargs)
        else:
            url = f'{self.base_url}/{path}/{_id}/{extra_path}{all_params}'
            req = self.res.get(url, *args, **kwargs)
        return req
    
    #Public methods for use
    def movies(self, *args, **kwargs):
        """ Returns all movies under given params."""
        path = 'movie'
        return self.request(path, *args, **kwargs).json()['docs']

    def movie_by_title(self, title: str, *args, **kwargs):
        """Returns movie with a given title, raises exception if not foundor not given a title. """
        if title != '':
            path = 'movie'
            found = False
            req = self.request(path, *args, **kwargs).json()['docs']
            for i in range(0, len(req)):
                if(str(req[i]['name']).lower().replace(" ", "") == title.lower().replace(" ", "")):
                    # print("FOUND!")
                    return req[i]
            if not found:
                raise Exception("Film not found Title: " + title)
        else:
            raise Exception("No title given.")

    def character(self, name='', *args, **kwargs):
        """ Returns character. If name given returns character of that name"""
        if name == '':
            path = 'character'
        else:
            path = f'character?name={name}'
        # print(self.request(path, *args, **kwargs).json()['docs']['_id'])
        return self.request(path, *args, **kwargs).json()['docs']

    def quotes(self, _id=None, *args, **kwargs):
        """ Returns quote. If a name is given, returns quotes from that character."""
        path = 'quote'
        if _id == None:
            return self.request(path, *args, **kwargs).json()['docs']
        else:
            ID = _id
            return self.request(path, _id = ID, *args, **kwargs).json()['docs']