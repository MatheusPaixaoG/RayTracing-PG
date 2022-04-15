import numpy as np

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

# Variaveis da Tela
v_res = 4  # Altura vertical da tela
h_res = 3  # Largura da tela
s = 10       # Tamanho de um pixel
d = 5        # Distancia da camera ao plano de exibicao

# Variaveis da camera

# origem do sistema de coordenadas e dos raios primarios (vulgo camera),
E = np.array([2, 2, 2])
L = np.array([4.67, 4.67, -0.67])  # para onde a camera aponta
up = np.array([0, 0, 1])  # vetor que aponta pra cima

objects = []  # Array de objetos
background_color = np.array([255, 0, 0])  # Cor do plano de fundo (RGB)


def render(v_res, h_res, s, d, E, L, up):
    image = np.zeros((v_res, h_res))

    # Criacao da base ortonormal {u,v,w}
    w = (E - L) / np.linalg.norm(E - L)
    cross_up_w = np.cross(up, w)
    u = cross_up_w / np.linalg.norm(cross_up_w)
    v = np.cross(w, u)

    # Lancamento dos raios
    q_00 = E - d * w + s * (((v_res - 1)/2)*v - ((h_res - 1)/2)*u)
    print(q_00)
    for i in image:
        for j in i:
            q_ij = q_00 + s * (j * u - i * v)
            dir_ray = (q_ij-E)/np.linalg.norm(q_ij - E)
            j = cast(E, dir_ray)
            # print(q_ij, end=" ")
        print()
    return image

# TODO: testar depois de implementar o trace


def cast(E, dir_ray):
    c = background_color
    S = trace(E, dir_ray)

    if (S):
        t, closest = min(S)
        c = closest.color
    return c


objects.append(Object(255, 255, 255, 10, 10, 10, -2, -2, 2))
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


# MAIN
if __name__ == "__main__":
    render(v_res, h_res, s, d, E, L, up)
