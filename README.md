[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# DurianSat SAT solver
MapleLCMDistChronoBTv3 from SAT Race '19 with some new heuristics implemented. Our [SAT 2020 paper](https://arxiv.org/abs/2005.04850) describes Decaying Polarity Score and LSIDS, which are available in [decay-pol](https://github.com/meelgroup/duriansat/tree/decay-pol) and [lsids](https://github.com/meelgroup/duriansat/tree/lsids) branches respectively.

## Compiling in Linux
To build and install, issue:
```
# getting the code
git clone https://github.com/meelgroup/duriansat
cd duriansat/simp
make
```
### Running
```
./glucose filename.cnf
