
ANALYSIS_SUMMARY_COL_NAMES = ['Submitted nucleotide sequences',
 'Nucleotide sequences after format-specific filtering',
 'Nucleotide sequences after length filtering',
 'Nucleotide sequences after undetermined bases filtering',
 'Reads with predicted CDS',
 'Reads with predicted RNA',
 'Reads with InterProScan match',
 'Predicted CDS',
 'Predicted CDS with InterProScan match',
 'Total InterProScan matches']
 
CLASSIFICATION_MAP ={"sk": "Domain",
 "k": "Kingdom",
 "p": "Phylum",
 "c": "Class",
 "o": "Order",
 "f": "Family",
 "g": "Genus",
 "s": "Species"
 }

SAMPLE_CLASSIFICATION_DICT = {
    'Domain': None,
    'Kingdom': None,
    'Phylum': None,
    'Class': None,
    'Order': None,
    'Family': None,
    'Genus': None,
    'Species': None
 }