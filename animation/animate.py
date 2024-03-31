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
import csv

WINH = 600
WINW = 800
BG_COLOR = [10, 10, 10]

CAM_POS = np.array([0, 0, -5], dtype=np.float64)
SCREEN_DIST = 1000.0

FRAMES = 360
FPS = 12
LOOPS = 1

LERPRES = 50

sphere_center = np.array([0,0,0], dtype=np.float64)
sphere_radius = 1.0

earth_radius = 6.371e6

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

def lonlat2dir(lon, lat):
    lon = np.radians(lon)
    lat = np.radians(lat)

    x = np.cos(lat) * np.sin(lon) * -1
    y = np.sin(lat)
    z = np.cos(lat) * np.cos(lon)

    dir = np.array([x, y, z], dtype=np.float64)
    dir /= np.linalg.norm(dir)
    return dir

def get_earth_color(lon, lat):
    width, height = earth_img.size
    x = int(((540-lon)%360)/360 * (width-1))
    y = int((90-lat)/180 * (height-1))
    color = earth_img.getpixel((x,y))
    return np.array(color, dtype=np.uint8)

def render_ray(ray_origin, ray_dir, depth, lon_offset):
    if depth < 0:
         return np.array(BG_COLOR, dtype=np.uint8)
    p = ray_origin + depth*ray_dir
    po = p - sphere_center
    lon, lat = dir2lonlat(po)
    lon += lon_offset
    return get_earth_color(lon, lat)

def draw_dot(image_data, x, y, r=1, color=np.array([240, 20, 20])):
    for i in range(-r, r+1):
        for j in range(-r, r+1):
            if 0 <= x + i < WINW and 0 <= y + j < WINH:
                image_data[y+j][x+i] = color

def render_frame(image_data, depth_buffer, data, lon_offset):
    for i in range(WINH):
        for j in range(WINW):
            ray_origin = CAM_POS
            ray_dir = np.array([j - WINW/2, WINH/2 - i, SCREEN_DIST], dtype=np.float64)
            ray_dir /= np.linalg.norm(ray_dir)
            image_data[i][j] = render_ray(ray_origin, ray_dir, depth_buffer[i][j], lon_offset)
    if data is not None:
        prevp = None
        for point in data:
            lat = point[0]
            lon = point[1]
            alt = point[2]
            lon += lon_offset
            dir = lonlat2dir(lon, lat)
            curp = sphere_center + (earth_radius+alt)*(sphere_radius/earth_radius)*dir
            if prevp is None:
                p = curp
                dir2p = p - CAM_POS
                dist2p = np.dot(dir2p, np.array([0,0,1]))
                screen_pos_screen = (dir2p/dist2p)*SCREEN_DIST
                x = np.dot(screen_pos_screen, np.array([1,0,0]))
                y = np.dot(screen_pos_screen, np.array([0,1,0]))
                x += WINW/2
                y = WINH/2 - y
                x, y = int(x), int(y)
                if 0 <= x and x < WINW and 0 <= y and y < WINH:
                    if depth_buffer[y][x] < 0 or np.linalg.norm(dir2p) < depth_buffer[y][x]:
                        draw_dot(image_data, x, y)
            else:
                for i in range(1,LERPRES):
                    p = prevp + (i/LERPRES)*(curp-prevp)
                    dir2p = p - CAM_POS
                    dist2p = np.dot(dir2p, np.array([0,0,1]))
                    screen_pos_screen = (dir2p/dist2p)*SCREEN_DIST
                    x = np.dot(screen_pos_screen, np.array([1,0,0]))
                    y = np.dot(screen_pos_screen, np.array([0,1,0]))
                    x += WINW/2
                    y = WINH/2 - y
                    x, y = int(x), int(y)
                    if 0 <= x and x < WINW and 0 <= y and y < WINH:
                        if depth_buffer[y][x] < 0 or np.linalg.norm(dir2p) < depth_buffer[y][x]:
                            draw_dot(image_data, x, y)
            prevp = curp

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

# data is a collection of points [long, lat, alt]
def render_anim(frames=FRAMES, fps=FPS, loops=LOOPS, data=None):
    image_data = np.full((WINH,WINW,3), BG_COLOR, dtype=np.uint8)
    depth_buffer = np.full((WINH,WINW), 0, dtype=np.float64)
    render_depth_buffer(depth_buffer)

    print("rendering frames")
    for i in tqdm(range(frames)):
        render_frame(image_data, depth_buffer, data[:i+1] if data is not None else None, i*3)
        plt.imsave("frames/frame{}.png".format(i), image_data)

    print("writing to video")
    video = cv2.VideoWriter("animation.avi", cv2.VideoWriter_fourcc(*"DIVX"), fps, (WINW,WINH))
    for loop in range(loops):
        for i in range(frames):
            video.write(cv2.imread("frames/frame{}.png".format(i)))
    cv2.destroyAllWindows()
    video.release()

def get_data(filename="../ISSgeodeticData.csv"):
    data = []
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append([float(row[1]), float(row[2]), float(row[3])])
    return data

render_anim(FRAMES, FPS, LOOPS, get_data())
