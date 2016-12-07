from taichi.visual import *
from taichi.util import Vector
from taichi.visual.texture import Texture
from taichi.visual.post_process import *
import math

def create_mis_scene(eye_position):
    downsample = 1
    width, height = 960 / downsample, 540 / downsample
    camera = Camera('perspective', width=width, height=height, fov_angle=70,
                    origin=(-3, 0, 3), look_at=(0, 0, 0), up=(0, 1, 0))

    scene = Scene()
    with scene:
        scene.set_camera(camera)
        rep = Texture.create_taichi_wallpaper(20, rotation=0, scale=0.95)
        material = SurfaceMaterial('pbr', diffuse_map=rep.id)
        #scene.add_mesh(Mesh('holder', material=material, translate=(0, -1, -7), scale=2))

        mesh = Mesh('plane', SurfaceMaterial('emissive', color=(1, 1, 1)),
                    translate=(0, 1, 0), scale=0.1, rotation=(180, 0, 0))
        #scene.add_mesh(mesh)

        material = SurfaceMaterial('plain_interface')
        vol = VolumeMaterial("homogeneous", scattering=10, absorption=0)
        material.set_internal_material(vol)
        mesh = Mesh('cube', material=material,
                    translate=(0, -0, -0), scale=0.3, rotation=(0, 0, 0))
        scene.add_mesh(mesh)

        envmap = EnvironmentMap('base', filepath='d:/assets/schoenbrunn-front_hd.hdr')
        scene.set_environment_map(envmap)

    return scene

if __name__ == '__main__':
    renderer = Renderer('pt', '../output/frames/volumetric.png', overwrite=True)

    eye_position = Vector(0.9, -0.3)
    scene = create_mis_scene(eye_position)
    renderer.set_scene(scene)
    renderer.initialize(min_path_length=1, max_path_length=10,
                        initial_radius=0.005, sampler='sobol', russian_roulette=False, volmetric=True, direct_lighting=1,
                        direct_lighting_light=1, direct_lighting_bsdf=1, envmap_is=1, mutation_strength=1, stage_frequency=3,
                        num_threads=8)
    renderer.set_post_processor(LDRDisplay(exposure=1, bloom_radius=0.00))
    renderer.render(1000, 100)
