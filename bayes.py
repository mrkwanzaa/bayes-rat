import gensim
import gensim.downloader
import dat
import csv
import numpy as np
import json

# Change to false for divergent task
closest = False
# Some words in the dataset shouldn't be considered
excluded_words = {"ll"}
# Change to false to use dat model
word2vecModel = True

# Issues: inv negative log still doesn't work great
# Dat model is missing some prompt words (at least swiss)
# Q: do we want top 5 for gpt (can re run)
# TODO write methods section about gpt3 and bayes?

# Look at different distance metrics
# Get methods done for tuesday

model1 = (
    gensim.downloader.load("word2vec-google-news-300")
    if word2vecModel
    else dat.Model("glove.840B.300d.txt", "words.txt")
)
print("finished model setup")

def checkWord(word):
    """
    Checks if the given word is valid in our model
    """
    if word2vecModel:
        return word if model1.has_index_for(word) else None
    else:
        return model1.validate(word)

word_frequencies = {}
with open("SUBTLEXfreqPoS.csv", mode="r") as file:
    # reading the CSV file
    csvFile = csv.DictReader(file)
    # Total frequency to normalize to a probability
    total = 0
    for word in csvFile:
        if (
            "Noun" in word["All_PoS_SUBTLEX"]
            and word["Word"] not in excluded_words
        ):
            word_name = checkWord(word["Word"])
            if word_name is not None:
                word_frequencies[word_name] = float(word["SUBTLWF"])
                total += float(word["SUBTLWF"])

for (word, value) in word_frequencies.items():
    word_frequencies[word] =  1 / (-1 * np.log(value / total))

print("finished importing frequencies")

prompts = []

with open('bayes_test_data.jsonl', 'r') as f:
  for line in f:
    prompts.append(json.loads(line))

solutions = []

for given_words in prompts:

    def find_similarity(word):
        if word2vecModel:
            if closest:
                return sum((model1.similarity(word, given) for given in given_words))
            else:
                return sum(((1 - model1.similarity(word, given)) for given in given_words))
        else:
            if closest:
                return sum(((1 - model1.distance(word, given)) for given in given_words))
            else:
                return sum((model1.distance(word, given) for given in given_words))
                

    similarity_total = sum((find_similarity(word) for word in word_frequencies.keys()))

    freq_normalizer = sum(
        (
            (1/len(word_frequencies.keys()) * find_similarity(word) / similarity_total)
            for (word, prior) in word_frequencies.items()
        )
    )

    probs = {}
    for (hypothesis, freq) in word_frequencies.items():
        # ensure that we dont take a word in given
        if hypothesis not in given_words:
            value = (
                1/len(word_frequencies.keys()) * (find_similarity(hypothesis) / similarity_total)
            ) / freq_normalizer
            probs[hypothesis] = value
    sorted_results = sorted(probs.items(), key=lambda x: x[1], reverse=True)
    print(given_words)
    print(sorted_results[:5])

    solutions.append(sorted_results[:5])

with open('bayes_test_results_uniform_dat.jsonl', 'w') as f:
  for item in solutions:
    f.write(json.dumps(item) + '\n')