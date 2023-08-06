from typing import Sequence, Union, Optional, Dict
import numpy as np
import torch
import pandas as pd
from scipy.stats import norm
from statsmodels.stats.multitest import fdrcorrection

def get_sd_quantile(quantiles):
    # 16-84% quantile is 2 sigma.
    return (quantiles[83]-quantiles[15])/2

def get_fdr(mu_z: Union[np.ndarray, torch.Tensor], plot: bool=False, get_p = False):
    """Return B-H corrected p-values of normal distribution based on z-score
    
    Args
        mu_z: Tensor of z-scores
        plot: If True, print gnu histogram plot
    """
    if isinstance(mu_z, torch.Tensor): mu_z = mu_z.detach().numpy()
    p_dec = norm.cdf(mu_z)
    p_inc = 1-norm.cdf(mu_z)
    # if plot:
    #     gp.plot(p_dec, dict(histogram = 'freq'))
    #     gp.plot(p_inc, dict(histogram = 'freq'))
    _, fdr_dec = fdrcorrection(p_dec)
    _, fdr_inc = fdrcorrection(p_inc)
    fdr = np.minimum(fdr_dec, fdr_inc)
    if not get_p:
        return(fdr_dec, fdr_inc, fdr)
    else:
        return(fdr_dec, fdr_inc, fdr, p_dec, p_inc, np.minimum(p_dec, p_inc))

def write_result_table(
    target_info_df: pd.DataFrame, 
    param_hist_dict: Dict[str,Union[Dict,torch.Tensor]], 
    prefix: str="", 
    write_fitted_eff: Optional[bool] = True, 
    guide_index: Optional[Sequence]=None, 
    guide_acc: Optional[Sequence[float]] = None, 
    return_result: Optional[bool]=False,
    ) -> Union[None, pd.DataFrame]:
    """Write fitted result into text files.
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
    fdr_dec, fdr_inc, fdr = get_fdr(mu_z)
    fit_df = pd.DataFrame({
        "mu": mu,
        "mu_sd": mu_sd,
        "mu_z": mu/mu_sd,
        "sd": sd,
        "fdr_dec": fdr_dec,
        "fdr_inc":fdr_inc,
        "fdr":fdr
        }
    )
    if "negctrl" in param_hist_dict.keys():
        print("Normalizing with common negative control distribution")
        try:
            mu0 = param_hist_dict['negctrl']['params']['mu_loc'].detach().numpy()
            sd0 = param_hist_dict['negctrl']['params']['sd_loc'].detach().numpy()
        except KeyError:
            print(param_hist_dict['negctrl']['params'].keys())
        print(f"Fitted mu0={mu0}, sd0={sd0}.")
        fit_df['mu_adj'] = (mu - mu0)/sd0
        fit_df['mu_sd_adj'] = mu_sd / sd0
        fit_df['mu_z_adj'] = fit_df.mu_adj / fit_df.mu_sd_adj
        fit_df['sd_adj'] = sd / sd0
        fdr_dec, fdr_inc, fdr = get_fdr(fit_df.mu_z_adj)
        fit_df['fdr_dec_adj'], fit_df['fdr_inc_adj'], fit_df['fdr_adj'] = fdr_dec, fdr_inc, fdr
    fit_df = pd.concat([target_info_df, fit_df], axis=1)
    if return_result: return(fit_df)
    fit_df.to_csv(f"{prefix}CRISPRbean_element_result.csv")

    if write_fitted_eff or not guide_acc is None:
        if not "alpha_pi" in param_hist_dict['params'].keys():
            pi=1.0
        else:
            a_fitted = param_hist_dict['params']['alpha_pi'].detach().numpy()
            pi = a_fitted[...,0]/a_fitted.sum(axis=1)
        try:
            sgRNA_df = pd.DataFrame({"edit_eff":pi}, index=guide_index)
        except ValueError:
            print(pi.shape)
        if not guide_acc is None:
            sgRNA_df['accessibility'] = guide_acc
        sgRNA_df.to_csv(f"{prefix}CRISPRbean_sgRNA_result.csv")
