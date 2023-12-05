import os
import pandas as pd
from .constants import CLASSIFICATION_MAP, SAMPLE_CLASSIFICATION_DICT

def read_otu_tsv_file(file_path):
    sample_id = file_path.split("/")[-1].split('_')[0]
    study_id = file_path.split("/")[-2]
    otu_df=pd.read_table(file_path,sep='\t',header=1)
    otu_df.rename(columns={"# OTU ID": "OTU_ID", otu_df.columns[1]: "Count"}, inplace=True)
    otu_df["Taxa Dict"] = otu_df.apply(split_taxonomy_info, axis=1)
    otu_df["Study_id"] = study_id
    otu_df["Sample_id"] = sample_id
    return otu_df

sample_dict = {'Super Kingdom': None,
 'Kingdom': None,
 'Phylum': None,
 'class': None,
 'order': None,
 'family': None,
 'genus': None}

def split_taxonomy_info(row):
    taxonomy = row['taxonomy']
    taxonomy_list = taxonomy.split(';')
    taxonomy_dict = SAMPLE_CLASSIFICATION_DICT.copy()
    for x in taxonomy_list:
        taxa = x.split('__')
        level = taxa[0]
        label = taxa[1]
        if label == "":
            taxonomy_dict[CLASSIFICATION_MAP[level]] = None
        else:
            taxonomy_dict[CLASSIFICATION_MAP[level]] = label

    return taxonomy_dict


def build_otu_lookup_df(df_to_add, otu_df=None):
    if otu_df is None:
        otu_df = pd.DataFrame(columns=["OTU_ID", "Domain", "Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species", "taxonomy"])
    sub_df = df_to_add[['OTU_ID', 'taxonomy', 'Taxa Dict']]
    sub_df[["Domain", "Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"]] = sub_df.apply(split_phyla_dict, axis=1, result_type='expand')
    sub_df.drop(['Taxa Dict'], axis=1, inplace=True)
    df = pd.concat([otu_df, sub_df])
    df.drop_duplicates(inplace=True)
    return df

def split_phyla_dict(row):
    taxa = row['Taxa Dict']
    return [taxa['Domain'], taxa['Kingdom'], taxa['Phylum'], taxa['Class'], taxa['Order'], taxa['Family'], taxa['Genus'], taxa['Species']]


def build_otu_count_df(df_to_add, count_df=None):
    if count_df is None:
        count_df = pd.DataFrame(columns=["OTU_ID", "Count", "Study_id", "Sample_id"])
    sub_df = df_to_add[["OTU_ID", "Count", "Study_id", "Sample_id"]]
    df = pd.concat([count_df, sub_df])
    return df

def build_otu_count_df_and_lookup_df(directory):
    file_list = os.listdir(directory)
    count_df = pd.DataFrame(columns=["OTU_ID", "Count", "Study_id", "Sample_id"])
    otu_df = pd.DataFrame(columns=["OTU_ID", "Domain", "Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species", "taxonomy"])
    for f in file_list:
        df = read_otu_tsv_file(os.path.join(directory, f))
        count_df = build_otu_count_df(df, count_df)
        otu_df = build_otu_lookup_df(df, otu_df)
    return otu_df, count_df