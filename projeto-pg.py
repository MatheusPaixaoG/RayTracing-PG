import numpy as np

# INPUT:
# v_res h_res                      //resolucao vertical e horizontal
# s d                              //s=largura do pixel |  d= distancia do centro da camera ao plano de exibicao
# Ex Ey Ez                         // origem do sistema de coordenadas e dos raios primarios (vulgo camera),
# Lx Ly Lz                         // para onde a camera aponta
# upx upy upz                      // vetor que aponta pra cima
# k_obj                             // qt de objetos
# C.r C.g C.b * Ox Oy Oz r          // circulo
# C.r C.g C.b / Px Py Pz nx ny nz   //plano

# Variaveis da Tela
v_res = 4  # Altura vertical da tela
h_res = 3  # Largura da tela
s = 10       # Tamanho de um pixel
d = 5        # Distancia da camera ao plano de exibicao

# Variaveis da camera
# origem do sistema de coordenadas e dos raios primarios (vulgo camera),
E = np.array([2, 2, 2])
L = np.array([0, 0, 1])  # para onde a camera aponta
up = np.array([0, 0, 1])  # vetor que aponta pra cima

objects = []  # Array de objetos


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
    for i in range(v_res):
        for j in range(h_res):
            q_ij = q_00 + s * (j * u - i * v)
            dir_ray = (q_ij-E)/np.linalg.norm(q_ij - E)
            image[i][j] = cast(E, dir_ray)
            print(q_ij, end=" ")
        print()
    return image


def cast(E, dir_ray):
    return


# MAIN
render(v_res, h_res, s, d, E, L, up)
