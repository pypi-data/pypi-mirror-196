#Tests run by pytest
import pytest
from SDK import LOTR_SDK
#Insert your API_KEY
API_KEY = 'SpItiWofvfNo4rjVx5xm '

@pytest.fixture
def SDK():
    return LOTR_SDK.LOTR(API_KEY)

def test_all_movies(SDK):
    response =  SDK.movies()
    #Test get respone and several fields
    assert response
    assert response[0]['name'] == "The Lord of the Rings Series"
    assert response[2]['boxOfficeRevenueInMillions'] == 1021
    assert response[2]['academyAwardNominations'] == 3
    #Test with limit option
    response = SDK.movies(limit = 2)
    assert len(response) == 2
    #Test with specific ID
    response = SDK.movies(_id = '5cd95395de30eff6ebccde5a')
    assert len(response) == 1
    assert response[0]['name'] == "The Battle of the Five Armies"


def test_get_by_title(SDK):
    #Test that spaces and capitals don't matter
    response = SDK.movie_by_title("the unexpected  Journey")
    assert response
    response = SDK.movie_by_title("The Unexpected Journey")
    assert response
    #Test exception on bad title.
    with pytest.raises(Exception):
        response = SDK.movie_by_title("th unexpected  Journey")
    #Test different title
    response = SDK.movie_by_title("The Return of the King")
    assert response

def test_quotes(SDK):
    #Test get quotes
    response = SDK.quotes()
    assert response
    assert response[0]['dialog'] == 'Deagol!'
    #Test get quote by an ID
    response = SDK.quotes(_id="5cd96e05de30eff6ebcce978")
    assert response[0]['dialog'] == 'What would you have me do?'