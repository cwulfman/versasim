import pytest
from pyairtable import Base, Table
import versasim.edf as edf
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values()

election_id = 'recPTDvg1KWgN2dzx'
precinct_id = 'recBpUK5BY7YR4VHo'

def table_ids(base, table):
    return [r['id'] for r in base.get_table(table).all()]


@pytest.fixture
def base():
    return Base(config['API_KEY'], config['TEST_BASE_ID'])


@pytest.fixture
def report(base):
    return edf.ElectionReport(base, election_id, precinct_id)


def test_election(report):
    assert report.Election[0].id == election_id


def test_dict(report):
    the_dict = report.as_dict()
    assert the_dict['@type'] == "ElectionResults.ElectionReport"
