# Changelog

## [0.7.1] - 2023-07-21

### Added/Changed

* switched to Ver 0.7.1
* added the ability to choose analytical derivatives for DL, tc, phic (changes in wf_derivatives_num + where needed, added of wf_derivatives_ana)
* improved example_scripts to reflect this possibility
* fixed bug in injections.py
* cleaned up some code

## [0.7.0] - 2023-06-19

### Added/Changed

* switched to Ver 0.7.0
* **noise curves**
  * added 4 most recent, official CE curves from https://dcc.cosmicexplorer.org/CE-T2000017/public
    *  `'CE-40', 'CE-40-LF', 'CE-20', 'CE-20-PM'`
  * added ET 10km xylophone curve from https://apps.et-gw.eu/tds/?content=3&r=18213
    *  `'ET-10-XYL'`
  * added A_sharp curve from https://dcc.ligo.org/LIGO-T2300041-v1/public
    *  `'A#'`
* **general changes and cleanup of code for readability**
  * renamed 2 modules: wf_class.py -> waveform.py and detector_class.py -> detector.py
  * switched from copy to deepcopy in network.py where needed
  * added a logger that prints the previous "verbose" logs at "INFO"-level, but not at "WARNING"-level and above
  * added the available detector technologies and locations to utils.py (and removed them from psd.py and antenna_pattern_np.py, respectively)
  * removed the `df`-option from the functions in snr.py and respective calls
* **antenna_pattern_np.py / antenna_pattern_sp.py**
  * added new detector locations for the MPSAC project: CEA, CEB, CES, ETS, LLO, LHO, LIO
  * using the more precise detector angles for H, L, V, K, I, ET1, ET2, ET3
  * changed the output named `beta` of function `det_angles` in antenna_pattern_np.py and antenna_pattern_sp.py from polar angle to latitude for consistency with the waveform parameter `dec`
  * added function `det_shape` to antenna_pattern_np.py to streamline the definition of which locations are L- or V-shaped
  * removed function `check_loc_gen` from antenna_pattern_np.py and adjusted the only call in network.py
  * removed `ap_symbs_string, det_shape, det_angles` from antenna_pattern_sp.py and import these from antenna_pattern_np.py instead (for code consistency)
* **fisher_analysis_tools.py**
  * added `mpmath` for arbitrary precision matrix inversion of Fisher matrices and removed well-conditioning checks and variables as these are not needed anymore
  * `cond_sup` is now used to set the level up to which `np.linalg.inv` is used (beyond that the code is uses the `mpmath` inversion
    * when set to `None` (*default*) the code will always use `mpmath`
  * removed `np.abs` inside `get_errs_from_cov`
    * if the covariance matrix has negative elements on the diagonal something went bad and this should not be hidden
  * switched `inv_err` into a dictionary containing information about the quality of the inversion of the Fisher matrix
  * removed `by_element` option from inversion error calculation
* **utils.py**
  * united basic_constants.py, basic_functions.py, io_mod.py, and wf_manipulations.py  in utils.py

## [0.6] - 2021-11-05

### Added/Changed

*  fixed a bug in gwbench/detector_response_derivatives.py when attempting to calculate derivatives of wf polarizations wrt ra, dec, psi

## [0.6] - 2021-10-12

### Added/Changed

*  set default step-size for numerical differentiation to 1e-9
*  change the passing of psd_file_dict to allow the keys to be either det_key or psd tags (tec_loc or just tec) in detector_class.py

## [0.6] - 2021-09-21

### Added/Changed

*  updated requirements_conda.txt to use more modern packages
*  added Network to be called directly from gwbench (from gwbench import Network)
*  made detector_class.py less verbose
*  small code clean-ups

## [0.6] - 2021-08-18

### Added/Changed

*  switched to Ver 0.65
*  corrected (original formula was for theta not dec) and improved sky_area_90 calculations in err_deriv_handling.py, network.py, and detector_class.py

## [0.6] - 2021-07-07

### Added/Changed

*  fixed a bug for cos and log conversion of derivatives in detector_class.py
*  fixed mass sampling methods power_peak and power_peak_uniform in injections.py
*  cleaned up numerical detector response differentiation calls in detector_class.py and network.py

## [0.6] - 2021-07-07

### Added/Changed

*  added Planck's constant to basic_constants.py
*  added early warning frequency functions to basic_relations.py
*  added the functionality to specify user definied path for the lambdified sympy functions in detector_response_derivatives.py
*  added new mass samplers to injections.py
*  added new redshift/distance samplers to injections.py (in a previous commit)
*  added the option to limit the frequency range and which variables to use when using get_det_responses_psds_from_locs_tecs in network.py
*  changed function names for better understanding in detector_response_derivatives.py, detector_calls.py, fisher_analysis_tools.py, and network.py
*  changed sampling to maintain ordering when changing the number of injections in injections.py
*  changed example_scripts as necessary
*  renamed detector_responses.py to detector_response_derivatives.py

## [0.6] - 2021-02-15

### Added/Changed

*  attempted fix for segmentation fault: specify specific version of dependencies in requirements_conda.txt

## [0.6] - 2020-10-24

### Added/Changed

*  Initial Release
