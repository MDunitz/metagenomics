def qc_nucleotide_sequences(row):
    final_count = int(row['Nucleotide sequences after format-specific filtering'])
    submitted_count = int(row['Submitted nucleotide sequences'])
    if final_count/submitted_count > 0.5:
        return True
    else:
        return False