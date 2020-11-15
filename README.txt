Assignment 3: Truth Discovery and Credibility Analysis
Nick Milikich
CSE 60437 Social Sensing & Cyber-Physical Systems
March 6, 2019

This project implements a maximum likelihood algorithm for truth discovery in a dataset. The algorithm relies on being able to convert social data into a matrix of sources and claims. The social sensing matrix contains a row for each source and a column for each claim. Each entry contains a 1 if that source makes that claim, and a 0 if not. This is an implementation of algorithm 1 described in Wang et al. 2012. Algorithm returns two vectors of information: the predited truth of each claim (can be left as predicted probabilities, or converted to a binary result: 1 if the predicted probability of truth is greater than or equal to 0.5, 0 if not), and the predicted reliability of each source (the predicted probability that any claim is true given that that source made that claim).

The project is split into two parts. The first (Assignment 3_1) implements algorithm 1 from Wang et al. 2012. It accepts a sensing matrix (computed from the claim information in SensingMatrix.txt), computes the predicted truth of each claim and reliability of each source, and writes this information to Assignment3_1_output.txt. The accuracy of this implementation is examined in Assignment3_1_check, in which three test datasets of claims are converted to sensing matrices and shown to converge to the ground truth.

The second part implements the same algorithm with a real-world case study. A dataset of 251 tweets related to the Boston Marathon bombing incident (stored and read in from Tweets.txt) that has been clustered into 25 clusters (the clusters are stored and read in from ClusteringResults.txt) is converted into a sensing matrix: each unique user is treated as a source and each cluster is treated as a claim. The truth of each claim (cluster) is calculated from the algorithm implemented in part 1 and the results are written to Assignment3_2_output.txt.

The truth discovery algorithm on the toy dataset can be run by executing Assignment3_1.py; the results are written to Assignment3_1_output.txt. The check of the truth discovery algorithm can be run by executing Assignment3_1_check.py; the results are printed on running. The truth discovery algorithm on the real-world case study Boston Marathon bombing twitter dataset can be run by executing Assignment3_2.py; the results are written to Assignment3_2_output.txt. No arguments need to be passed to the programs. This code was tested using Python version 2.7.16.

Running this source code requires that the Python packages json and random be installed.

To run the source code, the following should be included in the same directory (all included in this submission):
   
   - A file named ClusteringResults.txt that contains the clusters for the twitter dataset; each line is in the form [Cluster ID]: [IDs of tweets in that cluster separated by commas]
   - A file named GroundTruth.txt that contains the truth of each claim in the toy dataset; each line is in the form [claim ID],[0 or 1]. The results of the three checks of the algorithm implementation are compared to these results.
   - A file named SensingMatrix.txt that contains the claims made in the toy dataset to calculate the predicted truth in part 1. Each line is in the form [source ID],[claim ID], and this information can be converted to the sensing matrix by entering a 1 if that source,claim combination appears in the file and a 0 otherwise.
   - Files named TestSensingMatrix1.txt, TestSensingMatrix2.txt, and TestSensingMatrix3.txt that contain the claims made in three test datasets in the same format as SensingMatrix.txt. Calculating the truth of each of the test sensing matrices should converge to the information in GroundTruth.txt.
   - A file named Tweets.txt that contains the information for the 251 tweets to be clustered, stored in json format. The tweets are stored one per line.

Sources:
D. Wang, L. Kaplan, H. Le, and T. Abdelzaher. On Truth Discovery in Social Sensing: A Maximum Likelihood Estimation Approach. In Proceedings of the 11th international conference on Information Processing in Sensor Networks, ISPN '12, pages 233-244, Beijing, China, Apr 2012.
















