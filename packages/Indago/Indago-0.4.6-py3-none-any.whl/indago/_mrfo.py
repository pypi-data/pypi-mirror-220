# -*- coding: utf-8 -*-
""" MANTA RAY FORAGING OPTIMIZATION (MRFO) """


import numpy as np
from ._optimizer import Optimizer, CandidateState 


class MRFO(Optimizer):
    """Manta Ray Foraging Optimization method class.
    
    Reference: Zhao, Weiguo, Zhenxing Zhang, and Liying Wang. 
    Manta ray foraging optimization: An effective bio-inspired optimizer for engineering applications.
    Engineering Applications of Artificial Intelligence 87 (2020): 103300.
    
    Attributes
    ----------
    variant : str
        Name of the MRFO variant. Default: ``Vanilla``.
    params : dict
        A dictionary of MRFO parameters.
        
    Returns
    -------
    optimizer : MRFO
        MRFO optimizer instance.
    """

    def __init__(self):
        Optimizer.__init__(self)
        
        self.variant = 'Vanilla'
        self.params = {}

    def _check_params(self):
        """Private method which performs some MRFO-specific parameter checks
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
            mandatory_params = 'pop_size f_som'.split()
            if 'pop_size' not in self.params:
                self.params['pop_size'] = self.dimensions
                defined_params += 'pop_size'.split()
            if 'f_som' not in self.params:
                self.params['f_som'] = 2
                defined_params += 'f_som'.split()    
        else:
            assert False, f'Unknown variant! {self.variant}'

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)

    def _init_method(self):
        """Private method for initializing the MRFO optimizer instance.
        Initializes and evaluates the swarm.

        Returns
        -------
        err_msg : str or None
            Error message (if any).
        """
        assert self.max_iterations or self.max_evaluations or self.max_elapsed_time, \
            'optimizer.max_iteration, optimizer.max_evaluations, or self.max_elapsed_time should be provided for this method/variant'

        self._evaluate_initial_candidates()
        err_msg = None

        # Generate a swarm
        self.cS = np.array([CandidateState(self) for c in range(self.params['pop_size'])], dtype=CandidateState)
        
        # Generate initial positions
        n0 = 0 if self._cS0 is None else self._cS0.size
        for p in range(self.params['pop_size']):
            
            # Random position
            self.cS[p].X = np.random.uniform(self.lb, self.ub)
            
            # Using specified particles initial positions
            if p < n0:
                self.cS[p] = self._cS0[p].copy()

        # Evaluate
        if n0 < self.params['pop_size']:
            err_msg = self.collective_evaluation(self.cS[n0:])
        # if all candidates are NaNs       
        if np.isnan([cP.f for cP in self.cS]).all():
            err_msg = 'ALL CANDIDATES FAILED TO EVALUATE.'
        if err_msg:
            return err_msg
        
        self._finalize_iteration()
        
    def _run(self):
        """Main loop of MRFO method.

        Returns
        -------
        optimum: CandidateState
            Best solution found during the MRFO optimization.
        """
        
        self._check_params()
        
        err_msg = self._init_method()
        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'

        while True:
            
            X_ = np.copy(self.cS)
            
            if np.random.uniform() < 0.5:
                
                # CYCLONE FORAGING
                r = np.random.uniform(size=self.dimensions)
                r1 = np.random.uniform(size=self.dimensions)
                # beta = 2*np.exp(r1*((self.max_iterations-self.it+1)/self.max_iterations))*np.sin(2*np.pi*r1)
                beta = 2 * np.exp(r1 * (1 - self._progress_factor())) * np.sin(2*np.pi*r1)
                
                if self._progress_factor() < np.random.uniform():
                    X_rand = np.random.uniform(self.lb, self.ub, size=self.dimensions)
                    self.cS[0].X = X_rand + r*(X_rand - X_[0].X) + beta*(X_rand - X_[0].X)
                    for p in range(1, len(self.cS)):
                        self.cS[p].X = X_rand + r*(self.cS[p-1].X - X_[p].X) + beta*(X_rand - X_[p].X)
                else:
                    self.cS[0].X = self.best.X + r*(self.best.X - X_[0].X) + beta*(self.best.X - X_[0].X)
                    for p in range(1, len(self.cS)):
                        self.cS[p].X = self.best.X + r*(self.cS[p-1].X - X_[p].X) + beta*(self.best.X - X_[p].X)
                        
            else: 
                
                # CHAIN FORAGING
                r = np.random.uniform(size=self.dimensions)
                alpha = 2*r*np.sqrt(np.abs(np.log(r)))
                self.cS[0].X = X_[0].X + r*(self.best.X - X_[0].X) + alpha*(self.best.X - X_[0].X)
                for p in range(1, len(self.cS)):
                    self.cS[p].X = X_[p].X + r*(self.cS[p-1].X - X_[p].X) + alpha*(self.best.X - X_[p].X)
            
            for cP in self.cS:                              
                cP.clip(self)
            
            err_msg = self.collective_evaluation(self.cS)
            if err_msg:
                break
                               
            # SOMERSAULT FORAGING        
            r2 = np.random.uniform(size=self.dimensions)
            r3 = np.random.uniform(size=self.dimensions)
            for p, p_ in zip(self.cS, X_):
                p.X = p_.X + self.params['f_som']*(r2*self.best.X - r3*p_.X)
            
            for cP in self.cS:                              
                cP.clip(self)
                
            err_msg = self.collective_evaluation(self.cS)
            if err_msg:
                break
            
            if self._finalize_iteration():
                break
        
        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'

        return self.best
