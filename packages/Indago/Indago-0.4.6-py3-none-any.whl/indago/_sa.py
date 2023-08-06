# -*- coding: utf-8 -*-
"""SIMULATED ANNEALING ALGORITHM"""



import numpy as np
from ._optimizer import Optimizer, CandidateState 
import random as rnd


Agent = CandidateState

class SA(Optimizer):
    """Simulated Annealing Algorithm class
    
    Returns
    -------
    optimizer : SA
        SA optimizer instance.
    """

    def __init__(self):
        """Initialization"""
        Optimizer.__init__(self)

        self.variant = 'Vanilla'
        self.params = {}

    def _check_params(self):
        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        if self.variant == 'Vanilla':
            mandatory_params = 'pop T0'.split()

            if 'pop' not in self.params:
                self.params['pop'] = 1 #just 1 agent, might experiment with a population
                defined_params += 'pop'.split()

            if 'T0' not in self.params:
                self.params['T0'] = self.dimensions #initial temperature
                defined_params += 'T0'.split()
        else:
            assert False, f'Unknown variant! {self.variant}'

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)


    def _init_method(self):

        self._evaluate_initial_candidates()
        err_msg = None

        # Generate agents
        self.cS = np.array([Agent(self) for c in range(self.params['pop'])], dtype=Agent)

        # Generate initial points
        n0 = 0 if self._cS0 is None else self._cS0.size
        for p in range(self.params['pop']):
            # Random position
            self.cS[p].X =  np.random.uniform(self.lb, self.ub)

            # Using specified initial positions
            if p < n0:
                self.cS[p] = self._cS0[p].copy()

        # Evaluate
        if n0 < self.params['pop']:
            err_msg = self.collective_evaluation(self.cS[n0:])

        # if all candidates are NaNs       
        if np.isnan([cP.f for cP in self.cS]).all():
            err_msg = 'ALL CANDIDATES FAILED TO EVALUATE.'
        if err_msg:
            return err_msg
        
        self.cB = np.array([cP.copy() for cP in self.cS], dtype=CandidateState)

        self._finalize_iteration()

    def _run(self):
        self._check_params()
        err_msg = self._init_method()
        if err_msg:
            print('Error: ' + err_msg + ' OPTIMIZATION ABORTED\n')
            return

        while True:
            
            epsilon = []
            for i in range(len(self.lb)):
                rand_ = np.random.normal(np.mean(np.linspace(self.lb[i],self.ub[i])),np.std(np.linspace(self.lb[i],self.ub[i]))) #random gaussian walk in each dimension
                epsilon.append(rand_)

            for cP in self.cS:
                cP.X = cP.X + epsilon
                cP.clip()

            cS_old = np.copy(self.cS)

            # Evaluate agent
            err_msg = self.collective_evaluation(self.cS)
            if err_msg:
                break

            T = self.params['T0'] / float(self.it + 1)


            for p, cP in enumerate(self.cS):
                if self.cS[p].f < cS_old[p].f:
                    self.cS[p].f = np.copy(cS_old[p].f)
                    self.cS[p].X = np.copy(cS_old[p].X)
                else:
                    r = np.random.uniform(0,1)
                    p_ = np.exp((-1*(self.cS[p].f - cS_old[p].f))/T)
                    if p_ > r:
                        self.cS[p].f = np.copy(cS_old[p].f)
                        self.cS[p].X = np.copy(cS_old[p].X)

            if self._finalize_iteration():
                break

        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'
        
        return self.best

