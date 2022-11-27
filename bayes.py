import gensim
import gensim.downloader
import csv

# Change to false for divergent task
closest = True
# Some words in the dataset shouldn't be considered
excluded_words = {"ll"}

model1 = gensim.downloader.load("word2vec-google-news-300")
print("finished model setup")

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
            and model1.has_index_for(word["Word"])
        ):
            word_frequencies[word["Word"]] = float(word["SUBTLWF"])
            total += float(word["SUBTLWF"])
for (word, value) in word_frequencies.items():
    word_frequencies[word] = value / total

print("finished importing frequencies")

while True:
    given_words = []
    given_words.append(input("Word 1: "))
    given_words.append(input("Word 2: "))
    given_words.append(input("Word 3: "))
    correct = input("Correct: ")

    def find_similarity(word):
        if closest:
            return sum((model1.similarity(word, given) for given in given_words))
        else:
            return sum((1 - model1.similarity(word, given) for given in given_words))

    similarity_total = sum((find_similarity(word) for word in word_frequencies.keys()))

    freq_normalizer = sum(
        (
            prior * (find_similarity(word) / similarity_total)
            for (word, prior) in word_frequencies.items()
        )
    )

    probs = {}
    for (hypothesis, freq) in word_frequencies.items():
        # ensure that we dont take a word in given
        if hypothesis not in given_words:
            value = (
                freq * (find_similarity(hypothesis) / similarity_total)
            ) / freq_normalizer
            probs[hypothesis] = value
    print(find_similarity(correct) / similarity_total)
    print(word_frequencies[correct])
    print("correct: " + str(probs[correct]))
    result = max(probs, key=probs.get)
    print(find_similarity(result) / similarity_total)
    print(word_frequencies[result])
    print(result + ": " + str(probs[result]))
