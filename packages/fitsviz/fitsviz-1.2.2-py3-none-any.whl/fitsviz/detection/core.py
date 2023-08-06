"""
This module implements the base class and star finder kernel for
detecting stars in an astronomical image. Each star-finding class should
define a method called ``find_stars`` that finds stars in an image.
"""

from abc import abstractmethod, ABCMeta


class DetectionBase(metaclass=ABCMeta):
    """Base class for detection algorithms,
    new algorithms should inherit from this class and implement
    the get_sources method.

    Args:
        metaclass (_type_, optional): _description_. Defaults to ABCMeta.
    """
    @abstractmethod
    def get_sources(self, science_data, rms_data):
        """Given science and rms files, apply a custom detection algorithm

        Args:
            science_data (np.ndarray): Science data
            rms_data (np.ndarray): RMS data

        Returns:
            table (pd.DataFrame): table with xcentroid,ycentroid,flux,spectral_index as columns. or None
        """
        raise NotImplementedError('Needs to be implemented in a subclass.')

    @abstractmethod
    def get_fluxs(self, sources):
        """Given science and rms files, apply a custom detection algorithm

        Args:
            science_data (np.ndarray): Science data
            rms_data (np.ndarray): RMS data

        Returns:
            table (pd.DataFrame): table with xcentroid,ycentroid,flux,spectral_index as columns. or None
        """
        raise NotImplementedError('Needs to be implemented in a subclass.')

    @abstractmethod
    def get_summary(self, fluxs):
        """Given science and rms files, apply a custom detection algorithm

        Args:
            science_data (np.ndarray): Science data
            rms_data (np.ndarray): RMS data

        Returns:
            table (pd.DataFrame): table with xcentroid,ycentroid,flux,spectral_index as columns. or None
        """
        raise NotImplementedError('Needs to be implemented in a subclass.')
