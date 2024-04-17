#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code  # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

# set default
gamma = 2.2
viewDir = np.array([0, 0, -1]).astype(np.float64)
viewUp = np.array([0, 1, 0]).astype(np.float64)
viewProjNormal = -1 * viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
viewWidth = 1.0
viewHeight = 1.0
projDistance = 1.0
intensity = np.array([1, 1, 1]).astype(np.float64)  # how bright the light is.


class Color:
    def __init__(self, R, G, B):
        self.color = np.array([R, G, B]).astype(np.float64)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma
        self.color = np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0, 1) * 255).astype(np.uint8)


class FileParser:
    def __init__(self, argv):
        self.tree = ET.parse(argv)
        self.root = self.tree.getroot()

    def getImageSize(self):
        return np.array(self.root.findtext('image').split()).astype(np.int32)

    def getLight(self):
        light, intensity = 0., 0.
        for c in self.root.findall('light'):
            light = np.array(c.findtext('position').split()).astype(np.float64)
            intensity = np.array(c.findtext('intensity').split()).astype(np.float64)
        return light, intensity

    def getCamera(self):
        viewPoint = 0.
        for c in self.root.findall('camera'):
            viewPoint = np.array(c.findtext('viewPoint').split()).astype(np.float64)
            viewDir = np.array(c.findtext('viewDir').split()).astype(np.float64)
            projNormal = np.array(c.findtext('projNormal').split()).astype(np.float64)
            projDistance = np.array(c.findtext('projDistance').split()).astype(np.float64)
            viewWidth = np.array(c.findtext('viewWidth').split()).astype(np.float64)
            viewHeight = np.array(c.findtext('viewHeight').split()).astype(np.float64)
            print('viewpoint', viewPoint)
            print('viewDir', viewDir)
            print('projNormal', projNormal)
            print('projDistance', projDistance)
        return viewPoint, viewDir, projNormal, projDistance, viewWidth, viewHeight

    def getShader(self):
        colorName, colorType = "", ""
        diffuseColor_c = 0.
        exponent = 0.
        for c in self.root.findall('shader'):
            diffuseColor_c = np.array(c.findtext('diffuseColor').split()).astype(np.float64)
            colorType = c.get('type')
            colorName = c.get('name')
            exponent = np.array(c.findtext('exponent').split()).astype(np.float64)
            # print('name', c.get('name'))
            # print('diffuseColor', diffuseColor_c)
        return colorName, colorType, diffuseColor_c, exponent


class Sphere(FileParser):

    def getSurface(self):
        center, radius = 0., 0.
        for c in self.root.findall('surface'):
            center = np.array(c.findtext('center').split()).astype(np.float64)
            radius = np.array(c.findtext('radius').split()).astype(np.float64)
        return center, radius

    def getMultipleSurface(self):
        center, radius = np.empty(0), np.empty(0)
        for c in self.root.findall('surface'):
            center = np.array(c.findtext('center').split()).astype(np.float64)
            radius = np.array(c.findtext('radius').split()).astype(np.float64)
        return center, radius


class RayTracer:
    def __init__(self, viewPoint, radius, center):

        self.viewPoint = viewPoint
        self.radius = radius
        self.center = center
        self.t = 0

    def intersect(self, viewDir):
        view = self.viewPoint - self.center
        a1 = np.dot(view, view)
        b1 = 2. * np.dot(view, viewDir)
        c1 = np.dot(view, view) - self.radius * self.radius
        D1 = (b1 ** 2) - (4. * a1 * c1)
        # print((-b1 + np.sqrt(D1)) / 2.0 * a1)
        if D1 < 0:
            return False
        else:
            return (-b1 - np.sqrt(D1)) / 2.0 * a1

    def calculate_normal(self, viewDir, sphere_center):
        return (self.intersect(viewDir) - sphere_center) / np.linalg.norm(self.intersect(viewDir) - sphere_center)

    # def ray_algorithm(self, img, imageSize, color):
    #
    #     white = Color(1, 1, 1)
    #     red = Color(1, 0, 0)
    #     blue = Color(0, 0, 1)
    #
    #     for row in np.arange(imageSize[0]):
    #         for col in np.arange(imageSize[1]):
    #             if self.intersect() >= 0:
    #                 if color == 'blue':
    #                     img[row][col] = blue.toUINT8()
    #                 elif color == 'red':
    #                     img[row][col] = red.toUINT8()
    #                 else:
    #                     img[row][col] = white.toUINT8()
    #             else:
    #                 continue
    #     return img


class Shader:
    def __init__(self, viewDirection, diffuseValue, lightposition, intersectionPoint, lightIntensity,
                 specularExponent):
        self.viewDirection = viewDirection
        self.diffuseValue = diffuseValue
        self.lightposition = lightposition
        self.intersectionPoint = intersectionPoint
        self.lightIntensity = lightIntensity
        self.specularExponent = specularExponent

    def lambertian(self, normal, intersectionPoint):
        lightDirection = self.lightposition - intersectionPoint / np.linalg.norm(self.lightposition - intersectionPoint)
        return np.max(np.dot(normal, lightDirection), 0) * self.lightIntensity

    def phong(self, normal, intersectionPoint):
        lightDirection = self.lightposition - intersectionPoint / np.linalg.norm(self.lightposition - intersectionPoint)
        reflection_direction = 2 * np.dot(normal, lightDirection) * normal - lightDirection
        specular_reflection = np.dot(reflection_direction,
                                     -self.viewDirection) ** self.specularExponent * self.lightIntensity
        return self.lambertian(normal, intersectionPoint) + specular_reflection


def main():
    # initialize variables
    fileFrom = sys.argv[1]
    NewFile = FileParser(fileFrom)
    NewSphere = Sphere(fileFrom)
    newCenter, newRadius = NewSphere.getSurface()
    newViewPoint, newViewDir, newProjNormal, newProjDist, CamWidth, CamHeight = NewFile.getCamera()
    Ray = RayTracer(newViewPoint, newRadius, newCenter)
    SphereColor, ShadeType, ShadeValue, newExponent = NewFile.getShader()
    newLight, newIntensity = NewFile.getLight()
    newShader = Shader(newViewDir, ShadeValue, newLight, Ray.intersect(newViewDir), newIntensity, newExponent)
    # code.interact(local=dict(globals(), **locals()))
    imgSize = NewFile.getImageSize()
    # print(np.cross(viewDir, viewUp))
    newNormal = Ray.calculate_normal(newViewDir, newCenter)

    cameraRatio = CamWidth / CamHeight

    # Create an empty image
    channels = 3
    img = np.zeros((imgSize[1], imgSize[0], channels))
    img[:, :] = 0

    # replace the code block below!
    white = Color(1,1,1)
    blue = Color(1,0, 0)
    red = Color(0,0,1)
    # Start Ray Tracing Algorithm
    for i in np.arange(imgSize[0]):
        for j in np.arange(imgSize[1]):

            t = Ray.intersect(newViewDir)
            newNormal = Ray.calculate_normal(newViewDir, newCenter)
            newViewDir /= np.linalg.norm(newViewDir)
            # Calculate the ray
            if t >= 0:
                if ShadeType == 'Phong':
                    img[i][j] = newShader.phong(newNormal, t)
                else:
                    img[i][j] = newShader.lambertian(newNormal, t)
            else:
                img[i][j] = Color(0, 0, 0).toUINT8()

    rawimg = Image.fromarray(img, 'RGB')
    # rawimg.save('out.png')
    rawimg.save(fileFrom + '.png')


if __name__ == "__main__":
    main()
