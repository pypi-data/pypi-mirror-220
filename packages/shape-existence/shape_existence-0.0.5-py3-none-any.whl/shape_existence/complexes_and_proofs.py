from .flexible_cqp import simplex_square_distance
from .fractions_and_interval_arithmetic import Fraction, FractionArray
from .obj_stuff import *
import random

#helper functions
def sublists(L, size):
    if size == 0:
        return [[]]
    if size > len(L):
        return []
    use_first = list(map(lambda x: [L[0]] + x, sublists(L[1:], size - 1)))
    dont_use_first = sublists(L[1:], size)
    return use_first + dont_use_first
def bannerize(text_line):
    return len(text_line) * '#' + '\n' + text_line + '\n' + len(text_line) * '#'
def tabbed_string(text, num_tabs = 1):
    lines = text.split('\n')
    return ''.join([num_tabs * '\t' + line + '\n' for line in lines])[:-1]

class AbstractSimplicialComplex():
    def __init__(self, data, mode = "maximal_simplices"):
        '''
        mode: either "polyhedron" or "maximal_simplices"
        data: 
            if mode is "polyhedron", the data should look like:\n
                e.g. {"a": ["b", "c", "d"], "b": ["d","c","a'], "c": ["a", "b","d"], "d": ["a", "c", "b"]}\n
                where the the keys of the dictionary are vertex names, and the corresponding value is a list
                of adjacent vertices in ccw order (or clockwise, it doesn't matter since we ignore orientation).
                The above example is (the surface of a) tetrahedron.

            if mode is "maximal_simplices", the data should be a list of maximal simplices in the complex,
            where a maximal simplex is represented by its list of vertices:\n
                e.g. [["a", "b", "c", "d"]] <-- a solid tetrahedron\n
                e.g. [["a", "b", "c"], ["a", "d"], ["e"] <-- a triangle (abc) with an edge (ad) coming off and an isolated vertex (e)
        '''
        self.mode = mode
        assert self.mode in ["polyhedron", "maximal_simplices"]
        self.data = data
        #enforce some basic ok-ness
        if self.mode == "polyhedron":
            assert len(self.data) > 0
            for vertex in self.data:
                assert len(self.data[vertex]) >= 3
        if self.mode == "maximal_simplices":
                assert len(self.data) > 0
    def __str__(self):
        out = f"mode: {self.mode}" + '\n'
        out += f"data: {self.data}"
        return out
    def dimension(self):
        if self.mode == "polyhedron":
            return 2
        elif self.mode == "maximal_simplices":
            return max(map(len, self.data)) - 1
        else:
            raise Exception("shouldn't reach this case")
    def k_simplices(self, k):
        '''returns a list of tuples of the edges (pairs of vertices)'''
        assert isinstance(k, int) and k >= 0
        out = set()
        if self.mode == "polyhedron":
            if k == 0:
                return list(self.data)
            elif k == 1:
                out = set()
                for vertex in self.data:
                    for neighbor in self.data[vertex]:
                        out.add(frozenset([vertex, neighbor]))
                return list(map(list, out))
            elif k == 2:
                out = set()
                for v in self.data:
                    for i, neighbor in enumerate(self.data[v]):
                        neighbor_2 = self.data[v][(i + 1) % len(self.data[v])]
                        out.add(frozenset([v, neighbor, neighbor_2]))
                return list(map(list, out))
            else:
                return []
        elif self.mode == "maximal_simplices":
            out = set()
            for maximal_simplex in self.data:
                #get all size k+1 subsets of maximal_simplex
                for k_simplex in sublists(maximal_simplex, k + 1):
                    out.add(frozenset(k_simplex))
            return list(map(list, out))
        else:
            Exception("should not arrive here")
        return list(map(list, out))
    def collision_simplex_pairs(self):
        '''
        returns a list of pairs of simplices (a list of vertices)
        which suffices to compute collision distance.
        more abstractly, it is a set S of non-adjacent pairs of simplices such
        that any non-adjacent pair is contained in one in S, where containment is componentwise.
        '''
        #naively implemented for now, all non-adjacent pairs
        out = []
        all_simplices = []
        for d in range(self.dimension() + 1):
            all_simplices += self.k_simplices(d)
        for i, s1 in enumerate(all_simplices):
            for s2 in all_simplices[i + 1 :]:
                #check non-adjacent
                non_adjacent = True
                for item in s1:
                    if item in s2:
                        non_adjacent = False
                        break
                if non_adjacent:
                    out.append((s1, s2))
        return out
    def heuristic_embed(self, dim, desired_sq_lengths, final_round_digits = 3, num_tries = 10, num_fine_tuning_tries = 5, verbose = False):
        verbose_print = lambda x: print(x) if verbose else None
        
        verbose_print(f"Attempting to embed in R ^ {dim} with close to the desired square edge lengths")
        verbose_print(f"Will work in floating point and round to {final_round_digits} digits at the end.")

        vertices = list(map(lambda x: x[0], self.k_simplices(0)))
        edges = list(map(tuple, self.k_simplices(1)))

        desired_copy = dict()
        for item in desired_sq_lengths:
            if isinstance(desired_sq_lengths[item], Fraction):
                desired_copy[item] = desired_sq_lengths[item].to_float()
            else:
                desired_copy[item] = desired_sq_lengths[item]

        desired_lengths = dict() 
        for edge in edges:
            if edge in desired_sq_lengths:
                desired_lengths[edge] = desired_copy[edge] ** .5
            elif (edge[1], edge[0]) in desired_sq_lengths:
                desired_lengths[edge] = desired_copy[(edge[1], edge[0])] ** .5
            else:
                assert "default" in desired_sq_lengths
                desired_lengths[edge] = desired_copy["default"] ** .5

        for attempt_no in range(1, num_tries + 1):
            verbose_print("\n" + f"Attempt {attempt_no} (max attempts is {num_tries})")
            verbose_print(tabbed_string("Randomly initializing vertices in the unit cube"))

            point_dict = dict()
            for v in vertices:
                point_dict[v] = [random.random() for i in range(dim)]

            verbose_print(tabbed_string("Phase 1: edge springs and repelling nodes"))
            def spring_and_repel(t0, dt, t_max, spring_coeff, repel_coeff):
                t = t0
                average_diff = None
                while t < t_max:
                    #spring forces
                    if spring_coeff != 0:
                        total_diff = 0
                        for v1, v2 in edges:
                            dist = sum([(point_dict[v1][i] - point_dict[v2][i]) ** 2 for i in range(dim)]) ** .5
                            desired_length = desired_lengths[(v1, v2)]
                            multiplier = spring_coeff * (dist - desired_length)
                            total_diff += abs(dist - desired_length)
                            for k in range(dim):
                                diff = point_dict[v1][k] - point_dict[v2][k] 
                                point_dict[v1][k] -=  multiplier * diff * dt
                                point_dict[v2][k] += multiplier * diff * dt
                        new_average_diff = total_diff / len(edges)
                        #print(new_average_diff)
                        if new_average_diff < 1e-20 or (average_diff is not None and new_average_diff / average_diff > .999999):
                            if repel_coeff == 0:
                                return
                        average_diff = new_average_diff

                    #repelling forces
                    if repel_coeff != 0:
                        for i, v1 in enumerate(vertices):
                            for v2 in vertices[i + 1: ]:
                                dist = sum([(point_dict[v1][i] - point_dict[v2][i]) ** 2 for i in range(dim)]) ** .5
                                multiplier = repel_coeff / (dist * dist + .01)
                                for k in range(dim):
                                    diff = point_dict[v1][k] - point_dict[v2][k] 
                                    point_dict[v1][k] +=  multiplier * diff * dt
                                    point_dict[v2][k] -= multiplier * diff * dt
                    #step time
                    t += dt
                return
            spring_and_repel(t0 = 0, dt =.1, t_max = 3, spring_coeff = 1, repel_coeff = .5)

            verbose_print(tabbed_string("Phase 2: edge springs"))
            spring_and_repel(t0 = 0, dt =.1, t_max = 80, spring_coeff = 2, repel_coeff = 0)
            spring_and_repel(t0 = 0, dt =.1, t_max = 80, spring_coeff = 1, repel_coeff = 0)
            spring_and_repel(t0 = 0, dt =.1, t_max = 80, spring_coeff = .5, repel_coeff = 0) 
            spring_and_repel(t0 = 0, dt =.1, t_max = 80, spring_coeff = .25, repel_coeff = 0)
            spring_and_repel(t0 = 0, dt =.1, t_max = 80, spring_coeff = .125, repel_coeff = 0)
            #convert to realization
            rsc = RealizedSimplicialComplex(self, point_dict, lambda x: Fraction(x, float_digits = final_round_digits, allow_float_conversion = True))

            verbose_print(tabbed_string("Checking non-self-intersecting"))
            sq_coll_dist = rsc.square_collision_distance()
            if sq_coll_dist > Fraction(1, 100):
                verbose_print(tabbed_string(f"True, square collision dist is {sq_coll_dist}", 2))
                verbose_print(f"\nSuccess")
                return rsc
            else:
                verbose_print(tabbed_string(f"False, self-intersecting{', will try again' if attempt_no < num_tries else ''}", 2))

        verbose_print("\nHeuristic embedding failed")
        return None

class RealizedSimplicialComplex() :
    def __init__(self, asc, point_dict, coordinate_map = lambda x : x):
        '''
        asc: an AbstractSimplicialComplex object representing the abstract structure
        point_dict: a dictionary mapping vertex names to lists of coordinates
                    e.g. {"a": [Fraction(1), Fraction(4), Fraction(5)], "b": ... }
        coordinate_map: a function that will be 
        applied to each coordinate on initialization
                for example, one could give the coordinates of point_dict as floating point numbers,
                then make coordinate_map a function which rounds a float to 3 digits and yields a Fraction object.
        '''
        self.asc = asc
        self.point_dict = point_dict
        self.d = None
        for item in self.point_dict:
            coords = self.point_dict[item]
            self.point_dict[item] = [coordinate_map(entry) for entry in coords]
            #make sure everything's the same dimension
            if self.d is None:
                self.d = len(coords)
            else:
                assert self.d == len(coords)
        self.sq_coll_dist = None
    def save_as_obj(self, filename = "my_3d_file.obj", folder_path = './'):
        assert self.d > 1
        #plot edges
        objs = []
        for i, edge in enumerate(self.asc.k_simplices(1)):
            v1, v2 = edge
            v1_coords, v2_coords = self.point_dict[v1], self.point_dict[v2]
            v1_to_plot = list(map(lambda x: x.to_float(), v1_coords + [Fraction(0)] if self.d == 2 else v1_coords[:3]))
            v2_to_plot = list(map(lambda x: x.to_float(), v2_coords + [Fraction(0)] if self.d == 2 else v2_coords[:3]))
            cyl_vs, cyl_fs = cylinder_obj(v1_to_plot, v2_to_plot, .01, 30)
            cyl_obj = objObject(f"cyl{i}", blue_mat, cyl_vs, cyl_fs)
            objs.append(cyl_obj)
        write_mtl(all_mats, folder_path + "shape_existence.mtl")
        write_obj("shape_existence.mtl", objs, folder_path + filename)
    def __str__(self):
        out = f"Abstract data:"
        out += tabbed_string("\n" + self.asc.__str__())
        out += f"\nCoordinate Data:\n"
        for v in self.point_dict:
            out += f"\t{v} : {self.point_dict[v]}\n"
        return out[:-1] 
    def square_collision_distance(self):
        if self.sq_coll_dist is not None:
            return self.sq_coll_dist
        collision_pairs = self.asc.collision_simplex_pairs()
        min_sq_dist = None
        for s1, s2 in collision_pairs:
            s1_coords = [self.point_dict[v] for v in s1]
            s2_coords = [self.point_dict[v] for v in s2]
            sq_dist = simplex_square_distance(s1_coords, s2_coords)[0]
            if min_sq_dist is None or sq_dist < min_sq_dist:
                min_sq_dist = sq_dist
        self.sq_coll_dist = min_sq_dist
        return min_sq_dist
    def rho_squared(self, desired_sq_lengths):
        default_sq_length = None
        if "default" in desired_sq_lengths:
            default_sq_length = desired_sq_lengths["default"]
        total = 0
        for v1, v2 in self.asc.k_simplices(1):
            p1, p2 = self.point_dict[v1], self.point_dict[v2]
            assert len(p1) == len(p2)
            sq_dist = sum([(p1[i] - p2[i]) * (p1[i] - p2[i]) for i in range(len(p1))])
            if (v1, v2) in desired_sq_lengths:
                des_sq_length = desired_sq_lengths[(v1, v2)]
            elif (v2, v1) in desired_sq_lengths:
                des_sq_length = desired_sq_lengths[(v2, v1)]
            else:
                assert default_sq_length is not None
                des_sq_length = default_sq_length
            total = total + (sq_dist - des_sq_length) * (sq_dist - des_sq_length)
        return total 
    def Dl_squared(self):
        vertices = self.asc.k_simplices(0)
        edges = self.asc.k_simplices(1)
        d = self.d
        V = len(vertices)
        E = len(edges)
        jacobian = [[0 for j in range(d * V)] for i in range(E)]
        for edge_idx, edge in enumerate(edges):
            v1, v2 = edge
            v1_coords, v2_coords = self.point_dict[v1], self.point_dict[v2]
            i1, i2 = vertices.index([v1]), vertices.index([v2])
            for k in range(d):
                jacobian[edge_idx][d * i1 + k] = 2 * (v1_coords[k] - v2_coords[k])
                jacobian[edge_idx][d * i2 + k] = 2 * (v2_coords[k] - v1_coords[k])
        return jacobian
    def sigma_min(self):
        jacobian = FractionArray(self.Dl_squared())
        return jacobian.bound_smallest_sv()
    def prove_existence(self, desired_sq_lengths, verbose = False):
        verbose_print = lambda x: print(x) if verbose else None

        verbose_print("Attempting to prove existence")
        verbose_print("\nStarting realization:")
        verbose_print(tabbed_string(self.__str__()))
        verbose_print("\nDesired square lengths:")
        if "default" in desired_sq_lengths:
            verbose_print(tabbed_string(f"default : {desired_sq_lengths['default']}"))
        for item in desired_sq_lengths:
            if item == "default":
                continue
            verbose_print(tabbed_string(f"{item} : {desired_sq_lengths[item]}"))

        #check d|V| >= |E|
        verbose_print("\nChecking inequality 1:")
        d = self.d
        V = len(self.asc.k_simplices(0))
        E = len(self.asc.k_simplices(1))
        verbose_print(tabbed_string(f" d  = {d}"))
        verbose_print(tabbed_string(f"|V| = {V}"))
        verbose_print(tabbed_string(f"|E| = {E}")) 
        if not (d * V >= E):
            fail_string = "Failed: not d|V| >= |E|"
            verbose_print(tabbed_string(fail_string))
            return False, fail_string
        verbose_print(tabbed_string("Success: d|V| >= |E|"))

        #check self-intersection
        verbose_print("\nChecking self-intersection:")
        coll_dist_squared = self.square_collision_distance()
        coll_dist = coll_dist_squared.sqrt()
        verbose_print(tabbed_string(f"Square collision distance = {coll_dist_squared}"))
        verbose_print(tabbed_string(f"Collision distance in {coll_dist}"))
        if coll_dist == 0:
            fail_string = "Failed: starting realization self-intersecting"
            verbose_print(tabbed_string(fail_string))
            return False, fail_string
        verbose_print(tabbed_string("Success: starting realization non-self-intersecting"))

        #check sigma_min > 0
        verbose_print("\nChecking inequality 2:") 
        sigma_min = self.sigma_min() #fraction interval, or 0
        verbose_print(tabbed_string(f"sigma_min in {sigma_min}"))
        if not (sigma_min > 0):
            fail_string = f"Failed: sigma_min not positive"
            verbose_print(tabbed_string(fail_string))
            return False, fail_string
        verbose_print(tabbed_string(f"Success: sigma_min > 0")) 

        #check the perturbation inequality (point 3 in paper)
        verbose_print("\nChecking inequality 3:") 
        rho_squared = self.rho_squared(desired_sq_lengths)
        rho = rho_squared.sqrt() #fraction interval
        lhs = rho
        rhs = (sigma_min * sigma_min) / (16 * Fraction(E).sqrt())
        verbose_print(tabbed_string(f"rho_squared = {rho_squared}"))
        verbose_print(tabbed_string(f"rho in {rho}"))
        verbose_print(tabbed_string(f"sigma_min ^ 2 / (16 * E ^ .5) in {rhs}"))
        if not lhs < rhs:
            fail_string = "Failed: unable to verify rho < sigma_min ^ 2 / (16 * E ^ .5)"
            verbose_print(tabbed_string(fail_string))
            return False, fail_string
        verbose_print(tabbed_string("Success: rho < sigma_min ^ 2 / (16 * E ^ .5)"))

        #check the perturbation collision inequality (point 4 in paper)
        verbose_print("\nChecking inequality 4:")  
        lhs_num = (sigma_min) - (sigma_min * sigma_min - 16 * rho * Fraction(E).sqrt()).sqrt()
        lhs_den = 8 * Fraction(E).sqrt()
        rhs = coll_dist / (Fraction(V).sqrt())
        verbose_print(tabbed_string(f"LHS NUM := sigma_min - [sigma_min ^ 2 - 16 * rho * |E| ^ .5 ] ^ .5 in {lhs_num}"))
        verbose_print(tabbed_string(f"LHS DEN := 8 * |E| ^ .5 in {lhs_den}"))
        verbose_print(tabbed_string(f"LHS     := (LHS NUM) / (LHS DEN) in {lhs_num / lhs_den}")) 
        verbose_print(tabbed_string(f"CD / |V| ^ .5 in {rhs}"))
        if not (lhs_num / lhs_den) < rhs:
            fail_string = f"Failed: unable to verify LHS < CD / |V| ^ .5"
            verbose_print(tabbed_string(fail_string))
            return False, fail_string
        verbose_print(tabbed_string(f"Success: LHS < CD / |V| ^ .5"))

        #we've succeeded
        success_string = "Success: existence proven"
        verbose_print('\n' + success_string)
        return True, success_string

if __name__ == '__main__':
    examples = [4]
    if 1 in examples:
        #tetrahedron
        tetrahedron_asc = AbstractSimplicialComplex(mode = "maximal_simplices", data = [["a", "b", "c", "d"]])
        tetrahedron_rsc = tetrahedron_asc.heuristic_embed(dim = 3, desired_sq_lengths = {"default" : 1}, final_round_digits = 5)
        tetrahedron_rsc.save_as_obj("tetrahedron.obj", "./obj_files/")
        tetrahedron_rsc.prove_existence(desired_sq_lengths = {"default" : Fraction(1)}, verbose = True)
    if 2 in examples:
        #octahdron
        octahedron_asc = AbstractSimplicialComplex(mode = "maximal_simplices", 
                                                   data = [["t", "1", "2"], ["t", "2", "3"], ["t", "3", "4"], ["t", "4", "1"],
                                                           ["b", "1", "2"], ["b", "2", "3"], ["b", "3", "4"], ["b", "4", "1"]]) 
        octahedron_rsc = octahedron_asc.heuristic_embed(dim = 3, desired_sq_lengths = {"default" : 1}, final_round_digits = 5)
        octahedron_rsc.save_as_obj("octahedron.obj", "./obj_files/")
        octahedron_rsc.prove_existence(desired_sq_lengths = {"default" : Fraction(1)}, verbose = True)
    if 3 in examples:
        #icosahedron
        icosahedron_asc = AbstractSimplicialComplex(mode = "maximal_simplices",
                                                    data = [["t", "a1", "a2"], ["t", "a2", "a3"], ["t", "a3", "a4"], ["t", "a4", "a5"], ["t", "a5", "a1"],
                                                            ["a1", "a2", "b1"], ["a2", "a3", "b2"], ["a3", "a4", "b3"], ["a4", "a5", "b4"], ["a5", "a1", "b5"],
                                                            ["b1", "b2", "a2"], ["b2", "b3", "a3"], ["b3", "b4", "a4"], ["b4", "b5", "a5"], ["b5", "b1", "a1"],
                                                            ["b", "b1", "b2"], ["b", "b2", "b3"], ["b", "b3", "b4"], ["b", "b4", "b5"], ["b", "b5", "b1"]])
        icosahedron_rsc = icosahedron_asc.heuristic_embed(dim = 3, desired_sq_lengths = {"default" : 1}, final_round_digits = 9)
        icosahedron_rsc.save_as_obj("icosahedron.obj", "./obj_files/")
        icosahedron_rsc.prove_existence(desired_sq_lengths = {"default" : Fraction(1)}, verbose = True)
    if 4 in examples:
        #existence of a triangle with sides 3, 4, and 5
        right_triangle = AbstractSimplicialComplex(mode = "maximal_simplices", 
                                                  data = [["a", "b"], ["b", "c"], ["c", "a"]])
        right_triangle_rsc = right_triangle.heuristic_embed(dim = 2, desired_sq_lengths = {("a", "b") : 9, ("b", "c") : 16, ("c", "a") : 25}, final_round_digits = 8)
        right_triangle_rsc.save_as_obj("345_triangle.obj", "./obj_files/")
        right_triangle_rsc.prove_existence(desired_sq_lengths = {("a", "b") : 9, ("b", "c") : 16, ("c", "a") : 25}, verbose = True)
