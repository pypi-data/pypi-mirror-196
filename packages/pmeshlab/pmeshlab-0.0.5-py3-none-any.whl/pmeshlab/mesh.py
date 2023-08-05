import pymeshlab
from pymeshlab import Mesh as _Mesh
import numpy as np
import subprocess
from gnutools.utils import id_generator
import os
import trimesh

class Mesh:
    def __init__(self, input):
        self._model = pymeshlab.MeshSet()
        if type(input) == str:
            self._model.load_new_mesh(input)
        elif type(input) == _Mesh:
            self._model.add_mesh(input)
        elif type(input) in [np.array, trimesh.caching.TrackedArray]:
            output_file = f"/tmp/.{id_generator(128)}.xyz"
            np.savetxt(output_file, input)
            self._model.load_new_mesh(output_file)
            os.remove(output_file)

    @staticmethod
    def fingerprint(filename):
        batcmd = ["xvfb-run", "-a", "meshlabserver", "-i", filename]
        p = subprocess.Popen(batcmd, stdout=subprocess.PIPE)
        result = p.stdout.read()
        splits = result.decode().split("\n")[-2].split(" ")
        return int(splits[-4]), int(splits[-2])

    def show(self):
        return self.to_nmesh().show()

    def to_nmesh(self):
        from nmesh import NMesh
        from trimesh import Trimesh

        return NMesh(
            Trimesh(
                vertices=self.vertices(),
                faces=self.faces(),
                face_colors=self.face_colors(),
                vertex_colors=self.vertex_colors(),
            )
        )

    def vertices(self):
        return self._model[0].vertex_matrix()

    def faces(self):
        return self._model[0].face_matrix()

    def face_colors(self):
        try:
            return self._model[0].face_color_matrix()
        except:
            return []

    def vertex_colors(self):
        try:
            return self._model[0].vertex_color_matrix()
        except:
            return []

    def face_color(self):
        return self._model[0].face_color_matrix()[0]

    def discrete_curvatures(self):
        output = self._model.apply_filter(
            "compute_scalar_by_discrete_curvature_per_vertex"
        )
        return self, output

    def split_binary(self):
        self.discrete_curvatures()
        c0, c1, border = self.to_nmesh().split_binary()
        return c0.to_PyMeshLab(), c1.to_PyMeshLab(), border.to_PyMeshLab()

    @staticmethod
    def get_vertex_wn(file):
        ms = pymeshlab.MeshSet()
        ms.load_new_mesh(file)
        ms.apply_filter("compute_normals_for_point_sets")
        ms.normalize_vertex_normals()
        vertex_wn = np.concatenate(
            (ms[0].vertex_matrix(), ms[0].vertex_normal_matrix()), axis=1
        )
        return vertex_wn

    def export(self, *args, **kwargs):
        self.to_nmesh().export(*args, **kwargs)

    def cp2mesh(self, taubin=True, skip_normals=False):
        self._model.compute_normal_for_point_clouds(k=100) if not skip_normals else None
        self._model.generate_surface_reconstruction_screened_poisson()
        self._model = Mesh(self._model[1])._model
        self._model.apply_coord_taubin_smoothing() if taubin else None
        return self

    def ball_pivoting_reconstruction(self):
        model = self._model
        model.compute_normal_for_point_clouds()
        model.generate_surface_reconstruction_ball_pivoting(ballradius=pymeshlab.Percentage(2.5))
        model.apply_coord_taubin_smoothing(stepsmoothnum=100)
        model.generate_surface_reconstruction_screened_poisson()
        self._model = Mesh(self._model[1])._model
        model = self._model
        model.apply_coord_taubin_smoothing(stepsmoothnum=100)
        return self
    
