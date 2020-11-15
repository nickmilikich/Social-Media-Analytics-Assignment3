import json
from Assignment3_1 import get_estimated_truth

# Accepts a string containing the name of a file from which to read tweets into a dicitonary
# Tweets should be in json format in the file
# Returns a list of dictionaries containing information about each tweet
def read_tweets(file_name):

	tweet_file = open(file_name, 'r')
	tweets = []
	for line in tweet_file:
		tweets.append(json.loads(line))
	tweet_file.close()

	return tweets

# Accepts a string containing the name of a file from which to read the clusters into a list of lists
# Clusters should be in the format specified in the assignment description:
# Cluster ID: IDs of tweets in that cluster, separated by commas
# Returns a list of lists of the IDs of tweets in each cluster
def read_clusters(file_name):

	cluster_file = open(file_name, 'r')
	clusters = []
	for line in cluster_file:
		cluster = []
		curr = ""
		for c in line[line.index(":")+1:]:
			if c == ",":
				cluster.append(int(curr))
				curr = ""
			else:
				curr = curr + c
		cluster.append(int(curr))
		clusters.append(cluster)
	cluster_file.close()

	return clusters

# Accepts tweets, a list of dictionaries of tweets
# Returns a list of all unique user IDs in the list of tweets
def get_unique_users(tweets):

	users = []

	for tweet in tweets:
		user = tweet["from_user_id"]
		if users.count(user) == 0:
			users.append(user)

	return users

# Checks whether a specified user makes a specified claim, i.e. whether a particular user ID
# tweeted a tweet in a particular cluster
# Accepts user, the ID of the user ("source") to check whether they made the claim;
# cluster, a list of tweet IDs, and tweets, the list of dictionaries of all tweets.
# Returns true if there is a tweet whose ID is contained in cluster and that comes from a user
# with ID matching the argument "user"; returns false otherwise.
def does_source_make_claim(user, cluster, tweets):

	for tweet in tweets:
		if (tweet["from_user_id"] == user) & (cluster.count(tweet["id"]) > 0):
			return True

	return False

# Accepts tweets, the list of dictionaries of tweets, and clusters, the list of lists containing
# the tweet IDs in each cluster.
# Converts the information into a matrix with one row for each source (unique user in the tweets)
# and one column for each claim (cluster).
# Element ij contains a 1 if source (user) i makes claim j (tweeted a tweet that is in cluster j)
# and a 0 otherwise.
# Returns this matrix in a list of lists.
def calculate_sensing_matrix(tweets, clusters):

	users = get_unique_users(tweets)

	sensing_matrix = []

	for user in users:
		curr_row = []
		for cluster in clusters:
			if does_source_make_claim(user, cluster, tweets):
				curr_row.append(1)
			else:
				curr_row.append(0)
		sensing_matrix.append(curr_row)

	return sensing_matrix

# Accepts string file_name and tuple est;
# the first element of est is h, the vector of predicted probabilities of each claim (cluster) being true;
# the second element of est is e, the vector of predicted reliabilities of each source (user) (not used
# in this method)
# Orders the claims in order of predicted probability of being true, greatest to least, and prints the
# results in the form "Claim ID: probability" in the file file_name
#
# Note: this method implements a minimum threshold for probabilities of 1e-16; i.e. it assumes that
# probabilities less than 1e-16 have converged to 0 and reassigns the value to 0
def write_results(file_name, est):

	est = est[0]

	for i in range(len(est)):
		if est[i] < 1e-16:
			est[i] = 0.0

	# Orders the claims in order of predicted probability of being true, from greatest to least
	# Stores the ordered probabilities in 'result' in tuples in the form (index, probability)

	result = []
	used_indices = []

	while len(result) < len(est):
		index = 0
		while used_indices.count(index) > 0:
			index = index + 1
		max_elem = est[index]
		for i in range(1, len(est)):
			if (est[i] > max_elem) & (used_indices.count(i) == 0):
				max_elem = est[i]
				index = i
		result.append((index, max_elem))
		used_indices.append(index)

	# Writes the results to file file_name

	result_file = open(file_name, 'w')

	result_file.write("Clusters Ranked by Credibility Score\n")
	result_file.write("Cluster ID: Credibility Score\n\n")
	for i in range(len(result)):
		result_file.write(str(result[i][0]+1) + ": " + str(result[i][1]) + "\n")

	result_file.close()

def main():

	# Read in tweets from input file
	tweets = read_tweets("Tweets.txt")

	# Read in the clusters of tweets from input file
	clusters = read_clusters("ClusteringResults.txt")

	# Computes the sensing matrix of sources and claims from the tweets (each twitter user
	# is a source) and clusters (each cluster is a claim)
	sensing_matrix = calculate_sensing_matrix(tweets, clusters)

	# Calculate estimated truth from the sensing matrix
	est = get_estimated_truth(sensing_matrix, 0.5, True, d_guess = 0.5)

	# Writes the resulting estimates to the output file
	write_results("Assignment3_2_output.txt", est)

if __name__ == "__main__":
	main()








































