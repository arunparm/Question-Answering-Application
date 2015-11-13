import sys

from nltk.corpus import stopwords
from nltk.tokenize import *
from Story import *
from Question import *
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
from nltk.tree import Tree

directoryName = ''
storyIds = []  # All the story ids in the input file
storyObjects = []
answerFile = None


def readInputFile():
    inputFile = open("inputfile.txt", 'r')  # Read from command line
    global directoryName
    directoryName = inputFile.readline().rstrip("\n")
    for line in inputFile:
        storyIds.append(line.rstrip("\n"))


def readQuestionsFile(storyId):
    questionFile = open(directoryName.replace("\\", "/") + "/" + storyId + ".questions", "r")
    readQuestions = []
    while True:
        ques = Question()
        # Question Id of the question
        questionId = questionFile.readline()
        if not questionId: break
        colonIndex = questionId.index(":")
        ques.quesId = questionId[colonIndex + 2:]
        # print(ques.quesId)
        # Question of the question
        question = questionFile.readline()
        colonIndex = question.index(":")
        ques.ques = question[colonIndex + 2:]
        # print(ques.ques)
        # Question Type of the question
        questionText = question[colonIndex + 2:]
        spaceIndex = questionText.index(" ")
        ques.quesType = questionText[0:spaceIndex]
        # print(ques.quesType)
        # Question Difficulty of the question
        questionDiff = questionFile.readline()
        colonIndex = questionDiff.index(":")
        ques.difficulty = questionDiff[colonIndex + 2:]
        # print(ques.difficulty)
        questionFile.readline()
        readQuestions.append(ques)
    return readQuestions


def readStoryFiles():
    for storyId in storyIds:
        storyFile = open(directoryName.replace("\\", "/") + "/" + storyId + ".story", 'r')
        story = Story()
        # Headline of the story
        headline = storyFile.readline()
        colonIndex = headline.index(":")
        story.headline = headline[colonIndex + 2:]
        # Date of the story
        date = storyFile.readline()
        colonIndex = date.index(":")
        story.date = date[colonIndex + 2:]
        # Story ID of the story
        id = storyFile.readline()
        story.storyId = storyId
        # Sentences of the story
        storyFile.readline()
        storyFile.readline()
        fileContent = storyFile.read()
        # story.sentences = fileContent.replace("\n", " ").split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s")
        # story.sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', fileContent.replace("\n", " "))
        sent_detector = load('tokenizers/punkt/english.pickle')
        story.sentences = sent_detector.tokenize(fileContent.strip())
        # Questions of the story
        story.questions = readQuestionsFile(storyId)
        storyObjects.append(story)


def wordMatch(sentences, ques):
    stopWords = stopwords.words('english')
    quesWords = word_tokenize(ques.ques)
    lemmatizer = WordNetLemmatizer()
    quesWords_Lemmatized = [lemmatizer.lemmatize(word) for word in quesWords]
    maxSentence = ''
    maxScore = 0
    for sent in sentences:
        score = 0
        sent = sent.replace(".", "")
        sent = sent.replace(",", "")
        sentenceWords = word_tokenize(sent)
        # Removing stop words
        filteredWords = []
        for word in sentenceWords:
            if word not in stopWords:
                filteredWords.append(word)

        filteredWords_Lemmatized = [lemmatizer.lemmatize(word) for word in filteredWords]

        postags = nltk.pos_tag(filteredWords_Lemmatized)
        dict = {}
        propernouns = []
        referencetohuman = 'false'
        for tag in postags:
            dict[tag[0]] = tag[1]
            if 'NNP' in tag[1]:
                propernouns.append(tag[0])
            if 'NN' in tag[1]:
                referencetohuman = 'true'

        #Rule 1
        for qWord in quesWords_Lemmatized:
            if qWord in filteredWords_Lemmatized:
                if 'VB' in dict[qWord]:
                    score += 6
                    #break
                else:
                    score += 3
                    #break

        # Rule 2
        for pn in propernouns:
            if pn in quesWords_Lemmatized: # The same noun word is present in the ques as well
                score += 6

        # Rule 3
        quesposttags = nltk.pos_tag(quesWords_Lemmatized)
        for tag in quesposttags:
            if 'NNP' in tag[1] and 'name' in filteredWords_Lemmatized:
                score += 4

        # Rule 4
        if propernouns.__len__() > 0 or referencetohuman == 'true':
            score += 4

        if score > maxScore:
            maxScore = score
            maxSentence = sent
    print("Answer: " + maxSentence.replace("\n", " "))
    answerFile.write("\nAnswer: " + maxSentence.replace("\n", " ") + "\n\n")



def whoQuestions(sentences, ques):
    # Rule 1
    wordMatch(sentences, ques)

def whenQuestions(sentences, ques):
    timeKeywords = ['first', 'last', 'since', 'ago']
    sentKeywords = ['start', 'begin', 'since', 'year']
    quesKeywords = ['start', 'begin']
    TIME = ['morning', 'evening', 'tomorrow', 'soon', 'yesterday', 'last', 'week', 'recently', 'hour', 'ago', 'while', 'past', 'present', 'january', 'february', 'march',
            'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
            'noon', 'month', 'year', 'everyday', 'day', 'today', 'seconds', 'minute', 'night', 'time', 'sunrise', 'sunset', 'decade']
    for year in range(1400, 2016):
        TIME.append(year)

    stopWords = stopwords.words('english')
    quesWords = word_tokenize(ques.ques)
    lemmatizer = WordNetLemmatizer()
    quesWords_Lemmatized = [lemmatizer.lemmatize(word) for word in quesWords]

    maxScore = 0
    maxSentence = ''
    for sent in sentences:
        score = 0
        sent = sent.replace(".", "")
        sent = sent.replace(",", "")
        # Rule 1
        sentenceWords = word_tokenize(sent)
        for word in sentenceWords:
            if word.lower() in TIME:
                score += 4
                # WordMatch
                # Removing stop words
                filteredWords = []
                for word in sentenceWords:
                    if word not in stopWords:
                        filteredWords.append(word)

                filteredWords_Lemmatized = [lemmatizer.lemmatize(word) for word in filteredWords]

                postags = nltk.pos_tag(filteredWords_Lemmatized)
                dict = {}
                propernouns = []
                referencetohuman = 'false'
                for tag in postags:
                    dict[tag[0]] = tag[1]
                    if 'NNP' in tag[1]:
                        propernouns.append(tag[0])
                    if 'NN' in tag[1]:
                        referencetohuman = 'true'

                for qWord in quesWords_Lemmatized:
                    if qWord in filteredWords_Lemmatized:
                        if 'VB' in dict[qWord]:
                            score += 6
                            #break
                        else:
                            score += 3
                            #break

        # Rule 2
        if 'the last' in ques.ques and any(key in sent for key in timeKeywords):
            score += 20

        # Rule 3
        if any(key in ques.ques for key in quesKeywords) and any(key1 in sent for key1 in sentKeywords):
            score += 20

    if score > maxScore:
        maxScore = score
        maxSentence = sent

    print("Answer: " + maxSentence.replace("\n", " "))
    answerFile.write("\nAnswer: " + maxSentence.replace("\n", " ") + "\n\n")



def whereQuestions(sentences, ques):
    stopWords = stopwords.words('english')
    quesWords = word_tokenize(ques.ques)
    lemmatizer = WordNetLemmatizer()
    quesWords_Lemmatized = [lemmatizer.lemmatize(word) for word in quesWords]
    locationPreps = ['in', 'on', 'at', 'by', 'near', 'nearby', 'above', 'below', 'over', 'under', 'up', 'down', 'around', 'through', 'inside', 'outside', 'between', 'beside',
                     'beyond', 'in front of', 'in back of', 'behind', 'next to', 'on top of', 'within', 'beneath', 'underneath', 'among', 'along', 'against']
    maxSentence = ''
    maxScore = 0
    for sent in sentences:
        score = 0
        sent = sent.replace(".", "")
        sent = sent.replace(",", "")
        sentenceWords = word_tokenize(sent)
        # Removing stop words
        filteredWords = []
        for word in sentenceWords:
            if word not in stopWords:
                filteredWords.append(word)

        filteredWords_Lemmatized = [lemmatizer.lemmatize(word) for word in filteredWords]

        postags = nltk.pos_tag(filteredWords_Lemmatized)
        dict = {}
        propernouns = []
        referencetohuman = 'false'
        for tag in postags:
            dict[tag[0]] = tag[1]
            if 'NNP' in tag[1]:
                propernouns.append(tag[0])
            if 'NN' in tag[1]:
                referencetohuman = 'true'

        #Rule 1
        for qWord in quesWords_Lemmatized:
            if qWord in filteredWords_Lemmatized:
                if 'VB' in dict[qWord]:
                    score += 6
                    #break
                else:
                    score += 3
                    #break

        # Rule 2
        for word in sentenceWords:
            if word in locationPreps:
                score += 4

        # Rule 3
        sentTags = nltk.pos_tag(sentenceWords)
        tree = nltk.ne_chunk(sentTags)
        for i in tree:
            if type(i) == Tree and 'LOCATION' in i.label():
                score += 6

        if score > maxScore:
            maxScore = score
            maxSentence = sent

    print("Answer: " + maxSentence.replace("\n", " "))
    answerFile.write("\nAnswer: " + maxSentence.replace("\n", " ") + "\n\n")

def beginAnswering():
    global answerFile
    answerFile = open("answer.response", "w")
    for story in storyObjects:
        for ques in story.questions:
            print("Question: " + ques.quesId.replace("\n", ""))
            answerFile.write("QuestionID: " + ques.quesId.replace("\n", ""))
            if ques.quesType == "Who":
                whoQuestions(story.sentences, ques)
            elif ques.quesType == "Where":
                whereQuestions(story.sentences, ques)
            elif ques.quesType == "Which":
                whoQuestions(story.sentences, ques)
            elif ques.quesType == "When":
                whenQuestions(story.sentences, ques)
            else:
                whoQuestions(story.sentences, ques)


if __name__ == '__main__':
    readInputFile()
    readStoryFiles()
    beginAnswering()
