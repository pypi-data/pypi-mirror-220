import numpy as np

from gwbench.utils import log_msg

def ana_derivs(key, hf, f, params_dic):
    if   key == 'DL':   return -hf / params_dic['DL']
    elif key == 'tc':   return (1j * 2 * np.pi) * f * hf
    elif key == 'phic': return -1j * hf
    else: log_msg(f'ana_derivs: - No analytical derivative known for the provided key={key}.', logger=None, level='ERROR')
