#! /usr/local/env python3
import os
import argparse
import random
################################
from scipy.stats import f_oneway as aov
################################
from kmodes.kmodes import KModes
import numpy as np
import pandas as pd
from copy import deepcopy
from scipy.spatial import distance
from matplotlib import pyplot as plt
import seaborn as sns
from mana_clust.simulate_datasets import get_cat_dataset, make_all_datasets
from mana_clust.run_simulation_study import get_purity, mutual_info_score, get_contingency_table_stats, get_group_from_clust_ome
from mana_clust.mana_clust import cluster_omes, write_ome_results, plot_ome_results
from mana_clust.common_functions import read_table, write_table, process_dir
###############################################################
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-out_dir',
        default = "/home/scott/bin/manaclust/lib/synthetic_data_categorical/",
        type=str)
    parser.add_argument(
        '-iters','-iterations',
        default = 5,
        type=int)
    parser.add_argument(
        '-num_cat_groups',
        default = [5,10,15,20],
        nargs = "+",
        type=int)
    parser.add_argument(
        '-num_cat_datasets','-cat_dat',
        default = 1,
        type=int)
    parser.add_argument(
        '-cat_missing','-cat_missing',
        default = 0.,#.50,
        type=float)
    parser.add_argument(
        '-cat_noise',
        default = .3,
        type=float)
    parser.add_argument(
        '-num_cat_rand_feat',
        default = 100,
        type=int)
    parser.add_argument(
        '-num_cat_real_feat',
        default = 50,
        type=int)
    parser.add_argument(
        '-samples','-s',
        default = 1000,
        type=int)
    parser.add_argument(
        '-seed',
        default = 123456,
        type=int)
    args = parser.parse_args()
    return(args)
#####################

def get_individual_result_stats(ground_truth, labels, out_dir, name):
    out_dir = process_dir(out_dir)
    ## get contingency table
    full_cont, full_row, full_col = get_contingency_table_stats(ground_truth, labels, out_dir+"contingency_table_"+str(name)+".png")
    ## get the mutual information
    full_mi = mutual_info_score(None, None, contingency = full_cont)
    ## get the ground truth maximum possible mi for normalizing the observed mi
    gt_cont, gt_row, gt_col = get_contingency_table_stats(ground_truth, ground_truth, out_dir+"gound_truth_contingency_table_"+str(name)+".png")
    full_mi = full_mi/mutual_info_score(None, None, contingency = gt_cont)
    ## get the purity
    full_purity = get_purity(full_cont)
    guessed_k = len(set(labels))
    return(full_mi, full_purity, guessed_k)


def get_elbow(values, is_max=True):
    second_derivatives = []
    for i in range(2,len(values) - 1):
        second_derivatives += [values[i + 1] + values[i - 1] - 2 * values[i]]
    print(second_derivatives)
    # sns.lineplot(np.arange(len(values)),values)
    # sns.lineplot(2+np.arange(len(second_derivatives)),second_derivatives)
    # plt.show()
    if is_max:
        return(np.argmax(second_derivatives))
    else:
        return(np.argmin(second_derivatives))


def get_pairwise_average_ham(data):
    out_dist = np.zeros((data.shape[0],data.shape[0]))
    ## have to make this nan compatible
    for i in range(data.shape[0]):
        ## goes through the rows (subjects in this case)
        i_is_nan = np.isnan(data[i,:])
        for j in range(i,data.shape[0]):
            if j!=i:
                j_is_nan = np.isnan(data[j,:])
                either_is_nan = np.array(i_is_nan * j_is_nan,dtype=bool)
                neither_is_nan_idxs = np.where(either_is_nan == False)[0]
                ## hamming distance divided by the number of non nan features that go into the comparison
                temp_dist = abs(distance.hamming(data[i,neither_is_nan_idxs], data[j,neither_is_nan_idxs])/np.shape(neither_is_nan_idxs)[0])
                out_dist[i,j] = temp_dist
                out_dist[j,i] = temp_dist
    return(out_dist)


def get_single_hamming_dist(data, clust_vect):
    temp_ham = 0
    all_clusts = list(set(clust_vect.tolist()))
    for clust in all_clusts:
        temp_idxs = np.where(clust_vect == clust)[0]
        pairwise_ham_mat = get_pairwise_average_ham(data[temp_idxs,:])
        temp_ham += np.sum(pairwise_ham_mat)
    return(temp_ham)


def get_hamming_distances(data, clusters):
    ## clusters is a 2d matrix where the rows are the samples
    ## and the columns are the clustering results
    ## returns a vector of the sum of the square within cluster distances
    all_hamms = []
    for i in range(clusters.shape[1]):
        all_hamms.append(get_single_hamming_dist(data, clusters[:,i]))
    print("within group hamming distances")
    print(all_hamms)
    return(all_hamms)


def get_encoding_dict(in_vect, na_str):
    all_entries = list(set(in_vect.tolist()))
    temp_int = 0
    temp_dict = {}
    for entry in all_entries:
        if entry == na_str:
            temp_dict[entry] = np.nan
        else:
            temp_dict[entry] = deepcopy(temp_int)
            temp_int += 1
    return(temp_dict)


def encode_table(in_table, na_str = "NA"):
    in_table = np.array(in_table)[1:,1:]
    ## 
    out_table = np.zeros(in_table.shape)
    for i in range(in_table.shape[1]):
        temp_encoding = get_encoding_dict(in_table[:,i], na_str = na_str)
        for j in range(in_table.shape[0]):
            out_table[j,i] = temp_encoding[in_table[j,i]]
    return(out_table)


def do_kmodes_elbow(in_cat_data, 
                    k_min = 2, 
                    k_max = 22):
    in_cat_raw = read_table(in_cat_data)
    in_cat = encode_table(in_cat_raw)
    print(in_cat)
    num_samples = in_cat.shape[0]
    ## read in the dataset
    cluster_table = np.zeros((num_samples,int(k_max - k_min +1)))
    for k in range(k_min,k_max+1):
        print("\nRunning KModes with K =",k)
        km = KModes(n_clusters=k, init='Huang', n_init=5, verbose=1)
        clusters = km.fit_predict(in_cat)
        #print(clusters)
        cluster_table[:,k-k_min] = clusters
    ham_vect = get_hamming_distances(in_cat, cluster_table)
    print("hamming second derivatives:")
    elbow_k = get_elbow(ham_vect)+k_min+1
    print("elbow K:",elbow_k)
    return(cluster_table[:,elbow_k-k_min])


def get_full_line_output(name,
                         gt_k,
                         guessed_k,
                         mi,
                         purity,
                         iteration):
    temp_line = [name, iteration, gt_k, guessed_k, abs(gt_k-guessed_k), mi, purity]
    return(temp_line)


def do_iter(in_cat_data, temp_outdir, iteration):
    k_modes_clust = do_kmodes_elbow(in_cat_data)
    temp_clustered_ome = cluster_omes([in_cat_data],[], out_dir = temp_outdir)
    temp_results = process_dir(temp_outdir+'/results')
    temp_group_vector = get_group_from_clust_ome(temp_clustered_ome)
    plot_ome_results(temp_clustered_ome, temp_results, temp_group_vector)
    write_ome_results(temp_results, temp_clustered_ome)
    temp_feat_select_mi, temp_feat_select_purity, temp_feat_k = get_individual_result_stats(temp_group_vector, 
                                                                         temp_clustered_ome.labels, 
                                                                         temp_results, 
                                                                         name = "MANAclust")
    temp_k_modes_mi, temp_k_modes_purity, temp_kmodes_k = get_individual_result_stats(temp_group_vector, 
                                                                         k_modes_clust, 
                                                                         temp_results, 
                                                                         name = "KModes_elbow")
    gt_num_groups = len(set(temp_group_vector))
    k_modes_line = get_full_line_output("KModes_elbow", 
                                        gt_num_groups, 
                                        temp_kmodes_k,
                                        temp_k_modes_mi, 
                                        temp_k_modes_purity,
                                        iteration)
    mana_feat_line = get_full_line_output("MANAclust",
                                          gt_num_groups,
                                          temp_feat_k, 
                                          temp_feat_select_mi, 
                                          temp_feat_select_purity,
                                          iteration)
    return([k_modes_line,
            mana_feat_line])


def get_aov_res(df, var_of_interest):
    all_methods = list(set(list(df['method'])))
    aov_in = []
    for temp_method in all_methods:
        aov_in.append(list(df[df['method']==temp_method][var_of_interest]))
        #aov_in.append(df[df['method']==temp_method][var_of_interest])
    print(aov_in)
    f, p = aov(*aov_in)
    return(f, p)


def plot_results(df, out_dir, plot_vars=["guessed_k", "abs_dist_k", "relative_mi", "purity"]):
    temp_out_dir = process_dir(os.path.join(out_dir, "results"))
    for temp_var in plot_vars:
        aov_f, aov_p = get_aov_res(df, temp_var)
        title_str = "F = "+str(aov_f)+"\np = "+str(aov_p)
        print(title_str)
        plt.clf()
        fig, ax = plt.subplots(figsize = ( 5 , 5 ))
        ax.set_title(title_str)
        sns.factorplot(data = df, x = "ground_truth_k", y = temp_var, hue = "method")
        #plt.show()
        out_file = os.path.join(temp_out_dir, temp_var+"_line.png")
        print(out_file)
        #ax.set_title(title_str)
        plt.savefig(out_file, dpi=600, bbox_inches = "tight")
        plt.clf()
        fig, ax = plt.subplots(figsize = ( 3 , 5 ))
        ax.set_title(title_str)
        sns.boxplot(data = df, x = "method", y = temp_var, hue = "method")
        #plt.show()
        out_file = os.path.join(temp_out_dir, temp_var+"_boxplot.png")
        print(out_file)
        plt.savefig(out_file, dpi=600, bbox_inches = "tight")
        plt.clf()
    df.to_csv(os.path.join(temp_out_dir,"categorical_clustering_results.tsv"),sep="\t", index = False)
    return()


def do_categorical_simulation(out_dir,
                              iters=3,
                              num_cat_groups=[20],
                              cat_missing=.5,
                              cat_noise=.5,
                              num_cat_rand_feat=200,
                              num_cat_real_feat=25,
                              samples=1000,
                              seed=123456789):
    np.random.seed(seed)
    random.seed(seed)
    all_results = [["method","iteration","ground_truth_k","guessed_k","abs_dist_k","relative_mi","purity"]]
    for group in num_cat_groups:
        temp_group_out_dir = process_dir(os.path.join(out_dir,str(group)))
        all_datasets, all_group_vectors = make_all_datasets(temp_group_out_dir, 
                                                            iters = iters, 
                                                            num_cat = 1, 
                                                            num_num = 0, 
                                                            samples = samples,
                                                            num_cat_groups = group, 
                                                            num_cat_rand_feat = num_cat_rand_feat,
                                                            num_cat_real_feat = num_cat_real_feat,
                                                            cat_noise = cat_noise,
                                                            cat_percent_missing = cat_missing)
        for i in range(len(all_datasets)):
            ## perform the clustering on the synthetic datset
            print('\n\n\nclustering ome #',i,"\n\n\n")
            temp_outdir = process_dir(os.path.join(temp_group_out_dir, str(i)))
            temp_dataset = all_datasets[i]['cat'][0]
            all_results += do_iter(temp_dataset, temp_outdir, i)
            # ## write the results and plot some stats at the per-ome level
            # write_ome_results(temp_results, temp_clustered_ome)
            # plot_ome_results(temp_clustered_ome, temp_results, temp_group_vector)
            ## get clustering accuracy statistics 
    df = pd.DataFrame(all_results[1:])
    df.columns = all_results[0]
    plot_results(df, out_dir)
    return(df)


#####################
if __name__ == "__main__":
    args = parse_args()
    all_results = do_categorical_simulation(out_dir = args.out_dir,
                                              iters=args.iters,
                                              num_cat_groups=args.num_cat_groups,
                                              cat_missing=args.cat_missing,
                                              cat_noise=args.cat_noise,
                                              num_cat_rand_feat=args.num_cat_rand_feat,
                                              num_cat_real_feat=args.num_cat_real_feat,
                                              samples=args.samples,
                                              seed=args.seed)
