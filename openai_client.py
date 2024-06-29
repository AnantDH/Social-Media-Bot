from openai import OpenAI

class GptInterface:

    def __init__(self, key):
        self.client = OpenAI(api_key=key)


    # method sends the query to gpt 3.5 turbo and parses the response
    def get_is_male(self, story):
        query = "Give me a one word response, either 'True,' or 'False,' based on whether you think the writer of this story is a male ore a female. True means you think it's a male, while False means you think its a female. Here's the story: "
        print(query + story)
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