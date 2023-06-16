# Notes:
# - u(z) ≡ 1/E(z)

# imports
from scipy.integrate import quad
from scipy.special import lambertw
import numpy as np

# return u(z) ≡ 1/E(z)
def u(z, theta):
    #h = theta[0]
    Omega_b = theta[1]
    Omega_c = theta[2]
    Omega_r = theta[3]
    Omega_L = theta[4]

    return ((Omega_b + Omega_c)*(1+z)**3 + Omega_r*(1+z)**4 + Omega_L)**(-0.5)

# return f(z)
def f(z, theta):
    h = theta[0]
    Omega_b = theta[1]
    #Omega_c = theta[2]
    #Omega_r = theta[3]
    #Omega_L = theta[4]

    Tcmb = 2.7255
    Rb = 31500*Omega_b*h**2*(2.7/Tcmb)**(4)

    return (3*(1 + Rb/(1+z)))**0.5

# return u(z)/f(z)
def uf(z, theta):
    return u(z, theta)/f(z, theta)

# return integral of u(x) ≡ 1/E(x) from 0 to z
def intofu(z, theta):
    sol = quad(u, 0, z, args=(theta,))

    return sol[0]

# return integral of u(x)/f(x), from z to infinity
def intofuf(z, theta):
    sol = quad(uf, z, np.inf, args=(theta,))

    return sol[0]

# main
def main():
    # mock parameters
    h = 0.7
    Omega_b = 0.05
    Omega_c = 0.25
    #Omega_r = 0.0001

    # derive Ωr from ωr (constant) and h
    wr = 4.15*10**(-5);
    Omega_r = wr/h**2;

    # first friedmann equation
    Omega_L = 1 - Omega_b - Omega_c - Omega_r

    # parameter array
    theta = (h, Omega_b, Omega_c, Omega_r, Omega_L)

    # compute zstar
    g1 = (0.0783*(Omega_b*h**2)**(-0.238)) / (1 + 39.5*(Omega_b*h**2)**0.763)
    g2 = 0.560 / (1 + 21.1*(Omega_b*h**2)**1.81)
    zstar = 1048 * (1 + 0.00124*(Omega_b*h**2)**(-0.738)) * (1+g1*((Omega_b + Omega_c)*h**2)**g2)

    # compute shift parameters
    uint = intofu(zstar, theta)
    ufint = intofuf(zstar, theta)
    R = (Omega_b + Omega_c)**0.5 * uint
    la = np.pi*uint/ufint
    wb = Omega_b*h**2

    # give mock errors, print as .json supressing scientific notation
    R_error = 0.001
    la_error = 0.1
    wb_error = 0.0001
    print('{')
    print(f'\t"R_exp": {R:.20f},')
    print(f'\t"R_error": {R_error:.20f},')
    print(f'\t"la_exp": {la:.10f},')
    print(f'\t"la_error": {la_error:.10f},')
    print(f'\t"wb_exp": {wb:.20f},')
    print(f'\t"wb_error": {wb_error:.20f}')
    print('}')

    return

# run if called
if __name__ == "__main__":
    main()
