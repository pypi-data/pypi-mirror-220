# -*- coding: utf-8 -*-
"""ARTIFICIAL BEE COLONY ALGORITHM"""


import numpy as np
from ._optimizer import Optimizer, CandidateState 


Bee = CandidateState


class ABC(Optimizer):
    """Artificial Bee Colony Algorithm class method class.
    
    Attributes
    ----------
    variant : str
        Name of the ABC variant. Default: ``Vanilla``.
    params : dict
        A dictionary of ABC parameters.
        
    Returns
    -------
    optimizer : ABC
        ABC optimizer instance.
    """

    def __init__(self):
        Optimizer.__init__(self)

        self.variant = 'Vanilla'
        self.params = {}


    def _check_params(self):
        """Private method which performs some ABC-specific parameter checks
        and prepares the parameters to be validated by Optimizer._check_params.

        Returns
        -------
        None
            Nothing
        """
        
        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        if self.variant == 'Vanilla':
            mandatory_params += 'pop_size trial_limit'.split()
            
            if 'pop_size' in self.params:
                self.params['pop_size'] = int(self.params['pop_size'])
            else:
                self.params['pop_size'] = self.dimensions
            defined_params += 'pop_size'.split()
            
            if 'trial_limit' in self.params:
                self.params['trial_limit'] = int(self.params['trial_limit'])            
            else:
                self.params['trial_limit'] = int((self.params['pop_size']*self.dimensions)/2) # Karaboga and Gorkemli 2014 - "A quick artificial bee colony (qabc) algorithm and its performance on optimization problems"
                defined_params += 'trial_limit'.split()
        
        else:
            assert False, f'Unknown variant! {self.variant}'

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)


    def _init_method(self):
        """Private method for initializing the ABC optimizer instance.
        Initializes and evaluates the population.

        Returns
        -------
        err_msg : str or None
            Error message (if any).
        """

        self._evaluate_initial_candidates()
        err_msg = None

        # Generate a swarm
        self.cS = np.array([Bee(self) for c in range(self.params['pop_size'])], dtype=Bee)
        self.cS_k = np.array([Bee(self) for c in range(self.params['pop_size'])], dtype=Bee)

        # Generate initial trial and probability vectors
        self.trials = np.zeros([self.params['pop_size']],dtype=np.int32)
        self.probability = np.zeros([self.params['pop_size']])

        n0 = 0 if self._cS0 is None else self._cS0.size
        for p in range(self.params['pop_size']):
            
            # Random position
            self.cS[p].X =  np.random.uniform(self.lb, self.ub)

            # Using specified particles initial positions
            if p < n0:
                self.cS[p] = self._cS0[p].copy()
            
        # Evaluate
        if n0 < self.params['pop_size']:
            err_msg = self.collective_evaluation(self.cS[n0:])
        # err_msg = self.collective_evaluation(self.cS)
        # err_msg = self.collective_evaluation(self.cS_k)
        #self.cS_k = np.copy(self.cS)

        # if all candidates are NaNs       
        if np.isnan([cP.f for cP in self.cS]).all():
            err_msg = 'ALL CANDIDATES FAILED TO EVALUATE.'
        
        if err_msg:
            return err_msg
        
        self.cB = np.array([cP.copy() for cP in self.cS])

        self._finalize_iteration()
        
    
    def _employed_bees_phase(self):
        """Private method for performing the employed bees phase of ABC.

        Returns
        -------
        err_msg : str or None
            Error message (if any).
        """
        
        err_msg = None
        
        for p, cP in enumerate(self.cS_k):
        
            k = np.random.randint(0,self.params['pop_size'])
            while k == p:
                k = np.random.randint(0,self.params['pop_size'])
     
            d = np.random.randint(0,self.dimensions)
            phi = np.random.uniform(-1,1)
            
            for i in range(self.dimensions):
                if i != d: self.cS_k[p].X[i] = self.cS[p].X[i]
     
            self.cS_k[p].X[d] = self.cS[p].X[d] + phi*(self.cS[p].X[d] - self.cS[k].X[d])
            
            cP.clip(self)
                
        for cP in self.cS:
            cP.clip(self)

        err_msg = self.collective_evaluation(self.cS_k)
        
        for p, cP in enumerate(self.cS_k):
            if self.cS_k[p] < self.cS[p]:
                self.cS[p] = self.cS_k[p].copy()
                self.trials[p] = 0
            else:
                self.trials[p] = self.trials[p] + 1
    
        if err_msg:
            return err_msg
        
    def _run(self):
        """Main loop of ABC method.

        Returns
        -------
        optimum: Bee
            Best solution found during the ABC optimization.
        """
        
        self._check_params()
        
        err_msg = self._init_method()
        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'

        if 'trial_limit' in self.params:
            trial_limit = self.params['trial_limit']

        while True:
            
            """employed bees phase"""
            err_msg = self._employed_bees_phase()
        
            
            """probability update"""
            fits = np.array([c.f for c in self.cS])
            for p, cP in enumerate(self.cS):
                # self.probability[p] = 0.1 + 0.9 * (self.cS[p].f/np.max(fits))
                self.probability[p] = self.cS[p].f / np.sum(fits)
                
            """onlooker bee phase"""
            i = 0
            t = 0
            while t < self.params['pop_size']:
                
                if np.random.uniform(0,1) < self.probability[i]:
                    
                    t = t + 1
                    err_msg = self._employed_bees_phase()
   
                i = (i + 1)%(self.params['pop_size'] - 1)

            
            """scout bee phase"""
            for p, cP in enumerate(self.cS):
                if self.trials[p] > trial_limit:
                    self.cS[p].X = np.random.uniform(self.lb, self.ub)
                    self.trials[p] = 0
            
            if err_msg:
                break

            if self._finalize_iteration():
                break

        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'
        
        return self.best

