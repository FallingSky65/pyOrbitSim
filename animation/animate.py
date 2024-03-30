# Daniel Li
# 03/30/2024
#
# pyOrbitSim::animation::animate.py
#
# use swath data to animate satellites around earth

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2
from tqdm import tqdm

WINH = 300
WINW = 400
BG_COLOR = [10, 10, 10]

CAM_POS = np.array([0, 0, -3], dtype=np.float64)
SCREEN_DIST = 300

FRAMES = 60
FPS = 60
LOOPS = 5

sphere_center = np.array([0,0,0], dtype=np.float64)
sphere_radius = 1.0

earth_img = Image.open("./earth2D.png")

def ray_sphere_intersection(ray_origin, ray_direction):
    oc = ray_origin - sphere_center
    a = np.dot(ray_direction, ray_direction)
    b = 2 * np.dot(oc, ray_direction)
    c = np.dot(oc, oc) - sphere_radius**2
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None
    else:
        t1 = (-b + np.sqrt(discriminant)) / (2*a)
        t2 = (-b - np.sqrt(discriminant)) / (2*a)
        return min(t1, t2) if t1 >= 0 or t2 >= 0 else None

def dir2lonlat(dir):
    dir /= np.linalg.norm(dir)
    longitude = np.degrees(np.arctan2(dir[0], dir[2]))
    latitude = np.degrees(np.arcsin(dir[1]))
    return longitude, latitude

def get_earth_color(lon, lat):
    width, height = earth_img.size
    x = int(((360-lon)%360)/360 * (width-1))
    y = int((90-lat)/180 * (height-1))
    color = earth_img.getpixel((x,y))
    return np.array(color, dtype=np.uint8)

def render_ray(ray_origin, ray_dir, depth, findex):
    if depth < 0:
         return np.array(BG_COLOR, dtype=np.uint8)
    p = ray_origin + depth*ray_dir
    po = p - sphere_center
    lon, lat = dir2lonlat(po)
    lon += findex*6
    return get_earth_color(lon, lat)

def render_frame(image_data, depth_buffer, findex):
    for i in range(WINH):
        for j in range(WINW):
            ray_origin = CAM_POS
            ray_dir = np.array([j - WINW/2, WINH/2 - i, SCREEN_DIST], dtype=np.float64)
            ray_dir /= np.linalg.norm(ray_dir)
            image_data[i][j] = render_ray(ray_origin, ray_dir, depth_buffer[i][j], findex)

def render_depth_buffer(depth_buffer):
    for i in range(WINH):
        for j in range(WINW):
            ray_origin = CAM_POS
            ray_dir = np.array([j - WINW/2, WINH/2 - i, SCREEN_DIST], dtype=np.float64)
            ray_dir /= np.linalg.norm(ray_dir)
            t = ray_sphere_intersection(ray_origin, ray_dir)
            if t is None:
                depth_buffer[i][j] = -1
            else:
                depth_buffer[i][j] = t

def render_anim(frames=36, fps=12, loops=1):
    image_data = np.full((WINH,WINW,3), BG_COLOR, dtype=np.uint8)
    depth_buffer = np.full((WINH,WINW), 0, dtype=np.float64)
    render_depth_buffer(depth_buffer)

    print("rendering frames")
    for i in tqdm(range(frames)):
        render_frame(image_data, depth_buffer, i)
        plt.imsave("frames/frame{}.png".format(i), image_data)

    print("writing to video")
    video = cv2.VideoWriter("animation.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (WINW,WINH))
    for loop in range(loops):
        for i in range(frames):
            video.write(cv2.imread("frames/frame{}.png".format(i)))
    cv2.destroyAllWindows()
    video.release()


render_anim(FRAMES, FPS, LOOPS)
