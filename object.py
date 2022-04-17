from logging import exception
import numpy as np
import enum
import math


class ObjectType(enum.Enum):
    SPHERE = 1
    PLANE = 2


class Object:
    ''''Represents an object on the scene'''
    e = 10 ^ (-6)  # constante para evitar erros da aritmetica de ponto flutuante

    def __init__(self, Cr, Cg, Cb, Px, Py, Pz, Nx, Ny, Nz) -> None:
        self.color = np.array([Cr, Cg, Cb])
        self.sample_point = np.array([Px, Py, Pz])
        self.normal_vector = np.array([Nx, Ny, Nz])
        self.type = ObjectType.PLANE

    # @classmethod
    # def sphere_constructor(Ox, Oy, Oz, r):
    #   self.

    # def __init__(self, Cr, Cg, Cb, Ox, Oy, Oz, r) -> None:
    #     self.color = np.array([Cr, Cg, Cb])
    #     self.center = np.array([Ox, Oy, Oz])
    #     self.ray = r
    #     self.type = ObjectType.SPHERE

    def __str__(self):
        text = ""
        text += self.color + "\n"
        text += self.sample_point + "\n"
        text += self.normal_vector + "\n"
        text += self.type + "\n"  
        return text

    def intersection(self, ray_origin, ray_dir):
        if self.type == ObjectType.SPHERE:
            return self._intersect_sphere(ray_origin, ray_dir)
        else:
            return self._intersect_plane(ray_origin, ray_dir)

    # TODO
    def _intersect_sphere(self, ray_origin, ray_dir):
        t = math.inf
        return t

    def _intersect_plane(self, ray_origin, ray_dir):
        # print(ray_origin)
        # print(ray_dir)
        # print(self.normal_vector)
        t = math.inf
        den = np.inner(ray_dir, self.normal_vector)
        if abs(den) > Object.e:
            t = np.inner((self.sample_point - ray_origin),
                         self.normal_vector)/den
            if t < 0:
                raise exception("Ray don't intersect the plane!")
            else:
                return t
        else:
            raise exception(
                "Inner product between ray_dir and normal_vector too low")


if __name__ == "__main__":
    ray_dir = np.array([-0.71, 0.71, 0])
    plane = Object(255, 255, 255, 10, 10, 10, -2, -2, 2)
    origin = np.array([2, 2, 2])

    t = plane.intersection(origin, ray_dir)
    print(t)
