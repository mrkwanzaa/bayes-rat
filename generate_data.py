import requests
import json
from bs4 import BeautifulSoup

def parse_data():
  # the target we want to open
  url='https://www.remote-associates-test.com/'

  #open with GET method
  resp=requests.get(url)
  
  #http_respone 200 means OK status
  if resp.status_code==200:
    print("Successfully opened the web page")
    
    # we need a parser,Python built-in HTML parser is enough .
    soup=BeautifulSoup(resp.text,'html.parser')


    questions=soup.find_all("a")[2:-1] # remove non question links
    solutions=soup.find_all("span",{"class":"hidden"})

    solutions = [i.text for i in solutions]
    questions = [i.text for i in questions]

    split_questions = [i.split(' / ') for i in questions]

    return (split_questions, solutions)
  else:
    print("Error")
    
(questions, solutions) = parse_data()

def generate_prompt(question):
  return f"This test consists of three common stimulus words that appear to be unrelated. The subject must think of a fourth word that can be added to each of the first three words to form a compound meaning. Consider these three words: {question[0]}, {question[1]}, {question[2]}. What is the fourth word?\n\n###\n\n"

pairs = []
# create list of dictionaries with formatted prompts and completions
for i in range(len(solutions)):
  value = {"prompt": generate_prompt(questions[i]), "completion": f"{solutions[i]} END"}
  pairs.append(value)

# write to jsonl file
with open("data.jsonl", 'w') as f:
    for item in pairs:
        f.write(json.dumps(item) + "\n")

# create a seperate test file with prompts not in data_prepared
with open('data_prepared.jsonl', 'r') as f:
  for line in f:
    for pair in pairs:
      if json.dumps(pair['prompt']) in line:
        pairs.remove(pair)

with open("test_data.jsonl", 'w') as f:
    for item in pairs:
        f.write(json.dumps(item['prompt']) + "\n")

filtered_questions = questions.copy()
# create a seperate test file with prompts not in data_prepared
with open('data_prepared.jsonl', 'r') as f:
  for line in f:
    for q in questions:
      if json.dumps(generate_prompt(q)) in line:
        filtered_questions.remove(q)


with open("bayes_test_data.jsonl", 'w') as f:
    for item in filtered_questions:
        f.write(json.dumps(item) + "\n")        
