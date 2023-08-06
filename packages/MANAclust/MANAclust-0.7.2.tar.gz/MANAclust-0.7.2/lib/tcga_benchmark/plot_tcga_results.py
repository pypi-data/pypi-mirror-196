import pandas as pd
import os
import seaborn as sns
from matplotlib import pyplot as plt
import argparse
from mana_clust.common_functions import *
#####################
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-out_dir',
        default = "/home/scott/Documents/mana_clust_cancer/datasets/results/plots/",
        type=str)
    parser.add_argument(
        '-in_csv_list','-i',
        default = ["/home/scott/Documents/mana_clust_cancer/datasets/results/tables/survival_multi_omics.csv","/home/scott/Documents/mana_clust_cancer/datasets/results/tables/clinical_multi_omics.csv"],
        nargs = "+",
        type=int)
    args = parser.parse_args()
    return(args)
#####################

def do_box_swarm(df, temp_name, out_dir):
	plt.clf()
	hex_colors = ["#8DD3C7", "#BEBADA", "#FB8072", "#80B1D3", "#6B8E23", "#FDB462", "#FF1493", "#FCCDE5", "#BC80BD", "#842121"]
	sns.boxplot(x = "method", y= "value", data = df, palette = hex_colors).set_title(temp_name.replace("_"," "))
	sns.swarmplot(x = "method", y= "value", linewidth=1, edgecolor = "white", data = df, palette = hex_colors)
	out_file = os.path.join(out_dir, temp_name+".png")
	print(out_file)
	plt.savefig(out_file, dpi=600, bbox_inches= "tight")
	return()


def process_file(in_file):
	temp_in = read_table(in_file, sep=',')
	temp_name = os.path.splitext(os.path.basename(in_file))[0]
	print(temp_name)
	df = pd.DataFrame(temp_in[1:])
	df.columns = ['method'] + temp_in[0][1:]
	df = df.melt(id_vars = "method")
	print(df.dtypes)
	df["value"] = df["value"]
	df = df.astype({"value":float}) 
	print(df)
	return(df, temp_name)


def plot_tcga_main(in_csv_list, out_dir):
	for in_table_file in in_csv_list:
		temp_df, temp_name = process_file(in_table_file)

		do_box_swarm(temp_df, temp_name, out_dir)


if __name__ == "__main__":
	args = parse_args()
	plot_tcga_main(args.in_csv_list, args.out_dir)