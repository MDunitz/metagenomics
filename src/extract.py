
import pandas as pd
## todo switch to dask
from jsonapi_client import Session, Modifier

def fetch_metadata(endpoint, api_path):
    with Session(api_path) as mgnify:
        studies = map(lambda r: r.json, mgnify.iterate(endpoint))
        studies = pd.json_normalize(studies)
    return studies


def fetch_study_data(api_path, study_metadata, sample_count=6):
    studies_samples = []
    with Session(api_path) as mgnify:
        # todo add threading
        for idx, study in study_metadata[:sample_count].iterrows():
            print(f"fetching {study.id} samples")
            samples = map(lambda r: r.json, mgnify.iterate(f'studies/{study.id}/samples?page_size=1000'))
            samples = pd.json_normalize(samples)
            samples = pd.DataFrame(data={
                'accession': samples['id'],
                'sample_id': samples['id'],
                'study': study.id, 
                'lon': samples['attributes.longitude'],
                'lat': samples['attributes.latitude'],
                'color': "#FF0000",
            })
            samples.set_index('accession', inplace=True)
            studies_samples.append(samples)
    studies_samples = pd.concat(studies_samples)
    return studies_samples

def get_sample_analyses(api_path, study_samples, analysis_limit=10):
    analyses = []
    with Session(api_path) as mgnify:
        for idx, sample in study_samples[:analysis_limit].iterrows():
            filtering = Modifier(f"pipeline_version=5.0&sample_accession={sample.sample_id}&experiment_type=assembly")
            analysis = map(lambda r: r.json, mgnify.iterate('analyses', filter=filtering))
            analysis = pd.json_normalize(analysis)
            analyses.append(analysis)
    analyses = pd.concat(analyses)
    return analyses
