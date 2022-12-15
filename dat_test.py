import json
import numpy as np
import gensim
import gensim.downloader

words = []

with open('human_dat_questions.jsonl', 'r') as f:
  for line in f:
    words.append(json.loads(line))

results = []

with open('dat_results_standard.jsonl', 'r') as f:
  for line in f:
    results.append(json.loads(line))

model = gensim.downloader.load("word2vec-google-news-300")

distances = []
for i in range(len(words)):
  prompt_similarity = []
  result = results[i]
  prompt = words[i]
  for word in result:
    prompt_similarity.append(sum((model.similarity(word.strip(), given) for given in prompt)))
  distances.append(prompt_similarity)
means = []
for item in distances:
  means.append(np.mean(item))
with open('average_w2v_similarities.jsonl', 'w') as f:
  for item in means:
    f.write(json.dumps(item) + '\n')
  f.write('overall average: ' + str(np.mean(means)) + '\n')
  