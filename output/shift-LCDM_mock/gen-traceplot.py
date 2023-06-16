
import os
import matplotlib.pyplot as plt
import arviz as az
posterior = az.from_cmdstan(posterior=os.path.dirname(__file__) + '/chain/*.csv', save_warmup=True)
az.plot_trace(posterior, var_names=('h', 'Omega_b', 'Omega_c'), compact=False, combined=False)
plt.tight_layout()
plt.savefig(os.path.dirname(__file__) + '/analysis/traceplot.png')

