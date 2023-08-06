# Copyright (C) 2020  Ssohrab Borhanian
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


"""This module handles the benchmarking of graviational waveforms observed by a network of detectors.

"""

import logging
import sys
from copy import copy, deepcopy

import dill
import numpy as np

import gwbench.antenna_pattern_np as ant_pat_np
import gwbench.detector as dc
import gwbench.detector_response_derivatives as drd
import gwbench.err_deriv_handling as edh
import gwbench.fisher_analysis_tools as fat
import gwbench.waveform as wfc
import gwbench.utils as utils

# logger
glob_logger = logging.getLogger('network_module')
glob_logger.setLevel('INFO')

class Network:

    ###
    #-----Init methods-----
    def __init__(self, network_spec=None, logger_name='Network', logger_level='INFO'):
        ##-----logger-----
        self.set_logger(name=logger_name, level=logger_level)

        ##-----initialize network object-----
        if network_spec is None:
            #-----network and detectors
            # network label
            self.label = None
            # detector labels list
            self.det_keys = None
            # list of detectors in network
            self.detectors = None

        elif isinstance(network_spec, str):
            #-----network and detectors
            self.set_network_and_detectors_from_label(network_spec)
        elif isinstance(network_spec, list) or isinstance(network_spec, tuple):
            #-----network and detectors
            self.set_network_and_detectors_from_key_list(network_spec)

        #-----injection and waveform quantities-----
        # frequency array
        self.f = None
        # dictionary of injection parameters
        self.inj_params = None
        # derivative variables - symbs_string and list
        self.deriv_symbs_string = None
        self.deriv_variables = None
        # derivative variables for which analytical derivatives should be used
        self.ana_deriv_symbs_list = None
        # waveform
        self.wf = None

        #-----analysis settings-----
        # list of inj_params to convert to cos, ln versions
        self.conv_cos = None
        self.conv_log = None
        # use f-dependent gmst (SPA) in antenna patterns
        self.use_rot = None

        #-----user defined detector locations and PSDs-----
        self.user_locs = None
        self.user_psds = None
        self.user_lambdified_functions_path = None

        #-----waveform polarizations-----
        # plus/cross polarizations
        self.hfp = None
        self.hfc = None
        # derivative dictionary for polarizations
        self.del_hfpc = None
        # sympy expressions of derivative dictionary for polarizations
        self.del_hfpc_expr = None

        #-----network SNR-----
        # SNR, SNR^2 calculated from hf
        self.snr = None
        self.snr_sq = None

        #-----network errors-----
        # Fisher matrix
        self.fisher = None
        # condition number of Fisher matrix
        self.cond_num = None
        # covariance matrix
        self.cov = None
        # dictionary containing information about the inversion error between the two matrices
        self.inv_err = None
        # dictionary of errors for given derivative variables
        self.errs = None

        if self.label is None: self.logger.debug('Empty network initialized.')
        else:                  self.logger.debug('Network initialized.')


    ###
    #-----Setter methods-----
    #
    # it is best practice to always change the instance variables using these setter methods
    #
    def set_logger(self, name='Network', level='INFO', stdout=True, logfile=None):
        logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s : %(message)s')
        if stdout: logging.basicConfig(stream = sys.stdout)
        if logfile is not None: logging.basicConfig(filename = logfile, filemode = 'w')
        self.logger = logging.getLogger(name)
        self.set_logger_level(level)

    def set_logger_level(self, level):
        self.logger.setLevel(level)

    def set_network_and_detectors_from_label(self, network_label):
        #-----network and detectors
        self.label = network_label
        self.det_keys = utils.read_det_keys_from_label(network_label)
        self.detectors = []
        for det_key in self.det_keys:
            self.detectors.append(dc.Detector(det_key))

    def set_network_and_detectors_from_key_list(self, det_key_list):
        if isinstance(det_key_list, tuple):
            tmp_list = []
            for tec,loc in zip(det_key_list[0],det_key_list[1]):
                tmp_list.append(tec + '_' + loc)
            det_key_list = tmp_list

        #-----network and detectors
        self.label = '..'.join(det_key_list)
        self.det_keys = det_key_list
        self.detectors = []
        for det_key in self.det_keys:
            self.detectors.append(dc.Detector(det_key))

    def set_wf_vars(self, wf_model_name, wf_other_var_dic=None, user_waveform=None, cosmo=None):
        self.wf = wfc.Waveform(wf_model_name, wf_other_var_dic=wf_other_var_dic, user_waveform=user_waveform, cosmo=cosmo, logger=self.logger)

    def set_net_vars(self, f=None, inj_params=None, deriv_symbs_string=None, conv_cos=None, conv_log=None,
                     use_rot=None, user_locs=None, user_psds=None, user_lambdified_functions_path=None, ana_deriv_symbs_list=None):
        if f is not None:
            self.f = copy(f)
            if self.detectors is not None:
                for det in self.detectors:
                    det.set_f(self.f)
        if inj_params is not None:
            self.inj_params = deepcopy(inj_params)
        if deriv_symbs_string is not None:
            self.deriv_symbs_string = copy(deriv_symbs_string)
            self.deriv_variables = deriv_symbs_string.split(' ')
        if ana_deriv_symbs_list is not None:
            self.ana_deriv_symbs_list = copy(ana_deriv_symbs_list)
        if conv_cos is not None:
            self.conv_cos = copy(conv_cos)
        if conv_log is not None:
            self.conv_log = copy(conv_log)
        if use_rot is not None:
            self.use_rot = copy(use_rot)
        if user_locs is not None:
            self.user_locs = deepcopy(user_locs)
        if user_psds is not None:
            self.user_psds = deepcopy(user_psds)
        if user_lambdified_functions_path is not None:
            self.user_lambdified_functions_path = deepcopy(user_lambdified_functions_path)

    ##
    #-----Resetter methods for instance variables-----
    def reset_ant_pat_lpf_psds(self):
        for det in self.detectors:
            det.Fp = None
            det.Fc = None
            det.Flp = None
            det.psd = None

    def reset_wf_polarizations(self):
        self.hfp = None
        self.hfc = None
        self.del_hfpc = None
        self.del_hfpc_expr = None

    def reset_det_responses(self):
        for det in self.detectors:
            det.hf = None
            det.del_hf = None
            det.del_hf_expr = None

    def reset_snrs(self):
        self.snr = None
        self.snr_sq = None
        for det in self.detectors:
            det.snr = None
            det.snr_sq = None
            det.d_snr_sq = None

    def reset_errors(self):
        self.fisher = None
        self.cond_num = None
        self.cov = None
        self.inv_err = None
        self.errs = None
        for det in self.detectors:
            det.fisher = None
            det.cond_num = None
            det.cov = None
            det.inv_err = None
            det.errs = None


    ###
    #-----Getters-----
    def get_detector(self,det_key):
        return self.detectors[self.det_keys.index(det_key)]

    def get_snrs_errs_cov_fisher_inv_err_for_key(self,key='network'):
        if key == 'network': out_obj = self
        else:                out_obj = self.detectors[self.det_keys.index(key)]
        return out_obj.snr, out_obj.errs, out_obj.cov, out_obj.fisher, out_obj.inv_err


    ###
    #-----PSDs and antenna patterns-----
    def setup_ant_pat_lpf_psds(self, F_lo=-np.inf, F_hi=np.inf):
        self.setup_psds(F_lo, F_hi)
        self.setup_ant_pat_lpf()

    def setup_psds(self, F_lo=-np.inf, F_hi=np.inf):
        for det in self.detectors:
            det.setup_psds(F_lo, F_hi, user_psds=self.user_psds)
        self.logger.info('PSDs loaded.')

    def setup_ant_pat_lpf(self):
        for det in self.detectors:
            det.setup_ant_pat_lpf(self.inj_params, self.use_rot, user_locs=self.user_locs)
        self.logger.info('Antenna patterns and LPFs loaded.')


    ###
    #-----Waveform polarizations-----
    def calc_wf_polarizations(self):
        self.hfp, self.hfc = self.wf.eval_np_func(self.f,utils.get_sub_dict(self.inj_params,self.wf.wf_symbs_string))
        self.logger.info('Polarizations calculated.')

    def calc_wf_polarizations_derivs_num(self, step=1e-9, method='central', order=2, n=1):
        self.logger.info('Calculate numeric derivatives of polarizations.')
        self.calc_wf_polarizations()
        wf_deriv_symbs_string = utils.remove_symbols(self.deriv_symbs_string,self.wf.wf_symbs_string)
        self.del_hfpc = drd.calc_det_responses_derivs_num(None, self.wf, wf_deriv_symbs_string, self.f, self.inj_params, use_rot=self.use_rot, label='hf',
                                               step=step, method=method, order=order, n=n, user_locs=self.user_locs,
                                               ana_deriv_symbs_list=self.ana_deriv_symbs_list)
        self.del_hfpc, c_quants = edh.get_conv_del_eval_dic(self.del_hfpc, self.inj_params, self.conv_cos, self.conv_log, self.deriv_symbs_string)
        self.inj_params, self.deriv_variables = edh.get_conv_inj_params_deriv_variables(c_quants, self.inj_params, self.deriv_variables)
        self.logger.info('Numeric derivatives of polarizations calculated.')

    def load_wf_polarizations_derivs_sym(self, return_bin=0):
        wf_deriv_symbs_string = utils.remove_symbols(self.deriv_symbs_string,self.wf.wf_symbs_string)
        self.del_hfpc_expr = drd.load_det_responses_derivs_sym('pl_cr', self.wf.wf_model_name, wf_deriv_symbs_string, return_bin, self.user_lambdified_functions_path)
        self.logger.info('Lambdified polarizations loaded.')

    def calc_wf_polarizations_derivs_sym(self):
        self.logger.info('Evaluate polarizations.')
        self.calc_wf_polarizations()
        self.del_hfpc = {}
        for deriv in self.del_hfpc_expr:
            if deriv in ('variables','deriv_variables'): continue
            self.del_hfpc[deriv] = self.del_hfpc_expr[deriv](self.f, **utils.get_sub_dict(self.inj_params, self.del_hfpc_expr['variables']))
        self.del_hfpc, c_quants = edh.get_conv_del_eval_dic(self.del_hfpc, self.inj_params, self.conv_cos, self.conv_log, self.deriv_symbs_string)
        self.inj_params, self.deriv_variables = edh.get_conv_inj_params_deriv_variables(c_quants, self.inj_params, self.deriv_variables)
        self.logger.info('Lambdified polarizations evaluated.')


    ###
    #-----Detector responses-----
    def calc_det_responses(self):
        for det in self.detectors:
            det.calc_det_responses(self.wf,self.inj_params)
        self.logger.info('Detector responses calculated.')

    def calc_det_responses_derivs_num(self, step=1e-9, method='central', order=2, n=1):
        self.logger.info('Calculate numeric derivatives of detector responses.')
        for det in self.detectors:
            self.logger.info(f'   {det.det_key}')
            det.calc_det_responses_derivs_num(self.inj_params, self.deriv_variables, self.wf, self.deriv_symbs_string, self.conv_cos, self.conv_log, self.use_rot, step, method, order, n, self.user_locs, self.ana_deriv_symbs_list)
        self.logger.info('Numeric derivatives of detector responses calculated.')

    def load_det_responses_derivs_sym(self, return_bin=0):
        for det in self.detectors:
            det.load_det_responses_derivs_sym(self.wf.wf_model_name, self.deriv_symbs_string, return_bin, self.user_lambdified_functions_path)
        self.logger.info('Lambdified detector responses loaded.')

    def calc_det_responses_derivs_sym(self):
        self.logger.info('Evaluate lambdified detector responses.')
        for det in self.detectors:
            self.logger.info(f'   {det.det_key}')
            det.calc_det_responses_derivs_sym(self.wf, self.inj_params, self.deriv_variables, self.conv_cos, self.conv_log, self.deriv_symbs_string)
        self.logger.info('Lambdified detector responses evaluated.')


    ###
    #-----SNR calculations-----
    def calc_snrs(self, only_net=0):
        self.snr_sq = 0
        for det in self.detectors:
             self.snr_sq += det.calc_snrs(only_net)
        self.snr = np.sqrt(self.snr_sq)
        self.logger.info('SNRs calculated.')

    def calc_snr_sq_integrand(self):
        for det in self.detectors:
            det.calc_snr_sq_integrand()
        self.logger.info('SNR integrands calculated.')


    ###
    #-----Error calculation and Fisher analysis-----
    def calc_errors(self, cond_sup=None, only_net=0):
        self.logger.info('Calculate errors (Fisher & cov matrices).')
        #-----calculate the error matrices: Fisher and Cov-----
        self.fisher = 0
        for det in self.detectors:
            self.logger.info(f'   {det.det_key}')
            self.fisher += det.calc_fisher_cov_matrices(only_net, cond_sup, logger=self.logger)
        self.cond_num = fat.calc_cond_number(self.fisher, logger=self.logger, tag='network')
        self.cov, self.inv_err = fat.calc_cov_inv_err(self.fisher, self.cond_num, cond_sup=cond_sup, logger=self.logger, tag='network')
        #-----calculate the absolute errors of the various variables-----
        self.errs = fat.get_errs_from_cov(self.cov,self.deriv_variables)
        if not only_net:
            for det in self.detectors:
                det.calc_errs(self.deriv_variables)
        self.logger.info('Errors calculated.')

    def calc_sky_area_90(self, only_net=0):
        if self.cov is None or self.errs is None:
            self.logger.warning("calc_sky_area_90: tag = network - Nothing done since either 'cov' or 'errs' are None.")
            return
        if 'ra' in self.deriv_variables and ('cos_dec' in self.deriv_variables or 'dec' in self.deriv_variables):
            if 'cos_dec' in self.deriv_variables: dec_str = 'cos_dec'
            else:                                 dec_str = 'dec'
            ra_id      = self.deriv_variables.index('ra')
            dec_id     = self.deriv_variables.index(dec_str)
            is_cos_dec = (dec_str == 'cos_dec')
            self.errs['sky_area_90'] = edh.sky_area_90(self.errs['ra'],self.errs[dec_str],self.cov[ra_id,dec_id],self.inj_params['dec'],is_cos_dec)
            if not only_net:
                for det in self.detectors:
                    det.calc_sky_area_90_network(ra_id, dec_id, self.inj_params['dec'], is_cos_dec, dec_str)
            self.logger.info('Sky areas calculated.')
        else:
            self.logger.warning('calc_sky_area_90: tag = network - Nothing done due to missing of either RA or COS_DEC (DEC) errors.')


    ###
    #-----IO methods-----
    def save_network(self,filename_path):
        '''Save the network under the given path using *dill*.'''
        with open(filename_path, "wb") as fi:
            dill.dump(self, fi, recurse=True)
        self.logger.info('Network pickled.')
        return

    def load_network(self,filename_path):
        '''Loading the network from the given path using *dill*.'''
        with open(filename_path, "rb") as fi:
            self = dill.load(fi)
        self.logger.info('Network loaded.')
        return network

    def print_network(self):
        sepl='--------------------------------------------------------------------------------------'
        print()
        print(sepl)
        print('Printing network.')
        print(sepl)
        print()
        for key,value in vars(self).items():
            if type(value) == dict:
                print('Key: ',key)
                for kkey in value.keys():
                    print('',kkey)
                    print('',value[kkey])
                print()
            elif value is not None:
                if key == 'wf':
                    print('Key: ',key)
                    for kkey,vvalue in vars(value).items():
                        print('',kkey.ljust(16,' '),'  ',vvalue)
                    print()
                else:
                    print('Key: ',key)
                    print(value)
                    print()
        print(sepl)
        print('Printing network done.')
        print(sepl)
        print()

    def print_detectors(self):
        sepl='--------------------------------------------------------------------------------------'
        sepl1='-------------------------------------------'
        print()
        print(sepl)
        print('Printing detectors.')
        print(sepl)
        for det in self.detectors:
            print(sepl1)
            print(det.det_key)
            print(sepl1)
            det.print_detector(0)
        print(sepl)
        print('Printing detectors done.')
        print(sepl)
        print()

    ###
    #-----Dealing with several networks-----
    def get_det_responses_psds_from_locs_tecs(self,loc_net,tec_net,F_lo=-np.inf,F_hi=np.inf,sym_derivs=0,keep_variables=None):

        self.inj_params = loc_net.inj_params
        self.deriv_variables = loc_net.deriv_variables
        self.f = loc_net.f

        for i,det in enumerate(self.detectors):
            tec_det = tec_net.get_detector(det.tec+'_loc')

            f_lo = np.maximum(tec_det.f[0], F_lo)
            f_hi = np.minimum(tec_det.f[-1], F_hi)
            ids_det_f = np.logical_and(tec_det.f>=f_lo,tec_det.f<=f_hi)
            ids_net_f = np.logical_and(self.f>=f_lo,self.f<=f_hi)

            det.f = tec_det.f[ids_det_f]
            det.psd = tec_det.psd[ids_det_f]

            loc_det = loc_net.get_detector('tec_'+det.loc)
            det.hf = deepcopy(loc_det.hf[ids_net_f])
            det.del_hf = deepcopy(loc_det.del_hf)
            for deriv in det.del_hf:
                det.del_hf[deriv] = det.del_hf[deriv][ids_net_f]
            if sym_derivs:
                det.del_hf_expr = deepcopy(loc_det.del_hf_expr)

        # only keep derivs defined by the the variables in keep_variables
        if keep_variables is not None:
            keep_derivs = []
            keep_deriv_variables = []

            for keep_variable in keep_variables:
                k = 0
                for i,deriv in enumerate(list(self.detectors[0].del_hf.keys())):
                    if keep_variable in deriv:
                        keep_derivs.append(deriv)
                        keep_deriv_variables.append(self.deriv_variables[i])
                        k = 1
                if not k:
                    self.logger.warning(f'get_det_responses_psds_from_locs_tecs: {keep_variable} not among the derivatives.')

            self.deriv_variables = keep_deriv_variables
            for det in self.detectors:
                det.del_hf = utils.get_sub_dict(det.del_hf,keep_derivs,keep_in_list=1)

        self.logger.info('Detector responses transferred.')


###
#-----Dealing with several networks-----
def unique_tecs(network_specs, f, F_lo=-np.inf, F_hi=np.inf, user_psds=None, logger_level='WARNING'):
    # initialize empty network
    tec_net = Network(logger_name='unique_tecs', logger_level=logger_level)
    # get the detector keys
    tec_net.det_keys = []

    tec_net.logger.info('Calculate PSDs for unique detector technologies.')

    # find unique technologies
    for network_spec in network_specs:
        network = Network(network_spec, logger_name='unique_tecs', logger_level=logger_level)
        for det in network.detectors:
            tec_net.det_keys.append(det.tec)
    tec_net.det_keys = list(dict.fromkeys(tec_net.det_keys))

    # make them into fake detector keys
    for i,tec in enumerate(tec_net.det_keys):
        tec_net.det_keys[i] = tec+'_loc'
    # initialize fake detectors
    tec_net.detectors = []
    for det_key in tec_net.det_keys:
        tec_net.detectors.append(dc.Detector(det_key))

    # get PSDs
    tec_net.set_net_vars(f=f, user_psds=user_psds)
    tec_net.setup_psds(F_lo, F_hi)

    tec_net.logger.info('PSDs for unique detector technologies calculated.')
    return tec_net


def unique_locs_det_responses(network_specs, f, inj_params, deriv_symbs_string, wf_model_name,
                              wf_other_var_dic=None, conv_cos=None, conv_log=None, use_rot=1,
                              user_waveform=None, user_locs=None, user_lambdified_functions_path=None,
                              ana_deriv_symbs_list=None, cosmo=None, logger_level='WARNING', num_cores=None,
                              step=None, method=None, order=None, n=None):
    # initialize empty network
    loc_net = Network(logger_name='unique_locs_det_responses', logger_level=logger_level)
    # get the detector keys
    loc_net.det_keys = []

    # find unique locations
    for network_spec in network_specs:
        network = Network(network_spec, logger_name='unique_locs_det_responses', logger_level=logger_level)
        for det in network.detectors:
            loc_net.det_keys.append(det.loc)
    loc_net.det_keys = list(dict.fromkeys(loc_net.det_keys))

    # make them into fake detectpr keys
    for i,loc in enumerate(loc_net.det_keys):
        loc_net.det_keys[i] = 'tec_'+loc
    # initialize fake detectors
    loc_net.detectors = []
    for det_key in loc_net.det_keys:
        loc_net.detectors.append(dc.Detector(det_key))
    # set all the other necessary variables
    loc_net.set_wf_vars(wf_model_name, wf_other_var_dic=wf_other_var_dic, user_waveform=user_waveform, cosmo=cosmo)
    loc_net.set_net_vars(f=f, inj_params=inj_params, deriv_symbs_string=deriv_symbs_string, conv_cos=conv_cos, conv_log=conv_log,
                         use_rot=use_rot, user_locs=user_locs, user_lambdified_functions_path=user_lambdified_functions_path)

    # setup Fp, Fc, and Flp and calculate the detector responses
    loc_net.setup_ant_pat_lpf()
    loc_net.calc_det_responses()

    if step is None:
        loc_net.logger.info('Loading the lamdified functions.')
        loc_net.load_det_responses_derivs_sym(return_bin = 1)
        loc_net.logger.info('Loading done.')

    loc_net.logger.info('Evaluate lambdified detector responses for unique locations.')
    if num_cores is None:
        if step is None:
            for det in loc_net.detectors:
                det.del_hf, c_quants = eval_loc_sym(det.loc,det.del_hf_expr,deriv_symbs_string,f,inj_params,conv_cos,conv_log,logger=loc_net.logger)
        else:
            for det in loc_net.detectors:
                det.del_hf, c_quants = eval_loc_num(det.loc,loc_net.wf,deriv_symbs_string,f,inj_params,conv_cos,conv_log,use_rot,
                                                    step,method,order,n,user_locs,ana_deriv_symbs_list,logger=loc_net.logger)
        loc_net.inj_params, loc_net.deriv_variables = edh.get_conv_inj_params_deriv_variables(c_quants, loc_net.inj_params, loc_net.deriv_variables)

    else:
        from multiprocessing import Pool
        pool = Pool(num_cores)
        if step is None:
            arg_tuple_list = [(det.loc,det.del_hf_expr,deriv_symbs_string,f,inj_params,conv_cos,conv_log,loc_net.logger) for det in loc_net.detectors]
            result = pool.starmap_async(eval_loc_sym, arg_tuple_list)
            result.wait()
        else:
            arg_tuple_list = [(det.loc,loc_net.wf,deriv_symbs_string,f,inj_params,conv_cos,conv_log,use_rot,
                               step,method,order,n,user_locs,ana_deriv_symbs_list,loc_net.logger) for det in loc_net.detectors]
            result = pool.starmap_async(eval_loc_num, arg_tuple_list)
            result.wait()

        for det, (del_hf,c_quants) in zip(loc_net.detectors, result.get()):
            det.del_hf = del_hf

        loc_net.inj_params, loc_net.deriv_variables = edh.get_conv_inj_params_deriv_variables(c_quants, loc_net.inj_params, loc_net.deriv_variables)

    if step is None:
        for det in loc_net.detectors:
            det.del_hf_expr = dill.loads(det.del_hf_expr)

    loc_net.logger.info('Lambdified detector responses for unique locations evaluated.')
    return loc_net

def eval_loc_sym(loc ,del_hf_expr, deriv_symbs_string, f, inj_params, conv_cos, conv_log, logger=None):
    if logger is None: glob_logger.info(f'   {loc}')
    else:              logger.info(f'   {loc}')
    del_hf = {}
    del_hf_expr = dill.loads(del_hf_expr)
    for deriv in del_hf_expr:
        if deriv in ('variables','deriv_variables'): continue
        del_hf[deriv] = del_hf_expr[deriv](f,**utils.get_sub_dict(inj_params,del_hf_expr['variables']))
    return edh.get_conv_del_eval_dic(del_hf,inj_params,conv_cos,conv_log, deriv_symbs_string)

def eval_loc_num(loc, wf, deriv_symbs_string, f, inj_params, conv_cos, conv_log, use_rot,
                 step, method, order, n, user_locs, ana_deriv_symbs_list, logger=None):
    if logger is None: glob_logger.info(f'   {loc}')
    else:              logger.info(f'   {loc}')
    del_hf = drd.calc_det_responses_derivs_num(loc, wf, deriv_symbs_string, f, inj_params, use_rot=use_rot, label='hf',
                                               step=step, method=method, order=order, n=n, user_locs=user_locs,
                                               ana_deriv_symbs_list=ana_deriv_symbs_list)
    return edh.get_conv_del_eval_dic(del_hf,inj_params,conv_cos,conv_log, deriv_symbs_string)
