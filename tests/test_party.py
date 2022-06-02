import pytest
from pyairtable import Base
from versasim import edf
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values()

identifiers = {'hadron_party': 'recg6kdFZ9iBvR2nF'}


@pytest.fixture
def base():
    return Base(config['API_KEY'], config['BASE_ID'])

@pytest.fixture
def hadron_party(base):
    return edf.Party(base, identifiers['hadron_party'])


def test_object(hadron_party):
    assert hadron_party.Label == "Hadronicrat"
    assert hadron_party.Name == "The Hadron Party of Farallon"
    assert hadron_party.Abbreviation == "HAD"
