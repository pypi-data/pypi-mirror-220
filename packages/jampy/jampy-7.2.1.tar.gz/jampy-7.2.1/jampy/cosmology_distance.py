"""
 NAME:
    comoving_distance
       
 PURPOSE: 
    Calculate comoving distance (in Mpc) of an object given its redshift

    V1.0.0: Michele Cappellari, Oxford, 6 June 2016
    V1.1.0: Included angular_diameter_distance and luminosity_distance.
        MC, Oxford, 17 August 2022

"""

import numpy as np

from jampy.quad1d import quad1d

###############################################################################

def integrand(z, omega_m, omega_k, omega_lam):
    """
    Equation (14) of Hogg-99 http://arxiv.org/abs/astro-ph/9905116v4

    """
    ez = np.sqrt(omega_m*(1 + z)**3 + omega_k*(1 + z)**2 + omega_lam)

    return 1/ez

###############################################################################

def comoving_distance(z, h0=70, omega_m=0.3, omega_lam=None):
    """ Comoving distance in Mpc """

    if omega_lam is None:   # flat Universe
        omega_lam = 1 - omega_m

    # Equation (7) of Hogg-99
    omega_k = 1 - omega_m - omega_lam

    c = 299792.458                  #  speed of light in km/s
    dh = c/h0

    is_scalar = np.isscalar(z)
    z = np.atleast_1d(z)
    dc = np.zeros_like(z, dtype=float)
    for i, zi in enumerate(z):  # equation (15) of Hogg-99
        dc[i] = dh*quad1d(integrand, [0, zi], args=(omega_m, omega_k, omega_lam)).integ

    # Equation (16) of Hogg-99
    if omega_k > 0:
        dm = dh*np.sinh(np.sqrt(omega_k)*dc/dh)/np.sqrt(omega_k)
    elif omega_k < 0:
        dm = dh*np.sin(np.sqrt(np.abs(omega_k))*dc/dh)/np.sqrt(np.abs(omega_k))
    else:
        dm = dc

    if is_scalar:
        dm = dm.item()  # Make it a scalar if input was scalar

    return dm
 
##############################################################################

def angular_diameter_distance(z, **kwargs):

    return comoving_distance(z, **kwargs)/(1 + z)

##############################################################################

def luminosity_distance(z, **kwargs):

    return comoving_distance(z, **kwargs)*(1 + z)

##############################################################################

if __name__ == '__main__':

    from cap_lumdist import lumdist

    z = 3.0
    print(lumdist(z, quiet=False))

    dm = comoving_distance(z)

    print("############################################")
    print('Comoving distance:', dm)
    print('Luminosity distance:', dm*(1 + z))
    print('Angular diameter distance:', dm/(1 + z))

    dm = comoving_distance(z, omega_m=0.4, omega_lam=0.3)

    print("############################################")
    print('Comoving distance:', dm)
    print('Luminosity distance:', dm * (1 + z))
    print('Angular diameter distance:', dm / (1 + z))
