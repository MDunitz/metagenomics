# Todo abstract and reorg
from jsonapi_client import Session
import pandas as pd



def set_row_color_by_term_presence(api_url, term, field, analyses):
    go_data = []
    with Session(api_url) as mgnify:
        print(f"analyzing {analyses.shape[0]} rows")
        for idx, mgya in analyses.iterrows():
            print(f"processing {mgya.id}")
            analysis_identifier = map(lambda r: r.json, mgnify.iterate(f'analyses/{mgya.id}/{field}'))
            analysis_identifier = pd.json_normalize(analysis_identifier)
            go_data.append("#0000FF" if term in list(analysis_identifier.id) else "#FF0000")
    analyses.insert(2, term, go_data, True)
    return analyses


def join_on_sample_id_sub_select_df_columns(analyses, rename_columns, columns_list, study_samples):
    df = analyses.join(study_samples.set_index('sample_id'), on='relationships.sample.data.id')
    df2 = df[columns_list].copy()
    df2 = df2.set_index("study")
    df2 = df2.rename(columns=rename_columns)
    return df2
