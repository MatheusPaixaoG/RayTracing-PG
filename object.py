from logging import exception
import numpy as np
import enum
import math
import abc

class ObjectType(enum.Enum):
    SPHERE = 1
    PLANE = 2

class Object:
    ''''Represents an object on the scene'''
    e = 10 ^ (-6)  # constante para evitar erros da aritmetica de ponto flutuante

    def __init__(self, Cr, Cg, Cb):
        self.color = np.array([Cr, Cg, Cb])
        self.type = None

    @abc.abstractmethod
    def intersect(self, ray_origin, ray_dir):
        return


class Plane(Object):
    def __init__(self, Cr, Cg, Cb, Px, Py, Pz, Nx, Ny, Nz):
        super().__init__(Cr, Cg, Cb)
        self.sample_point = np.array([Px, Py, Pz])
        self.normal_vector = np.array([Nx, Ny, Nz])
        self.type = ObjectType.PLANE


    def __str__(self):
        text = ""
        text += "{" + str(self.type.name) +":"               + "\n"

        text += "Sample Point: " + str(self.sample_point)    + "\n"
        text += "Normal: " + str(self.normal_vector)         + "\n"
        text += "Color: " + str(self.color) + "}"            + "\n"
        
        return text

    def intersect(self, ray_origin, ray_dir):
        t = math.inf
        den = np.inner(ray_dir, self.normal_vector)
        if abs(den) > Object.e:
            t = np.inner((self.sample_point - ray_origin),
                         self.normal_vector)/den
            if t < 0:
                # "Ray don't intersect the plane!"
                return
            else:
                return t
        else:
            #Inner product between ray_dir and normal_vector too low
            return

class Sphere(Object):
    def __init__(self, Cr, Cg, Cb, Ox, Oy, Oz, r):
        super().__init__(Cr, Cg, Cb)
        self.center = np.array([Ox, Oy, Oz])
        self.radius = r
        self.type = ObjectType.SPHERE

    def __str__(self):
        text = ""
        text += "{" + str(self.type.name) +":"               + "\n"

        text += "Center: " + str(self.center)    + "\n"
        text += "radius: " + str(self.radius)         + "\n"
        text += "Color: " + str(self.color) + "}"            + "\n"

        return text

    def intersect(self, ray_origin, ray_dir):
        l = self.center - ray_origin
        t_ca = np.inner(l, ray_dir)
        d_2 = (np.inner(l, l)) - (t_ca)*(t_ca)
        if d_2 > (self.radius)**2:
            #Ray doesn't intersect the sphere!"
            return
        else:
            t_hc = math.sqrt(self.radius**2 - d_2)
            t0 = t_ca - t_hc
            t1 = t_ca + t_hc
            if t0 > t1:
                t0,t1 = t1,t0
            if t0 < 0:
                if t1 < 0:
                    # Off-screen intersection with sphere
                    return None
                else:
                    return t1

            return t0
