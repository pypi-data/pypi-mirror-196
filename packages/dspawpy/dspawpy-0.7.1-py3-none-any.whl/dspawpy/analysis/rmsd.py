from pymatgen.core.structure import Structure
import numpy as np
from typing import List
from dspawpy.analysis.aimd_traj import _read_h5
import matplotlib.pyplot as plt
import os

class RMSD:
    def __init__(self, structures: List[Structure]):
        self.structures = structures

        self.n_frames = len(self.structures)
        self.n_particles = len(self.structures[0])
        self.lattice = self.structures[0].lattice

        self._position_array = np.zeros(
            (self.n_frames, self.n_particles, 3))

        for i, s in enumerate(self.structures):
            self._position_array[i, :, :] = s.frac_coords

    def run(self, base_index=0):
        result = np.zeros(self.n_frames)
        rd = np.zeros((self.n_frames, self.n_particles, 3))
        for i in range(1, self.n_frames):
            disp = self._position_array[i, :, :] - \
                self._position_array[i - 1, :, :]
            # mic by periodic boundary condition
            disp[np.abs(disp) > 0.5] = disp[np.abs(disp) > 0.5] - \
                np.sign(disp[np.abs(disp) > 0.5])
            disp = np.dot(disp, self.lattice.matrix)
            rd[i, :, :] = disp
        rd = np.cumsum(rd, axis=0)

        for i in range(self.n_frames):
            sqdist = np.square(rd[i] - rd[base_index]).sum(axis=-1)
            result[i] = sqdist.mean()

        return np.sqrt(result)


def get_Structures(aimdh5: str = 'aimd.h5'):
    """get pymatgen structures from aimd.h5 file
    """
    Nstep, elements, positions, lattices = _read_h5(aimdh5)
    strs = []
    for i in range(Nstep):
        strs.append(Structure(lattices[i], elements, positions[i], coords_are_cartesian=True))
    return strs


def build_structure_list(filepath):
    if filepath.endswith('.json'):
        from monty.serialization import loadfn
        # Parse the DiffusionAnalyzer object from json file directly
        obj = loadfn(filepath)
        structure_list = []
        for i, s in enumerate(obj.get_drift_corrected_structures()):
            structure_list.append(s)
            if i == 9:
                break
    elif filepath.endswith('.h5'):
        # create Structure structure_list from aimd.h5
        structure_list = get_Structures(filepath)
    else:
        raise ValueError("File format not supported")

    return structure_list


def rmsd_analysis(datafile:str):
    """AIMD计算后分析rmsd并画图

    Parameters
    ----------
    datafile : str
        aimd.h5或aimd.json文件或包含这两个文件之一的目录

    Returns
    -------
    rmsd分析结果

    Examples
    --------
    >>> from dspawpy.analysis.rmsd import rmsd_analysis
    >>> rsmd_result = rmsd_analysis(datafile='aimd.h5')
    >>> print(rsmd_result)
    """
    # 寻找数据源文件
    if datafile.endswith(".h5") or datafile.endswith(".json"):
        df = datafile
    elif os.path.exists(os.path.join(datafile, 'aimd.h5')):
        df = os.path.join(datafile, 'aimd.h5')
    elif os.path.exists(os.path.join(datafile, 'aimd.json')):
        df = os.path.join(datafile, 'aimd.json')
    else:
        raise FileNotFoundError("不存在相应的aimd.h5或aimd.json文件！")
    
    # 开始分析数据
    print(f'Reading {os.path.abspath(df)}...')
    strs = build_structure_list(df)
    result = RMSD(structures=strs).run()
    
    return result
