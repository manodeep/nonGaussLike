'''

code for assessing galaxy clustering data and etc. 


'''
import numpy as np 
# -- local -- 
import util as UT

class Pk: 
    def __init__(self):
        ''' Pk object
        '''
        self.k = None 
        self.pk = None 
        self.counts = None 

    def Read(self, name, i, ell=0): 
        ''' ***NEED TO IMPLEMENT quadrupole and hexadecapole*** 
        Read in the i th mock catalog P(k) 
        '''
        if ell not in [0, 2, 4]: 
            raise ValueError("ell can only be 0, 2, or 4") 

        if name == 'nseries': 
            if ell == 0: 
                f = ''.join([UT.dat_dir(), 'nseries/power_CutskyN', str(i), '.dat.grid360.P020000.box3600'])
            else: 
                f = ''.join([UT.dat_dir(), 'nseries/POWER_Q_CutskyN', str(i), '.fidcosmo.dat.grid480.P020000.box3600'])
        elif name == 'qpm': 
            if ell == 0: 
                f = ''.join([UT.dat_dir(), 'qpm/power_a0.6452_', str(i).zfill(4), '.dr12d_cmass_ngc.vetoed.dat.grid360.P020000.box3600'])
            else: 
                f = ''.join([UT.dat_dir(), 'qpm/POWER_Q_a0.6452_', str(i).zfill(4), '.dr12d_cmass_ngc.vetoed.fidcosmo.dat.grid480.P020000.box3600']) 
        else: 
            raise NotImplementedError

        if ell == 0: 
            k, pk, counts = np.loadtxt(f, unpack=True, usecols=[0, 1, -1]) # k, p0(k), and number of modes 
        else: 
            k, pk, counts = np.loadtxt(f, unpack=True, usecols=[0, 1+ell/2, -2]) # k, p0(k), and number of modes 

        self.k = k
        self.pk = pk
        self.counts = counts
        return None
    
    def rebin(self, rebin, pk_arr=None): 
        ''' Rebin the P(k) using the counts 

        pk_arr = [k, pk, count] 
        '''
        if pk_arr is None and self.k is None: 
            raise ValueError("what am I rebinning") 
        if pk_arr is not None: 
            if self.k is not None: 
                print "Pk object already has k, Pk, and count. They will be ignored."
            k = pk_arr[0] 
            pk = pk_arr[1] 
            counts = pk_arr[2]
        else: 
            k = self.k 
            pk = self.pk 
            counts = self.counts

        N = len(k) # array length 

        if isinstance(rebin, int): 
            # reducing binning by a factor or rebin 
            tot_counts, k_rebin, pk_rebin = [], [], []
            for istart in range(N)[::rebin]: 
                indices = range(N)[istart:istart+rebin]

                cnts = np.sum(counts[indices]) # number of modes in bin 
                tot_counts.append(cnts)
                k_rebin.append(np.sum(k[indices] * counts[indices])/cnts)
                pk_rebin.append(np.sum(pk[indices] * counts[indices])/cnts)
            # note that if rebin does not divide evenly into N, 
            # the last bin will be uneven
        else: 
            raise NotImplementedError

        return [np.array(k_rebin), np.array(pk_rebin), np.array(tot_counts)]
    
    def _n_mock(self, name): 
        ''' Given name of mock return n_mock. 
        '''
        if name == 'nseries': 
            n_mock = 84
        elif name == 'qpm': 
            n_mock = 1000 
        else: 
            raise ValueError
        return n_mock 
