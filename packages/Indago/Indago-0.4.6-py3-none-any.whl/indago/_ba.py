# -*- coding: utf-8 -*-
"""BAT ALGORITHM"""



import numpy as np
from ._optimizer import Optimizer, CandidateState 


class Bat(CandidateState):
    """BA Bat class. A Bat is a member of a BA swarm.
    
    Attributes
    ----------
    V : ndarray
        Bat velocity.
    Freq : ndarray
        Bat frequency.    
    A : float
        Bat loudness.
    r : float
        Bat pulse rate.
         
    Returns
    -------
    agent : Bat
        Bat instance.
    """
    
    def __init__(self, optimizer: Optimizer):
        CandidateState.__init__(self, optimizer)
        #super(Particle, self).__init__(optimizer) # ugly version of the above
        self.V = np.zeros([optimizer.dimensions]) * np.nan
        self.Freq = None
        self.A = None
        self.r = None     


class BA(Optimizer):
    """Bat Algorithm method class.
    
    References: [1] Yang, Xin‐She, and Amir Hossein Gandomi. Bat algorithm: a novel approach 
    for global engineering optimization. Engineering computations (2012). https://arxiv.org/pdf/1211.6663.pdf, 
    [2] Yang, Xin‐She. Nature-inspired optimization algorithms (2021).
    
    In this implementation loudness **A** and pulse rate **r** are generated for each Bat seperately (initial*2*rand).
    
    Attributes
    ----------
    variant : str
        Name of the BA variant. Default: ``Vanilla``.
    params : dict
        A dictionary of BA parameters.
        
    Returns
    -------
    optimizer : BA
        BA optimizer instance.
    """

    def __init__(self):
        Optimizer.__init__(self)

        self.variant = 'Vanilla'
        self.params = {}

    def _check_params(self):
        """Private method which performs some BA-specific parameter checks
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
            mandatory_params = 'pop_size loudness pulse_rate alpha gamma freq_range'.split()

            if 'pop_size' not in self.params:
                self.params['pop_size'] = self.dimensions
                defined_params += 'pop_size'.split()
            if 'loudness' not in self.params:
                self.params['loudness'] = 1
                defined_params += 'loudness'.split()
            if 'pulse_rate' not in self.params:
                self.params['pulse_rate'] = 0.001
                defined_params += 'pulse_rate'.split()
            if 'alpha' not in self.params:
                self.params['alpha'] = 0.9
                defined_params += 'alpha'.split()
            if 'gamma' not in self.params:
                self.params['gamma'] = 0.1
                defined_params += 'gamma'.split()
            if 'freq_range' not in self.params:
                self.params['freq_range'] = [0, 1]
                defined_params += 'freq_range'.split()
        else:
            assert False, f'Unknown variant! {self.variant}'

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)


    def _init_method(self):
        """Private method for initializing the BA optimizer instance.
        Initializes and evaluates the swarm.

        Returns
        -------
        err_msg : str or None
            Error message (if any).
        """

        self._evaluate_initial_candidates()
        err_msg = None

        # Generate a swarm
        self.cS = np.array([Bat(self) for c in range(self.params['pop_size'])], dtype=Bat)

        # Generate initial positions
        n0 = 0 if self._cS0 is None else self._cS0.size
        for p in range(self.params['pop_size']):
            
            # Random position
            self.cS[p].X = np.random.uniform(self.lb, self.ub)
            
            # Using specified particles initial positions
            if p < n0:
                self.cS[p] = self._cS0[p].copy()
            
            # Generate velocity
            self.cS[p].V = 0.0
            
            # Frequency
            self.cS[p].Freq = np.random.uniform(self.params['freq_range'][0], self.params['freq_range'][1])
            
            # Loudness
            self.cS[p].A = self.params['loudness']*2*np.random.uniform()
            
            # Pulse rate
            self.cS[p].r = self.params['pulse_rate']*2*np.random.uniform()

        # Evaluate
        if n0 < self.params['pop_size']:
            err_msg = self.collective_evaluation(self.cS[n0:])

        # if all candidates are NaNs
        if np.isnan([cP.f for cP in self.cS]).all():
            err_msg = 'ALL CANDIDATES FAILED TO EVALUATE.'
        if err_msg:
            return err_msg
        
        self.cB = np.array([cP.copy() for cP in self.cS])
        
        self._finalize_iteration()
        

    def _run(self):
        """Main loop of BA method.

        Returns
        -------
        optimum: Bat
            Best solution found during the BA optimization.
        """
        
        self._check_params()
        
        err_msg = self._init_method()
        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'

        if 'pulse_rate' in self.params:
            r_ = self.params['pulse_rate']
        if 'alpha' in self.params:
            alpha = self.params['alpha']
        if 'gamma' in self.params:
            gamma = self.params['gamma']
        if 'freq_range' in self.params:
            freq_min = self.params['freq_range'][0]
            freq_max = self.params['freq_range'][1]
        
        for p, cP in enumerate(self.cS):
            cP.A = alpha*cP.A
            cP.r = r_ *(1 - np.exp(-gamma*self.it))
        
        while True:
            
            A_avg = np.mean(np.array([self.cS[p].A for p in range(len(self.cS))]))
            
            #Calculate new velocity and new position
            for p, cP in enumerate(self.cS):
            
                cP.Freq = freq_min + (freq_max - freq_min)*np.random.uniform()

                cP.V = cP.V + (cP.X - self.best.X)*cP.Freq
                cP.X = cP.X + cP.V
                
                if np.random.uniform() > cP.r:
                    cP.X = self.best.X + 0.05*np.abs(self.lb - self.ub)*np.random.normal(size=self.dimensions)*A_avg
                                       
                cP.clip(self)
               
            #Evaluate swarm
            for p, cP in enumerate(self.cS):
                # Update personal best
                if cP <= self.cB[p] and np.random.uniform() < cP.A:
                    self.cB[p] = cP.copy()
                    cP.A = alpha*cP.A
                    cP.r = r_ *(1 - np.exp(-gamma*self.it))
                    
            err_msg = self.collective_evaluation(self.cS)
            if err_msg:
                break
            
            if self._finalize_iteration():
                break
            
        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'
        
        return self.best
