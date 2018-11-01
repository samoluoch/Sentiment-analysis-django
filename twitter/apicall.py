from secrets import Oauth_Secrets
import tweepy
from textblob import TextBlob


# class Oauth_Secrets:
#     def __init__(self):
#         self.consumer_key = "WRxcgZHq8HOA9AiACeoz7pc61"
#         self.consumer_secret = "IJnOARqL3baljF5VfMPB4Gy1GmxVLlSv6L4BgJoh3bVDslSQYL"
#         self.access_token = "32554005-yIgL0lbl0aWXyJ0E8q61zDF8BpOtVzWwRoZyCDm1n"
#         self.access_token_secret = "PzknR8jcAmNgG35G0D99BH9qEJfF7n477AxK1kgFDnVWl"


def getdata(input_hashtag):

    # input_hashtag = 'obama'
    secrets = Oauth_Secrets()
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)

    api = tweepy.API(auth)

    N = 500  # number of tweets
    Tweets = tweepy.Cursor(api.search, q=input_hashtag).items(N)

    negative = 0.0
    positive = 0.0
    negative_count = 0
    neutral_count = 0
    postive_count = 0

    # print(Tweets)
    for tweet in Tweets:
        # print(tweet.text)
        blob = TextBlob(tweet.text)
        if blob.sentiment.polarity < 0:
            negative += blob.sentiment.polarity
            negative_count += 1
        elif blob.sentiment.polarity == 0:
            neutral_count += 1
        else:
            positive += blob.sentiment.polarity
            postive_count += 1
    # post = ("Positive ", float(postive_count/N)*100, "%")

    data = {
        'Positive': postive_count,
        'Neutral': neutral_count,
        'Negative': negative_count
    }
    # print(post)
    print(data)
    return data
    # return [['Sentiment', 'number of tweets'], ['Positive', postive_count],
    #         ['Neutral', neutral_count], ['Negative', negative_count]]
