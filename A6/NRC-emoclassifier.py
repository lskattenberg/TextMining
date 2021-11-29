# this script classifies pieces of text into emotions (see # emotion settings)
# the code is party based on http://jonathansoma.com/lede/algorithms-2017/classes/more-text-analysis/nrc-emotional-lexicon/
# the emotion lexicon used can be dowmloaded here https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm

# input file  (csv):(["ID", "Gold","Text"])
# output file (csv) :  (["ID", "Gold", "Pred", "Text"]) (input for evaluation_classifier.py)
# output file (NRCemo-detailed-overview.txt) : ID,Gold,overview (information useful for error analysis)

# the output classes are one of the emotions of the choosen emotion set, 'noEmo' and 'mixedEmo'
# 'noEmo' in case no emotions are found; 'mixedEmo' in case none of  the found emotiomns is most frequent
# if emotionset=NRCpolarity , output classes are 'positive', 'negative' or 'neutral'
# input file: csv  # csv output (["ID", "Gold", "Pred", "Text"])

import spacy
import pandas as pd
import csv
from collections import Counter
nlp = spacy.load('en')


## emotion settings
NRCemotions=   ['anger', 'fear', 'anticipation','disgust','joy','sadness','surprise','trust']
myEmotions = ['anger','fear','disgust','sadness','joy','anticipation']
NRCpolarity= ['positive','negative']
NRCcomplete=NRCpolarity+NRCemotions
myEmotionsSet = ['anger','sadness','joy','anticipation']
emotionset=NRCpolarity
# emotionset=NRCemotions

## input output files
filename="Nirvana/Leonard/Lyrics_with_Gold_annotations_formatted.csv"
outputfilename="Nirvana/Leonard/NRC_Nirvana_Gold.csv"
detailed_outputfile = "Nirvana/Leonard/NRC_Nirvana_Gold_detailed_overview.txt"
f_out=open(detailed_outputfile,"w+")

# emotion lexicon
filepath = "lexical_resources/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"
emolex_df = pd.read_csv(filepath,  names=["word", "emotion", "association"],  sep='\t')


def preprocess_token(token):
    ## token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha, token.is_stop
    # key=token.lemma_
    key=token.text
    return(key)

def analyze_line(s, emotionset):
    # initialize emotion counters
    emoCounter = Counter()
    for e in emotionset:
        emoCounter[e] = 0


    # analyze line
    for token in s:

        key=preprocess_token(token)
        word_df=emolex_df[emolex_df.word == key]
        #print(word_df)
        for index, row in word_df.iterrows():
            if row['emotion'] in  emotionset:
                emoCounter[row['emotion']]  += int(row['association'])
    return(emoCounter)

def aggregate_emotions(emoCounter):
    # main emotion is the most frequent emotion
    # in case of a tie => mixedEmo
    # in case of no emotions => noEmo
    mainEmotion="noEmo"
    #print(sorted(emoCounter.values(),reverse=True))
    if (sum(emoCounter.values()))>0:
        emoCounter_sorted=sorted(emoCounter.values(), reverse=True)
        if emoCounter_sorted[0]> emoCounter_sorted[1]:
            mainEmotion = emoCounter.most_common()[0][0]
        else:
            mainEmotion='mixedEmo'
    return(mainEmotion)

def aggregate_polarity(emoCounter):
    # polarity value : number of positive words - number of negative words
    # if result = 0 or no positive or negative word is found  => polarity value = neutral
    polarity="ntr"
    if (emoCounter['positive']-emoCounter['negative'])>0:
        polarity='pos'
    elif (emoCounter['positive']-emoCounter['negative'])<0:
        polarity='neg'
    return(polarity)

def aggregate_propotional_polarity(emoCounter):
    relevant_proportion = 0.67
    totalemos = emoCounter['positive'] + emoCounter['negative']
    if totalemos == 0:
        return 'ntr'
    if (emoCounter['positive'] / totalemos) > relevant_proportion:
        return 'pos'
    if (emoCounter['negative'] / totalemos) > relevant_proportion:
        return 'neg'
    return 'ntr'

def main():
    aggrEmoCounter = Counter()
    for e in emotionset:
        aggrEmoCounter[e] = 0
    with open(outputfilename, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["ID", "Gold", "Pred", "Text"])
        f_out.write("ID;Pred;details\n")
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            next(reader)  # skip header
            for row in reader:
                # iterate over lines
                s = nlp(row[2])
                emoCounter=analyze_line(s, emotionset)
                if len(emotionset)==2 and 'positive' in emotionset and 'negative' in emotionset:
                    main_result = aggregate_propotional_polarity(emoCounter)
                    # main_result=aggregate_polarity(emoCounter)
                else :
                    main_result=aggregate_emotions(emoCounter)
                # write result to files
                writer.writerow([row[0], row[1], main_result, row[2]])
                f_out.write( row[0] + ";" + main_result + ";" + str(emoCounter)[8:-1]+"\n")
                # f_out.write("ID;PRED;details")

                # overall stats
                aggrEmoCounter[main_result]+=1
    print("emotionset:\t\t",emotionset,"\nglobal stats:\t",aggrEmoCounter,sum(aggrEmoCounter.values()))
    # print(len(reader))



if __name__ == "__main__": main()
