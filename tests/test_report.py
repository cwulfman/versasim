import pytest
from pyairtable import Base, Table
import versasim.edf as edf
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values()

identifiers = {'farallon': 'rec5K8APzm54h7Vnj',
               'gadget_county': 'recKCyQwhLDHp1cBD',
               'orbit_city': 'recbrO0CGN0P0C1mC'}

def table_ids(base, table):
    return [r['id'] for r in base.get_table(table).all()]


@pytest.fixture
def base():
    return Base(config['API_KEY'], config['TEST_BASE_IDn'])

@pytest.fixture
def party_ids(base):
    return table_ids(base, 'Party')

def officeids(base):
    return table_ids(base, 'Office')
