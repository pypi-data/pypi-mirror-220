"""
    Copyright (C) 2022-2023, Michele Cappellari

    E-mail: michele.cappellari_at_physics.ox.ac.uk

    Updated versions of the software are available from my web page
    https://purl.org/cappellari/software

    This software is provided as is without any warranty whatsoever.
    Permission to use, for non-commercial purposes is granted.
    Permission to modify for personal or internal use is granted,
    provided this copyright and disclaimer are included unchanged
    at the beginning of the file. All other rights are reserved.
    In particular, redistribution of the code is not allowed.

Changelog
---------

V1.0.0: Michele Cappellari, Oxford, 17 January 2022
  - Written and tested as a separate procedure.
Vx.x.x: Additional changes are documented in the CHANGELOG of the JamPy package.

"""

import numpy as np
import matplotlib.pyplot as plt

from mgefit.mge_fit_1d import mge_fit_1d
from jampy.jam_axi_proj import jam_axi_proj
from jampy.cosmology_distance import angular_diameter_distance
from plotbin.plot_velfield import plot_velfield

###############################################################################

def sersic_profile(n, rad):
    """ Sersic profile with rad=R/Re """

    # This has a maximum absolute error of 5.6e-4 in the interval n = [0.2, 16]
    k = 0.000207/n**2 + 0.015987/n - 0.34025 + 2.0015*n
    surf = np.exp(-k*(rad)**(1/n))   # r^(1/n) Sersic profile

    return surf  # Profile is NOT normalized

###############################################################################

def sersic_mge(n_ser, ngauss, lg_rmax, plot, quiet):
    """ MGE for a Sersic profile """

    m = 300 # Number of values to sample the profile for the fit
    r = np.logspace(-lg_rmax, lg_rmax, m)
    rho = sersic_profile(n_ser, r)
    w = rho > rho[0]/1e40  # samples at most 40 orders of magnitude in density
    total_counts, sigma = mge_fit_1d(r[w], rho[w], ngauss=ngauss, plot=plot,
                                     rbounds=[np.min(r)/2, np.max(r)], quiet=quiet).sol
    surf = total_counts/(np.sqrt(2*np.pi)*sigma)  # Surface density in Msun/pc**2

    if plot:
        plt.pause(1)
        plt.clf()

    return surf, sigma

###############################################################################

def jam_axi_sersic_mass(re_maj_ser, n_ser, qobs, qintr, sigma_ap, sigma_ap_err,
                        dxy_ap, sigma_psf, distance, beta=0., ngauss=16,
                        lg_rmax=2., plot=True, quiet=False):
    """
    Compute the mass M_Ser and uncertainty of a mass-follow-light Sersic model,
    at the given distance, that produces a given second moment of the stellar
    velocity sigma_ap inside a rectangular aperture of sides dxy_ap, assuming an
    intrinsic axial ratio qintr.
    Ideally, the Sersic model should be fitted to the photometry in a band close
    to the wavelength of the spectroscopic observations used to extract sigma_ap.

    The physical meaning of M_Ser is the following: when divided by the total
    luminosity L_Ser of the Sersic model in a given band, then

        (M/L)_e = M_Ser/L_Ser

    closely approximates the average mass-to-light ratio in the same band,
    within a sphere of radius R_e equal to the projected hal-light radius.
    (see Cappellari+13 https://ui.adsabs.harvard.edu/abs/2013MNRAS.432.1709C)

    This procedure is meant as a simple replacement for the less accurate virial
    mass estimators.

    """
    assert qintr <= qobs, "Must be `qintr <= qobs`"
    inc = np.degrees(np.arctan2(np.sqrt(1 - qobs**2), np.sqrt(qobs**2 - qintr**2)))

    # Adopt as reference an arbitrary galaxy mass and find how much I need to
    # scale it to match the observed sigma
    mass = 1e11

    pc = distance*np.pi/0.648  # Factor to convert arcsec --> pc (with distance in Mpc)
    surf, sigma = sersic_mge(n_ser, ngauss, lg_rmax, plot, quiet)
    sigma = sigma*re_maj_ser
    qobs_mge = np.full_like(sigma, qobs)            # projected axial ratio

    mtot = (2*np.pi*surf*qobs_mge*(sigma*pc)**2).sum()
    surf *= mass/mtot  # Rescale MGE to have input total mass

    dx, dy = dxy_ap
    d = max(dx, dy)
    npix = 100    # pixels discretizing the aperture
    x, pixsize = np.linspace(-d/2, d/2, npix, retstep=True)   # Avoids (0, 0)
    xbin, ybin = map(np.ravel, np.meshgrid(x, x))
    beta = np.full_like(sigma, beta)
    mbh = mass*0.002   # 0.2% BH mass

    jam = jam_axi_proj(surf, sigma, qobs_mge, surf, sigma, qobs_mge,
                       inc, mbh, distance, xbin, ybin, beta=beta,
                       sigmapsf=sigma_psf, pixsize=pixsize, quiet=quiet)

    w = (np.abs(xbin) < dx/2) & (np.abs(ybin) < dy/2)  
    sigma_ap2 = (jam.flux[w]*jam.model[w]**2).sum()/jam.flux[w].sum()
    lg_mjam = np.log10(mass*sigma_ap**2/sigma_ap2)
    d_lg_mjam = 2*sigma_ap_err/(sigma_ap*np.log(10))   # error propagation

    if not quiet:
        print(f'lg(M_JAM/M_Sun) = ({lg_mjam:.2f} +/- {d_lg_mjam:.2f})')

    if plot:
        plot_velfield(xbin, ybin, jam.model, flux=jam.flux, nodots=1)
        plt.plot(xbin[~w], ybin[~w], '+')
        plt.title("JAM $V_{\\rm rms}$")
        plt.pause(1)

    return lg_mjam, d_lg_mjam

###############################################################################

def jam_axi_sersic_mass_example():
    """Usage example for jam_axi_sersic_mass"""

    # Input parameters
    dxy_ap = [1.1, 0.7]     # sides of rectangular aperture in arcsec
    n_ser = 2.57            # Sersic exponent (e.g. n = 4 --> de Vaucouleurs)
    qobs = 0.656            # Observed axial ratio of the fitted Seric model
    qintr = 0.4             # assumed intrinsic axial ratio
    beta = 0.2              # anisotropy beta = 1 - (sig_z/sig_R)^2
    re_maj_ser = 0.67       # arcsec. Semimajor axis half-light ellipse of Sersic model
    sigma_psf = 0.5/2.355   # dispersion of the PSF in arcsec
    redshift = 0.8          # galaxy redshift
    sigma_ap = 166          # km/s. Observed second velocity moment (sigma)
    sigma_ap_err = 19       # km/s. 1sigma uncertainty on sigma_ap

    # Computation
    dist_ang = angular_diameter_distance(redshift)  # D_A angular diameter distance
    lg_mjam = jam_axi_sersic_mass(re_maj_ser, n_ser, qobs, qintr, sigma_ap,
                                  sigma_ap_err, dxy_ap, sigma_psf, dist_ang, beta=beta)

###############################################################################

if __name__ == '__main__':

    jam_axi_sersic_mass_example()
