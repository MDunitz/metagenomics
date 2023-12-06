import math
import numpy as np
from skbio.diversity import alpha_diversity, beta_diversity

def calculate_simpsons_index(sample_count_df):
    total_population = sample_count_df['Count'].sum()
    sample_count_df['proportion'] = sample_count_df['Count'] / total_population
    sample_count_df['sub_shannon'] = sample_count_df['proportion']*(1-sample_count_df['proportion'])
    simpsons_index = sample_count_df['sub_shannon'].sum()
    return simpsons_index


def calculate_shannon_index(sample_count_df):
    total_population = sample_count_df['Count'].sum()
    sample_count_df['proportion'] = sample_count_df['Count'] / total_population
    sample_count_df['log_prop'] = sample_count_df.apply(lambda row: math.log(row['proportion']), axis=1)
    sample_count_df['sub_shannon'] = sample_count_df['proportion'] * sample_count_df['log_prop']
    shannon_index = sample_count_df['sub_shannon'].sum()*-1
    return shannon_index

def calculate_alpha_diversity(count_df):
    sample_by_otu_df = count_df.pivot_table(columns=["OTU_ID"], index=["Sample_id"], values=["Count"], fill_value=0)
    sample_list = sample_by_otu_df.reset_index()['Sample_id']
    matrix_data = sample_by_otu_df.values
    adiv_obs_otus = alpha_diversity('observed_otus', matrix_data, sample_list)
    return adiv_obs_otus


def calculate_bray_curtis_beta_diversity(count_df):
    sample_by_otu_df = count_df.pivot_table(columns=["OTU_ID"], index=["Sample_id"], values=["Count"], fill_value=0)
    sample_list = sample_by_otu_df.reset_index()['Sample_id']
    matrix_data = sample_by_otu_df.values
    bc_dm = beta_diversity('braycurtis', matrix_data, sample_list)
    return bc_dm


def calculate_bray_curtis_beta_diversity_ordered(count_df, sample_ids_0, sample_ids_1):
    sample_by_otu_df = count_df.pivot_table(columns=["OTU_ID"], index=["Sample_id"], values=["Count"], fill_value=0)
    sample_list = np.concatenate([sample_ids_0, sample_ids_1])
    matrix_data = sample_by_otu_df.values
    bc_dm = beta_diversity('braycurtis', matrix_data, sample_list)
    return bc_dm