# Notes:
# - u(z) ≡ 1/E(z)

# imports
from scipy.integrate import odeint, quad
from scipy.special import lambertw
from math import exp, sqrt
import numpy as np

# return u'(z)
def dudz(u, z, theta):
    #h = theta[0]
    Omega_b = theta[1]
    Omega_c = theta[2]
    Omega_r = theta[3]
    l = theta[4]

    f1 = exp(-l*u**2) / (l*u*(u**(-2)-2*l) - u**(-3))
    f2 = 1.5*(Omega_b + Omega_c)*(1+z)**2 + 2*Omega_r*(1+z)**3

    return f1*f2

# return u(z)
def u(z, theta):
    # initial conditions plus desired time to get the value of u(z)
    t = [0, z]
    u0 = 1

    # solve using ODE solver
    sol = odeint(dudz, u0, t, args=(theta,))

    return float(sol[1])

# return f(z)
def f(z, theta):
    h = theta[0]
    Omega_b = theta[1]
    #Omega_c = theta[2]
    #Omega_r = theta[3]
    #l = theta[4]

    Tcmb = 2.7255
    Rb = 31500*Omega_b*h**2*(2.7255/2.7)**(-4)

    return (3*(1 + Rb/(1+z)))**0.5

# return u(z)/f(z)
def uf(z, theta):
    return u(z, theta)/f(z, theta)

# return integral of u(x), from 0 to z
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

    # lambda
    l = 0.5 + lambertw(-(Omega_b + Omega_c + Omega_r)/(2*exp(0.5))).real

    # (pseudo) parameter array
    theta = (h, Omega_b, Omega_c, Omega_r, l)

    # compute zstar
    g1 = 0.0783*(Omega_b*h**2)**(-0.238) / (1 + 39.5*(Omega_b*h**2)**0.763)
    g2 = 0.560 / (1 + 21.1*(Omega_b*h**2)**1.81)
    zstar = 1048 * (1 + 0.00124*(Omega_b*h**2)**(-0.738)) * (1+g1*((Omega_b + Omega_c)*h**2)**g2)

    # compute shift parameters
    uint = intofu(zstar, theta)
    ufint = intofuf(zstar, theta)
    R = sqrt(Omega_b + Omega_c) * uint
    la = np.pi*uint/ufint
    wb = Omega_b*h**2

    # give mock errors, print as .json supressing scientific notation
    R_error = 0.001
    la_error = 0.1
    wb_error = 0.0001
    print('{')
    print(f'\t"R_exp": {R:.10f},')
    print(f'\t"R_error": {R_error:.10f},')
    print(f'\t"la_exp": {la:.10f},')
    print(f'\t"la_error": {la_error:.10f},')
    print(f'\t"wb_exp": {wb:.10f},')
    print(f'\t"wb_error": {wb_error:.10f}')
    print('}')

    return

# run if called
if __name__ == "__main__":
    main()
