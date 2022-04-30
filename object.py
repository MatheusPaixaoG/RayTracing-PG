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
    e = 10 ** (-6)  # constante para evitar erros da aritmetica de ponto flutuante

    def __init__(self, Color_r, Color_g, Color_b, K_a, K_d, K_s, exp):
        self.color = np.array([Color_r, Color_g, Color_b])
        self.type = None
        self.k_a = K_a
        self.k_d = K_d
        self.k_s = K_s
        self.exp = exp

    @abc.abstractmethod
    def intersect(self, ray_origin, ray_dir):
        pass

    @abc.abstractmethod
    def get_normal(self, point_on_object):
        pass


class Plane(Object):
    def __init__(self, Color_r, Color_g, Color_b, Px, Py, Pz, Nx, Ny, Nz, K_a, K_d, K_s, exp):
        '''Create a plane receiving its color, a sample point and its normal vector'''
        super().__init__(Color_r, Color_g, Color_b, K_a, K_d, K_s, exp)
        self.sample_point = np.array([Px, Py, Pz])
        self.normal_vector = np.array([Nx, Ny, Nz])
        self.type = ObjectType.PLANE

    def __str__(self):
        text = ""
        text += "{" + str(self.type.name) + ":" + "\n"

        text += "Sample Point: " + str(self.sample_point) + "\n"
        text += "Normal: " + str(self.normal_vector) + "\n"
        text += "Color: " + str(self.color) + "}" + "\n"

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
            # Inner product between ray_dir and normal_vector too low
            return

    def get_normal(self, point_on_object=None):
        '''Returns the normalized norm of the plane'''
        norm = np.linalg.norm(self.normal_vector)
        return self.normal_vector/norm


class Sphere(Object):
    def __init__(self, Color_r, Color_g, Color_b, Ox, Oy, Oz, r, K_a, K_d, K_s, exp):
        '''Create a sphere receiving its color and center'''
        super().__init__(Color_r, Color_g, Color_b, K_a, K_d, K_s, exp)
        self.center = np.array([Ox, Oy, Oz])
        self.radius = r
        self.type = ObjectType.SPHERE

    def __str__(self):
        text = ""
        text += "{" + str(self.type.name) + ":" + "\n"

        text += "Center: " + str(self.center) + "\n"
        text += "radius: " + str(self.radius) + "\n"
        text += "Color: " + str(self.color) + "}" + "\n"

        return text

    def intersect(self, ray_origin, ray_dir):
        l = self.center - ray_origin
        t_ca = np.inner(l, ray_dir)
        d_2 = (np.inner(l, l)) - (t_ca)*(t_ca)
        if d_2 > (self.radius)**2:
            # Ray doesn't intersect the sphere!"
            return
        else:
            t_hc = math.sqrt(self.radius**2 - d_2)
            t0 = t_ca - t_hc
            t1 = t_ca + t_hc
            if t0 > t1:
                t0, t1 = t1, t0
            if t0 < 0:
                if t1 < 0:
                    # Off-sColor_reen intersection with sphere
                    return None
                else:
                    return t1

            return t0

    def get_normal(self, point_on_object):
        center = self.center
        center_to_point_vec = point_on_object - center
        norm = np.linalg.norm(center_to_point_vec)
        return center_to_point_vec/norm
