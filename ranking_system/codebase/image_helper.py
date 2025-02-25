# for resize img
import cv2
# for basic load/save
import os
import requests
import shutil
# logging
import logging


class Helper:
    """
    for resizing image for imagenet
    fixing path to dynamic directory
    """
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.images = self.get_images()
        self.paths = []
        self.fix_path()
        logging.debug('Image helper has been initialized')


    def get_images(self):
        self.images = os.listdir(self.dataset_path)
        return self.images

    def download_images(self, photo_urls):
        """
        download images
        :return: self.images
        """
        for photo_url in photo_urls:
            response = requests.get(photo_url, stream=True)
            with open(self.dataset_path + photo_url.split('/')[-1], 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
        self.images = os.listdir(path=self.dataset_path)
        logging.debug('All photos has been downloaded')

    def resize(self, path, dim=(224,224)):
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        cv2.imwrite(path, resized)

    def fix_path(self):
        """
        help fix paths for all images in dataset_path
        """
        self.get_images()
        for img in self.images:
            self.paths.append(self.dataset_path + img)

    def download_image(self, photo_url):
        """
        for download single image
        :param photo_url: what to download
        :return:photo_path
        """
        response = requests.get(photo_url, stream=True)
        path = self.dataset_path + photo_url.split('/')[-1]
        with open(path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        logging.debug(path+' Has been downloaded')
        return path

    def remove_image(self, photo_path):
        os.remove(photo_path)
        logging.debug(photo_path + ' Has been removed')
