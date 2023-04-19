import openai

import config

openai.api_key = config.OPENAI_API_KEY

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "Расскажи о мире в стиле пирата"}
  ]
)

print(completion.choices[0].message.content)
