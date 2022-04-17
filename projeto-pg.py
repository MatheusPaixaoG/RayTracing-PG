import numpy as np
import math
import json

from object import Object

# INPUT:
# v_res h_res                      //resolucao vertical e horizontal
# s d                              //s=largura do pixel |  d= distancia do centro da camera ao plano de exibicao
# Ex Ey Ez                         // origem do sistema de coordenadas e dos raios primarios
# Lx Ly Lz                         // para onde a camera aponta
# upx upy upz                      // vetor que aponta pra cima
# B.r B.g B.b                      // Cor do Background
#  k_obj                           // qt de objetos
# C.r C.g C.b * Ox Oy Oz r         // circulo
# C.r C.g C.b / Px Py Pz nx ny nz  //plano

objects = []  # Array de objetos
background_color = np.array([255, 0, 0])  # Cor do plano de fundo (RGB)


def render(v_res, h_res, s, d, E, L, up):
    image = np.zeros((v_res, h_res,3))

    # Criacao da base ortonormal {u,v,w}
    w = (E - L) / np.linalg.norm(E - L)
    cross_up_w = np.cross(up, w)
    u = cross_up_w / np.linalg.norm(cross_up_w)
    v = np.cross(w, u)

    # Lancamento dos raios
    q_00 = E - d * w + s * (((v_res - 1)/2)*v - ((h_res - 1)/2)*u)
    # print(q_00)
    for i in range(v_res):
        for j in range(h_res):
            q_ij = q_00 + s * (j * u - i * v)
            dir_ray = (q_ij-E)/np.linalg.norm(q_ij - E)
            # print(q_ij, end=" ")
            image[i][j] = cast(E, dir_ray)
            # print(j)
        # print()
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
        try:
            t = obj.intersection(E, dir_ray)
            s.append((t, obj))
        except:
            pass
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

            objects.append(Object(r,g,b,sx,sy,sz,nx,ny,nz))

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
                 
    # Imprime a cor de cada píxel da imagem
    img_list = img.tolist()

    for row in img_list:
        print(row,"\n\n")
