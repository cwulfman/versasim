""" Airtable interface. """

from datetime import datetime
from pyairtable import Base, Table

BASE_ID =  "appTNDM2DwCS2vYun"
API_KEY = "keyuXobQvG2xmGv1q"


def language_string(content, language="en"):
    """returns a dictionary-model of a LanguageString"""
    return {"@type": "ElectionResults.LanguageString",
            "Content": content,
            "Language": language}

def internationalized_text(content, label='', language="en"):
    """returns a dictionary-model of an InternationalizedText"""

    data = {"@type": "ElectionResults.InternationalizedText",
            "Text": [language_string(content, language)]}
    if label:
        data['Label'] = label

    return data


# def gp_unit(record):
#     fields = record['fields']
#     return {"@type": "ElectionResults.ReportingUnit",
#             "@id": record['id'],
#             "Name": internationalized_text(fields['Name'])}

# def election(record):
#     fields = record['fields']
#     data = {"@type": "ElectionResults.Election",
#             "@id": record['id'],
#             "Type": fields['Type'],
#             "StartDate": fields['StartDate'],
#             "EndDate": fields['EndDate'],
#             "ElectionScopeId": fields['ElectionScope'],
#             "Name": internationalized_text(fields['Name'])
#             }
    
#     return data

# def ballot_style(record):
#     fields = record['fields']
#     data = {"@type": 'ElectionResults.BallotStyle',
#             "@id": record['id'],
#             "GpUnitIds": fields['GpUnits']
#             }
#     return data


class Edf():
    def __init__(self, base, id, table, type):
        self.type = type
        self.base = base
        self.id = id
        self.record = base.get(table, id)['fields']


class GpUnit(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'GpUnit',
                         'ElectionResults.ReportingUnit')
        self.Label = self.record['Label']
        self.Name = self.record['Name']
        self.Type = self.record['Type']
        self.ComposingGpUnits = []
        if 'ComposingGpUnits' in self.record:
            self.ComposingGpUnits = [GpUnit(base, c_id)
                                     for c_id
                                     in self.record['ComposingGpUnits']]

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "Type": self.Type,
                "Name": internationalized_text(self.Name, self.Label)
                }
        return data

class Party(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'Party',
                         'ElectionResults.Party')
        self.Label = self.record['Label']
        self.Name = self.record['Name']
        self.Abbreviation = self.record['Abbreviation']

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "Name": internationalized_text(self.Name, self.Label)
                }
        return data



class Office(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'Office',
                         'ElectionResults.Office')
        if 'Name' in self.record:
            self.Name = self.record['Name']
        self.Label = self.record['Label']
        self.IsPartisan = self.record['IsPartisan']
        self.ElectionDistrict = None
        if 'ElectionDistrict' in self.record:
            self.ElectionDistrict = GpUnit(base,
                                           self.record['ElectionDistrict'][0])

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "IsPartisan": True,
                "Name": internationalized_text(self.Name, self.Label)
                }
        return data


class Person(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'Person',
                         'ElectionResults.Person')
        self.LastName = self.record['LastName']
        self.FirstName = self.record['FirstName']
        self.Profession = self.record['Profession']

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "FirstName": self.FirstName,
                "LastName": self.LastName,
                "Profession": internationalized_text(self.Profession)
        }
        return data

class Candidate(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'Candidate',
                         'ElectionResults.Candidate')
        self.BallotName = self.record['BallotName']

        self.Person = None
        if 'Person' in self.record:
            self.Person = Person(base, self.record['Person'][0])

        self.Party = None
        if 'Party' in self.record:
            self.Party = Party(base, self.record['Party'][0])

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "PersonId": self.Person.id,
                "BallotName": internationalized_text(self.BallotName),
                "PartyId": self.Party.id
        }
        return data


class CandidateSelection(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'CandidateSelections',
                         'ElectionResults.CandidateSelection')
        self.CandidateIds = self.record['Candidates']
        self.Label = self.record['Label']
        if 'IsWriteIn' in self.record:
            self.IsWriteIn = self.record['IsWriteIn']
        else:
            self.IsWriteIn = False

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id
                }
        if self.IsWriteIn:
            data["IsWriteIn"] = True
        else:
            data["CandidateIds"] = self.CandidateIds

        return data

class Contest(Edf):
    def __init__(self, base, id, table, type):
        super().__init__(base, id, table, type)
        self.Abbreviation = None
        self.BallotSubTitle = None
        self.BallotTitle = None
        self.ContestSelection = []
        self.ElectionDistrict = GpUnit(base, self.record['ElectionDistrict'][0])
        self.Name = self.record['Name']
        if 'VoteVariation' in self.record:
            self.VoteVariation = self.record['VoteVariation']
        self.ContestSelection = []

class CandidateContest(Contest):
    def __init__(self, base, id):
        super().__init__(base, id, 'CandidateContest',
                         'ElectionResults.CandidateContest')
        self.VotesAllowed = self.record['VotesAllowed']
        self.Office = self.record['Office']

        if 'ContestSelections' in self.record:
            self.ContestSelection = [CandidateSelection(self.base, selection_id)
                                     for selection_id
                                     in self.record['ContestSelections']]

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "Name": self.Name,
                "OfficeIds": self.Office,
                "VoteVariation": self.VoteVariation,
                "VotesAllowed": self.VotesAllowed,
                "ElectionDistrictId": self.ElectionDistrict.id,
                "ContestSelection": [selection.as_dict()
                                     for selection
                                     in self.ContestSelection]
                }
        return data

class BallotMeasure(Contest):
    def __init__(self, base, id):
        super().__init__(base, id, 'BallotMeasure',
                         'ElectionResults.BallotMeasureContest')
        self.FullText = self.record['FullText']
        if 'ContestSelections' in self.record:
            self.ContestSelection = [BallotMeasureSelection(self.base, selection_id)
                                     for selection_id
                                     in self.record['ContestSelections']]

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "ElectionDistrictId": self.ElectionDistrict.id,
                "Name": self.Name,
                "FullText": internationalized_text(self.FullText),
                "ContestSelection": [selection.as_dict()
                                     for selection
                                     in self.ContestSelection]
                }
        return data


class BallotMeasureSelection(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier,
                         'BallotMeasureSelections',
                         'ElectionResults.BallotMeasureSelection')
        self.Selection = self.record['Selection']

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "Selection": internationalized_text(self.Selection)}
        return data


class OrderedContest(Edf):
    def __init__(self, contest_object):
        self.type = 'ElectionResults.OrderedContest'
        self.Contest = contest_object
        self.OrderedContestSelection = self.Contest.ContestSelection

    def as_dict(self):
        data = { "@type": self.type,
                 "ContestId": self.Contest.id,
                 "OrderedContestSelectionIds": [selection.id
                                                for selection
                                                in self.OrderedContestSelection]
        }
        return data


class BallotStyle(Edf):
    def __init__(self, base, id):
        super().__init__(base, id, 'BallotStyle', 'ElectionResults.BallotStyle')
        self._contests = []
        if 'Contests' in self.record:
            self._contests += [CandidateContest(base, id)
                              for id in self.record['Contests']]
        if 'BallotMeasures' in self.record:
            self._contests += [BallotMeasure(base, id)
                              for id in self.record['BallotMeasures']]
        

    @property
    def name(self):
        return internationalized_text(self.record['Name'])

    @property
    def OrderedContests(self):
        return [OrderedContest(contest) for contest in self._contests]

    def as_dict(self):
        data = {"@type": self.type,
                "GpUnitIds": self.record['GpUnits'],
                "OrderedContent": [c.as_dict() for c in self.OrderedContests]}
        return data


class Election(Edf):
    def __init__(self, base, id):
        super().__init__(base, id, "Election", "ElectionResults.Election")
        candidate_contests = [CandidateContest(base, id) for id in self.record['CandidateContest']]
        ballot_measure_contests = [BallotMeasure(base, id)
                                        for id in self.record['BallotMeasure']]
        self.Contest = candidate_contests + ballot_measure_contests
        self.BallotStyle = [BallotStyle(base, id) for id in self.record['BallotStyle']]
        self.Name = self.record['Name']
        self.StartDate = self.record['StartDate']
        self.EndDate = self.record['EndDate']
        self.Type = self.record['Type']
        self.ElectionScopeId = self.record['ElectionScope'][0]

    def as_dict(self):
        data = {"@type": self.type,
                "ElectionScopeId": self.ElectionScopeId,
                "StartDate": self.StartDate,
                "EndDate": self.EndDate,
                "Type": self.Type,
                "Name": internationalized_text(self.Name),
                "Contest": [c.as_dict() for c in self.Contest],
                "BallotStyle": [b.as_dict() for b in self.BallotStyle]
                }

        return data

class ElectionReport(Edf):
    def __init__(self, base):
        self.type = "ElectionResults.ElectionReport"
        self.base = base
        self._Party = []
        self._GpUnit = []

    def record_ids(self, table_name):
        return [r['id'] for r in self.base.get_table(table_name).all()]

    

    def generate_report(self):
                report = {"@type": "ElectionResults.ElectionReport",
                          "Format": "precinct-level",
                          "GeneratedDate" : datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                          "VendorApplicationId": "ElectionReporter",
                          "Issuer": "TrustTheVote",
                          "IssuerAbbreviation": "TTV",
                          "Status": "pre-election",
                          "SequenceStart": 1,
                          "SequenceEnd": 1}
                report['Party'] = [Party(self.base, id).as_dict() for id in self.record_ids('Party')]
                report['GpUnit'] = [GpUnit(self.base, id).as_dict() for id in self.record_ids('GpUnit')]
                report['Office'] = [Office(self.base, id).as_dict() for id in self.record_ids('Office')]
                report['Person'] = [Person(self.base, id).as_dict() for id in self.record_ids('Person')]
                report['Election'] = [Election(self.base, id).as_dict() for id in self.record_ids('Election')]

                return report


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
        
