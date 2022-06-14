import pytest
from pyairtable import Base
from versasim import edf
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values()

identifiers = {'the_election': 'recTcX2svm8ivEbff'}


@pytest.fixture
def base():
    return Base(config['API_KEY'], config['TEST_BASE_ID'])


@pytest.fixture
def the_election(base):
    return edf.Election(base, identifiers['the_election'])


# won't work yet
def test_for_candidates(the_election):
    assert len(the_election.candidates) > 0
