import os
import openai
import json

model = "davinci:ft-personal-2022-12-06-19-07-55"  # alternative: "text-davinci-003"

openai.api_key = os.getenv("OPENAI_API_KEY")

prompts = []

with open('test_data.jsonl', 'r') as f:
  for line in f:
    prompts.append(json.loads(line))

results = []
for prompt in prompts:
  print(prompt)
  result = openai.Completion.create(
    model=model,
    prompt= prompt,
    max_tokens=256,
    temperature=0.95,
    presence_penalty=1,
    stop="end"
  )
  # add stop="end" for fine-tuned
  results.append(result.choices[0].text)

print(results)

with open('test_results.jsonl', 'w') as f:
  for item in results:
    f.write(json.dumps(item) + '\n')