import sys
from Story import *
from Question import *

directoryName = ''
storyIds = [] # All the story ids in the input file
storyObjects = []

def readInputFile():
    inputFile = open("inputfile.txt", 'r') # Read from command line
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
        ques.quesId = questionId[colonIndex+2:]
        print(ques.quesId)
        # Question of the question
        question = questionFile.readline()
        colonIndex = question.index(":")
        ques.ques = question[colonIndex+2:]
        print(ques.ques)
        # Question Type of the question
        questionText = question[colonIndex+2:]
        spaceIndex = questionText.index(" ")
        ques.quesType = questionText[0:spaceIndex+1]
        print(ques.quesType)
        # Question Difficulty of the question
        questionDiff = questionFile.readline()
        colonIndex = questionDiff.index(":")
        ques.difficulty = questionDiff[colonIndex+2:]
        print(ques.difficulty)
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
        story.headline = headline[colonIndex+2:]
        # Date of the story
        date = storyFile.readline()
        colonIndex = date.index(":")
        story.date = date[colonIndex+2:]
        # Story ID of the story
        id = storyFile.readline()
        story.storyId = storyId
        # Sentences of the story
        fileContent = storyFile.read()
        story.sentences = fileContent.replace("\n", "").split(".")
        print(story.sentences.__len__())
        # Questions of the story
        story.questions = readQuestionsFile(storyId)
        storyObjects.append(story)

if __name__ == '__main__':
    readInputFile()
    readStoryFiles()



