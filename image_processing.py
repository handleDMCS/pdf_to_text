import cv2
import numpy as np
from collections import deque

def ResizeWithAspectRatio(img, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = img.shape[0], img.shape[1]
    if width is None and height is None:
        return img
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    return cv2.resize(img, dim, interpolation=inter)

def PIL_to_cv2(pil_img):
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def draw_box(img, bbox, caption = ''):
    (min_x, min_y, max_x, max_y) = bbox
    img = cv2.rectangle(img, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)
    if(caption != ''):
        cv2.putText(img, caption, (min_x, min_y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

def get_bin_image(img, txt_box_list = []): # Apply Otsu's thresholding
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, result = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if np.sum(result == 0) > np.sum(result == 255):
        result = cv2.bitwise_not(result) 
    for (x_min, y_min, x_max, y_max) in txt_box_list:
        result = cv2.rectangle(result, (x_min, y_min), (x_max, y_max), 255, -1)
    return result

def transpose(coord): # np <-> open cv coord 
    x, y = coord
    return (y, x)

def transpose_list(coord_list): # apply transpose() to a list  
    return [transpose(coord) for coord in coord_list]

def bfs(bin_img, visited, coord, dir, cluster_list, min_cluster = -1): # find the cluster where (x, y) belongs
    x, y = coord[0], coord[1]
    if (visited[x, y] == True) or (bin_img[x, y] == 255):
        return 
    visited[x, y] = True
    nxt = deque([coord])
    cluster_list.append([coord])
    while nxt:
        x, y = nxt.popleft()
        for (dx, dy) in dir:
            new_x, new_y = x+dx, y+dy
            if(new_x not in range(0, bin_img.shape[0])) or (new_y not in range(0, bin_img.shape[1])):
                continue
            if (visited[new_x, new_y] == True) or (bin_img[new_x, new_y] == 255):
                continue
            visited[new_x, new_y] = True
            nxt.append((new_x, new_y))
            cluster_list[-1].append((new_x, new_y))
    if(len(cluster_list[-1]) < min_cluster):
        cluster_list.pop()

def get_cluster(bin_img, dist = (5, 5), min_cluster = 50): # get the list of clusters
    dir = []
    for dx in range(0, dist[0]+1):
        for dy in range(0, dist[1]+1):
            dir.append((dx, dy))       
            dir.append((-dx, dy))       
            dir.append((dx, -dy))       
            dir.append((-dx, -dy))       
    dir = list(set(dir))             
    visited = np.zeros_like(bin_img, dtype=bool)
    cluster_list = []
    for x in range(bin_img.shape[0]):
        for y in range(bin_img.shape[1]):
            bfs(bin_img, visited, (x, y), dir, cluster_list, min_cluster)
    return cluster_list

def bfs_check(bin_img, visited, coord, dir, min_cluster = -1): # a modified version of bfs()
    x, y = coord[0], coord[1]
    if (visited[x, y] == True) or (bin_img[x, y] == 255):
        return False
    visited[x, y] = True
    nxt = deque([coord])
    cluster_size = 0
    while nxt:
        x, y = nxt.popleft()
        for (dx, dy) in dir:
            new_x, new_y = x+dx, y+dy
            if(new_x not in range(0, bin_img.shape[0])) or (new_y not in range(0, bin_img.shape[1])):
                continue
            if (visited[new_x, new_y] == True) or (bin_img[new_x, new_y] == 255):
                continue
            visited[new_x, new_y] = True
            nxt.append((new_x, new_y))
            cluster_size += 1
            if(cluster_size >= min_cluster):
                return True
    return False

def check_cluster(bin_img, dist = (5, 5), min_cluster = 50): # return true if a cluster surpasses the min_cluster threshold
    dir = []
    for dx in range(0, dist[0]+1):
        for dy in range(0, dist[1]+1):
            dir.append((dx, dy))       
            dir.append((-dx, dy))       
            dir.append((dx, -dy))       
            dir.append((-dx, -dy))       
    dir = list(set(dir))             
    visited = np.zeros_like(bin_img, dtype=bool)
    for x in range(bin_img.shape[0]):
        for y in range(bin_img.shape[1]):
            if(bfs_check(bin_img, visited, (x, y), dir, min_cluster) == True):
                return True
    return False

def crop(img, bbox):
    min_x, min_y, max_x, max_y = bbox 
    result = img[min_y:max_y, min_x:max_x] 
    return result

def has_content(img, bbox, min_height = 50):
    min_y, max_y = bbox[1], bbox[3]
    if(max_y-min_y < min_height):
        return False
    if not check_cluster(get_bin_image(crop(img, bbox))):
        return False
    return True
