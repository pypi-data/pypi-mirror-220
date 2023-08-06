# -*- coding: utf-8 -*-
"""DIFFERENTIAL EVOLUTION METHOD"""

import numpy as np
from ._optimizer import Optimizer, CandidateState 
from scipy.stats import cauchy


class Solution(CandidateState):
    """DE solution class.
    
    Attributes
    ----------
    V : ndarray
        Mutant vector.  
    CR : float
        DE control parameter CR.
    F : float
        DE control parameter F.
         
    Returns
    -------
    solution : Solution
        Solution instance.
    """
    
    def __init__(self, optimizer: Optimizer):
        CandidateState.__init__(self, optimizer)
        #super(Particle, self).__init__(optimizer) # ugly version of the above
        
        self.CR = None
        self.F = None
        self.V = np.zeros([optimizer.dimensions]) * np.nan # mutant vector


class DE(Optimizer):
    """Differential Evolution method class.
    
    Reference: R. Tanabe and A. S. Fukunaga. Improving the search performance of SHADE using 
    linear population size reduction”, in Proceedings of the 2014 IEEE Congress on 
    Evolutionary Computation (CEC), pp. 1658–1665, Beijing, China, July 2014.
    
    Attributes
    ----------
    variant : str
        Name of the DE variant (``SHADE`` or ``LSHADE``). Default: ``SHADE``.
    params : dict
        A dictionary of DE parameters.
        
    Returns
    -------
    optimizer : DE
        DE optimizer instance.        
    """

    def __init__(self):
        Optimizer.__init__(self)
        #super(PSO, self).__init__() # ugly version of the above

        self.variant = 'SHADE'
        self.params = {}

    def _check_params(self):
        """Private method which performs some DE-specific parameter checks
        and prepares the parameters to be validated by Optimizer._check_params.

        Returns
        -------
        None
            Nothing
        """
        
        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []
        
        if 'pop_init' in self.params:
            self.params['pop_init'] = int(self.params['pop_init'])
        if 'hist_size' in self.params:
            self.params['hist_size'] = int(self.params['hist_size'])

        if self.variant == 'SHADE':
            mandatory_params = 'pop_init f_archive hist_size p_mutation'.split()
            if 'pop_init' not in self.params:
                self.params['pop_init'] = self.dimensions * 18
                defined_params += 'pop_init'.split()
            if 'f_archive' not in self.params:
                self.params['f_archive'] = 2.6
                defined_params += 'f_archive'.split()
            if 'hist_size' not in self.params: # a.k.a. H
                self.params['hist_size'] = 6
                defined_params += 'hist_size'.split()
            if 'p_mutation' not in self.params:
                self.params['p_mutation'] = 0.11
                defined_params += 'p_mutation'.split()    
            optional_params = 'rank_enabled'.split()
            if 'rank_enabled' not in self.params:
                self.params['rank_enabled'] = False # Rank-based variant off by default
                defined_params += 'rank_enabled'.split()  
        elif self.variant == 'LSHADE':
            mandatory_params = 'pop_init f_archive hist_size p_mutation'.split()
            if 'pop_init' not in self.params:
                self.params['pop_init'] = self.dimensions * 18
                defined_params += 'pop_init'.split()
            if 'f_archive' not in self.params:
                self.params['f_archive'] = 2.6
                defined_params += 'f_archive'.split()
            if 'hist_size' not in self.params: # a.k.a. H
                self.params['hist_size'] = 6
                defined_params += 'hist_size'.split()
            if 'p_mutation' not in self.params:
                self.params['p_mutation'] = 0.11
                defined_params += 'p_mutation'.split()  
            optional_params = 'rank_enabled'.split()
            if 'rank_enabled' not in self.params:
                self.params['rank_enabled'] = False # Rank-based variant off by default
                defined_params += 'rank_enabled'.split()
        else:
            assert False, f'Unknown variant! {self.variant}'
        
        if self.constraints > 0:
            assert False, 'DE does not support constraints'
        
        assert isinstance(self.params['pop_init'], int) \
            and self.params['pop_init'] > 0, \
            "pop_init should be positive integer"
        assert self.params['f_archive'] > 0, \
            "external_archive_size should be positive"
        assert isinstance(self.params['hist_size'], int) \
            and self.params['hist_size'] > 0, \
            "hist_size should be positive integer"

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)
        
    def _init_method(self):
        """Private method for initializing the DE optimizer instance.
        Initializes and evaluates the population.

        Returns
        -------
        err_msg : str or None
            Error message (if any).
        """

        if self.variant == 'LSHADE':
            assert self.max_iterations or self.max_evaluations or self.max_elapsed_time, \
                'optimizer.max_iteration, optimizer.max_evaluations, or self.max_elapsed_time should be provided for this method/variant'

        self._evaluate_initial_candidates()
        err_msg = None

        # Generate a population
        self.Pop = np.array([Solution(self) for c in \
                             range(self.params['pop_init'])], dtype=Solution)
        
        # Generate a trial population
        self.Trials = np.array([Solution(self) for c in \
                                range(self.params['pop_init'])], dtype=Solution)
        
        # Initalize Archive
        self.A = np.empty([0])
        
        # Prepare historical memory
        self.M_CR = np.full(self.params['hist_size'], 0.5)
        self.M_F = np.full(self.params['hist_size'], 0.5)

        # Generate initial positions
        n0 = 0 if self._cS0 is None else self._cS0.size
        for i in range(self.params['pop_init']):
            
            # Random position
            self.Pop[i].X = np.random.uniform(self.lb, self.ub)
            
            # Using specified particles initial positions
            if i < n0:
                self.Pop[i] = self._cS0[i].copy()

        # Evaluate
        if n0 < self.params['pop_init']:
            err_msg = self.collective_evaluation(self.Pop[n0:])

        # if all candidates are NaNs
        if np.isnan([p.f for p in self.Pop]).all():
            err_msg = 'ALL CANDIDATES FAILED TO EVALUATE.'
        if err_msg:
            return err_msg
        
        self._finalize_iteration()
        
    def _run(self):
        """Main loop of DE method.

        Returns
        -------
        optimum: Solution
            Best solution found during the DE optimization.
        """
        
        self._check_params()
        
        err_msg = self._init_method()
        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'
        
        k = 0 # memory index

        while True:
            
            S_CR = np.empty([0])
            S_F = np.empty([0])
            S_df = np.empty([0])
            
            # find pbest
            top = max(round(np.size(self.Pop) * self.params['p_mutation']), 1)
            pbest = np.random.choice(np.sort(self.Pop)[0:top])
            
            if self.params['rank_enabled']:
                self.Pop = np.sort(self.Pop)
            
            for p, t in zip(self.Pop, self.Trials):
                
                # Update CR, F
                r = np.random.randint(self.params['hist_size'])
                if np.isnan(self.M_CR[r]):
                    p.CR = 0
                else:
                    p.CR = np.random.normal(self.M_CR[r], 0.1)
                    p.CR = np.clip(p.CR, 0, 1)
                p.F = -1
                while p.F <= 0:
                    p.F = min(cauchy.rvs(self.M_F[r], 0.1), 1)
                
                # Compute mutant vector
                r1 = r2 = p
                while r1 is r2 or r1 is p or r2 is p:
                    r1 = np.random.choice(self.Pop)
                    r2 = np.random.choice(np.append(self.Pop, self.A))
                p.V = p.X + p.F * (pbest.X - p.X) + p.F * (r1.X - r2.X)
                p.V = np.clip(p.V, (p.X + self.lb)/2, (p.X + self.ub)/2)
                
                # Compute trial vector
                t.CR = p.CR
                t.F = p.F
                jrand = np.random.randint(self.dimensions)
                for j in range(self.dimensions):
                    if np.random.rand() <= p.CR or j == jrand:
                        t.X[j] = p.V[j]
                    else:
                        t.X[j] = p.X[j]

            # Evaluate population
            err_msg = self.collective_evaluation(self.Trials)
            if err_msg:
                break
            
            # Survival for next generation
            if not self.params['rank_enabled']:
                for p, t in zip(self.Pop, self.Trials):
                    if not np.isnan(t.f) and t.f < p.f:
                        # Update external archive
                        self.A = np.append(self.A, p)
                        if np.size(self.A) > round(np.size(self.Pop) * self.params['f_archive']):
                            self.A = np.delete(self.A, 
                                               np.random.randint(np.size(self.A)))
                        S_CR = np.append(S_CR, t.CR) 
                        S_F = np.append(S_F, t.F)
                        S_df = np.append(S_df, p.f - t.f)
                        # Update population
                        p.X = np.copy(t.X)
                        p.f = t.f 
            
            # Rank-based variant - very poor performance
            if self.params['rank_enabled']: 
                # p_ranking = np.argsort(self.Pop)
                p_ranking = np.arange(np.size(self.Pop))
                # self.Trials = np.sort(self.Trials)
                t_ranking = np.argsort(self.Trials)
                # Calculating rank-based improvement of trials
                S_df = (p_ranking - t_ranking) / (1 + p_ranking)**2
                S_df = S_df[S_df > 0]
                # S_df = 1.0 + S_df ** 2                                               
                for p, t, p_rank, t_rank in zip(self.Pop, self.Trials, p_ranking, t_ranking):
                    if t_rank < p_rank:                      
                        # Update external archive
                        self.A = np.append(self.A, p)
                        if np.size(self.A) > round(np.size(self.Pop) * self.params['f_archive']):
                            self.A = np.delete(self.A, 
                                                np.random.randint(np.size(self.A)))
                        S_CR = np.append(S_CR, t.CR) 
                        S_F = np.append(S_F, t.F)
                        #S_df = np.append(S_df, p_rank - t_rank)
                        # Update population
                        p.X = np.copy(t.X)
                        p.f = t.f 
                        p.O, p.C = np.copy(t.O), np.copy(t.C)

            # Memory update
            if np.size(S_CR) != 0 and np.size(S_F) != 0:
                w = S_df / np.sum(S_df)
                if np.isnan(self.M_CR[k]) or np.max(S_CR) < 1e-100:
                    self.M_CR[k] = np.nan
                else:
                    self.M_CR[k] = np.sum(w * S_CR**2) / np.sum(w * S_CR)
                self.M_F[k] = np.sum(w * S_F**2) / np.sum(w * S_F)
                k += 1
                if k >= self.params['hist_size']:
                    k = 0
                    
            # Linear Population Size Reduction (LPSR)
            if self.variant == 'LSHADE':
                N_init = self.params['pop_init']
                N_new = round((4 - N_init) * self._progress_factor() + N_init)
                if N_new < np.size(self.Pop):
                    self.Pop = np.sort(self.Pop)[:N_new]
                    self.Trials = self.Trials[:N_new]          
                
            if self._finalize_iteration():
                break

        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'
        
        return self.best
