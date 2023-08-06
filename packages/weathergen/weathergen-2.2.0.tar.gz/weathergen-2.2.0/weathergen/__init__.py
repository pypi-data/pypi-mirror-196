import time as ttime
import numpy as np
import scipy as sp
import pandas as pd
import h5py, os
from . import utils

base, this_filename = os.path.split(__file__)

class InvalidRegionError(Exception):
    def __init__(self, invalid_region):
        region_string = regions.to_string(columns=['location', 'country', 'latitude', 'longitude', 'altitude'])
        super().__init__(f"The region \'{invalid_region}\' is not supported. Available regions are:\n\n{region_string}")

def get_regions(base):
    regions = pd.read_hdf(f'{base}/regions.h5').fillna('')
    regions = regions.loc[[os.path.exists(f'{base}/region_data/{tag}.h5') for tag in regions.index]]
    return regions

regions = get_regions(base)
region_string = regions.to_string(columns=['location', 'country', 'latitude', 'longitude', 'altitude'])
        
class Quantiles():

    def __init__(self, q):

        self.q = q
        self.n_q = len(q)

class Weather():

    def __init__(self, region='princeton', time=None, verbose=False, mode='random', generate=True):

        if not region in regions.index:
            raise InvalidRegionError(region)

        self.region, self.verbose = region, verbose
        self.entry = regions.loc[self.region]
        self.lat, self.lon, self.alt = regions.loc[self.region, ['latitude', 'longitude', 'altitude']]

        self.quantiles = Quantiles(q=np.linspace(0,1,101))

        filename = f'{base}/region_data/{self.region}.h5'
        self._gen_data = {}
        with h5py.File(filename, 'r') as f:
            for key in list(f.keys()): 
                self._gen_data[key] = f[key][()] if not key == 'gen_labels' else f[key][()].astype(str)

        if generate:
            self.generate(time=time, mode=mode)

        
    def generate(self, time=None, mode='median'):

        if not mode in ['random', 'median']:
            raise ValueError(f"mode must be one of ['random', 'median']")
        if time is None: 
            time = np.atleast_1d(ttime.time()) # if no time is supplied, use current time

        self.time = time

        dt_gen = 1e0 if len(self.time) == 1 else np.gradient(self.time).min() 
        gen_time = np.arange(self.time.min() - dt_gen, self.time.max() + dt_gen, dt_gen)

        n_quantiles = len(self._gen_data['q'])
        n_features  = len(self._gen_data['eigenmodes'])

        n_gen = len(gen_time)
        f_gen = np.fft.fftfreq(n_gen, dt_gen)

        self.year_day = list(map(utils.get_utc_year_day, gen_time))
        self.day_hour = list(map(utils.get_utc_day_hour, gen_time))

        yd_edge_index = self._gen_data['year_day_edge_index']
        dh_edge_index = self._gen_data['day_hour_edge_index']
        yd_knots = self._gen_data['year_day_edge_points']
        dh_knots = self._gen_data['day_hour_edge_points']

        self._gen_data['quantiles']  = self._gen_data['normalized_quantiles'].astype(float)
        self._gen_data['quantiles'] *= self._gen_data['quantiles_scaling']
        self._gen_data['quantiles'] += self._gen_data['quantiles_offset']

        if self.verbose: print('Generating time-ordered distributions …')

        qu = sp.interpolate.RegularGridInterpolator((yd_knots, dh_knots), 
        self._gen_data['quantiles'][yd_edge_index][:,dh_edge_index], 
        method='linear')((self.year_day, self.day_hour)).reshape(n_features * n_gen, n_quantiles, order='F')

        if mode == 'random':
            if self.verbose: print('Generating seeds …')
            GOOD_F_BINS = ~np.isnan(self._gen_data['azdft_binned'])
            AZDFT       = np.c_[[sp.interpolate.interp1d(self._gen_data['azdft_freq'][g], azdft[g], fill_value=0, bounds_error=False, kind='cubic')(f_gen) 
                                                        for azdft, g in zip(self._gen_data['azdft_binned'], GOOD_F_BINS)]]

            GEN_DFT = 2 * AZDFT * np.sqrt(n_gen / dt_gen) * np.exp(1j*np.random.uniform(low=0,high=2*np.pi,size=AZDFT.shape))
            GEN_V   = np.real(np.fft.ifft(GEN_DFT, axis=1))
            GD      = np.matmul(self._gen_data['eigenmodes'], GEN_V)

        else:
            GD = np.zeros((self._gen_data['eigenmodes'].shape[0], n_gen))
            
        gu = np.swapaxes(GD, 0, -1).reshape(n_features * n_gen, order='F')

        bin_data = sp.interpolate.interp1d(self._gen_data['z'], np.arange(n_quantiles), 
                                        bounds_error=False, fill_value='extrapolate')(gu)

        bin_data = np.minimum(np.maximum(bin_data, 0), n_quantiles - 2)

        DATA  = qu[np.arange(len(gu)), bin_data.astype(int)]
        DATA += (bin_data % 1) * (qu[np.arange(len(qu)), bin_data.astype(int) + 1] - DATA)
        DATA  = np.swapaxes(DATA.reshape(n_gen, n_features, order='F'), 0, 1)

        QUANTILES = np.swapaxes(qu.reshape(n_gen, n_features, n_quantiles, order='F'), 0, 1)

        feature_splits = np.r_[0, np.cumsum(self._gen_data['gen_widths'].astype(int))]

        for c, shaped, f0, f1 in zip(self._gen_data['gen_labels'], 
                                     self._gen_data['gen_shaped'], 
                                     feature_splits[:-1],
                                     feature_splits[1:],
                                     ):                                
        
            _resampled = sp.interpolate.interp1d(gen_time, DATA[f0:f1])(self.time)
            _quantiles = sp.interpolate.interp1d(self._gen_data['q'], QUANTILES[f0:f1], axis=-1, fill_value='extrapolate', kind='linear')(self.quantiles.q)

            if not shaped: 
                _resampled = _resampled.reshape(-1)
                _quantiles = _quantiles.reshape(-1, self.quantiles.n_q)

            setattr(self.quantiles, c, _quantiles.mean(axis=-2))
            setattr(self, c, _resampled)

        setattr(self, 'height', self._gen_data['height'])

        # define some stuff
        if 'S' in self.entry.type:

            self.rain_precipitation_rate[self.rain_precipitation_rate < 1e-3] = 0 # we ignore precipitation less than 0.01 mm/hr
            self.snow_precipitation_rate[self.snow_precipitation_rate < 1e-3] = 0
            self.quantiles.rain_precipitation_rate[self.quantiles.rain_precipitation_rate < 1e-3] = 0
            self.quantiles.snow_precipitation_rate[self.quantiles.snow_precipitation_rate < 1e-3] = 0
            
        if 'P' in self.entry.type:

            self.cloud_cover = np.minimum(1, np.maximum(0, self.cloud_cover))

            for k in ['water_vapor', 'ozone', 'ice_water', 'snow_water', 'rain_water', 'liquid_water']:
                setattr(self, f'column_{k}', np.trapz(getattr(self, k), self.height, axis=0))

        self.wind_bearing      = np.degrees(np.arctan2(self.wind_east, self.wind_north) + np.pi)
        self.wind_speed        = np.sqrt(np.square(self.wind_east) + np.square(self.wind_north))
        self.relative_humidity = utils.absolute_to_relative_humidity(self.temperature, self.water_vapor)
        self.relative_humidity = np.minimum(100, np.maximum(1, self.relative_humidity))
        self.dew_point         = utils.get_dew_point(self.temperature, self.relative_humidity)
