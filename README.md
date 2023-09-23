## About
Source code for the article [PhysRevD.108.063521](https://link.aps.org/doi/10.1103/PhysRevD.108.063521), available for free at [arXiv:2396.10186](https://arxiv.org/abs/2306.10176): "Testing Λ-free f(Q) Cosmology".

This study relies on previous published work, which is available at [jpmvferreira/forecasting-FQ-cosmology-with-SS](https://github.com/jpmvferreira/forecasting-FQ-cosmology-with-SS).


## Table of contents
- [Repository outline](#repository-outline)
- [Virtual environment](#virtual-environment)
- [Citation](#citation)
- [Feedback](#feedback)
- [License](#license)


## Repository outline
- `/analyzed`: Includes processed data, mainly plots.
- `/aux`: Auxiliary scripts to aid in analysis or in automation.
. `/config`: The configuration files used for the command line interface of the [Stan](https://mc-stan.org/) programming language, [cmdstan](https://mc-stan.org/users/interfaces/cmdstan.html).
- `/data`: The real and mock datasets with the values of the shift parameters.
- `/jobs`: Bash scripts to run the MCMC's locally or via the [slurm](https://slurm.schedmd.com/documentation.html) workload manager.
- `/model`: The cosmological models to be constrained using [cmdstan](https://mc-stan.org/users/interfaces/cmdstan.html).
- `/output`: The output of the MCMC's (chains, plots, diagnostics, and backup of the data+model+config used).
- `/venv`: The virtual environment used to carry out our analysis.

## Virtual environment
To replicate the virtual environment start by cloning this repository locally using `git` to a specific folder (using "shift-params" as an example):
```console
$ git clone https://github.com/jpmvferreira/testing-L-free-fQ-cosmology shift-params
```

Use `conda` (or any other compatible package manager) to create a new virtual environment from the file `shift-params/venv/environment.yml`, which the default name is "msc" and is enconded on the file:
```console
$ conda env create -f fqgw/venv/environment.yml
```

Activate the newly created environment:
```console
$ conda activate msc
```

Use `pip` to install all Python packages listed in `fqgw/venv/environment.yml`:
```console
$ pip install -r shift-params/venv/requirements.txt
```

## Citation
If you used any of the contents available in this repository, or found it useful in any way, you can cite it using the following BibTeX entry:
```
@article{Ferreira2023,
  title = {Testing $\Lambda$-free $f(Q)$ cosmology},
  author = {Ferreira, Jos\'e and Barreiro, Tiago and Mimoso, Jos\'e P. and Nunes, Nelson J.},
  journal = {Phys. Rev. D},
  volume = {108},
  issue = {6},
  pages = {063521},
  numpages = {9},
  year = {2023},
  month = {Sep},
  publisher = {American Physical Society},
  doi = {10.1103/PhysRevD.108.063521},
  url = {https://link.aps.org/doi/10.1103/PhysRevD.108.063521}
}
```


## Feedback
Any discussion, suggestions or bug reports are always welcome. To do so, feel free to use this issue section in this repository or send me an email at:
- Personal email: [jose@jpferreira.me](mailto:jose@jpferreira.me) - [[PGP key](https://pastebin.com/raw/REkhQKg2)]
- Institutional email: [jpmferreira@fc.ul.pt](mailto:jpmferreira@fc.ul.pt) - [[PGP key](https://pastebin.com/raw/AK2trPBw)]


## License
All of the contents provided in this repository are available under the MIT license.

For further information, refer to the file [LICENSE.md](./LICENSE.md) provided in this repository.
