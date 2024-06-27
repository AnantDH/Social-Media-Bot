from openai import OpenAI

class GptInterface:

    def __init__(self, key):
        self.client = OpenAI(api_key=key)


    def get_is_male(self, story):
        query = "Give me a one word response, either 'True,' or 'False,' if you think the following story is written by a male or female. True means you think it's a male, while False means you think its a female. Here's the story: "
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user", 
                    "content": query + story
                    }
                    ]
        )
        return completion.choices[0].message.content