from typing import Dict, Sequence
import pandas as pd
from .utils import get_fdr, get_sd_quantile

def get_result_table(target_info_df: pd.DataFrame, param_hist_dict: Dict, guide_index: Sequence=None, suffix_fitted:str = ""):
    """ Return fitted result as table

    Args
        suffix_fitted: suffix the fitted parameters
    """
    try:
        mu = param_hist_dict['quantiles']['mu_alleles'][50].detach()[:,0].numpy()
        mu_sd = get_sd_quantile(param_hist_dict['quantiles']['mu_alleles'].detach())[:,0].numpy()
        sd = param_hist_dict['quantiles']['sd_alleles'][50].detach()[:,0].numpy()
    except:
        mu = param_hist_dict['params']['mu_loc'].detach()[:,0].numpy()
        mu_sd = param_hist_dict['params']['mu_scale'].detach()[:,0].numpy()
        sd = param_hist_dict['params']['sd_loc'].detach().exp()[:,0].numpy()
    mu_z = mu/mu_sd
    fdr_dec, fdr_inc, fdr, p_dec, p_inc, p = get_fdr(mu_z, get_p = True)
    fit_df = pd.DataFrame({
        f"mu{suffix_fitted}": mu,
        f"mu_sd{suffix_fitted}": mu_sd,
        f"mu_z{suffix_fitted}": mu/mu_sd,
        f"sd{suffix_fitted}": sd,
        f"p_dec{suffix_fitted}": p_dec,
        f"p_inc{suffix_fitted}":p_inc,
        f"p{suffix_fitted}":p,
        f"fdr_dec{suffix_fitted}": fdr_dec,
        f"fdr_inc{suffix_fitted}":fdr_inc,
        f"fdr{suffix_fitted}":fdr
        }
    )
    if "negctrl" in param_hist_dict.keys():
        print("Normalizing with common negative control distribution")
        mu0 = param_hist_dict['negctrl']['mu_loc']
        sd0 = param_hist_dict['negctrl']['sd_loc']
        print(f"Fitted mu0={mu0:3f}, sd0={sd0:3f}.")
        fit_df[f'mu_adj{suffix_fitted}'] = (mu - mu0)/sd0
        fit_df[f'mu_sd_adj{suffix_fitted}'] = mu_sd / sd0
        fit_df[f'sd_adj{suffix_fitted}'] = sd / sd0
    fit_df = pd.concat([target_info_df, fit_df], axis=1)

    if not "alpha_pi" in param_hist_dict['params'].keys():
        print("Model didn't have fitted editing rate. Not writing the sgRNA result file.")
        sgRNA_df = None
    else:
        a_fitted = param_hist_dict['params']['alpha_pi'].detach().numpy()
        pi = a_fitted[:,0]/a_fitted.sum(axis=1)
        sgRNA_df = pd.DataFrame({f"edit_eff{suffix_fitted}":pi}, index=guide_index)
    return(fit_df, sgRNA_df)

def write_result_table(target_info_df, param_hist_dict, prefix="", guide_index=None, suffix_fitted = ""):
    """ Write fitted result as table

    Args
        suffix_fitted: suffix the fitted parameters in the resulting table
    """
    fit_df, sgRNA_df = get_result_table(target_info_df, param_hist_dict, prefix=prefix, guide_index=guide_index, suffix_fitted=suffix_fitted)
    fit_df.to_csv(f"{prefix}_variant_result.csv")
    if sgRNA_df: sgRNA_df.to_csv(f"{prefix}_CRISPRbean_sgRNA_result.csv")
    else:
        print("No sgRNA info fitted.")
