import warnings
# warnings.filterwarnings("ignore")
from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.nddata.utils import Cutout2D
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales
from reproject import reproject_adaptive, reproject_exact, reproject_interp
import getpass
import time

from .wcs import transform_wcs


def zscale(img, vmin=None, vmax=None):
    """
    Normalization of zscale.
    Input is a 2D numpy array.

    Return a Normalization class to be used with Matplotlib.
    """
    from astropy.visualization import (ImageNormalize, LinearStretch,
                                       ZScaleInterval)
    if vmin is None:
        if vmax is None:
            norm = ImageNormalize(img, interval=ZScaleInterval(), stretch=LinearStretch())
        else:
            norm = ImageNormalize(img, interval=ZScaleInterval(), stretch=LinearStretch(), vmax=vmax)
    else:
        if vmax is None:
            norm = ImageNormalize(img, interval=ZScaleInterval(), stretch=LinearStretch(), vmin=vmin)
        else:
            norm = ImageNormalize(img, interval=ZScaleInterval(), stretch=LinearStretch(), vmin=vmin, vmax=vmax)
    return norm

def gamma_correction(colorbar, gamma=1.0):
    '''
    Gamma correction for colorbar.
    Input is a colormap instance.

    Return a new colormap instance.
    '''
    from matplotlib import cm
    from matplotlib.colors import ListedColormap
    default = cm.get_cmap(colorbar, 256)
    de_color = default(np.linspace(0, 1, 256))
    newcolors = de_color.copy()
    for i in range(256):
        newcolors[i, :] = de_color[int(255 * np.power(i/255, gamma)), :]
    return ListedColormap(newcolors)

# build RGB image.
def combine_RGB(b, g, r, fwhm=2, Q=10, stretch=0.05, filename=None):
    from astropy.convolution import Gaussian2DKernel, convolve
    from astropy.stats import gaussian_fwhm_to_sigma
    from astropy.visualization import make_lupton_rgb

    sigma = fwhm * gaussian_fwhm_to_sigma
    kernel = Gaussian2DKernel(sigma, x_size=11, y_size=11)
    g = convolve(g, kernel, normalize_kernel=True)
    r = convolve(r, kernel, normalize_kernel=True)
    b = convolve(b, kernel, normalize_kernel=True)

    if(filename):
        rgb = make_lupton_rgb(r, g, b, Q=Q, stretch=stretch, filename=filename)
    else:
        rgb = make_lupton_rgb(r, g, b, Q=Q, stretch=stretch)

    return rgb

def plot_beam(ax, header, xy=(2,2)):
    import matplotlib.patches as mpatches
    BMAJ = 3600. * header["BMAJ"] # [arcsec]
    BMIN = 3600. * header["BMIN"] # [arcsec]
    BPA =  header["BPA"] # degrees East of North
    print('BMAJ: {:.3f}", BMIN: {:.3f}", BPA: {:.2f} deg'.format(BMAJ, BMIN, BPA))
    # However, to plot it we need to negate the BPA since the rotation is the opposite direction
    # due to flipping RA.
    ax.add_artist(mpatches.Ellipse(xy=xy, width=BMIN, height=BMAJ, angle=-BPA, facecolor="none", color='white',linewidth=3))



class AstroImage:
    def __init__(self, data, header):
        self.data = data
        self.__fix_data__()
        self.header = header
        self.__fix_header__()
        self.wcs = WCS(self.header)

    def __fix_data__(self):
        # fix the data for axes with length 1
        self.data = np.squeeze(self.data)


    def __fix_header__(self):
        """Fix the header for empty axes. Adapted from Qubefit."""
        # update the NAXIS keywords
        axes = ['NAXIS1', 'NAXIS2', 'NAXIS3', 'NAXIS4']
        for cnt, axis in enumerate(axes):
            if cnt >= self.data.ndim:
                break
            if (self.header.get(axis, default=-1) !=
                    self.data.shape[self.data.ndim-cnt-1]):
                self.header[axis] = self.data.shape[self.data.ndim-cnt-1]
        self.header['NAXIS'] = self.data.ndim

        # remove the fourth dimension if not needed
        if self.data.ndim <= 3:
            keys = ['PC04_01', 'PC04_02', 'PC04_03', 'PC04_04',
                    'PC01_04', 'PC02_04', 'PC03_04', 'CTYPE4',
                    'CRVAL4', 'CDELT4', 'CRPIX4', 'CUNIT4',
                    'CROTA4', 'NAXIS4', 'CNAME4', 'PC4_1',
                    'PC4_2', 'PC4_3', 'PC1_4', 'PC2_4', 'PC3_4', 'PC4_4']
            for key in keys:
                self.header.remove(key, ignore_missing=True)

        # remove the third dimension if not needed
        if self.data.ndim <= 2:
            keys = ['PC03_01', 'PC03_02', 'PC03_03', 'PC01_03',
                    'PC02_03', 'CTYPE3', 'CRVAL3', 'CDELT3',
                    'CRPIX3', 'CUNIT3', 'CROTA3', 'NAXIS3', 'CNAME3',
                    'CD3_3', 'PC3_1', 'PC3_2', 'PC3_3', 'PC1_3',
                    'PC2_3']
            for key in keys:
                self.header.remove(key, ignore_missing=True)

    @classmethod
    def read(cls, url, ext=0):
        with fits.open(url) as hdulist:
            data = hdulist[ext].data
            header = hdulist[ext].header
        return cls(data, header)

    @property
    def pixel_scale(self, unit=u.arcsec):
        pscale = proj_plane_pixel_scales(self.wcs)[0] * 3600 * unit
        return pscale.to(unit).value

    @property
    def shape(self):
        x = getattr(self.wcs, 'NAXIS1', np.shape(self.data)[1])
        y = getattr(self.wcs, 'NAXIS2', np.shape(self.data)[0])
        return x, y

    @property
    def skycenter(self):
        ra, dec = np.array(self.wcs.wcs_pix2world(*self.pixcenter, 0))
        return ra, dec

    @property
    def pixcenter(self):
        x, y = self.shape
        x, y = (x-1)/2, (y-1)/2
        return x, y

    @property
    def hdu(self):
        return fits.ImageHDU(data=self.data, header=self.header)

    @property
    def footprint(self):
        return AstroImage(data=(~np.isnan(self.data)).astype(float), header=self.header)

    def __repr__(self, plot=True):
        __info__ = """
        Image information:
        ------------------
        Image shape: {} pixels <-> {:.3f} x {:.3f} arcsec
        Image center: {:.7f}, {:.7f} (RA, Dec)
        Pixel scale: {:.3f} arcsec/pixel
        """.format(self.shape, self.shape[0] * self.pixel_scale, self.shape[1] * self.pixel_scale,
        self.skycenter[0], self.skycenter[1], self.pixel_scale)

        if(plot):
            self.preview()
        return __info__

    def save(self, url):
        hdu = fits.PrimaryHDU(self.data, header=self.header)
        hdu.writeto(url, overwrite=True)

    def preview(self, color_map='gray_r', gamma=1.0, colorbar=True, **kwargs):
        fig, ax = plt.subplots(figsize=(6, 6), dpi=100, subplot_kw={'projection': self.wcs})
        norm = zscale(self.data)
        if(gamma == 1):
            img = ax.imshow(self.data, cmap=color_map,
                            norm=norm, origin='lower')
        else:
            img = ax.imshow(self.data, cmap=gamma_correction(
                color_map, gamma=gamma), norm=norm, origin='lower')
        ax.set_xlabel('RA')
        ax.set_ylabel('Dec')
        if(colorbar):
            fig.colorbar(img, ax=ax, shrink=0.8)
        return fig, ax

    def cutout(self, coord, size, coord_unit=u.deg, size_unit=u.arcsec, mode='partial'):
        if(coord_unit == u.deg):
            coord = SkyCoord(coord[0], coord[1], unit='deg')
        if(size_unit == u.arcsec):
            size = size * size_unit
        elif(size_unit == 'pixel'):
            size = size
        hdu_crop = Cutout2D(self.data, position=coord, size=size,
                            wcs=self.wcs, mode=mode)
        wcs_crop = hdu_crop.wcs
        header = self.header.copy()
        header.update(wcs_crop.to_header())
        header['history'] = f"Image cropped with AstroMy by {getpass.getuser()} on {time.strftime('%Y/%m/%d %H:%m', time.localtime())}"
        header['coord'] = f"{coord.ra.value:.6f}, {coord.dec.value:.6f}"
        header['size'] = f"{size} {size.unit}"

        return AstroImage(data=hdu_crop.data, header=header)

    def rotate(self, angle, algorithm='interpolation'):
        input_wcs = deepcopy(self.wcs)
        input_wcs.wcs.crpix = self.pixcenter
        input_wcs.wcs.crval = self.skycenter
        output_wcs = transform_wcs(input_wcs, rotation=np.deg2rad(angle))
        if(algorithm == 'interpolation'):
            data = reproject_interp(self.hdu, output_wcs, shape_out=np.array(self.shape), return_footprint=False)
        elif(algorithm == 'exact'):
            data = reproject_exact(self.hdu, output_wcs, shape_out=np.array(self.shape), return_footprint=False)
        elif(algorithm == 'adaptive'):
            data = reproject_adaptive(self.hdu, output_wcs, shape_out=np.array(self.shape), return_footprint=False, conserve_flux=True)
        else:
            raise ValueError('Algorithm not supported')
        return AstroImage(data=data, header=output_wcs.to_header())

    def mask_blank(self, threshold=10000):
        '''
        Masking the probably border or blank region
        '''
        values, counts = np.unique(self.data, return_counts=True)
        critical_counts = np.mean(counts) + 5*np.std(counts) + threshold
        print("critical counts = ", critical_counts)
        mode_values = values[counts > critical_counts]
        mode_counts = counts[counts > critical_counts]
        for i, m in enumerate(mode_values):
            print(mode_counts[i], " pixels' value is ", m)
            outregion = (self.data == m)
            self.data[outregion] = np.nan
        return self
