/* block for user defined functions */
functions {
  // return E(z)
  real E(real z, array[] real theta) {
    real Omega_b = theta[2];
    real Omega_c = theta[3];
    real Omega_r = theta[4];
    real Omega_L = theta[5];

    return ((Omega_b + Omega_c)*(1.0+z)^3 + Omega_r*(1.0+z)^4 + Omega_L)^0.5;
  }

  // return f(z)
  real f(real z, array[] real theta) {
   real h = theta[1];
   real Omega_b = theta[2];

   real Tcmb = 2.7255;  // Zhai2018
   real Rb = 31500*Omega_b*(h^2)*((2.7/Tcmb)^4);

   return (3*(1+Rb/(1+z)))^0.5;
  }

  // return v'(z) ≡ 1/E(z)
  vector dvdz(real z, vector y, array[] real theta) {
    vector[1] yderiv = [1.0/E(z, theta)]';
    return yderiv;
  }

  // return 1/[E(z)*f(z)]
  real integrand(real x, real xc, array[] real theta, array[] real x_r, array[] int x_i) {
    return 1/(E(x, theta)*f(x, theta));
  }
}

/* block for datasets used */
data {
  real la_exp;
  real la_error;
  real R_exp;
  real R_error;
  real wb_exp;
  real wb_error;
}

/* block for transformed data */
transformed data {
  // create null data values to give to integrate_1d because it's required
  array[0] real x_r;
  array[0] int x_i;

  // inverse of the covariance matrix
  // computed with auxiliary script available in this repository
  matrix[3,3] Cinv;
  Cinv[1,1] = 70.41272413  ; Cinv[1,2] = -472.33176518  ; Cinv[1,3] = 4150.71131541;
  Cinv[2,1] = -472.33176518; Cinv[2,2] = 31027.46200904 ; Cinv[2,3] = 477813.59257032;
  Cinv[3,1] = 4150.71131541; Cinv[3,2] = 477813.59257032; Cinv[3,3] = 30083780.34236922;
}

/* block for model parameters */
parameters {
  // lower bound for the Hubble constant is 0
  real<lower=0> h;

  // no lower bound of either to provide extra statistical freedom
  real Omega_b;
  real Omega_c;
}

/* block for transformed parameters */
transformed parameters {
  // Ωr is a derived parameter from ωr
  // no lower bound because it's expected to be close to 0
  real wr = 4.15*10^(-5);
  real Omega_r = wr/h^2;

  // conservation laws to obtain Omega_L
  real Omega_L = 1 - Omega_c - Omega_b - Omega_r;

  // (pseudo) parameter array
  array[5] real theta = {h, Omega_b, Omega_c, Omega_r, Omega_L};

  // compute zstar
  real g1 = (0.0783*(Omega_b*h^2)^(-0.238)) / (1 + 39.5*(Omega_b*h^2)^0.763);
  real g2 = 0.560 / (1 + 21.1*(Omega_b*h^2)^1.81);
  real zstar = 1048 * (1 + 0.00124*(Omega_b*h^2)^(-0.738)) * (1+g1*((Omega_b + Omega_c)*h^2)^g2);

  // compute v ≡ v(zstar) ≡ the integral of 1/E(x) from 0 to zstar
  real z0 = 0;          // initial conditions: v(0) = 0
  vector[1] v0 = [0]';  // .
  array[1] vector[1] sol_v = ode_rk45(dvdz, v0, z0, {zstar}, theta);
  real v = sol_v[1][1];

  // compute the integral of 1/(E(x)*f(x)) from zstar to ∞
  real g = integrate_1d(integrand, zstar, positive_infinity(), theta, x_r, x_i);

  // shift parameters
  real la = pi()*v/g;
  real R = sqrt(Omega_b + Omega_c)*v;
  real wb = Omega_b*h^2;

  // difference vector between the model predictions and the observations
  vector[3] x = [la - la_exp, R - R_exp, wb - wb_exp]';
}

/* block for model definition */
model {
  // priors
  h ~ normal(0.7, 1);
  Omega_b ~ normal(0.05, 1);
  Omega_c ~ normal(0.25, 1);

  // increase log likelihood
  target += -x'*Cinv*x;
}

/* block for generated quantites */
generated quantities {
}
