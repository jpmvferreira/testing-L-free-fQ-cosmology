#!/usr/bin/env python3

# tentar meter isto a variar a escala do matplotlib e meter a tracejado a regiao assintotica no infinito meio transparente (tb precisa de se ajustar ao valor dos parametros)

# imports
import matplotlib.pyplot as plt
import matplotlib.widgets as mplw
from scipy.special import lambertw
from scipy.optimize import fsolve
from math import exp

## fotis
def f(E, z, Om):
    l  = 0.5 + lambertw(-Om/(2*exp(0.5))).real   # compute lambda twice :(

    return (E**2 - 2*l)*exp(l/E**2) - Om*(1+z)**3

def E_fotis(z, Om):
    x0 = 10*z + 0.1                     # random inital value
    E = fsolve(f, x0, args=(z, Om))[0]  # solve for E(z) numerically

    return E

# correction
# M in units of H0
def correction(z, Ωr, Ωm):
    λ  = 0.5 + lambertw(-Ωm/(2*exp(0.5))).real   # lambda
    E2 = E_fotis(z, Ωm)**2
    # to-do: resolver eq de friedmann modificada para obter E2 (E²)
    return ( ((1-λ)/(1-λ/E2) )**0.5) * exp(λ/2 * (1-1/E2))

def run(Ωm, Ωr, zmax, N):
    redshifts = []
    values = []

    for i in range(0, N):
        redshift = (i/N)*zmax
        value = correction(redshift, Ωr, Ωm)

        redshifts.append(redshift)
        values.append(value)

    return redshifts, values

def main():
    # initial guess for M and Ωm
    M = 0
    Ωm = 0.335
    Ωr = 0.0001

    # number of points to compute the correction
    N = 10000

    # maximum redshift
    zmax = 10

    # get redshifts and values with the parameters defined so far
    redshifts, values = run(Ωm, Ωr, zmax, N)

    # fancy stuff for the plot
    plt.subplots_adjust(left=0.12, bottom=0.32)
    plt.axis([0, 10, 0, 2])
    plt.xlabel("redshift")
    plt.ylabel("$d_L^{(gw)}/d_L$")
    plt.grid()

    # actually plot something
    l, = plt.plot(redshifts, values)

    ## create sliders
    ΩrAx = plt.axes([0.15, 0.15, 0.65, 0.03])
    ΩmAx = plt.axes([0.15, 0.10, 0.65, 0.03])
    ΩrSlider = mplw.Slider(ΩrAx, 'Ωr', -2, 4, valinit=0)
    ΩmSlider = mplw.Slider(ΩmAx, 'Ωₘ', 0, 1, valinit=0.335)

    ## update defined here because matplotlib is god awful sometimes
    def update(val):
        redshifts, values = run(ΩrSlider.val, ΩmSlider.val, zmax, N)
        l.set_xdata(redshifts)
        l.set_ydata(values)

    ## set to run function update() on slider change
    ΩrSlider.on_changed(update)
    ΩmSlider.on_changed(update)

    # show!
    plt.show()

    return

if __name__ == "__main__":
    main()
