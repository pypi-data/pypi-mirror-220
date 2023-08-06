from scipy.linalg import svdvals
import random
import numpy as np

def gcd(a,b):
	if a < 0 or b < 0:
		return gcd(abs(a), abs(b))
	if b > a:
		return gcd(b,a)
	while True:
		if b == 0:
			return a
		a, b = b,  a % b

from math import gcd

class Fraction():
	def __init__(self, n, d = 1, float_digits = 8, allow_float_conversion = False):
		#manage types
		if not isinstance(d, int):
			raise Exception("Must provide an integer d on initialization (or use default)")	
		if not isinstance(n, int) and d != 1:
			raise Exception("Special initialization of Fraction should have d = 1.")	
		if isinstance(n, str):
			if n == "inf":
				self.n = 1
				self.d = 0
				return
			elif n == "-inf":
				self.n = -1
				self.d = 0
				return
			raise Exception(f"Cannot create fraction from value '{n}'")
		if isinstance(n, Fraction): #to make a copy
			self.n = n.n
			self.d = n.d 
			return
		if isinstance(n, float):
			if n == float("inf"):
				self.n = 1
				self.d = 0
				return
			elif n == float("-inf"):
				self.n = -1
				self.d = 0
				return
			else:
				if not allow_float_conversion:
					raise Exception("Direct conversion of float to frac not allowed!")
				temp = Fraction.frac_via_truncate_float(n, float_digits)
				self.n = temp.n
				self.d = temp.d
				return
		#manage signs
		sign = 1
		if n < 0:
			sign *= -1
			n = -n
		if d < 0:
			sign *= -1
			d = -d 			
		#manage undefined, zero, infinities
		if n == 0 and d == 0:
			raise Exception("Cannot create fraction 0/0.")
		if n == 0:
			self.n = 0
			self.d = 1
			return
		if d == 0:
			self.n = sign
			self.d = 0
			return
		#reduce by gcd and store
		g = gcd(n,d)
		self.n = sign * n // g
		self.d = d // g
	def frac_via_truncate_float(f, float_digits = 8):
		n_string = str(f)
		e_power = None
		if 'e' in n_string:
			e_idx = n_string.index('e')
			n_string, e_power = n_string[:e_idx], int(n_string[e_idx + 1:])
			#raise Exception(f"e's not handled for floating point number to fraction conversion: {n_string}")	
		try:
			dot_idx = n_string.index('.')
			digits_after_dot = len(n_string) - dot_idx - 1
			if digits_after_dot < float_digits:
				n_string = n_string[:dot_idx] + n_string[dot_idx + 1:] + (float_digits - digits_after_dot) * '0'
			else:
				n_string = n_string[:dot_idx] + n_string[dot_idx + 1: dot_idx + 1 + float_digits]
		except ValueError: #no . in number
			n_string += float_digits * '0'
		n = int(n_string)
		d = 10 ** float_digits
		if e_power is None:
			return Fraction(n,d)
		if e_power > 0:
			n *= 10 ** (e_power)
		else:
			d *= 10 ** (-e_power)
		return Fraction(n,d)	
	def is_inf(self):
		return self.n == 1 and self.d == 0
	def is_neginf(self):
		return self.n == -1 and self.d == 0
	def is_zero(self):
		return self.n == 0 and self.d == 1
	def is_int(self):
		return self.d == 1
	def to_int(self):
		if self.is_int():
			return self.n
		return None
	def __str__(self):
		if self.is_inf():
			return "inf"
		if self.is_neginf():
			return "-inf"
		if self.d == 1:
			return f"{self.n}"	
		return f"{self.n} / {self.d}"	
	def __neg__(self):
		return Fraction(-self.n, self.d)
	def inverse(self):
		return Fraction(self.d, self.n)
	def __add__(self, other):
		if not isinstance(other, Fraction):
			other = Fraction(other)
		if (self.is_inf() and other.is_neginf()) or (self.is_neginf() and other.is_inf()):
			raise Exception("Cannot add inf and neginf.")	
		if self.is_inf() or other.is_inf():
			return Fraction("inf")
		if self.is_neginf() or other.is_neginf():
			return Fraction("-inf")
		return Fraction(self.n * other.d + other.n * self.d, self.d * other.d)
	def __radd__(self, other):
		return self + other
	def __sub__(self, other):
		return self + (- other)
	def __rsub__(self, other):
		return (-self) + other
	def __mul__(self, other):
		#convert other
		if not isinstance(other, Fraction):
			if isinstance(other, FractionArray):
				return other.__rmul__(self)
			elif isinstance(other, int):
				other = Fraction(other)
			else:
				try:
					return other.__rmul__(self)
				except:
					other = Fraction(other)
		#check bad cases
		if ((self.is_inf() or self.is_neginf()) and other.is_zero()) or (self.is_zero() and (other.is_inf() or other.is_neginf())):
			raise Exception("Cannot multiply zero and infinite quantity.")
		return Fraction(self.n * other.n, self.d * other.d)
	def __rmul__(self, other):
		return self * other
	def __truediv__(self, other):
		if isinstance(other, Fraction):
			return self * other.inverse()
		elif isinstance(other, int):
			return self * Fraction(1,other)
		else:
			raise Exception(f"division not supported between fraction and '{type(other)}'.")
	def __rtruediv__(self, other):
		return self.inverse() * other
	def __pow__(self, other):
		if not isinstance(other, Fraction):
			other = Fraction(other)
		assert (other is not None) and other.d == 1
		if other.n == 0:
			return Fraction(1)
		elif other.n < 0:
			return self.inverse() ** (-other)
		else:
			out = 1
			for i in range(other.n):
				out *= self
			return out	 
	def __eq__(self, other):
		if not isinstance(other, Fraction):
			other = Fraction(other)
		return self.n == other.n and self.d == other.d
	def __lt__(self, other):
		if not isinstance(other, Fraction):
			other = Fraction(other)
		if self.is_inf():
			return False
		if other.is_inf():
			return True
		if other.is_neginf():
			return False
		if self.is_neginf():
			return True
		return self.n * other.d - other.n * self.d < 0
	def __le__(self, other):
		return self < other or self == other
	def __gt__(self, other):
		return not (self <= other)
	def __ge__(self, other):
		return not (self < other)
	def __repr__(self):
		return self.__str__()	
	def sqrt(self, num_digs = 8):
		assert self >= 0
		if self.is_inf():
			return FractionInterval(Fraction(1,0), Fraction(1,0))
		if self.is_zero():
			return FractionInterval(Fraction(0), Fraction(0))
		float_val = (self.n / self.d) ** .5
		lb = Fraction.lower_bound_on_nonnegative_floats([float_val], num_digs)
		ub = lb + Fraction(1, 10 ** num_digs)
		#now verify it works
		assert lb * lb <= self, print(self, lb * lb) 
		assert self <= ub * ub, print(self, ub * ub)
		return FractionInterval(lb, ub)
	def to_float(self):
		if self.is_inf():
			return float("inf")
		if self.is_neginf():
			return float("-inf")
		else:
			return self.n / self.d
	def lower_bound_on_nonnegative_floats(float_array, num_digits = 5):
		min_float = min(float_array)
		assert min_float >= 0
		return Fraction.frac_via_truncate_float(min_float, num_digits)

class FractionInterval():
	def __init__(self, left, right = None):
		if right is None:
			right = left
		self.left = Fraction(left)
		self.right = Fraction(right)
		assert self.left <= self.right
	def __str__(self, give_approx = True):
		if not give_approx:
			return f"[{self.left.__str__()}, {self.right.__str__()}]"
		else:
			return f"[{self.left.__str__()}, {self.right.__str__()}] ~ [{round(self.left.to_float(), 5)}, {round(self.right.to_float(), 5)}]"
	def __lt__(self, other):
		if not isinstance(other, FractionInterval):
			other = FractionInterval(other)
		return self.right < other.left
	def __gt__(self, other):
		if not isinstance(other, FractionInterval):
			other = FractionInterval(other)
		return other < self
	def __neg__(self):
		return FractionInterval(-self.right, -self.left)
	def inverse(self):
		if self.left == self.right == 0:
			raise Exception(f"Cannot invert interval {self}.")	
		if self.left >= 0 and self.right >= 0:
			if self.left == 0:
				return FractionInterval(1/self.right, Fraction("inf"))
			return FractionInterval(1/self.right, 1/self.left)	
		elif self.left <= 0 and self.right <= 0:
			if self.right == 0:	
				return FractionInterval(Fraction("-inf"), 1/self.left)
			return FractionInterval(1/self.right, 1/self.left)
		else:
			return FractionInterval(Fraction("-inf"), Fraction("inf"))
	def __add__(self, other):
		if not isinstance(other, FractionInterval):
			other = FractionInterval(other)
		return FractionInterval(self.left + other.left, self.right + other.right)	
	def __radd__(self, other):
		return self + other
	def __sub__(self, other):
		return self + (-other)
	def __rsub__(self, other):
		return (-self) + other
	def __mul__(self, other):
		if not isinstance(other, FractionInterval):
			other = FractionInterval(other)
		endpoints = [self.left * other.left, self.left * other.right, self.right * other.left, self.right * other.right]
		return FractionInterval(min(endpoints), max(endpoints))
	def __pow__(self, other):
		if other != 2:
			raise Exception("Only squaring of FractionIntervals is implemented")
		return self * self
	def __rmul__(self, other):
		return self * other
	def __truediv__(self, other):
		if not isinstance(other, FractionInterval):
			other = FractionInterval(other)
		return self * other.inverse()
	def __rtruediv__(self, other):
		return self.inverse() * other
	def sqrt(self):
		assert self.left >= 0 and self.right >= 0
		left_int = self.left.sqrt()
		right_int = self.right.sqrt()
		return FractionInterval(left_int.left, right_int.right)				
				
class FractionArray():
	def __init__(self, array, allow_float_conversions = False):
		self.array = []
		self.m = len(array)
		self.n = len(array[0])
		self.had_to_convert = False
		for row in array:
			new_row = []
			for item in row:
				new_row.append(Fraction(item, allow_float_conversion = allow_float_conversions))
			self.array.append(new_row)
	def identity(n):
		assert isinstance(n, int) and n > 0
		return FractionArray([[1 if i == j else 0 for j in range(n)] for i in range(n)])	
	def assert_square(self):
		assert self.m == self.n, f"matrix must be square. dimensions: ({self.m, self.n})"
	def copy(self):
		return FractionArray([[self.array[i][j] for j in range(self.n)] for i in range(self.m)])
	def elementwise_func_in_place(self, f):
		for i in range(self.m):
			for j in range(self.n):
				self.array[i][j] = f(self.array[i][j])
		return self
	def elementwise_func_to_new(self, f):
		return self.copy().elementwise_func_in_place(f)
	def elementwise_binop(self, other, binop):
		assert isinstance(other, FractionArray)
		assert self.m == other.m and self.n == other.n, f"self.m, self.n: {self.m, self.n}; other.m, other.n: {other.m, other.n}"
		return FractionArray([[binop(self.array[i][j], other.array[i][j]) for j in range(self.n)] for i in range(self.m)])
	def __add__(self, other):
		return self.elementwise_binop(other, lambda x,y: x+y)
	def __neg__(self, other):
		return self.elementwise_func_to_new(lambda x: -x)
	def __sub__(self, other):
		return self.elementwise_binop(other, lambda x,y: x-y)	
	def __mul__(self, other):
		assert isinstance(other, FractionArray)
		assert self.n == other.m, f"Incompatible dimensions for multiplication: ({self.m},{self.n}) and ({other.m},{other.n})"
		out = []
		for i in range(self.m):
			new_row = []
			for j in range(other.n):
				array_1_row = self.array[i]
				array_2_col = [other.array[k][j] for k in range(other.m)]
				dot_product = sum([array_1_row[i] * array_2_col[i] for i in range(self.n)])
				new_row.append(dot_product)
			out.append(new_row)
		return FractionArray(out)
	def __rmul__(self, other):
		assert isinstance(other, int) or isinstance(other, Fraction)
		return self.elementwise_func_to_new(lambda x: x * other)
	def __repr__(self):
		return self.array.__repr__()
	def __str__(self):
		out = "["
		for i in range(self.m):
			out += (' ' if i != 0 else '') + str(self.array[i]) + '\n'
		return out[:-1]+']'
	def determinant(self, method = "row_reduce"):
		if method == "cofactors":
			return self.determinant_by_cofactors()
		elif method == "row_reduce":
			return self.determinant_by_row_reduction()
		else:
			raise Exception(f"Unknown method: {method}")
	def determinant_by_cofactors(self):	
		self.assert_square()
		n = self.n
		if n == 1:
			return self.array[0][0]
		#otherwise expand by cofactors on the first colum/
		out = 0
		for i in range(n):
			sign = (-1) ** i
			col_entry = self.array[i][0]
			remaining_array = []
			for j in range(n):
				if j == i:
					continue
				remaining_array.append(self.array[j][1:])
			out += sign * col_entry * FractionArray(remaining_array).determinant_by_cofactors()
		return out
	def determinant_by_row_reduction(self):
		self.assert_square()
		copy = self.copy()
		copy.upper_triangular_form_in_place()
		out = 1
		for i in range(self.m):
			out *= self.array[i][i]		
		return out
	def top_left_portion(self, i = 1, j = 1):
		assert 1 <= i <= self.m
		assert 1 <= j <= self.n
		return FractionArray([[self.array[a][b] for b in range(j)] for a in range(i)])
	def positive_definite(self):
		self.assert_square()
		n = self.n
		for corner_size in range(1, n+1):
			corner = self.top_left_portion(corner_size, corner_size)
			if corner.determinant() <= 0:
				return False
		return True		
	def to_float_array(self):
		return [[self.array[i][j].to_float() for j in range(self.n)] for i in range(self.m)]
	def float_singular_values(self):
		float_array = self.to_float_array()
		return svdvals(float_array)	
	def t(self):
		return FractionArray([[self.array[i][j] for i in range(self.m)] for j in range(self.n)])
	def add_mult_of_row_to_another_in_place(self, mult, row_idx, other_row_idx):
		for j in range(self.n):
			self.array[other_row_idx][j] = self.array[other_row_idx][j] + mult * self.array[row_idx][j]	
	def upper_triangular_form_in_place(self):	
		for col_idx in range(self.m - 1):
			#make the pivot entry 1 (or if can't leave 0's and move on)
			if self.array[col_idx][col_idx] == 0:
				nonzero_row_idx = None
				for row_idx in range(col_idx + 1, self.m):
					if self.array[row_idx][col_idx] != 0:
						nonzero_row_idx = row_idx
						break
				if nonzero_row_idx is None:
					continue
				else:
					self.add_mult_of_row_to_another_in_place(1, nonzero_row_idx, col_idx)
			#use the pivot to kill the zeros below
			for row_idx in range(col_idx + 1, self.m):
				entry_to_kill = self.array[row_idx][col_idx]
				self.add_mult_of_row_to_another_in_place(-entry_to_kill / self.array[col_idx][col_idx], col_idx, row_idx)
		return 
	def bound_smallest_sv(self, num_digs = 4, verbose = False):
		if self.n > self.m:
			return self.t().bound_smallest_sv()
		def verbose_print(x):
			if verbose:
				print(x)
		verbose_print(f"using matrix {self}")
		float_svs = self.float_singular_values()
		verbose_print(f"its (float) singular values are {float_svs}")	
		frac_lb = Fraction.lower_bound_on_nonnegative_floats(float_svs, num_digs) - Fraction(1, 10 ** num_digs) 
		frac_lb = max(frac_lb, 0)
		frac_ub = frac_lb + Fraction(2, 10 ** num_digs)  
		verbose_print(f"a frac lower bound on these is {frac_lb}")
		verbose_print(f"to check this is really a lower bound on the svs, we will verify M^T M - I * ({frac_lb}) ^ 2 is positive semidefinite")
		shifted_matrix = (self.t() * self) - (frac_lb ** 2) * FractionArray.identity(self.n)
		verbose_print(f"M^T = {str(self.t())}")
		verbose_print(f"M^T M = {self.t() * self}")
		verbose_print(f"M^T M - I * ({frac_lb}) ^ 2 = {shifted_matrix}")
		checks = shifted_matrix.positive_definite() #positive definite suffices and will work since we're approximate anyway
		verbose_print(f"checking the shifted matrix is positive semidefinite: {checks}.")
		assert checks, "set argument verbose = True for details"
		other_shifted_matrix = (self.t() * self) - (frac_ub ** 2) * FractionArray.identity(self.n)
		checks = not other_shifted_matrix.positive_definite()
		return FractionInterval(frac_lb, frac_ub)

if __name__ == '__main__':
	test = [2]
	#test initialization/printing
	if 0 in test:
		print(Fraction("inf"))
		print(Fraction(1,2))
		print(Fraction(-7,1))
		print(5 / (Fraction(1,5) * 4))
		print(3 / Fraction(-1,3))
		print(Fraction(1,3)**100)
		print(Fraction(-1) <= Fraction(3,5))
		print(1/Fraction(0))
	#test intervals
	if 1 in test:
		test_int = FractionInterval(Fraction(3,4), Fraction(4,5))
		test_int2 = FractionInterval(-1,2)
		print(test_int)
		print(test_int.inverse())
		print(3 - test_int)
		print(test_int2)
		print(test_int2.inverse())
		print(test_int * test_int2)
		print(test_int / test_int2)
		print(Fraction(-1.123123123123))
	#svd lower bound
	if 2 in test:
		for i in range(50):
			m,n = i+1,i+1
			print(f"\nTrying size {i+1}\n")
			matrix = FractionArray([[random.random() - .5 for j in range(n)] for i in range(m)], allow_float_conversions = True)
			sv_bound = matrix.bound_smallest_sv(verbose = False)
			print(sv_bound)
	#row reduction
	if 3 in test:
		m, n = 10, 10
		matrix = FractionArray([[Fraction(random.randint(-5,5), random.randint(1,10)) for j in range(n)] for i in range(m)])
		matrix.upper_triangular_form_in_place()
	#square root bounding:
	if 4 in test:
		f = Fraction(2)
		sqrt_bound = f.sqrt()
		sqrt_sqrt_bound = sqrt_bound.sqrt()
		print(sqrt_bound)
		print(sqrt_sqrt_bound)
