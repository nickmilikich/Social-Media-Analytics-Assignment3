from Assignment3_1 import get_matrix, get_estimated_truth

# Accepts a file truth_file that contains, by line, the index of each claim,
# followed by a comma, and a binary variable that is 1 if that claim is true
# Returns vector truth containing the truth variable for each claim
def get_ground_truth(truth_file):
	truth = []

	for line in truth_file:
		i = line.index(",")
		truth.append(int(line[i+1:]))

	return truth

def main():

	# Read in ground truth from file
	truth_file = open("GroundTruth.txt", 'r')
	ground_truth = get_ground_truth(truth_file)
	truth_file.close()

	for k in [1, 2, 3]:

		filename = "TestSensingMatrix" + str(k) + ".txt"

		# Read in sensing matrix from file
		matrix_file = open(filename, 'r')
		sensing_matrix = get_matrix(matrix_file)
		matrix_file.close()

		# Calculate estimated truth from each sensing matrix
		est = get_estimated_truth(sensing_matrix, 0.5, False)

		if est[0] == ground_truth:
			print("Test " + str(k) + " successful!")
		else:
			print("Test " + str(k) + " not successful")

if __name__ == "__main__":
	main()







































