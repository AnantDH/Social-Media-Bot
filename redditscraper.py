import praw

class RedditScraper:

    # save important info and initialize reddit obj for post retrieval
    def __init__(self, client_id, client_secret, user_agent):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

    
    def get_controversial(self, sub_name, num_posts):
        library = dict()
        subreddit = self.reddit.subreddit(sub_name)
        for submission in subreddit.controversial(limit=num_posts):
            title = submission.title
            body = submission.selftext
            score = submission.score
            library[title] = (body, score)
        return library
    

    def get_hot(self, sub_name, num_posts):
        library = dict()
        subreddit = self.reddit.subreddit(sub_name)
        for submission in subreddit.hot(limit=num_posts):
            title = submission.title
            body = submission.selftext
            score = submission.score
            library[title] = (body, score)
        return library
    

    def get_new(self, sub_name, num_posts):
        library = dict()
        subreddit = self.reddit.subreddit(sub_name)
        for submission in subreddit.new(limit=num_posts):
            title = submission.title
            body = submission.selftext
            score = submission.score
            library[title] = (body, score)
        return library
    

    def get_top(self, sub_name, num_posts):
        library = dict()
        subreddit = self.reddit.subreddit(sub_name)
        for submission in subreddit.top(limit=num_posts):
            title = submission.title
            body = submission.selftext
            score = submission.score
            library[title] = (body, score)
        return library
    



