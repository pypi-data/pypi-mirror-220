'''
Matthew Ellison
July 2023

Future Improvements:
    - optimize zero coefficients in LinearEquality
'''

from .fractions_and_interval_arithmetic import Fraction
import random

liberal_CLP_success = True

def choose(n, k):
    out = 1
    for i in range(k):
        out *= n - i
    for i in range(1, k + 1):
        out /= i
    return out

class LinearEquality():
    def __init__(self, lhs_var, linear_combination_dict):
        '''
        example:
            x = 3y + z + 5
            lhs_var : 'x'
            linear_combination_dict : {'y': 3, 'z': 1, '1': 5}
        '''
        self.lhs_var = lhs_var
        self.rhs_dict = linear_combination_dict 
    def solve(self, rhs_var):
        assert rhs_var in self.rhs_dict
        coeff = self.rhs_dict[rhs_var]
        assert coeff != 0
        new_rhs_dict = dict()
        new_rhs_dict[self.lhs_var] = 1 / coeff
        for item in self.rhs_dict:
            if item != rhs_var:
                new_rhs_dict[item] = - self.rhs_dict[item] / coeff
        return LinearEquality(rhs_var, new_rhs_dict)
    def rhs_coeff(self, var):
        assert var in self.rhs_dict
        return self.rhs_dict[var]
    def __str__(self):
        out = str(self.lhs_var)
        out += ' ='
        first = True
        for var in self.rhs_dict:
            coeff = self.rhs_dict[var]
            if coeff == 0:
                continue
            if coeff < 0:
                if var == '1':
                   out += f' - {-coeff}' 
                else:
                    out += f' - {-coeff}{var}'
            else:
                symb = '' if first else '+'
                if var == '1':
                    out += f' {symb} {coeff}'
                else:
                    out += f' {symb} {coeff}{var}' 
            first = False
        return out
    def add_rhs_term(self, new_var, new_coeff):
        self.rhs_dict[new_var] = new_coeff
    def substitute(self, other):
        assert other.lhs_var in self.rhs_dict
        scale = self.rhs_dict[other.lhs_var]
        del self.rhs_dict[other.lhs_var]
        for other_var in other.rhs_dict:
            other_coeff = other.rhs_dict[other_var]
            if other_var in self.rhs_dict:
                self.rhs_dict[other_var] += scale * other_coeff
            else:
                self.add_rhs_term(other_var, scale * other_coeff)
        
def generate_lenke_eqs_from_LCP_qM(q, M, one_in_type = Fraction(1)):
    #quick checks
    assert len(q) == len(M)
    for row in M:
        assert len(row) == len(q)
    #and generate
    out = []
    for row_idx in range(len(q)):
        eq = LinearEquality(f"w_{row_idx}", {'1' : q[row_idx]})
        for j, entry in enumerate(M[row_idx]):
            eq.add_rhs_term(f"z_{j}", entry)
        eq.add_rhs_term(f"z_{len(q)}", one_in_type)
        out.append(eq)
    return out

def solve_LCP_lenke(q, M, one_in_type, verbose = False):
    eqs = generate_lenke_eqs_from_LCP_qM(q, M, one_in_type)
    to_make_basic = f"z_{len(q)}"
    first_time = True
    def print_eqs(eqs):
        for eq in eqs:
            print(eq)
        print(100 * '-')
    if verbose: print_eqs(eqs)
    num_iters = 0 #can track and see if we've cycled
    max_iters = choose(2 * len(q), len(q) + 1)
    while True:
        if verbose: print(f"switching in {to_make_basic}")
        #decide which basic to replace
        if first_time: #use eq with smallest constant
            min_const = eqs[0].rhs_coeff('1')
            min_idx = 0
            for i, eq in enumerate(eqs):
                const = eq.rhs_coeff('1')
                if const < min_const:
                    min_const = const
                    min_idx = i
            going_out_idx = min_idx
            if verbose: print(f"switching out {eqs[going_out_idx].lhs_var}")
            first_time = False
        else: 
            '''
            let y = to_make_basic 
            look for the equation where the coeff of y is negative and -const / coeff is minimized
            ''' 
            min_ratio = None
            min_idxs = None
            for i, eq in enumerate(eqs):
                coeff = eq.rhs_coeff(to_make_basic)
                if coeff < 0:
                    ratio = - eq.rhs_coeff('1') / coeff
                    if (min_ratio is None) or (ratio < min_ratio):
                        min_ratio = ratio
                        min_idxs = [i]
                    else:
                        if ratio == min_ratio:
                            min_idxs.append(i)
            if min_ratio is None:
                #we can still have success if z_6 has constant term 0
                for eq in eqs:
                    if eq.lhs_var == f'z_{len(q)}':
                        if eq.rhs_dict['1'] != 0 or not liberal_CLP_success:
                            raise Exception("The LCP has no solution")
                        else:
                            #also success
                            wz_values = dict()
                            for eq in eqs:
                                wz_values[eq.lhs_var] = eq.rhs_coeff('1')
                            for i in range(len(q)):
                                if f'w_{i}' not in wz_values:
                                    wz_values[f'w_{i}'] = 0
                                if f'z_{i}' not in wz_values:
                                    wz_values[f'z_{i}'] = 0
                            return wz_values 
            else:
                going_out_idx = random.choice(min_idxs)
                if verbose: print(f"switching out {eqs[going_out_idx].lhs_var}")
        #make the replacement
        going_out_var = eqs[going_out_idx].lhs_var
        new_eq = eqs[going_out_idx].solve(to_make_basic)
        new_eqs = []
        for i, eq in enumerate(eqs):
            if i == going_out_idx:
                new_eqs.append(new_eq)
            else:
                new_eqs.append(eq)
                new_eqs[-1].substitute(new_eq)
        eqs = new_eqs
        if verbose: print_eqs(eqs)
        #decide what to replace next
        if going_out_var == f"z_{len(q)}":
            #SUCCESS!
            wz_values = dict()
            for eq in eqs:
                wz_values[eq.lhs_var] = eq.rhs_coeff('1')
            for i in range(len(q)):
                if f'w_{i}' not in wz_values:
                    wz_values[f'w_{i}'] = 0
                if f'z_{i}' not in wz_values:
                    wz_values[f'z_{i}'] = 0
            return wz_values
        to_make_basic = {'w': 'z', 'z': 'w'}[going_out_var[0]] + going_out_var[1:]
        num_iters += 1
        if num_iters > max_iters: 
            raise Exception("Cycling")

def solve_CQP(A = None, b = None, c = 0, D = None, e = None, map_to_type = lambda x: x):
    '''
    the problem is to minimize
    1/2 x^T A x + b^T x + c subject to x >= 0 and Dx >= e.
    '''
    #empty case
    if (A is None) and (b is None):
        return c, []
    #infer number of variables and data type
    data_type = None
    if A is not None:
        num_vars = len(A)
        for row in A:
            for item in row:
                if item != 0:
                    data_type = type(map_to_type(item))
                    break
            if data_type is not None:
                break
    else:
        num_vars = len(b)
        if data_type is None:
            for item in b:
                if item != 0:
                    data_type = type(map_to_type(item))
                    break
    if data_type is None:
        data_type = int
    #fill in A,b Nones
    if A is None:
        A = [[0 for j in range(num_vars)] for i in range(num_vars)]
    if b is None:
        b = num_vars * [0]
    #build q
    q = []
    q = q + b
    if e is not None:
        q = q + [-elt for elt in e]
    if map_to_type is not None:
        q = list(map(map_to_type, q))
    #build M
    if D is None:
        dim_M = num_vars
    else:
        dim_M = num_vars + len(D)
    M = [[0 for j in range(dim_M)] for i in range(dim_M)]
    for i in range(num_vars):
        for j in range(num_vars):
            M[i][j] = map_to_type(A[i][j])
    if D is not None:
        for i in range(len(D)):
            for j in range(num_vars):
                M[num_vars + i][j] = map_to_type(D[i][j])
                M[j][num_vars + i] = map_to_type(-D[i][j])
    #solve LCP
    lcp_sol = solve_LCP_lenke(q, M, data_type(1))
    #get solution vector
    x = []
    for i in range(num_vars):
        x.append(lcp_sol[f"z_{i}"])
    #find optimal value
    A_term = 0
    for i in range(num_vars):
        for j in range(num_vars):
            A_term = A_term + x[i] * map_to_type(A[i][j]) * x[j]
    A_term = A_term / 2
    b_term = 0
    if b is not None:
        for i in range(num_vars):
            b_term = b_term + map_to_type(b[i]) * x[i]
    opt_val = A_term + b_term + c
    return opt_val, x

def simplex_square_distance(s1_pts, s2_pts, map_to_type = lambda x: x):
    '''
    returns (d_min^2, (closest_pt on s1), (closest_pt on s2))
    '''
    #we will build a CQP and solve it
    d = len(s1_pts[0])
    s1_dim = len(s1_pts) - 1
    s2_dim = len(s2_pts) - 1
    #build A
    A_dim = s1_dim + s2_dim + 2
    A = [[0 for j in range(A_dim)] for i in range(A_dim)]
    for i in range(s1_dim + 1):
        for j in range(s1_dim + 1):
            for k in range(d):
                A[i][j] = A[i][j] + map_to_type(s1_pts[i][k]) * map_to_type(s1_pts[j][k])
            A[i][j] = 2 * A[i][j]
    for i in range(s2_dim + 1):
        for j in range(s2_dim + 1):
            for k in range(d):
                A[i + s1_dim + 1][j + s1_dim + 1] = A[i + s1_dim + 1][j + s1_dim + 1] + map_to_type(s2_pts[i][k]) * map_to_type(s2_pts[j][k]) 
            A[i + s1_dim + 1][j + s1_dim + 1] = 2 * A[i + s1_dim + 1][j + s1_dim + 1]
    for i in range(s1_dim + 1):
        for j in range(s2_dim + 1):
            for k in range(d):
                A[i][j + s1_dim + 1] = A[i][j + s1_dim + 1] - map_to_type(s1_pts[i][k]) * map_to_type(s2_pts[j][k])
            A[j + s1_dim + 1][i] = 2 * A[i][j + s1_dim + 1]
            A[i][j + s1_dim + 1] = 2 * A[i][j + s1_dim + 1] 
    #build D
    D = [[map_to_type(0) for j in range(2 * d)] for i in range(4)]
    for i in range(s1_dim + 1):
        D[0][i] = map_to_type(1)
        D[1][i] = map_to_type(-1)
    for i in range(s2_dim + 1):
        D[2][s1_dim + 1 + i] = map_to_type(1)
        D[3][s1_dim + 1 + i] = map_to_type(-1)
    #build e
    e = [1,-1,1, -1]
    #solve the qp
    val, sol_vec = solve_CQP(A = A, D = D, e = e, map_to_type = map_to_type)
    min_sq_dist = val
    s1_closest_pt = [map_to_type(0) for i in range(d)]
    s2_closest_pt = [map_to_type(0) for i in range(d)]
    for i in range(d):
        for j, pt in enumerate(s1_pts):
            s1_closest_pt[i] += pt[i] * sol_vec[j]
        for j, pt in enumerate(s2_pts):
            s2_closest_pt[i] += pt[i] * sol_vec[s1_dim + 1 + j]
    return min_sq_dist, (s1_closest_pt, s2_closest_pt)

if __name__ == '__main__':
    test = [3]
    if 0 in test:
        # x = 4 y + 3 z - 2
        comb = LinearEquality('x', {'y' : Fraction(4), 'z' : Fraction(3), '1' : Fraction(-2)})
        print(comb)
        #comb2 = comb.solve('y')
        #print(comb2)
        # z = 3t + y
        other_comb = LinearEquality('z', {'t' : Fraction(3), 'y' : Fraction(1)})
        print(other_comb)
        comb.substitute(other_comb)
        print(comb)
    if 1 in test:
        q = [2,-1,3,-2]
        q = list(map(Fraction, q))
        M = [[0,0,1,-1],[0,0,1,-2],[-1,-1,0,0],[1,2,0,0]]
        M = [list(map(Fraction, row)) for row in M]
        print(solve_LCP_lenke(q, M, Fraction(1)))
    if 2 in test:
        print(solve_CQP(b = [2, -1], D = [[-1,-1], [1,2]], e = [-3, 2], map_to_type = Fraction))
    if 3 in test:
        print(simplex_square_distance([[3,0], [1,0]], [[0,0], [0,1]], map_to_type = Fraction)) 
        print("expect distance 1, points (1,0), (0,0)")
        print(simplex_square_distance([[-1,-1], [1,1]], [[0,0], [0,1]], map_to_type = Fraction))
        print("expect distance 0, (0,0), (0,0)")
        print(simplex_square_distance([[-1,-1], [1,1]], [[0,1], [0,2]], map_to_type = Fraction))
        print("expect distance 1/2, (1/2, 1/2), (0,0)")
        print(simplex_square_distance([[1,0,0], [0,1,0], [0,0,1]], [[2,2,2],[3,3,3]], map_to_type = Fraction))
        print("expect 25/3, (1/3,1/3,1/3), (2,2,2)")
        print(simplex_square_distance([[1,0,0,0], [0,1,0,0], [0,0,1,0],[0,0,0,1]], [[2,2,2,2],[3,3,3,3]], map_to_type = Fraction)) 
        print("expect (Fraction(49, 4), ([Fraction(1, 4), Fraction(1, 4), Fraction(1, 4), Fraction(1, 4)], [Fraction(2, 1), Fraction(2, 1), Fraction(2, 1), Fraction(2, 1)]))")
        print(simplex_square_distance([[1,0,0], [0,1,0], [0,0,1]], [[1,0,0],[0,1,0]], map_to_type = Fraction))
        if True:
            import random
            min_int = -10
            max_int = 20
            f = lambda: random.randint(min_int, max_int)
            d = 20
            s1_dim = 5
            s2_dim = 13
            for i in range(100):
                s1 = [[f() for j in range(d)] for i in range(s1_dim + 1)]
                s2 = [[f() for j in range(d)] for i in range(s2_dim + 1)]
                print(s1, s2)
                print(simplex_square_distance(s1, s2, map_to_type = Fraction))
    if 4 in test:
        print(simplex_square_distance([[1,0]], [[1,0]], map_to_type = Fraction)) 