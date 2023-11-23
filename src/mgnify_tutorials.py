"""
MGnify notes
A Super Study is a collection of MGnify Studies originating from a major project. 
AtlantECO is one such project, aiming to develop and apply a novel, unifying framework that provides knowledge-based resources for a better understanding and management of the Atlantic Ocean and its ecosystem services
"""





from extract import fetch_metadata, fetch_study_data, get_sample_analyses
from plot import add_data_to_map
from todo import set_row_color_by_term_presence, join_on_sample_id_sub_select_df_columns
atlanteco_endpoint = 'super-studies/atlanteco/flagship-studies'
api_url="https://www.ebi.ac.uk/metagenomics/api/v1"
popup=["study", "sample_id"]
identifier = "go-terms"
go_term = 'GO:0015878'
rename_columns={
    "attributes.accession": "analysis_ID", 
    'relationships.study.data.id': "study_ID",
    'relationships.sample.data.id': "sample_ID", 
    'relationships.assembly.data.id': "assembly_ID"
    }
columns_list = [identifier, 'lon', 'lat', 'study', 'attributes.accession', 'relationships.study.data.id', 'relationships.sample.data.id', 'relationships.assembly.data.id']
popup_list = ["study_ID", "sample_ID", "assembly_ID", "analysis_ID"]



study_metadata = fetch_metadata(atlanteco_endpoint, api_url)
print(f"fetched study metadata: {study_metadata[:5]}")
study_samples = fetch_study_data(api_url, study_metadata)
print(f"fetched {len(study_samples)} samples")
print(f"Study samples {study_samples.head()}")
m = add_data_to_map(study_samples, popup, 'color')
analyses = get_sample_analyses(api_url, study_samples)
print(f"Sample analyses: {analyses[:5]}")
analyses = set_row_color_by_term_presence(api_url, go_term, identifier, analyses)
df2 = join_on_sample_id_sub_select_df_columns(analyses, rename_columns, columns_list, study_samples)
m2 = add_data_to_map(df2, popup_list, identifier)

