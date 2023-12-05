
import pandas as pd
## todo switch to dask
from jsonapi_client import Session, Modifier
from urllib.request import urlretrieve
from src.constants import ANALYSIS_SUMMARY_COL_NAMES

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
                'sample_description': samples['attributes.sample-desc'],
                'biome': samples['attributes.environment-biome'],
                'environment': samples['attributes.environment-feature'],
                'biome_relationship': samples['relationships.biome.data.id'],
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
            # filtering = Modifier(f"pipeline_version=5.0&sample_accession={sample.sample_id}&experiment_type=assembly")
            filtering = Modifier(f"sample_accession={sample.sample_id}")
            analysis = map(lambda r: r.json, mgnify.iterate('analyses', filter=filtering))
            analysis = pd.json_normalize(analysis)
            analyses.append(analysis)
    analyses_df = pd.concat(analyses)
    analyses_df[ANALYSIS_SUMMARY_COL_NAMES] = analyses_df.apply(handle_analysis_summary, axis='columns', result_type='expand')
    return analyses_df


def handle_analysis_summary(row):
    analysis_values = []
    sample_row_summaries = row['attributes.analysis-summary']
    for i in range(0,10):
        analysis_values.append(sample_row_summaries[i]['value'])
    return analysis_values

def check_available_sample_analysis_data(api_path, analysis_id):
    with Session(api_path) as session:
        print(f"\nFiles available for analysis {analysis_id}:")
        for download in session.iterate(f"analyses/{analysis_id}/downloads"):
            print(f"{download.alias}: {download.description.label}")
            print(f"relevant url: {download.links.self.url}")


def get_data_file(file_path, download_url):
    # with Session(api_path) as session:    
        # print(f"Processing: {analysis_id}")
        # for download in session.iterate(f"analyses/{analysis_id}/downloads"):
        #     # Start another for loop to go over the files to download
        #     file_name = f"../tmp/{analysis_id}_FASTQ_SSU_OTU.tsv"
        #     print(f"Downloading file for {analysis_id}")
        #     try:
    try:
        urlretrieve(download_url, file_path)
    except Exception as e:
        print(e)
    # print(f"Finished for: {analysis_id}, stored: {file_path}")