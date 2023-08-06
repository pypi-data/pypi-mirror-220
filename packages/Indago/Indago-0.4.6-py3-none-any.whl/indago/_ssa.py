# -*- coding: utf-8 -*-

import numpy as np
from ._optimizer import Optimizer, CandidateState 
from scipy.special import gamma


FlyingSquirrel = CandidateState


class SSA(Optimizer):
    """Squirrel Search Algorithm method class.
    
    Reference: Jain, M., Singh, V., & Rani, A. (2019). A novel nature-inspired algorithm 
    for optimization: Squirrel search algorithm. Swarm and evolutionary computation, 
    44, 148-175.
    
    Attributes
    ----------
    variant : str
        Name of the SSA variant. Default: ``Vanilla``.
    params : dict
        A dictionary of SSA parameters.
        
    Returns
    -------
    optimizer : SSA
        SSA optimizer instance.
    """

    def __init__(self):        
        Optimizer.__init__(self)

        self.variant = 'Vanilla'
        self.params = {}

    def _check_params(self):
        """Private method which prepares the parameters to be validated by Optimizer._check_params.

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
            mandatory_params = 'pop_size ata'.split()
            # the following params are better left at default
            mandatory_params += 'p_pred c_glide \
                                gd_lim'.split() 
            if 'pop_size' not in self.params:
                self.params['pop_size'] = self.dimensions
                defined_params += 'pop_size'.split()
            if 'ata' not in self.params:
                self.params['ata'] = 0.5
                defined_params += 'ata'.split()
            # the following params are better left at default
            if 'p_pred' not in self.params:
                self.params['p_pred'] = 0.1
                defined_params += 'p_pred'.split()
            if 'c_glide' not in self.params:
                self.params['c_glide'] = 1.9
                defined_params += 'c_glide'.split()
            if 'gd_lim' not in self.params:
                self.params['gd_lim'] = [0.5, 1.11]
                defined_params += 'gd_lim'.split()
            optional_params = ''.split()
        else:
            assert False, f'Unknown variant! {self.variant}'
            
        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)
        
    def _init_method(self):
        """Private method for initializing the SSA optimizer instance.
        Initializes and evaluates the swarm.

        Returns
        -------
        None
            Nothing
        """

        assert self.max_iterations or self.max_evaluations or self.max_elapsed_time, \
            'optimizer.max_iteration, optimizer.max_evaluations, or self.max_elapsed_time should be provided for this method/variant'

        err_msg = None

        # Generate a swarm of FS
        self.cS = np.array([FlyingSquirrel(self) for c in range(self.params['pop_size'])], \
                            dtype=FlyingSquirrel)
        
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
        """Main loop of SSA method.

        Returns
        -------
        optimum: FlyingSquirrel
            Best solution found during the PSO optimization.
        """
        
        self._check_params()
        
        err_msg = self._init_method()
        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'
      
        # Load params
        if 'ata' in self.params:
            # part of FSnt moving to FSat
            # ATA=0 (all move to FSht) - emphasize local search
            # ATA=1 (all move to FSat's) - emphasize global search
            ATA = self.params['ata']
        if 'p_pred' in self.params:
            Pdp = self.params['p_pred']
        if 'c_glide' in self.params:
            Gc = self.params['c_glide']
        if 'gd_lim' in self.params:
            gd_lim = self.params['gd_lim']
            
        def Levy():
            ra, rb = np.random.normal(0, 1), np.random.normal(0, 1)
            beta = 1.5
            sigma = ((gamma(1 + beta) * np.sin(np.pi * beta / 2)) / \
                     gamma((1 + beta) / 2) * beta * 2**((beta - 1)/2)) **(1 / beta)
            return 0.01 * (ra * sigma) / (np.abs(rb)**(1 / beta))

        while True:
            
            # Categorizing FS's
            FSht = np.sort(self.cS)[0] # best FS (hickory nut trees)
            FSat = np.sort(self.cS)[1:4] # good FS (acorn trees)
            FSnt = np.sort(self.cS)[5:] # bad FS (normal trees)
            
            """
            # Moving FSnt - cascading strategy
            # move principally to FSat; 
            # with probability = (1-Pdp)*Pdp = 0.09 move to Fsht
            for fs in FSnt:
                if np.random.rand() >= Pdp: # move towards FSat
                    dg = np.random.uniform(gd_lim[0], gd_lim[1])
                    fs.X = fs.X + dg * Gc * \
                            (np.random.choice(FSat).X - fs.X)
                elif np.random.rand() >= Pdp: # move towards FSht
                    dg = np.random.uniform(gd_lim[0], gd_lim[1])
                    fs.X = fs.X + dg * Gc * (FSht.X - fs.X)
                else: # not moving, i.e. respawning randomly
                    fs.X = np.random.uniform(self.lb, self.ub)
            """
            
            # Moving FSnt
            Nnt2at = int(np.size(FSnt) * ATA) # attracted to acorn trees
            np.random.shuffle(FSnt)
            for fs in FSnt[:Nnt2at]:
                if np.random.rand() >= Pdp: # move towards FSat
                    dg = np.random.uniform(gd_lim[0], gd_lim[1])
                    fs.X = fs.X + dg * Gc * \
                            (np.random.choice(FSat).X - fs.X)
                else: # not moving, i.e. respawning randomly
                    fs.X = np.random.uniform(self.lb, self.ub)
            for fs in FSnt[Nnt2at:]:
                if np.random.rand() >= Pdp: # move towards FSht
                    dg = np.random.uniform(gd_lim[0], gd_lim[1])
                    fs.X = fs.X + dg * Gc * (FSht.X - fs.X)
                else: # not moving, i.e. respawning randomly
                    fs.X = np.random.uniform(self.lb, self.ub)
            
            # Moving FSat
            for fs in FSat:
                if np.random.rand() >= Pdp: # move towards FSht
                    dg = np.random.uniform(gd_lim[0], gd_lim[1])
                    fs.X = fs.X + dg * Gc * (FSht.X - fs.X)
                else: # not moving, i.e. respawning randomly
                    fs.X = np.random.uniform(self.lb, self.ub)
            
            # Seasonal constants (for FSat)
            Sc = np.empty(3)
            for i, fs in enumerate(FSat):
                Sc[i] = np.sqrt(np.sum((fs.X - FSht.X)**2))
                
            # Minimum value of seasonal constant
            Scmin = 1e-6 / (365**(self._progress_factor() * 2.5)) # this is some black magic shit
            
            # Random-Levy relocation at the end of winter season
            if (Sc < Scmin).all():
                for fs in FSnt:
                    fs.X = self.lb + Levy() * (self.ub - self.lb)
            
            # Correct position to the bounds
            for cP in self.cS:               
                cP.clip(self)
                
            # Evaluate swarm
            err_msg = self.collective_evaluation(self.cS)
            if err_msg:
                break
             
            if self._finalize_iteration():
                break
            
        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'
        
        return self.best