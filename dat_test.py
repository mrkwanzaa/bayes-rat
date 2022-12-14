import json
import gensim
import gensim.downloader

model = gensim.downloader.load("word2vec-google-news-300")

# not sure how we want to import these
words = []

with open('bayes_test_data.jsonl', 'r') as f:
  for line in f:
    words.append(json.loads(line))

results = []

with open('dat_results_standard.jsonl', 'r') as f:
  for line in f:
    results.append(json.loads(line))

distances = []
for i in range(len(results)):
  prompt_similarity = []
  result = results[i]
  prompt = words[i]
  for word in result:
    prompt_similarity.append(sum((model.similarity(word.strip(), given) for given in prompt)))
  distances.append(prompt_similarity)

with open('w2v_distances.jsonl', 'w') as f:
  for item in distances:
    f.write(json.dumps(item) + '\n')