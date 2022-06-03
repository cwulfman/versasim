import json
from fastapi import FastAPI
from pyairtable import Base
from versasim import edf
from dotenv import load_dotenv, dotenv_values

def record_ids(base, table_name):
    return [r['id'] for r in base.get_table(table_name).all()]

load_dotenv()
config = dotenv_values()

base = Base(config['API_KEY'], config['BASE_ID'])

elections_table = base.get_table('Election')

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello Again",
            "elections": app.url_path_for("get_elections")
            }

@app.get("/elections")
async def get_elections():
    elections = elections_table.all()

    return {"elections": elections}

@app.get("/elections/{election_id}")
async def get_election(election_id):
    election = edf.Election(base, election_id)
    return election.as_dict()

@app.get("/electionReport/{election_id}")
async def get_election_report(election_id):
    report = edf.ElectionReport(base) # ignore id for now and return all
    return report.generate_report()

@app.get("/gpunits")
async def get_gpunits():
    rows = base.get_table('GpUnit').all()
    return [edf.GpUnit(base, id).as_dict()
            for id in record_ids(base, 'GpUnit')]

@app.get("/gpunits/{gpunit_id}")
async def get_gpunit(gpunit_id):
    return edf.GpUnit(base, gpunit_id).as_dict()

@app.get("/offices")
async def get_offices():
    return base.get_table('Office').all()

@app.get("/offices/{office_id}")
async def get_office(office_id):
    return edf.Office(base, office_id).as_dict()

@app.get("/persons")
async def get_persons():
    return base.get_table('Person').all()

@app.get("/persons/{person_id}")
async def get_person(person_id):
    return edf.Person(base, person_id).as_dict()

@app.get("/candidates")
async def get_candidates():
    return base.get_table('Candidate').all()

@app.get("/candidates/{candidate_id}")
async def get_candidate(candidate_id):
    return edf.Candidate(base, candidate_id).as_dict()

@app.get("/candidate_contests")
async def get_contests():
    return base.get_table('CandidateContest').all()

@app.get("/candidate_contests/{contest_id}")
async def get_candidate_contest(contest_id):
    return edf.CandidateContest(base, contest_id).as_dict()

@app.get("/ballot_measures")
async def get_ballot_measures():
    return base.get_table('BallotMeasure').all()

@app.get("/ballot_measure{contest_id}")
async def get_ballot_measure(contest_id):
    return edf.BalotMeasure(base, contest_id).as_dict()

@app.get("/ballotstyles")
async def get_ballotstyles():
    return base.get_table('BallotStyle').all()

@app.get("/ballotstyles/{ballotstyle_id}")
async def get_ballotstyle(ballotstyle_id):
    return edf.BallotStyle(base, ballotstyle_id).as_dict()

