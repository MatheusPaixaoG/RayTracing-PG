from weakref import ref
import numpy as np
import math
import json
import matplotlib.pyplot as plt
from light_src import light_src

from object import Object, Plane, Sphere

objects = []  # Array de objetos
background_color = np.array([255, 0, 0])  # Cor do plano de fundo (RGB)
ambient_light = np.zeros(3)
lights = []
e = 10**(-5)  # Constant to prevent shadow acne or that the secondary ray be generate inside the obj
max_recursion_depth = 0; # Limite máximo de recursão do raytracing

def reflect(dir_light, surface_normal):
    # Returns the reflected light vector
    return 2 * np.inner(surface_normal, dir_light)*surface_normal - dir_light


def tuple_comparator(object):
    return object[0]


def shade(obj, intersection_point, dir_focus, surface_normal):
    obj_color = obj.color
    obj_ka = obj.k_a
    obj_kd = obj.k_d
    obj_ks = obj.k_s
    obj_exp = obj.exp

    # Calculates the ambient color influence
    point_color = obj_ka*obj_color*ambient_light

    for light in lights:
        point_to_light_vec = light.position-intersection_point
        light_dir = (point_to_light_vec)/np.linalg.norm(point_to_light_vec)

        reflected = reflect(light_dir, surface_normal)
        intersection_point_corrected = intersection_point + e*light_dir
        intersected_objs = trace(intersection_point_corrected, light_dir)

        closest_t = math.inf

        if (intersected_objs):
            for t_obj in intersected_objs:
                if t_obj[0] < closest_t:
                    closest_t = t_obj[0]

        if (not intersected_objs or
                np.inner(light_dir, (light.position - intersection_point_corrected)) < closest_t):
            if (np.inner(surface_normal, light_dir) > 0):
                point_color = point_color + obj_kd*obj_color * \
                    (np.inner(surface_normal, light_dir))*light.intensity
            if (np.inner(dir_focus, reflected) > 0):
                point_color = point_color + \
                    (obj_ks*((np.inner(dir_focus, reflected))**obj_exp))*light.intensity

    return point_color


def refract(obj, observer_vec, normal_vec):
    refraction_index = obj.refraction_index
    cos_angle_normal_obs = np.inner(normal_vec, observer_vec)

    # Observador no meio interno 
    if cos_angle_normal_obs < 0:
        normal_vec = -normal_vec
        refraction_index = 1/refraction_index
        cos_angle_normal_obs = -cos_angle_normal_obs

    delta = 1 - (1/(refraction_index**2)) * (1 - cos_angle_normal_obs ** 2)

    # Reflexão total: não há refração de luz
    if delta < 0:
        return None
    
    return -(1/refraction_index)*observer_vec - (math.sqrt(delta) - (1/refraction_index)*cos_angle_normal_obs)*normal_vec

    

def render(v_res, h_res, tamanho_px, dist_focal, foco_camera, mira_camera, up, max_recursion_depth):
    image = np.zeros((v_res, h_res, 3), dtype=np.uint8)

    # Criacao do sistema de coordenadas da camera {u,v,w}
    w = (foco_camera - mira_camera) / np.linalg.norm(foco_camera - mira_camera)
    cross_up_w = np.cross(up, w)
    u = cross_up_w / np.linalg.norm(cross_up_w)
    v = np.cross(w, u)

    # Lancamento dos raios
    q_00 = foco_camera - dist_focal * w + tamanho_px * \
        (((v_res - 1)/2)*v - ((h_res - 1)/2)*u)
    for i in range(v_res):
        for j in range(h_res):
            q_ij = q_00 + tamanho_px * (j * u - i * v)
            dir_ray = (q_ij-foco_camera)/np.linalg.norm(q_ij - foco_camera)
            pixel_color = cast(foco_camera, dir_ray, max_recursion_depth)
            if (max(pixel_color) > 1):
                pixel_color = pixel_color/max(pixel_color)

            image[i][j] = pixel_color * np.array([255, 255, 255])
    return image


def cast(foco_camera, dir_ray, recursion_level):
    point_color = background_color
    intersected_objs = trace(foco_camera, dir_ray)

    if (intersected_objs):
        closest_t = math.inf
        closest_obj = None

        for t_obj in intersected_objs:
            if t_obj[0] < closest_t:
                closest_t = t_obj[0]
                closest_obj = t_obj[1]

        intersection_point = foco_camera + dir_ray*closest_t
        observer_vec = -dir_ray
        normal = closest_obj.get_normal(intersection_point)
        point_color = shade(closest_obj, intersection_point, observer_vec, normal)  
        
        if(recursion_level > 0):
            # Calcula a contribuição da reflexão na cor do ponto
            if closest_obj.k_r > 0: 
                reflected_ray = reflect(observer_vec, normal)
                intersection_point_corrected = intersection_point + e * reflected_ray

                reflected_color = closest_obj.k_r * cast(intersection_point_corrected,
                                                        reflected_ray, recursion_level-1)
                point_color = point_color +  reflected_color

            # Calcula a contribuição da refração na cor do ponto
            if closest_obj.k_t > 0:
                # refraction_normal = closest_obj.get_normal(intersection_point_corrected)

                refracted_ray = refract(closest_obj, observer_vec, normal)
                # Se não ocorrer reflexão total, continue o cálculo
                if (refracted_ray is not None):
                    intersection_point_corrected = intersection_point + e * refracted_ray
                    refracted_color = closest_obj.k_t * cast(intersection_point_corrected, 
                                                                    refracted_ray, recursion_level - 1)
                    point_color = point_color + refracted_color
    return point_color


def trace(foco_camera, dir_ray):
    s = []
    for obj in objects:
        t = obj.intersect(foco_camera, dir_ray)
        if t:
            s.append((t, obj))
    return s


def run_by_json(path):
    # Carrega o json em specs
    file = open(path)
    specs = json.load(file)
    file.close()

    # Define a cor do background
    global background_color
    background_color = specs["background_color"]

    # Define o limite máximo de recursão do raytracing
    global max_recursion_depth
    max_recursion_depth = specs["max_depth"]

    # Pega cada objeto do JSON e os coloca no array objects
    objects_json = specs["objects"]

    for obj in objects_json:
        r, g, b = obj["color"]
        r, g, b = r/255, g/255, b/255
        k_a = obj["ka"]
        k_d = obj["kd"]
        k_s = obj["ks"]
        exp = obj["exp"]
        k_r = obj["kr"]
        k_t = obj["kt"]
        refraction_index = obj["index_of_refraction"]

        if obj.get("plane"):  # Se o objeto for um plano ...
            plane = obj["plane"]
            sx, sy, sz = plane["sample"]
            nx, ny, nz = plane["normal"]

            objects.append(Plane(r, g, b, sx, sy, sz, nx,
                           ny, nz, k_a, k_d, k_s, exp,
                           k_r, k_t, refraction_index))

        elif obj.get("sphere"):
            sphere = obj["sphere"]
            cx, cy, cz = sphere["center"]
            radius = sphere["radius"]

            objects.append(Sphere(r, g, b, cx, cy, cz,
                           radius, k_a, k_d, k_s, exp,
                           k_r, k_t, refraction_index))

    # Define a luz ambiental
    global ambient_light
    ambient_light = np.array(specs["ambient_light"])/255

    # Pega a lista de fontes de luz
    for l in specs["lights"]:
        light = light_src(np.array(l["position"]),
                          np.array(l["intensity"])/255)
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
                 np.array(specs["up"]),
                 max_recursion_depth)

    return img
