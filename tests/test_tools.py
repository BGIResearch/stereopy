import numpy as np
import pandas as pd
from stereo.tools.dim_reduce import DimReduce
from stereo.tools.clustering import Clustering
from stereo.tools.find_markers import FindMarker
from stereo.tools.spatial_pattern_score import SpatialPatternScore
# from stereo.tools.spatial_lag import SpatialLag
from stereo.tools.cell_type_anno import CellTypeAnno
from stereo.core.stereo_exp_data import StereoExpData

from anndata import AnnData
from stereo.plots.clustering import plot_spatial_cluster
from stereo.plots.scatter import plot_scatter

test_gem = 'D:\projects\data\sgm.gem'
test_exp = 'D:\projects\data\sem.csv'
ref_dir = 'D:\projects\data\FANTOM5'
# test_gem = '/ldfssz1/ST_BI/USER/qindanhua/data/sgm.gem'
# test_exp = '/ldfssz1/ST_BI/USER/qindanhua/data/sem.csv'


def test_exp_data(file_input):
    data = pd.read_csv(file_input, index_col=[0]).dropna()
    data = data.loc[:, (data != 0).any(axis=0)]
    se = StereoExpData(exp_matrix=data.values, cells=data.index, genes=data.columns)
    return se


def test_io(file_input):
    se = StereoExpData(file_input, 'txt', 'bins')
    return se


def test_dim_reduce():
    se = test_io(test_gem)
    dr = DimReduce(se)
    dr.fit()
    return dr
    # dr.method = 'umap'
    # dr.fit()


# cluster
def test_cluster():
    se = test_io(test_gem)
    ct = Clustering(se, normalization=True)
    # dr = test_dim_reduce()
    # ct.pca_x = dr
    ct.method = 'leiden'
    ct.fit()


# maker
def test_maker():
    se = test_io(test_gem)
    fm = FindMarker(se)
    # fm = FindMarker(se, groups=ct.result.matrix)
    fm.fit()
    return fm


def test_sps():
    se = test_io(test_gem)
    sps = SpatialPatternScore(se)
    sps.fit()
    return sps


# def test_spatial_lag():
#     # se = test_io(test_gem)
#     ct = test_cluster()
#     sl = SpatialLag(ct.data, groups=ct.result.matrix)
#     sl.fit()
#     return sl

def test_cell_type():
    se = test_io(test_gem)
    ca = CellTypeAnno(se, ref_dir=ref_dir)
    # ca = CellTypeAnno(se)
    ca.fit()
    return ca
