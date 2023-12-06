
import pandas as pd
import os
## todo switch to dask
from jsonapi_client import Session, Modifier
from pathlib import Path
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
            analysis['sample_accession'] = sample.sample_id
            analysis['sample_description'] = sample.sample_description
            analysis['environment'] = sample.environment
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

def check_available_sample_analysis_data(api_path, analysis_ids):
    analysis_files = {}
    with Session(api_path) as session:
        for analysis_id in analysis_ids:
            analysis_files[analysis_id] = []
            for download in session.iterate(f"analyses/{analysis_id}/downloads"):
                file_info = {
                    "alias": download.alias, 
                    "description": download.description.label,
                    "url":download.links.self.url}
                analysis_files[analysis_id].append(file_info)
    return analysis_files


def get_data_file(file_storage_path, download_url):
    try:
        urlretrieve(download_url, file_storage_path)
    except Exception as e:
        print(e)


def get_SSU_tsv_file_list_for_study(analyses_file_info, study_id):
    tsv_files = {}
    for analysis, files in analyses_file_info[study_id].items():
        for file in files:
            if file['description'] == "Reads encoding SSU rRNA" and file['url'].endswith('tsv'):
                tsv_files[analysis] = file['url']
    return tsv_files


def get_tsv_files(tsv_files, file_root="..metagenomics/tmp/"):
    # make dir for study if it doesnt exist
    Path(file_root).mkdir(parents=True, exist_ok=True)
    for analysis_id, url in tsv_files.items():
        file_path = os.path.join(file_root, f"{analysis_id}_FASTQ_SSU_OTU.tsv")
        get_data_file(file_path, url)