from Summarizer import *

# enter links into the 'links.txt' file. If you just want to use the summarizer, you can download that specific file.
f = open('links.txt', 'r')

for url in f:
    #input error handling
    try:
        summaryLength = int(input('Enter how many lines do you want in the summary: '))
        print(url, '\n')
        summary, polarity, subjectivity = Summarizer(url, summaryLength).summarize_text()
        print(summary)
        print('\nPolarity (-1 to 1):', polarity)
        print('Subjectivity (-1 to 1):', polarity,'\n')
    except:
        print('Input gave an error!')