import random

def read_matrix(file_name):
	matrix_file = open(file_name, 'r')
	mat = get_matrix(matrix_file)
	matrix_file.close()
	return mat

# Accepts a file of Si,Cj pairs, one per line
# Returns a max_i x max_j matrix containing 1 in element i,j if Si,Cj appears in the file and 0 otherwise
def get_matrix(matrix_file):
	pairs = []
	for line in matrix_file:
		i = line.index(",")
		a = int(line[:i])
		b = int(line[i+1:])
		pairs.append([a,b])
	max_i = pairs[-1][0]
	max_j = pairs[0][1]
	for i in range(len(pairs)):
		j = pairs[i][1]
		if j > max_j:
			max_j = j
	mat = []
	for i in range(max_i):
		mat.append([0] * max_j)
	for pair in pairs:
		mat[pair[0]-1][pair[1]-1] = 1
	return mat

# Accepts the sensing matrix SiCj, a threshold, boolean leave_as_probability, and optional d_guess
# Computes the estimated truth vectors h and e from the equations specified in Wang et al. 2012
# If d_guess is supplied, it is used as the initial value for d in the algorithm. Otherwise a random
# number (0,1) is used, in accordance with the algorithm presented in Wang et al. 2012.
# Returns a tuple of estimated vectors h and e, (h, e)
# If leave_as_probability is false, h is a vector of binary elements: 1 if the predicted probability
# of that claim being true is greater than or equal to threshold, and 0 if not
# If leave_as_probability is true, h is a vector of floats representing the predicted probability of
# each claim being true
# e is a vector of the predicted reliability for each source, or the probability that a claim is
# true given that that source reported it
def get_estimated_truth(sensing_matrix, threshold, leave_as_probability, d_guess = random.random()):
	max_i = len(sensing_matrix)
	max_j = len(sensing_matrix[0])
	s = []
	for i in range(max_i):
		s.append(float(sum(sensing_matrix[i])) / float(max_j))

	# Initial guesses
	# As specified in the algorithm,
	# ai = si
	# bi = 0.5 * si
	# d = random(0,1)
	a = []
	for i in range(max_i):
		a.append(s[i])
	b = []
	for i in range(max_i):
		b.append(0.5 * s[i])
	d = d_guess
	theta_new = (a, b, s, d)

	# First iteration
	z = compute_z(sensing_matrix, a, b, d)
	
	theta_old = theta_new

	a = compute_a(sensing_matrix, z)
	b = compute_b(sensing_matrix, z)
	d = compute_d(sensing_matrix, z)

	theta_new = (a, b, s, d)

	# Further iterations
	while not is_converged(theta_old, theta_new, 1e-8):

		z = compute_z(sensing_matrix, a, b, d)
	
		theta_old = theta_new

		a = compute_a(sensing_matrix, z)
		b = compute_b(sensing_matrix, z)
		d = compute_d(sensing_matrix, z)

		theta_new = (a, b, s, d)

	if leave_as_probability:
		h = z
	else:
		h = compute_h(z, threshold)

	e = compute_e(a, b, s, d)

	return (h, e)

# Accepts two tuples, theta_old and theta_new, and a float tolerance
# Each theta is a tuple containing (a, b, s, d)
# Returns true if every element in a, b, and s, and the element d in theta_old and
# theta_new differ in absolute value by no more than tolerance
# Returns false otherwise
def is_converged(theta_old, theta_new, tolerance):
	for i in range(len(theta_old[0])):
		if abs(theta_old[0][i] - theta_new[0][i]) > tolerance:
			return False
	for i in range(len(theta_old[1])):
		if abs(theta_old[1][i] - theta_new[1][i]) > tolerance:
			return False
	for i in range(len(theta_old[2])):
		if abs(theta_old[2][i] - theta_new[2][i]) > tolerance:
			return False
	if abs(theta_old[3] - theta_new[3]) > tolerance:
		return False
	return True

# Accepts a matrix sensing_matrix and vector z
# Computes and returns the vector ai from equation 17 in Wang et al. 2012
def compute_a(sensing_matrix, z):
	max_i = len(sensing_matrix)
	max_j = len(sensing_matrix[0])

	a_new = []

	for i in range(max_i):
		num = 0.0
		denom = 0.0
		for j in range(max_j):
			if sensing_matrix[i][j] == 1:
				num = num + z[j]
			denom = denom + z[j]
		a_new.append(num / denom)

	return a_new

# Accepts a matrix sensing_matrix and vector z
# Computes and returns the vector bi from equation 17 in Wang et al. 2012
def compute_b(sensing_matrix, z):
	max_i = len(sensing_matrix)
	max_j = len(sensing_matrix[0])

	b_new = []

	for i in range(max_i):
		ki = sum(sensing_matrix[i])
		num_sum = 0.0
		denom_sum = 0.0
		for j in range(max_j):
			if sensing_matrix[i][j] == 1:
				num_sum = num_sum + z[j]
			denom_sum = denom_sum + z[j]
		num = ki - num_sum
		denom = max_j - denom_sum
		b_new.append(num / denom)

	return b_new

# Accepts a matrix sensing_matrix and vector z
# Computes and returns the vector di from equation 17 in Wang et al. 2012
def compute_d(sensing_matrix, z):
	max_i = len(sensing_matrix)
	max_j = len(sensing_matrix[0])

	d_new = []

	num = 0.0
	for j in range(max_j):
		num = num + z[j]

	d_new = num / float(max_j)

	return d_new

# Accepts vectors a, b, and s and float d
# Computes and returns the vector ei from equation 5 in Wang et al. 2012
# (ei corresponds to ti in equation 5)
# (Solving either equation in (5) for ti will allow you to compute ti, they are
# both equivalent, but the first equation is more simple)
def compute_e(a, b, s, d):
	max_i = len(a)

	e = []

	for i in range(max_i):
		e.append(a[i] * d / s[i])

	return e

# Accepts vector z and float threshold
# Computes and returns vector hj according to lines 15-21 in Wang et al. 2012
def compute_h(z, threshold):
	h = []
	
	for j in range(len(z)):
		if z[j] >= threshold:
			h.append(1)
		else:
			h.append(0)
	
	return h

# Accepts matrix sensing_matrix, vectors a and b, and float d
# Computes and returns vector zj from equation 11 in Wang et al. 2012
def compute_z(sensing_matrix, a, b, d):
	max_i = len(sensing_matrix)
	max_j = len(sensing_matrix[0])

	z = []

	for j in range(max_j):
		num = A(j, sensing_matrix, a) * d
		denom = A(j, sensing_matrix, a) * d + B(j, sensing_matrix, b) * (1.0 - d)
		z.append(num / denom)

	return z

# Accepts int claim index j, matrix sensing_matrix, and vector a
# Computes and returns Aj from equation 12 in Wang et al. 2012
def A(j, sensing_matrix, a):
	max_i = len(sensing_matrix)
	max_j = len(sensing_matrix[0])

	prod = 1.0
	for i in range(max_i):
		elem = a[i] ** sensing_matrix[i][j] * (1.0 - a[i]) ** (1.0 - sensing_matrix[i][j])
		prod = prod * elem
	return prod

# Accepts int claim index j, matrix sensing_matrix, and vector b
# Computes and returns Bj from equation 12 in Wang et al. 2012
def B(j, sensing_matrix, b):
	max_i = len(sensing_matrix)
	max_j = len(sensing_matrix[0])

	prod = 1.0
	for i in range(max_i):
		elem = b[i] ** sensing_matrix[i][j] * (1.0 - b[i]) ** (1.0 - sensing_matrix[i][j])
		prod = prod * elem
	return prod

# Accepts string file_name and tuple est;
# the first element of est is h, the vector of predicted truth of each claim (1 if the predicted probability
# of being true is greater than or equal to 0.5, 0 otherwise);
# the second element of est is e, the vector of predicted reliabilities of each source (user) (not used
# in this method)
# Prints the predicted truth of each claim in the form "Claim ID: predicted truth (0 or 1)" in the file file_name
def write_results(file_name, est):
	result_file = open(file_name, 'w')
	for i in range(len(est[0])):
		result_file.write(str(i+1) + "," + str(est[0][i]) + "\n")
	result_file.close()

def main():

	# Read in sensing matrix from file
	sensing_matrix = read_matrix("SensingMatrix.txt")

	# Calculate estimated truth from the sensing matrix
	est = get_estimated_truth(sensing_matrix, 0.5, False)

	# Writes the resulting estimates to the output file
	write_results("Assignment3_1_output.txt", est)

if __name__ == "__main__":
	main()






































