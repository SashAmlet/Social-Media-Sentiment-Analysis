from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from analyze import TextProcessor

analyzer = SentimentIntensityAnalyzer()
processor = TextProcessor()

pos_count = 0
pos_correct = 0

with open("positive.txt","r") as f:
    for line in f.read().split('\n'):
        resp = processor.analyze_sentiment(line)
        if resp == 'Positive':
            pos_correct += 1

        if resp != 'Neutral':
            pos_count +=1

        # vs = analyzer.polarity_scores(line)
        # if not vs['neg'] >= 0.005:
        #     if vs['pos']-vs['neg'] > 0:
        #         pos_correct += 1
        #     pos_count +=1


neg_count = 0
neg_correct = 0

with open("negative.txt","r") as f:
    for line in f.read().split('\n'):
        resp = processor.analyze_sentiment(line)
        if resp == 'Negative':
            neg_correct += 1

        if resp != 'Neutral':
            neg_count +=1
        # vs = analyzer.polarity_scores(line)
        # if not vs['pos'] >= 0.005:
        #     if vs['pos']-vs['neg'] < 0:
        #         neg_correct += 1
        #     neg_count +=1

print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))