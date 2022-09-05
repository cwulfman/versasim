import pytest
from pyairtable import Base
from versasim import edf
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values()

identifiers = {'contest_mayor': 'recE0Oha5OnxNLFv4'
               }


@pytest.fixture
def base():
    return Base(config['API_KEY'], config['TEST_BASE_ID'])

@pytest.fixture
def mayoral_contest(base):
    return edf.CandidateContest(base, identifiers['contest_mayor'])

@pytest.fixture
def contest_id():
    return  {"@type": "ElectionResults.ExternalIdentifier",
             "Type": "other",
             "OtherType": "TTV",
             "Value": "mayoral_contest",
             "Label": "mayoral_contest"}


def test_object(mayoral_contest, contest_id):
    assert mayoral_contest.ExternalIdentifier[0].as_dict() == contest_id
