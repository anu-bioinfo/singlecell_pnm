
import modish
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import flotilla
import os
import sys

sns.set(style='ticks', context='paper', rc={'font.sans-serif':'Arial', 'pdf.fonttype': 42})

# Ensure the iteration is always at least 1
iteration = max(int(sys.argv[1]), 1)
iteration_str = str(iteration).zfill(4)
base_folder = '/home/obotvinnik/Dropbox/figures2/singlecell_pnm/figure2_modalities/bayesian/permutations'

seed = (sum(ord(c) for c in 'randomly_permute_modalities')/i) % 5437
np.random.seed(seed)

study = flotilla.embark('singlecell_pnm_figure1_supplementary_post_splicing_filtering')

not_outliers = study.splicing.singles.index.difference(study.splicing.outliers.index)

print splicing_singles_no_outliers.shape
splicing_singles_no_outliers = splicing_singles_no_outliers.groupby(
    study.sample_id_to_phenotype).apply(lambda x: x.dropna(thresh=20, axis=1))
print splicing_singles_no_outliers.shape

permuted_psi = splicing_singles_no_outliers.groupby(study.sample_id_to_phenotype).apply(
    lambda x: pd.DataFrame(np.random.permutation(x), index=x.index, columns=x.columns))


bayesian = anchor.BayesianModalities()
modality_assignments = permuted_psi.groupby(study.sample_id_to_phenotype).apply(bayesian.fit_predict)

modality_assignments[splicing_singles_no_outliers.groupby(study.sample_id_to_phenotype).count() < 20] = np.nan
modalities_tidy = modality_assignments.stack().reset_index()
modalities_tidy = modalities_tidy.rename(columns={'level_1': 'event_name', 0: "modality",})
modalities_tidy.to_csv('{}/modalities_tidy/{}.csv'.format(base_folder, iteration_str), index=False)

sizes = modalities_tidy.groupby(['phenotype', 'modality']).size()
sizes.to_csv('{}/modalities_size/{}.csv'.format(base_folder, iteration_str))


g = anchor.barplot(modalities_tidy, x='phenotype', hue='modality', size=2)
g.savefig('{}/barplots/iteration_{}.pdf'.format(folder, iteration_str)