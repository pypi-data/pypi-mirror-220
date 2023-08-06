import random
from math import pi, cos, sin

class Vec3():
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
	def __add__(self, other):
		return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
	def __sub__(self, other):
		return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
	def __mul__(self, other):
		if type(other) is Vec3:
			return self.x * other.x + self.y * other.y + self.z * other.z
		else:
			return self.__rmul__(other)
	def __rmul__(self, other):
		return Vec3(other * self.x, other * self.y, other * self.z)
	def __truediv__(self, other):
		return self.__rmul__(1/other)
	def __neg__(self):
		return Vec3(-self.x, -self.y, -self.z)
	def __xor__(self, other):
		new_x = self.y * other.z - self.z * other.y
		new_y = self.z * other.x - self.x * other.z
		new_z = self.x * other.y - self.y * other.x
		return Vec3(new_x, new_y, new_z)	
	def norm(self):
		return (self * self) ** .5
	def __abs__(self):
		return self / self.norm()
	def __str__(self):
		return f"Vec3({self.x}, {self.y}, {self.z})"	
	def tuple(self):
		return self.x, self.y, self.z
	def is_zero(self, tol = 1e-5):
		return self.x < tol and self.y < tol and self.z < tol
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.z == other.z
	def __hash__(self):
		return self.tuple().__hash__()	
	def __and__(self, other): #scalar project
		return self * abs(other)	
	def __rshift__(self, other): #vector project
		return (self & other) * abs(other)
	def rotate(self, other, theta): #CCW, theta in rads
		A = self - (self >> other)
		B = abs(other) ^ A
		return cos(theta) * A + sin(theta) * B

def randVec3():
	return Vec3(random.random(), random.random(), random.random())				

#print(abs(Vec3(1,1,1)))
########################
class MaterialInfo():
	def __init__(self, name, Ka = (0,0,0), Kd = (0,0,0), Ks = (0,0,0), d = 1):
		self.name = name
		self.Ka = Ka #ambient reflectivity (rgb)
		self.Kd = Kd #diffuse reflectivity (rgb)
		self.Ks = Ks #specular reflectivity (rgb)
		self.d = d   #opacity [0,1]
	def copy(self):
		return MaterialInfo(self.name, self.Ka, self.Kd, self.Ks, self.d)
	def filestring(self):
		out = f"newmtl {self.name}\n"
		out += f"Ka {self.Ka[0]} {self.Ka[1]} {self.Ka[2]}\n"
		out += f"Kd {self.Kd[0]} {self.Kd[1]} {self.Kd[2]}\n"
		out += f"Ks {self.Ks[0]} {self.Ks[1]} {self.Ks[2]}\n"
		out += f"d {self.d}\n"
		return out

def write_mtl(material_info_list, filename):
	f = open(filename, "w")
	for mat_info in material_info_list:
		f.write(mat_info.filestring())
		f.write('\n')
	f.close()

white_mat = MaterialInfo("white", Kd = (1,1,1))
red_mat = MaterialInfo("red", Kd = (1,0,0))
green_mat = MaterialInfo("green", Kd = (0,1,0))
blue_mat = MaterialInfo("blue", Kd = (0,0,1))
white_light = MaterialInfo("light", Ka = (20,20,20), Kd = (1,1,1)) 
all_mats = [white_mat, red_mat, green_mat, blue_mat, white_light]

def make_transparent(mat_info, d):
	copy = mat_info.copy()
	copy.d = d
	all_mats.append(copy)
	return copy	

class objObject():
	def __init__(self, name, mat_info, vertices, faces, opacity = 1):
		self.name = name
		self.mat_info = mat_info
		self.vertices = vertices
		self.faces = faces
	def filestring(self):
		out = f"o {self.name}\n"
		out += f"usemtl {self.mat_info.name}\n"
		for v in self.vertices:
			out += f"v {v.x} {v.y} {v.z}\n"
		out += "\n"
		for face in self.faces:
			out += "f"
			for idx in face:
				out += f" -{len(self.vertices) - idx + 1}"  
			out += "\n"
		return out	

def cylinder_obj(start_xyz, end_xyz, radius, num_sides):
	v_start = Vec3(*start_xyz)
	v_end = Vec3(*end_xyz)
	v_dif = v_end - v_start
	normal = abs(randVec3() ^ v_dif)	
	f_start = [v_start + radius * normal]
	for i in range(num_sides - 1):
		f_start.append(v_start + (f_start[-1] - v_start).rotate(-v_dif, 2*pi/num_sides))
	f_end = [v + v_dif for v in f_start]
	obj_vs = f_start + f_end
	obj_fs = [list(range(1, num_sides + 1)), list(range(num_sides + 1, 2 * num_sides + 1))[::-1]]
	for i in range(1, num_sides + 1):
		next = num_sides if i == 1 else i-1
		obj_fs.append([i, next, next + num_sides, i + num_sides])
	return obj_vs, obj_fs		

def triangle_obj(xyz_1, xyz_2, xyz_3, both_faces = True):
	v1, v2, v3 = Vec3(*xyz_1), Vec3(*xyz_2), Vec3(*xyz_3)
	if both_faces:
		return [v1, v2, v3], [[1,2,3], [1,3,2]]	
	else:
		return [v1, v2, v3], [[1,2,3]]

def write_obj(mat_file, objObjects, filename):
	f = open(filename, "w")
	f.write(f"mtllib {mat_file}\n\n")
	for obj in objObjects:
		f.write(obj.filestring())
		f.write("\n")	
	f.close()

if __name__ == '__main__':			
	write_mtl(all_mats, "test_autowrite.mtl")	
	cyl_vs, cyl_fs = cylinder_obj((0,0,0), (100,100,100), 10, 100)
	cyl_obj = objObject("cyl", green_mat, cyl_vs, cyl_fs)
	cyl_vs_2, cyl_fs_2 = cylinder_obj((20,20,0), (100,100,100), 10, 100)
	cyl_obj_2 = objObject("cyl2", red_mat, cyl_vs_2, cyl_fs_2)

	write_obj("test_autowrite.mtl", [cyl_obj, cyl_obj_2], "test_autowrite.obj")	
