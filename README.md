![](https://i.imgur.com/05l9jh8.png)

## Team
Team Name: P.A.T.I.E.N.T.S.
Team Members:
* Varun Tandon (varunt@stanford.edu)
* Jeremy Lee (jeremylee821@gmail.com)
* Vincent Li (2007vincentli@gmail.com) 

Devpost: https://devpost.com/software/patients-wfg4nc

## Challenge
Office Ally Challenge 1: Patient Matching.

## Inspiration

Currently, medical records of patients are widely dispersed across various hospital and insurance databases, segregating the information of patients across a variety of sources. This is specially problematic when considering health data, since health data can have a large impact on the quality of care delivery. Unfortunately, matching patient records is not a simple task. There does not exist a single unifying identifier for patient data, and often the data collected by various healthcare providers differs, and is stored in varying underlying formats. Thus, P.A.T.I.E.N.T.S, we aim to solve this problem by using scripting, data science, natural language processing, and a variety of heuristics.

## Installation and Running Instructions

To run this we recommend using a Python 3.7.5 virtual enviornment.
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
To run the script, please run `submission.py`. You will need to change the `FILENAME` variable in submission.py to the path to your input file, and you will also need to ensure that your data matches the exact same format as the data for this problem. 
```
python submission.py
```
The code will output the results to `results.csv`, where the grouping column indicates matched patients.

## Files

| file                          | description                                                  |
| ----------------------------- | ------------------------------------------------------------ |
| data_cleaning.py              | Performs a number of data cleaning steps, including cleaning the state abbreviations, cleaning zipcode data, converting date strings, cleaning sex data, filling in empty data, normalizing patient first and last names, cleaning address data, and encoding name data as ASCII only. |
| confidence_aggregation.py     | Uses a number of heuristics, based on strings, Soundex tokens, hash tokens, and Levenshtein distance to calculate confidence levels in various ways, and compute a confidence matrix, representing the confidence that each pairing is a match of patient records. Also performs graph based calculations of connected components. |
| clustering.py                 | Uses a Heirarchical Clustering Algorithm (Agglomerative Clustering) to cluster patients according to Gower distance. |
| evaluation.py                 | Provides a suite for calculating statistics of model performance with raw data or unbiased data, calculating confusion matrix, accuracy, precision, recall, and F1 score. |
| hashing.py                    | Performs hashing operations similar to the provided patientMatchPOC.sql |
| levenshtein_distance_stats.py | Calculates the accuracy and confidence of various Levenshtein distance heuristics on the given data. |
| performance_test.py           | Loads an external data set to evaluate the performance of the algorithm at scale. |
| submission.py                 | CLI for generating labels for a new dataset                  |
| voting.py                     | Combines heuristics via voting to generate a final vote for final labels |

## How I built it

1. Our first step was to implement the patientMatchPOC.sql. We read through the file, taking note of the differences and similarities between the task we were given and the task the patientMatchPOC.sql attempts to solve. Once we understood the code, we implemented it in Python using the same confidences and hashing methods used in the POC.
2. Once we had implemented the POC, we wrote the code necessary for cleaning the data. Specifically we took the following steps:
   1. Read the CSV into a Pandas DataFrame
   2. Encode the text columns into ASCII characters
   3. Clean state data so that it is consistently 2 letter abbreviations
   4. Clean zipcode data so that it is 5 digits, and create separate columns for National Area, Sectional Center, and Delivery Area
   5. Clean Date of Birth data to be formatted consistently as 8 character strings (similar to the POC)
   6. Clean Sex data to be M, F, or U
   7. Normalize the patient first and last names by removing nonalphanumeric characters and converting to lowercase
   8. Cleaning address data to be consistent for later use in fuzzy text matching
3. We then implemented an algorithm for converting pairwise determinations of patient row records into clusters of patients. After a few minutes of brainstorming, we realized that this could be represented as a graph problem. Specifically, we took the following approach:
   1. Generate confidences for each pairwise combination of patients
   2. Determine a threshold value for confidence, and set all values above the threshold to be 1 and all values below the threshold to be 0
   3. Store this data in a matrix. Since we have only populated the top left corner of the matrix (to avoid redundant pairwise comparisons), we also mirror the top left corner into the bottom right corner to generate an adjacency matrix.
   4. Given this graph based representation of our patient records, where connections are high confidence matches between records, we now group connected components to be a collective group.
   5. Finally, we built out a testing harness that provides key information such as the confusion matrix of our model, accuracy, precision, recall, and F1 score. We also performed majority undersampling in order to de-bias our dataset and have realistic accuracy metrics.
   Graph Representation of Patient Record Clustering:
![](https://i.imgur.com/kjqFkh0.png)
4. After writing this code to convert pairwise matches to cluster groups, we developed our first more sophisticated algorithm for clustering, heirarchical clustering (specifically Agglomerative Clustering). We chose Agglomerative Clustering since it provides an unsupervised method for clustering data without a parameter to indicate the number of clusters. Since we do not know how many clusters of patients there will be in the end, we could not use algorithms such as k-Means (which require number of clusters as a parameter). We also realized that we would need to implement some metric for distance despite our categorical data. Our research revealed that we could use the Gower distance metric to convert categorical data to numerical values. A visualization of a generated clustering can be found below:
![](https://i.imgur.com/dwHvZix.png)
5. To build our main predictive model, we started with our Python implementation of the patientMatchPOC.sql. The implementation utlizied removed non-alphanumeric first and last names as well as the soundex of the original first and last names to gengerate a "confidence score" that two patients are the same. We built upon this model using different features and developed a set of rules for determining if each feature is similar.
    1. Tested levenshtein distance between non-alphanumeric first and last names with characters to generate confidence scpres similar to the patientMatchPOC.sql
    2. Preformed additional cleanings on features that weren't mentioned above in step 1
    3. Created rules for determining significance of differences and discrepencies between date of birth, cities, zipcodes based off levenshtein distance (features with levenshtein distance less than 1 are similar, or else different, or undefined for nan)
    4. Created similar rules to step 3 for deteremining significance of differences and discrepencies between account number, gender, and state through string comparisons
    5. Created a rule for determining significance of differences and discrepencies between addresses (taking the shorter of the two addresses compare levenshtein distance for each word in the address (accounts for extra specifications of a street)) then (taking the shortest piece of the shorter string and comparing levenshtein distance for the corresponding piece of the other string (this accounts for abbreviations like "ave", "st", ect))
    6. We based these rules heavily off what we would expect "real world" data to look like
    7. Aggregated these rules for each feature into a single function which determines if a patient should be grouped with another (a patient is not similar if more than one feature is different)
    8. Patients have to match for at least 5 features for them to be similar
7. After implementing the patientMatchPOC (which involved Soundex and Hash tokens), Agglomerative Clustering, and a Levenshtein-based ruleset, we finally created an ensemble voting algorithm to generate our final results. First we decided to give our main predictive model a majority of the votes, and only override our main predictive model if ALL of the other predictive models are in consensus in the opposing vote.
8. While the Heuristics Involving Approximate String Matching and Feature Distances (step 5) model had the highest overall accuracy, it has a weakness of associating false positives. However, we gave it the highest weight, because we expect that in the real world false positives are less likely than in the given set. In addition more false positives are easier to compare in depth than more false negatives, because a group of patients similar to a single patient is smaller than the group of patients different to the single patient. 
9. After looking at the metrics of our first ensemble voting method, we decided to come up with a voting system that did not favor our main predictive model as much. We wanted to combine strengths of all other models to make up for the lower precision seen in our main model. The final method we settled on gave out main voting method only twice as much voting power as any other model. This model gave us accuracry metrics that we felt were optimizing the powers of all of our models. Any other changes to the weighting at this point we felt would only be massaging the results and not be adding any new interesting anlysis/data. 
10. Finally, to stress test our code, we retrieved a larger dataset of patient records from the ONC's Patient Matching Challenge. Our program operates at O(N^2). We loaded a large dataset of 200,000 entries into our program, and from this we were able to encounter a large number of parsing errors that we could promptly fix. Unfortunately, this data did not have any labels, so it proved to be useless for being more than a stress test; however, from our analysis, we found that our code could feasibly run over millions of records within a reasonable timeframe (~8 hours).

Metrics:

| Model Type                                                   | Accuracy | Precision | Recall | F1     | TP (true positives) | FP (false positives) | TN (true negatives) | FN (false negatives) |
| ------------------------------------------------------------ | -------- | --------- | ------ | ------ | ------------------- | -------------------- | ------------------- | -------------------- |
| Proof of Concept Implementation                              | 0.9895   | 0.5775    | 0.9895 | 0.7205 | 272                 | 199                  | 19617               | 12                   |
| Matching via Full Hashes (POC)                               | 0.9875   | 0.8511    | 0.9875 | 0.24   | 40                  | 7                    | 19809               | 244                  |
| Matching via Partial Hashes (POC)                            | 0.9907   | 0.792     | 0.991  | 0.5885 | 133                 | 35                   | 19781               | 151                  |
| Agglomerative Clustering                                     | 0.9910   | 0.9       | 0.9910 | 0.5652 | 117                 | 13                   | 19803               | 167                  |
| Advanced Heuristics Involving Approximate String Matching and Feature Distances | 0.99438  | 0.7522    | 0.9943 | 0.8187 | 255                 | 84                   | 19732               | 29                   |
| Ensemble Voting                                              | 0.9936   | 0.7746    | 0.9936 | 0.7746 | 220                 | 64                   | 19752               | 64                   |
## Challenges I ran into
Most of the challenges we faced were due to limitations of our data. Since our data was so small, it was not viable for us to create a holdout set for us to perform validation on. Thus, we had to ensure that the algorithms we wrote were generalizeable, but we were unable to verify them. Having a sample real data set that contained real duplicate entries to see how common they were, in what ways were the duplicate entries wrong, and to test how robust our progarm was would have helped massively.

One of the implementation strategies that we tried but ultimately scrapped was using a probablistic record matching algorithm. In this strategy, rather than manually creating confidence levels, we used our data to determine the confidence levels of our heuristics based on probabilities. However, we decided not to use this strategy since we worried that we may overfit the data. This decision was one of many we had to make regarding design choices and on what methodologies to use to provide the best results. All choices had tradeoffs, and better planning and forward-thinking would have allowed us to spend more time implementing functions that we actually want

Another challenge we faced was the time constraints. We originally did not consider potential performance hiccups when scaling up to larger datasets, and as such by the time we had completed our initial implementation, we did not have enough time to multithread our code.

## Accomplishments that I'm proud of
We're incredibly proud of being able to tackle such a complex problem and apply our textbook knowledge to a real-world problem. Despite the time constraints and some struggles with virtual communication, we were able to create a project that moves a step closer to solving this extremely relevant problem. There are probably thousands of filing cabinets filled with tabulated entries like the ones we worked with, and if they are to be digitized they will need to analyzed for duplicates as we have done with our project.

We came up with an elegant model which expanded upon the patientMatchPOC and yieled both a high accuracy and high F1 score when run on the given data. We also developed a thought-out infrastructure which organizes the models into seperate files and makes testing them simpler, and this design is easy to expand upon.

## What's next for P.A.T.I.E.N.T.S.
Given more time, we plan to expand this project by looking at more patient records to construct a larger dataset. With a larger dataset of a few hundred thousand entries, we could isolate ten thousand as a holdout set and then perform probablistic record matching without any worries of overfitting. 

Furthermore, we would change the implementation of our methods to involve multithreading to allow for scalability to multi-core platforms, and allow for greater speed benefits.

Finally, we would want to unpack more features that were provided, such as information about previous residences. While we had some plans for using this data, in conjunction with our various segmentations of the zipcode data, we were not able to implement these in time.
