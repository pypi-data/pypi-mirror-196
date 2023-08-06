import numpy as np
import open3d as o3d

def create_points(depth):
    # create a point cloud from a depth image
    h, w = depth.shape
    theta, phi = np.mgrid[0:np.pi:h*1j,0:2*np.pi:w*1j]
    # points in the right-hand coordinate system. From the camera point of view:
    # x points to the right
    # y points up
    # z points backwards
    x = -depth * np.sin(theta) * np.sin(phi)
    y = depth * np.cos(theta)
    z = depth * np.sin(theta) * np.cos(phi)
    return np.dstack((x, y, z)).reshape((-1, 3)).astype('float32')

def create_triangles(h, w):
    # create triangles for a mesh assuming the points are in a grid
    i, j = np.mgrid[:h,:w]
    idx = i * w + j
    tri_up = np.dstack((idx[:-1,:], np.roll(idx[:-1,:], -1, axis=1), idx[1:])).reshape((-1, 3))
    tri_down = np.dstack((np.roll(idx[:-1,:], -1, axis=1), np.roll(idx[1:,:], -1, axis=1), idx[1:])).reshape((-1, 3))
    return np.concatenate((tri_up, tri_down), axis=0).astype('uint32')

def to_ply(rgb_image, depth_image, output_filename):
    points = create_points(depth_image)
    triangles = create_triangles(depth_image.shape[0], depth_image.shape[1])
    # create ply file with points, triangles and colors
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(points)
    mesh.triangles = o3d.utility.Vector3iVector(triangles)
    mesh.vertex_colors = o3d.utility.Vector3dVector(rgb_image.reshape(-1, 3) / 255.0)
    o3d.io.write_triangle_mesh(output_filename, mesh)