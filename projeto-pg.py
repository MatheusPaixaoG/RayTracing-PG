import numpy as np
import math
import json
import matplotlib.pyplot as plt

from object import Plane,Sphere

objects = []  # Array de objetos
background_color = np.array([255, 0, 0])  # Cor do plano de fundo (RGB)


def render(v_res, h_res, s, d, E, L, up):
    image = np.zeros((v_res, h_res,3),dtype=np.uint8)

    # Criacao da base ortonormal {u,v,w}
    w = (E - L) / np.linalg.norm(E - L)
    cross_up_w = np.cross(up, w)
    u = cross_up_w / np.linalg.norm(cross_up_w)
    v = np.cross(w, u)

    # Lancamento dos raios
    q_00 = E - d * w + s * (((v_res - 1)/2)*v - ((h_res - 1)/2)*u)
    for i in range(v_res):
        for j in range(h_res):
            q_ij = q_00 + s * (j * u - i * v)
            dir_ray = (q_ij-E)/np.linalg.norm(q_ij - E)
            image[i][j] = cast(E, dir_ray)
    return image

# TODO: testar depois de implementar o trace


def cast(E, dir_ray):
    c = background_color
    S = trace(E, dir_ray)

    if (S):
        closest_t = math.inf
        closest_obj = None
        
        for t_obj in S:
            if t_obj[0] < closest_t:
                closest_t = t_obj[0]
                closest_obj = t_obj[1]
                c = closest_obj.color
    return c


# TODO: testar depois de implementar os intersects


def trace(E, dir_ray):
    s = []
    for obj in objects:
        t = obj.intersect(E, dir_ray)
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

    # Pega cada objeto do JSON e os coloca no array objects
    objects_json = specs["objects"]

    for obj in objects_json:
        r,g,b = obj["color"]
        
        if obj.get("plane"): # Se o objeto for um plano ...
            plane = obj["plane"]
            sx,sy,sz = plane["sample"]
            nx,ny,nz = plane["normal"]

            objects.append(Plane(r,g,b,sx,sy,sz,nx,ny,nz))

        elif obj.get("sphere"):
            sphere = obj["sphere"]
            cx,cy,cz = sphere["center"]
            radius = sphere["radius"]

            objects.append(Sphere(r,g,b,cx,cy,cz,radius))

    print("Gerando a imagem ...")
    print("(Esse processo pode durar alguns minutos)")

    # Gera a imagem
    img = render(specs["v_res"],
                 specs["h_res"],
                 specs["square_side"],
                 specs["dist"],
                 np.array(specs["eye"]),
                 np.array(specs["look_at"]),
                 np.array(specs["up"]))

    return img

# MAIN
if __name__ == "__main__":
    path = input()           # Pega o caminho do arquivo json (não funciona passando como argumento pro terminal)
    img = run_by_json(path)  # Retorna a imagem a partir dos valores do cmd

    # Plota a imagem resultante    
    plt.imshow(img)
    plt.show()
