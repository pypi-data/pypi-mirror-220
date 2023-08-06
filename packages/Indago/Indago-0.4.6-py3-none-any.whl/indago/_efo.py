# -*- coding: utf-8 -*-
"""Electromagnetic Field Optimization method"""

import numpy as np
from ._optimizer import Optimizer, CandidateState 
from scipy.constants import golden_ratio as phi


emParticle = CandidateState

class EFO(Optimizer):
    """Electromagnetic Field Optimization method class.
    
    Reference: Abedinpourshotorban, H., Shamsuddin, S.M., Beheshti, Z., & Jawawi, D.N. (2016). 
    Electromagnetic field optimization: a physics-inspired metaheuristic 
    optimization algorithm. Swarm and Evolutionary Computation, 26, 8-22.
    
    Due to evaluating only one particle per iteration, this method:
    
    - needs many iterations to be efficient (much more than other methods)
    
    - is effectively not parallelized in **collective_evaluation** (hence parallel evaluation is not allowed, in order to avoid user confusion)
    
    Parameters
    ----------
    variant : str
        Name of the EFO variant. Default: ``Vanilla``.
    params : dict
        A dictionary of EFO parameters.
        
    Returns
    -------
    optimizer : EFO
        EFO optimizer instance.
    """

    def __init__(self):
        Optimizer.__init__(self)

        self.variant = 'Vanilla'
        self.params = {}

    def _check_params(self):
        """Private method which performs some EFO-specific parameter checks
        and prepares the parameters to be validated by Optimizer._check_params.

        Returns
        -------
        None
            Nothing
        """
        
        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []
        
        if 'pop_size' in self.params:
            self.params['pop_size'] = int(self.params['pop_size'])

        if self.variant == 'Vanilla':
            mandatory_params = 'pop_size R_rate Ps_rate P_field N_field'.split()
            if 'pop_size' not in self.params:
                self.params['pop_size'] = 10 * self.dimensions
                defined_params += 'pop_size'.split()
            if 'R_rate' not in self.params:
                self.params['R_rate'] = 0.25 # recommended [0.1, 0.4]
                defined_params += 'R_rate'.split()
            if 'Ps_rate' not in self.params:
                self.params['Ps_rate'] = 0.25 # recommended [0.1, 0.4]
                defined_params += 'Ps_rate'.split()
            if 'P_field' not in self.params:
                self.params['P_field'] = 0.075 # recommended [0.05, 0.1]
                defined_params += 'P_field'.split()
            if 'N_field' not in self.params:
                self.params['N_field'] = 0.45 # recommended [0.4, 0.5]
                defined_params += 'N_field'.split()
        else:
            assert False, f'Unknown variant! {self.variant}'
            
        if self.number_of_processes > 1:
            self.log('Warning: EFO does not support parallelization. Defaulting to number_of_processes=1.')
            self.number_of_processes = 1

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)
      
                    
    def _init_method(self):
        """Private method for initializing the EFO optimizer instance.
        Initializes and evaluates the swarm.

        Returns
        -------
        err_msg : str or None
            Error message (if any).
        """

        self._evaluate_initial_candidates()
        err_msg = None
        
        # Generate a population
        self.cS = np.array([emParticle(self) \
                            for _ in range(self.params['pop_size'])], 
                            dtype=emParticle)
        self.cNew = emParticle(self)
        
        # Initialize
        n0 = 0 if self._cS0 is None else self._cS0.size
        for i, p in enumerate(self.cS):
            
            # Random position
            self.cS[i].X = np.random.uniform(self.lb, self.ub)
            
            # Using specified particles initial positions
            if i < n0:
                self.cS[i] = self._cS0[i].copy()
                    
        self.cNew.X = np.random.uniform(self.ub, self.lb)
        
        # Evaluate
        if n0 < self.cS.size:
            err_msg = self.collective_evaluation(self.cS[n0:])
        self.cS = np.sort(self.cS)
        # if all candidates are NaNs       
        if np.isnan([cP.f for cP in self.cS]).all():
            err_msg = 'ALL CANDIDATES FAILED TO EVALUATE.'
        if err_msg:
            return err_msg
        
        self._finalize_iteration()
        

    def _run(self):
        """Main loop of EFO method.

        Returns
        -------
        optimum: emParticle
            Best solution found during the EFO optimization.
        """
        
        self._check_params()
        
        err_msg = self._init_method()
        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'
        
        if 'pop_size' in self.params:
            N_emp = self.params['pop_size']
        if 'P_field' in self.params:
            P_field = self.params['P_field']
        if 'N_field' in self.params:
            N_field = self.params['N_field']
        if 'Ps_rate' in self.params:
            Ps_rate = self.params['Ps_rate']
        if 'R_rate' in self.params:
            R_rate = self.params['R_rate']
                        
        RI = 0
        
        while True:
                          
            for d in range(self.dimensions):
                force = np.random.uniform(0,1)
                l_pos = np.random.randint(1, np.floor(N_emp * P_field))
                l_neg = np.random.randint(np.floor((1 - N_field) * N_emp), N_emp)
                l_neu = np.random.randint(np.ceil(N_emp * P_field), 
                                          np.ceil((1 - N_field) * N_emp))
                
                if np.random.uniform(0,1) < Ps_rate: 
                    self.cNew.X[d] = self.cS[l_pos].X[d]                
                else: 
                    self.cNew.X[d] = self.cS[l_neu].X[d] + \
                                        phi * force * (self.cS[l_pos].X[d] - self.cS[l_neu].X[d]) \
                                        - force * (self.cS[l_neg].X[d] - self.cS[l_neu].X[d])
                
                if self.cNew.X[d] > self.ub[d] or self.cNew.X[d] < self.lb[d]: 
                    self.cNew.X[d] = self.lb[d] + \
                                        np.random.uniform() * (self.ub[d] - self.lb[d])
            
            if np.random.uniform(0,1) < R_rate:
                self.cNew.X[RI] = self.lb[RI] + \
                                        np.random.uniform() * (self.ub[RI] - self.lb[RI])
                RI += 1
                if RI > self.dimensions-1:
                    RI = 0
            
            err_msg = self.collective_evaluation(np.array([self.cNew], dtype=emParticle))
            if err_msg:
                break
            
            # insert cNew if better than last in list    
            if self.cNew < self.cS[-1]:
                self.cS[-1] = self.cNew.copy()
            self.cS = np.sort(self.cS) 
                    
            if self._finalize_iteration():
                break
            
        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'
        
        return self.best
