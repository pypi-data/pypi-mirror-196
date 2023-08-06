import os
import pickle
import tqdm
from multiprocessing import Pool
from torch.utils.data import Dataset
import hashlib
import smart_open
from PIL import Image
from functools import partial
from dioptra.lake.utils import _decode_to_np_array

class ImageDataset(Dataset):
    def __init__(self, dataframe, transform=None):
        """
        A wrapper class on top of torch datasets.
        The goal is to allow either a data streaming from an object store or to cache the data locally and load it from there

        Parameters:
            dataframe: the datagframe to use as a data source
            transform: the transform to be applied when calling __getitem__

        """
        self.cache_dir = os.path.join(
            os.environ.get('DIOPTRA_CACHE_DIR',
            os.path.join(os.path.expanduser('~'), '.dioptra')))
        self.dataframe = dataframe
        self.transform = transform
        self.image_field = 'image_metadata.uri'
        self.use_caching = True

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def __getitem__(self, index, is_prefetch=False):
        """
        Main method to get the dataset items.
        In prefetch mode, it will pull the images from an object store, skip `transform` but won't return them
        If the dataset is already prefetched, the results will be loaded from the cache dir

        Parameters:
            index: index of the datapoint to be retreived
            is_prefetch: whether in prefetch mode or not

        """
        row = self.dataframe.iloc[index].copy()

        if self.image_field in row:
            if self.use_caching:
                row['image'] = self._handle_cache(
                    row[self.image_field], self._download_img, is_prefetch)
            else:
                row['image'] = self._download_img(row[self.image_field])

        if self.transform is not None and not is_prefetch:
            return self.transform(row)

        return row

    def _handle_cache(self, field, field_transform, is_prefetch):
        field_hash = hashlib.md5(field.encode()).hexdigest()
        cached_object_path = os.path.join(self.cache_dir, field_hash)

        if is_prefetch and os.path.exists(cached_object_path):
            return

        if self.use_caching and os.path.exists(cached_object_path):
            with open(cached_object_path, 'rb') as file:
                return pickle.load(file)

        object_transformed = field_transform(field)
        with open(cached_object_path, 'wb') as file:
            pickle.dump(object_transformed, file)
        return object_transformed

    def _download_img(self, image_path):
        return Image.open(smart_open.open(image_path, 'rb'))

    def __len__(self):
        """
        Length of the dataset

        """
        return len(self.dataframe)

    def prefetch_images(self, num_workers=1):
        """
        Run the multi processed prefetch on the dataset
        Parameters:
            num_workers: number of processors to be used

        """
        if not self.use_caching:
            raise RuntimeError('Turn use_caching to True to be able to prefetch images')

        with Pool(num_workers) as my_pool:
            list(tqdm.tqdm(
                my_pool.imap(partial(self.__getitem__, is_prefetch=True), range(self.__len__())),
                total=self.__len__(),
                desc='Prefetching your images ...',
                ncols=100
            ))
