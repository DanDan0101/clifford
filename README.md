# clifford

`entropy_time.py` and `entropy_hist.py` take the following command line arguments:

* `-L`, default 512
* `-T`, default 256
* `-s`, `--shots`, default 10
* `-t`, default 10
* `-p`, default 0.1
* `-D`, default 1

Output file is `L_T_st_p_D_*.npy`, where `*` is either `zero`, `me`, or `hist`.

## Requirements

NB: PyClifford will not run on Windows. Use a UNIX-based OS instead.

* [`pyclifford`](https://github.com/hongyehu/PyClifford)
* `numba`
* `numpy`
* `scipy`
* `matplotlib`
* `seaborn`
* `tqdm`
* `multiprocess`

## References

* [Measurement-driven entanglement transition in hybrid quantum circuits](https://doi.org/10.1103/PhysRevB.100.134306)
* [Absence of localization in two-dimensional Clifford circuits](https://doi.org/10.1103/PRXQuantum.4.030302)
* [Random Quantum Circuits](https://doi.org/10.1146/annurev-conmatphys-031720-030658)