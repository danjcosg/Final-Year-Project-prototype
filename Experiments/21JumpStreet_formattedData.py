filmname = "21_JUMP_STREET"

clipNames = ["21_JUMP_STREET_DVS20", "21_JUMP_STREET_DVS21", "21_JUMP_STREET_DVS22"]
annotationPath = "M-Vad_Names/M-VAD-refined-annotations/"

table1 = {}

def generateFormattedData():

    def extractNames(string):
        #there can be multiple names
        names = []
        count = 0
        for "<*>" in string:
            names.append(string.re("<*>\number" + count))
    #  \number
    #Matches the contents of the group of the same number. Groups are numbered starting from 1. For example, (.+) \1 matches 'the the' or '55 55', but not 'thethe' (note the space after the group). This special sequence can only be used to match one of the first 99 groups. If the first digit of number is 0, or number is 3 octal digits long, it will not be interpreted as a group match, but as the character with octal value number. Inside the '[' and ']' of a character class, all numeric escapes are treated as characters.

    #https://docs.python.org/3/library/re.html

        return names

    with open(annotationPath + filmname + "/_ID.srt", 'r') as srtFile:
        count = 0
        for line in srtFile.readlines() :
            if clipNames.contains(line.del('\n')):
                names = extractNames(lines[count+2])
                table1[ lines[count] ] = [names,[]] 


def getFormattedData():
    #unpickle
    return table1