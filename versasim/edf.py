""" Airtable interface. """

from datetime import datetime
from pyairtable import Base, Table

BASE_ID =  "appTNDM2DwCS2vYun"
API_KEY = "keyuXobQvG2xmGv1q"


def language_string(content, language="en"):
    return {"@type": "ElectionResults.LanguageString",
            "Content": content,
            "Language": language}

def internationalized_text(content, language="en"):
    return {"@type": "ElectionResults.InternationalizedText",
            "Text": language_string(content, language)}


def gp_unit(record):
    fields = record['fields']
    return {"@type": "ElectionResults.ReportingUnit",
            "@id": record['id'],
            "Name": internationalized_text(fields['Name'])}

def election(record):
    fields = record['fields']
    data = {"@type": "ElectionResults.Election",
            "@id": record['id'],
            "Type": fields['Type'],
            "StartDate": fields['StartDate'],
            "EndDate": fields['EndDate'],
            "ElectionScopeId": fields['ElectionScope'],
            "Name": internationalized_text(fields['Name'])
            }
    
    return data

def ballot_style(record):
    fields = record['fields']
    data = {"@type": 'ElectionResults.BallotStyle',
            "@id": record['id'],
            "GpUnitIds": fields['GpUnits']
            }
    return data


class Edf():
    def __init__(self, base, id, table, type):
        self.type = type
        self.base = base
        self.id = id
        self.record = base.get(table, id)['fields']


class GpUnit(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'GpUnit',
                         'ElectionResults.RecordingUnit')
        self.Label = self.record['Label']
        self.Name = self.record['Name']
        self.Type = self.record['Type']


class Party(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'Party',
                         'ElectionResults.Party')
        self.Label = self.record['Label']
        self.Name = self.record['Name']
        self.Abbreviation = self.record['Abbreviation']

class Office(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'Office',
                         'ElectionResults.Office')
        self.Name = self.record['Name']
        self.IsPartisan = self.record['IsPartisan']
        self.ElectionDistrict = self.record['ElectionDistrict']

class Person(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'Person',
                         'ElectionResults.Person')
        self.LastName = self.record['LastName']
        self.FirstName = self.record['FirstName']
        self.Profession = self.record['Profession']




class Candidate(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'Candidate',
                         'ElectionResults.Candidate')
        self.BallotName = self.record['BallotName']



class CandidateSelection(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'Candidate',
                         'ElectionResults.CandidateSelection')

    def as_dict(self):
        pass


class CandidateContest(Edf):
    def __init__(self, base, id):
        super().__init__(base, id, 'CandidateContest',
                         'ElectionResults.OrderedContest')
        ContestSelection = [CandidateSelection(self.base, id)
                                for id
                                in self.record['CandidateSelections']]
        Name = self.record['Name']

    def as_dict(self):
        data = {"@type": self.type,
                "ContestId": self.id,
                "OrderedContestSelectionIds": [selection.id
                                               for selection
                                               in self.candidate_selections]
                }
        return data

class BallotMeasure(Edf):
    def __init__(self, base, id):
        super().__init__(base, id, 'BallotMeasure',
                         'ElectionResults.OrderedContest')


class BallotStyle(Edf):
    def __init__(self, base, id):
        super().__init__(base, id, 'BallotStyle', 'ElectionResults.BallotStyle')
        contest_ids = self.record['Contests']
        self.candidate_contests = [CandidateContest(base, id) for id in contest_ids]
        self.ballot_measure_contests = [BallotMeasure(base, id)
                                        for id in self.record['BallotMeasures']]

    @property
    def name(self):
        return internationalized_text(self.record['Name'])

    @property
    def OrderedContests(self):
        return self.candidate_contests + self.ballot_measure_contests

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "Name": self.name,
                "GpUnitIds": self.record['GpUnits'],
                "OrderedContests": self.OrderedContests }
        return data


class Election(Edf):
    def __init__(self, base, id):
        super().__init__(base, id, "Election", "ElectionResults.Election")
        candidate_contests = [CandidateContest(base, id) for id in self.record['CandidateContest']]
        ballot_measure_contests = [BallotMeasure(base, id)
                                        for id in self.record['BallotMeasure']]
        self.contest = candidate_contests + ballot_measure_contests
        self.ballot_style = [BallotStyle(base, id) for id in self.record['BallotStyle']]
        self.name =  internationalized_text(self.record['Name'])

        

    def as_dict(self):
        c_contests = [c.as_dict() for c in self.candidate_contests]
        b_contests = [b.as_dict() for b in self.ballot_measure_contests]
        data = {"@type": self.type,
                "@id": self.id,
                "Name": self.name,
                "Contest": [c.as_dict() for c in self.contest],
                "BallotStyle": [b.as_dict() for b in self.ballot_style]
                }
        
        return data

class ElectionReporter:
    def __init__(self, base_id, api_key):
        self._base_id = base_id
        self._api_key = api_key
        self._base = None

        self._gp_units = None
        self._parties = None
        self._offices = None
        self._people = None
        self._headers = None
        self._candidates = None
        self._candidate_contests = None
        self._ballot_measures = None
        self._ballot_styles = None
        self._elections = None
        self.election_reports = []

    @property
    def base(self):
        if not self._base:
            self._base = Base(self._api_key, self._base_id)
        return self._base

    @property
    def gp_units(self):
        if not self._gp_units:
            table = self.base.get_table('GpUnit')
            self._gp_units = table.all()
        return self._gp_units

    @property
    def parties(self):
        if not self._parties:
            table = self.base.get_table('Party')
            self._parties = table.all()
        return self._parties

    @property
    def offices(self):
        if not self._offices:
            table = self.base.get_table('Office')
            self._offices = table.all()
        return self._offices

    @property
    def people(self):
        if not self._people:
            table = self.base.get_table('Person')
            self._people = table.all()
        return self._people

    @property
    def headers(self):
        if not self._headers:
            table = self.base.get_table('Header')
            self._headers = table.all()
        return self._headers

    @property
    def candidates(self):
        if not self._candidates:
            table = self.base.get_table('Candidate')
            self._candidates = table.all()
        return self._candidates

    @property
    def candidate_contests(self):
        if not self._candidate_contests:
            table = self.base.get_table('CandidateContest')
            self._candidate_contests = table.all()
        return self._candidate_contests

    @property
    def ballot_measures(self):
        if not self._ballot_measures:
            table = self.base.get_table('BallotMeasure')
            self._ballot_measures = table.all()
        return self._ballot_measures

    

    def ballot_styles(self):
        if not self._ballot_styles:
            table = self.base.get_table('BallotStyle')
            self._ballot_styles = table.all()
        return self._ballot_styles


    def ballot_styles_for(self, election_id):
        records = list(filter(lambda x: election_id in r['fields']['BallotStyle'], self.ballot_styles))
        
        

    @property
    def elections(self):
        if not self._elections:
            table = self.base.get_table('Election')
            self._elections = table.all()
        return self._elections

    def generate_election_report(self, election_id):
        report = {
            "@type": "ElectionResults.ElectionReport",
            "Format": "precinct-level",
            "GeneratedDate" : datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "VendorApplicationId": "ElectionReporter",
            "Issuer": "TrustTheVote",
            "IssuerAbbreviation": "TTV",
            "SequenceStart": 1,
            "SequenceEnd": 1
        }
        election_record = list(filter(lambda x: x['id'] == election_id, self.elections))[0]
        ballot_styles = list(filter(lambda x: x['id'] in election_record['fields']['BallotStyle'], self.ballot_styles))

        election_f = election(election_record)
        election_f['BallotStyle'] = [ballot_style(b) for b in ballot_styles]
        report['Election'] = election_f
        return report
        
