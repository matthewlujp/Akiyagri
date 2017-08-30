from __future__ import print_function
from __future__ import division

import numpy as np
import cv2
import re
from datetime import datetime
import os


DEVICE_DIR = '/dev'
CAMERA_DEVICE_PATTERN = r'video([0-9]+)'
GDRIVE_REMOTE_DIR = "0B_4qQMAmg8UXcjVXUl9lbC1uQnc"
ROOT_PATH = "/home/share/Akiyagri"
LOG_DIR = "{}/AkiyaLog".format(ROOT_PATH)


def sync_gdrive():
    command = "gdrive-linux-x64 sync upload {} {}".format(LOG_DIR, GDRIVE_REMOTE_DIR)
    os.system(command)


def get_timestamp():
    return datetime.now().strftime('%Y_%m_%d_%H_%M_%S')


def take_photos(cameras):
    """
        cameras: {'camera_0': camera_0, 'camera_1': camera_1, ...}
        return: {'camera_0': img_0, 'camera_1': img_1, ...}
    """
    imgs = {}
    for camera_name, camera in cameras.items():
        ret, img = camera.read()
        if ret is not None:
            imgs[camera_name] = img
    return imgs


def get_cameras():
    """
        cameras: {'camera_0': camera_0, 'camera_1': camera_1, ...}
    """
    camera_names = filter(lambda x: re.match(CAMERA_DEVICE_PATTERN, x), os.listdir(DEVICE_DIR))
    print("Camera device names", camera_names)
    cameras = {}
    for name in camera_names:
        camera_id = re.search(CAMERA_DEVICE_PATTERN, name).group(1)
        camera = cv2.VideoCapture(int(camera_id))
        if camera.isOpened():
            cameras[name] = camera
    return cameras


def main(save_dir):
    cameras = get_cameras()
    images = take_photos(cameras)

    save_dir = "{}/{}".format(save, get_timestamp())
    os.makedirs(save_dir)
    for camera_name, img in images.items():
        img_path = "{}/{}.png".format(save_dir, camera_name)
        cv2.imwrite(img_path, img)


if __name__ == '__main__':
    test_imgs_dir = sys.argv[1]
    main(test_imgs_dir)
