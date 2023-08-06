import glob
import os
from mana_clust.common_functions import *
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from copy import deepcopy


top_dir = "/home/scott/bin/manaclust/lib/HoldOutSig_comparison_with_diffInput/input"
method_dirs = {"All Data":'full', 
               "Clinical":'clin', 
               "All Numeric":'all_num', 
               "Transcriptome":'trans', 
               "Methylome":'meth', 
               "Microbiome":'micro'}


def get_full_results_file(in_dir):
	end_str = 'global_statistical_differences.tsv'
	for temp_file in glob.glob(in_dir+"/*"):
		if temp_file[-len(end_str):] == end_str:
			return(temp_file)
	return


def get_group_results(in_dir):
	temp_file = get_full_results_file(in_dir)
	## process the file
	temp_table = read_table(temp_file)
	temp_res = pd.DataFrame(temp_table[1:])
	temp_res.columns = temp_table[0]
	return(temp_res)


def get_consensus_group_results(in_dir):
	all_consensus = []
	looking_in = os.path.join(in_dir,"test_ome_differences_by_consensus_groups/SurveyDataNonClustering/*")
	for temp_dir in glob.glob(looking_in):
		all_consensus.append( get_group_results(temp_dir) )
	return(all_consensus)


def get_full_result(in_dir):
	fc_results = get_group_results(in_dir)
	all_results = [fc_results]
	consensus_results = get_consensus_group_results(in_dir)
	all_results += consensus_results
	return(all_results)

def get_max_sig(all_results):
	max_sig = np.zeros(all_results[0].shape[0])
	for res in all_results:
		temp_compare = np.array([max_sig, -np.log10(np.array(res.iloc[:,-1]))])
		#print(temp_compare)
		max_sig = np.max(temp_compare,axis = 0)
	return(max_sig)


all_results_dict = {}
for method in method_dirs.keys():
	print("\n\n",method,"\n")
	temp_dir = os.path.join(top_dir, method_dirs[method]+"/")
	print(temp_dir)
	method_full_results = get_full_result(temp_dir)
	method_max_sig = get_max_sig(method_full_results)
	all_results_dict[method] = method_max_sig


summary_df = pd.DataFrame(all_results_dict)
summary_df_norm = deepcopy(summary_df)
for i in range(summary_df_norm.shape[0]):
	summary_df_norm.iloc[i,:] = summary_df_norm.iloc[i,:] - np.min(summary_df_norm.iloc[i,:])




fig = plt.figure(figsize = (12,4))
sns.set(font_scale=1.5)
sns.boxplot(x="variable", y='value', data = summary_df_norm.melt())
plt.ylabel("Normalized max -log10(p-value)")
plt.savefig(os.path.join(top_dir,'norm_max_neg_log_p.png'), 
	        height = 4,
	        width = 20,
	        dpi = 600,
	        units = 'in',
	        bbox_inches='tight')

################

plt.clf()

fig = plt.figure(figsize = (12,4))
sns.set(font_scale=1.5)
sns.boxplot(x="variable", y='value', data = summary_df.melt())
plt.ylabel("max -log10(p-value)")
plt.savefig(os.path.join(top_dir,'max_neg_log_p.png'), 
	        height = 4,
	        width = 20,
	        dpi = 600,
	        units = 'in',
	        bbox_inches='tight')



