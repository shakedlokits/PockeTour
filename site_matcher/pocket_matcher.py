from skimage.color import rgb2gray
import cv2
import numpy as np
from location_db.pocket_db import PocketDB
from sklearn.neighbors import NearestNeighbors


def match_site(path, gps):
    """
    matches a site from database based on GPS
    location and image input
    :param path: the path of the input image
    :param gps: gps coordinates [lon, lat]
    :return:
    """

    # generate tuple
    gps = tuple(gps)

    # read sites close to me
    with PocketDB() as db:
        sites = db.get_descriptors(gps)

    # load input image
    gray_image = cv2.imread(path, 0)

    # initialize data members
    site_id = 0
    temp_id = 0
    best_score = float("inf")
    num_sites = len(sites)
    keypoints_input, descriptors_input = cv2.ORB_create().detectAndCompute(gray_image, None)
    nn = NearestNeighbors(2, 1, 'ball_tree').fit(descriptors_input)

    # run on the sites one by one
    for i in range(0,num_sites):

        # get id of site
        temp_id = sites[i]['id']

        # number of images of this site
        num_of_db_images_site = len(sites[i]['desc'])
        temp_score = 0

        # run throue the images for site
        for j in range(0, num_of_db_images_site):
            imJdes = np.reshape(sites[i]['desc'][j], (len(sites[i]['desc'][j])/32, 32))
            dis, indx = nn.kneighbors(imJdes, 2)

            # filtered_dis = filter(lambda distance: distance < np.median(dis), dis)
            temp_score += np.median(dis)

        if best_score > (temp_score / num_of_db_images_site):
            site_id = temp_id
            best_score = (temp_score / num_of_db_images_site)

    # get site data
    with PocketDB() as db:
        site_json_data = db.get_site_by_id(site_id)

    return site_json_data


