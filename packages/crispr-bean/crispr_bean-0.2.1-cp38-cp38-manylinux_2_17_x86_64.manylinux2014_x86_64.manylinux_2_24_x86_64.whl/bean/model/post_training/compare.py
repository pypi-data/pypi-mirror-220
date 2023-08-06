import pickle as pkl
import pandas as pd
import beret as be
from .post_training import get_result_table

def get_target_info(path):
    sim = be.read_h5ad(path)
    guide_info = sim.guides.copy()
    edit_rate_info = guide_info[['target', "effect_size", 'edit_rate', 'coverage']].groupby(
            'target', sort=False).agg({"edit_rate":["mean", "std"], 'coverage':'mean'})
    edit_rate_info.columns = ["edit_rate_mean", "edit_rate_std", "coverage_mean"]
    target_info = guide_info[['target', "effect_size"]].drop_duplicates().set_index("target", drop=True)
    target_info = target_info.join(edit_rate_info).reset_index()
    return(guide_info, target_info)

def get_multiple_result_table(adata_path, prefix, model_ids, path_pattern_string = "{}.model{}.result.pkl"):
    guide_info, target_info = get_target_info(adata_path)

    model_res = {}

    for model_id in model_ids:
        f = open(path_pattern_string.format(prefix, model_id), "rb")
        model_res[model_id] = pkl.load(f)
        f.close()

    var_dfs = {}
    sgrna_dfs = {}
    for model_id, d in model_res.items():
        res = get_result_table(target_info, d, guide_info.index, f"_{model_id}")
        var_dfs[model_id], sgrna_dfs[model_id] = res

    df = pd.concat(var_dfs.values(), axis=1)
    res_df = df.loc[:,~df.columns.duplicated()].copy()
    return res_df

def read_mageck_result(prefix, models = ['topbot', 'topbot_var', 'sort', 'sort_var'], suffix=""):
    tbls = []
    for model in models:
        df = pd.read_csv("{}/{}.gene_summary.txt".format(prefix, model), sep = "\t")
        df.columns = [s.split("|")[-1] for s in df.columns]
        df = df.add_suffix(f"_{model}{suffix}")
        tbls.append(df)
    return(pd.concat(tbls, axis=1))
    