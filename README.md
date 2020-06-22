[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# DurianSat SAT solver
DurianSat is a SAT solver that implements some newly proposed phase selection heuristics in [SAT 2020 paper](https://arxiv.org/abs/2005.04850) which leads to a good performance gain in MapleLCMDistChronoBTv3 (the SAT Race '19 winner).  

The proposed heuristics - Decaying Polarity Score and LSIDS are available in [decay-pol](https://github.com/meelgroup/duriansat/tree/decay-pol) and [lsids](https://github.com/meelgroup/duriansat/tree/lsids) branches respectively.

## Compiling in Linux
To build and install, issue:
```
# getting the code
git clone https://github.com/meelgroup/duriansat
git checkout <branchname>
cd duriansat/simp
make
```
### Running
```
./duriansat filename.cnf
