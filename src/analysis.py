from skbio.diversity import alpha_diversity, beta_diversity



def calculate_shannon_index():
    pass

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