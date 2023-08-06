## Ty Delargy: Lord of Ty Rings SDK
In order to use the SDK import. Create a context for API use.
    
    from src import LOTR_SDK
    SDK = LOTR_SDK.LOTR("YOUR API KEY")

Example Usage:
    
    all_movies = SDK.movies()
    a_movie = SDK.movies(_id = "movie_id")
    #Not capital or space sensitive
    SDK.movie_by_title("the unexpected  Journey")

    all_characters = SDK.character()
    character_by_name = SDK.character(name = 'Gandalf')

    all_quotes = SDK.quotes()
    quote_by_id = SDK.quotes(_id='quote_id')

Filtering, Sorting, and Pagination available as described by https://the-one-api.dev/

Simply enter fields as arguments into your call with: limit, page, offset, sort, and filter.

Testing can be accomplished by going into /tests folder and running 
    pytest all_test.py
