#!/usr/bin/env 
"""
# Author: Kai Cao
# Modified from SCALEX
"""

import numpy as np
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from scipy.sparse import issparse
import scipy

class SingleCellDataset(Dataset):

    def __init__(self, data, batch):
        
        self.data = data
        self.batch = batch
        self.shape = data.shape
        
    def __len__(self):
        return self.data.shape[0]
    
    def __getitem__(self, idx):

        domain_id = self.batch[idx]
        x = self.data[idx].toarray().squeeze()

        return x, domain_id, idx

class SingleCellDataset_vertical(Dataset):

    def __init__(self, adatas):

        self.adatas = adatas
        
    def __len__(self):
        return self.adatas[0].shape[0]
    
    def __getitem__(self, idx):

        x = self.adatas[0].X[idx].toarray().squeeze()

        for i in range(1, len(self.adatas)):

            x = np.concatenate((x, self.adatas[i].X[idx].toarray().squeeze()))

        return x, idx
    
def load_data(adatas, mode='h', use_rep=['X','X'], num_cell=None, max_gene=None, adata_cm=None, use_specific=False, domain_name='domain_id', batch_size=256, \
    drop_last=True, shuffle=True, num_workers=4):

    '''
    Load data for training.

    Parameters
    ----------
    adatas
        A list of AnnData matrice.
    mode
        training mode. Choose between ['h', 'd', 'v'].
    use_rep
        use '.X' or '.obsm'.
    num_cell
        numbers of cells of each adata in adatas.
    max_gene
        maximum number of genes of each adata in adatas.
    adata_cm
        adata with common genes of adatas.
    use_specific
        use dataset-specific genes.
    domain_name
        domain name of each adata in adatas.
    batch_size
        size of each mini batch for training.
    drop_last
        drop the last samples that not up to one batch.
    shuffle
        shuffle the data
    num_workers
        number parallel load processes according to cpu cores.

    Returns
    -------
    trainloader
        data loader for training
    testloader
        data loader for testing
    '''

    if mode == 'd':

        for i, adata in enumerate(adatas):

            if use_rep[i]=='X':
                tmp = adata.X
            else:
                tmp = adata.obsm[use_rep[i]]
            if tmp.shape[1] < max_gene:
                tmp =  scipy.sparse.hstack((tmp, scipy.sparse.coo_matrix(np.zeros((tmp.shape[0], max_gene-tmp.shape[1])))))
            if i == 0:
                x = tmp
                batches = adata.obs[domain_name].astype(int).tolist()
            else:
                x = scipy.sparse.vstack((x, tmp))
                batches.extend(adata.obs[domain_name])
        
        x = x.tocsr()

        scdata = SingleCellDataset(x, batches)
    
    elif mode == 'h':
        batches = adata_cm.obs[domain_name].cat.categories.tolist()

        if use_specific:

            for i, adata in enumerate(adatas):
            
                adata_tmp = adata_cm[adata_cm.obs[domain_name]==batches[i],]

                x_c = adata_tmp.X

                x_s = adata.X

                if x_s.shape[1] < max_gene:

                    x_s = scipy.sparse.hstack((x_s, scipy.sparse.coo_matrix(np.zeros((x_s.shape[0], max_gene-x_s.shape[1])))))

                if i == 0:
                    x = scipy.sparse.hstack((x_c, x_s))
                else:
                    x =  scipy.sparse.vstack((x, scipy.sparse.hstack((x_c, x_s))))
                x = x.tocsr()

        else:
            if not issparse(adata_cm.X):
                adata_cm.X = scipy.sparse.csr_matrix(adata_cm.X)
            x = adata_cm.X
            

        scdata = SingleCellDataset(x, adata_cm.obs[domain_name].astype(int).tolist())

    else:
        scdata = SingleCellDataset_vertical(adatas)

    trainloader = DataLoader(
        scdata, 
        batch_size=batch_size, 
        drop_last=drop_last, 
        shuffle=shuffle, 
        num_workers=num_workers,
    )

    testloader = DataLoader(scdata, batch_size=batch_size, drop_last=False, shuffle=False)

    return trainloader, testloader

















