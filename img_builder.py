import numpy as np 
import math
import json
import matplotlib.pyplot as plt
from light_src import light_src

from object import Plane,Sphere

objects = []  # Array de objetos
background_color = np.array([255, 0, 0])  # Cor do plano de fundo (RGB)
ambient_light = np.zeros(3)
lights = []
e = 10**(-5) # Constant to prevent shadow acne

def reflect(dir_light, surface_normal):
    # Returns the reflected light vector
    return 2 * np.inner(dir_light,surface_normal)*surface_normal-dir_light

def shade(obj, intersection_point, dir_focus, surface_normal):
    obj_color = obj.color
    obj_ka = obj.k_a
    obj_kd = obj.k_d
    obj_ks = obj.k_s
    obj_exp = obj.exp
    
    point_color = obj_ka*obj_color*ambient_light # Calculates the ambient color influence

    for light in lights:
        point_to_light_vec = light.position-intersection_point
        light_dir = (point_to_light_vec)/np.linalg.norm(point_to_light_vec)
        
        reflected = reflect(light)
        intersection_point_corrected = intersection_point - e*light_dir
        intersected_objs = trace(intersection_point_corrected, light_dir)
        
        closest_t = math.inf
        
        if (intersected_objs):
            for t_obj in intersected_objs:
                if t_obj[0] < closest_t:
                    closest_t = t_obj[0]
                    
        if (intersected_objs or 
            np.inner(light_dir, (point_to_light_vec - intersection_point_corrected)) < closest_t):
            if (np.inner(surface_normal, light_dir) > 0):
                point_color = point_color + obj_kd*obj_color * (np.inner(surface_normal, light_dir))*light.intensity
            if (np.inner(dir_focus, reflected) > 0):
                point_color = point_color + (obj_ks*(np.inner(dir_focus, reflected))**obj_exp)*light.intensity
        
    return point_color

def render(v_res, h_res, tamanho_px, dist_focal, foco_camera, mira_camera, up):
    image = np.zeros((v_res, h_res,3),dtype=np.uint8)

    # Criacao do sistema de coordenadas da camera {u,v,w}
    w = (foco_camera - mira_camera) / np.linalg.norm(foco_camera - mira_camera)
    cross_up_w = np.cross(up, w)
    u = cross_up_w / np.linalg.norm(cross_up_w)
    v = np.cross(w, u)

    # Lancamento dos raios
    q_00 = foco_camera - dist_focal * w + tamanho_px * (((v_res - 1)/2)*v - ((h_res - 1)/2)*u)
    for i in range(v_res):
        for j in range(h_res):
            q_ij = q_00 + tamanho_px * (j * u - i * v)
            dir_ray = (q_ij-foco_camera)/np.linalg.norm(q_ij - foco_camera)
            image[i][j] = cast(foco_camera, dir_ray)
    return image


def cast(foco_camera, dir_ray):
    point_color = background_color
    intersected_objs = trace(foco_camera, dir_ray)

    if (intersected_objs):
        closest_t = math.inf
        closest_obj = None
        
        for t_obj in intersected_objs:
            if t_obj[0] < closest_t:
                closest_t = t_obj[0]
                closest_obj = t_obj[1]
                #cor_background = closest_obj.color
        
        intersection_point = foco_camera + dir_ray*closest_t
        point_color = shade(closest_obj, intersection_point, -dir_ray, closest_obj.get_normal(intersection_point))
    return point_color


def trace(foco_camera, dir_ray):
    tamanho_px = []
    for obj in objects:
        t = obj.intersect(foco_camera, dir_ray)
        if t:
            tamanho_px.append((t, obj))
    return tamanho_px


def run_by_json(path):
    # Carrega o json em specs 
    file = open(path)
    specs = json.load(file)
    file.close()

    # Define a cor do background
    global background_color
    background_color = specs["background_color"]

    # Pega cada objeto do JSON e os coloca no array objects
    objects_json = specs["objects"]

    for obj in objects_json:
        r,g,b = obj["color"]
        k_a = obj["ka"]
        k_d = obj["kd"]
        k_s = obj["ks"]
        exp = obj["exp"]
        
        if obj.get("plane"): # Se o objeto for um plano ...
            plane = obj["plane"]
            sx,sy,sz = plane["sample"]
            nx,ny,nz = plane["normal"]

            objects.append(Plane(r,g,b,sx,sy,sz,nx,ny,nz,k_a,k_d,k_s,exp))

        elif obj.get("sphere"):
            sphere = obj["sphere"]
            cx,cy,cz = sphere["center"]
            radius = sphere["radius"]

            objects.append(Sphere(r,g,b,cx,cy,cz,radius,k_a,k_d,k_s,exp))

    # Define a luz ambiental
    global ambient_light
    ambient_light = np.array(specs["ambient_light"])

    # Pega a lista de fontes de luz
    for l in specs["lights"]:
        light = light_src(np.array(l["position"]), np.array(l["intensity"]))
        lights.append(light)

    # Gera a imagem
    print("Gerando a imagem ...")
    print("(Esse processo pode durar alguns minutos)")

    img = render(specs["v_res"],
                 specs["h_res"],
                 specs["square_side"],
                 specs["dist"],
                 np.array(specs["eye"]),
                 np.array(specs["look_at"]),
                 np.array(specs["up"]))

    return img

# l = np.array([2,2,2])/np.linalg.norm(np.array([2,2,2]))
# r = reflect(l,np.array([0,1,0]))
# print(r, np.linalg.norm(r))