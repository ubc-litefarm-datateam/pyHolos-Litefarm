import os 
import pandas as pd 

class CropChecker:
    """
    A class used to check the existence of a crop in  crop list.

    Attributes
    ----------
    path : str
        The file path to the crop list CSV.
    list : list
        A list of crop names from the crop list.
    crop_name : str
        The crop name to check.

    Methods
    -------
    crop_exists()
        Checks whether the crop exists in the crop list.
    """

    def __init__(self, crop_name):
        """
         Initializes the CropChecker with the path to the crop list and the crop name to check.

        Parameters
        ----------
        crop : str
            The crop name to check.
        """
        self.path = os.path.join(os.path.dirname(__file__), '../../data/preprocessed/crop_to_group.csv')
        self.list = pd.read_csv(self.path)['crop'].to_list()
        self.crop_name = crop_name

    def crop_exists(self):
        """
        Checks whether the crop exists in the crop list.

        Returns
        -------
        bool
            True if the crop exists in the list, False otherwise.

        Examples
        --------
        >>> checker = CropChecker("Wheat")
        >>> checker.crop_exists()
        True

        >>> checker = CropChecker("NonexistentCrop")
        >>> checker.crop_exists()
        False
        """
        return self.crop_name in self.list

