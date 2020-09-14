import bs4 as bs
import urllib.request
import re
import nltk
from textblob import TextBlob
from nltk import word_tokenize
from nltk.corpus import stopwords
import heapq

class Summarizer:
    def __init__(self, url, summaryLength):
        self.url = url
        self.summaryLength = summaryLength

    def summarize_text(self):
        # reads the inputted url and created a beauitful soup object that can be scraped
        stopWords = set(stopwords.words('english'))
        article = urllib.request.urlopen(self.url).read()
        textData = bs.BeautifulSoup(article, 'lxml')

        # finds all the text within the paragraph tags of the site
        text = ''
        for paragraph in textData.find_all('p'):
            text += paragraph.text + ' '

        # creates a dictionary of all the subjects in the text
        subjectFrequencies = {}
        blob = TextBlob(text)
        for wordTag in blob.tags:
            word = wordTag[0]
            if word not in stopWords:
                tag = wordTag[1]
                if tag == 'NN' or tag == 'NNS' or tag == 'NNP' or tag == 'NNPS':
                    if word not in subjectFrequencies:
                        subjectFrequencies[word] = 1
                    else:
                        subjectFrequencies[word] += 1

        # creates a sentence dictionary where each sentence is assigned the sum of subject fequencies it holds
        # the more subjects from the main article that appear in the sentence, the more likely it is relevant
        sentences = re.split('(?<=[\.\?\!])\s*', text)
        sentenceFrequencies = {}
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            for word in words:
                # if the word is a subject, the sentence's weight increases
                if word in subjectFrequencies:
                    if sentence not in sentenceFrequencies:
                        sentenceFrequencies[sentence] = subjectFrequencies[word]
                    else:
                        sentenceFrequencies[sentence] += subjectFrequencies[word]

        # only includes only the top 'self.summaryLength' sentences within the summary	
        summarySentences = heapq.nlargest(self.summaryLength, sentenceFrequencies, sentenceFrequencies.get)
        summary = '\n'.join(summarySentences)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        return summary, polarity, subjectivity