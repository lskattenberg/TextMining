# uses nltk and vader with own text files
# print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha, token.is_stop)
# format csv file with 3 columns ID,Gold,Text
# output format csv file with 4 columns : ID, GOLD, PRED, Text


from nltk.sentiment.vader import SentimentIntensityAnalyzer
import csv
import spacy
nlp=spacy.load('en')



analyzer = SentimentIntensityAnalyzer()
filename="Nirvana/Leonard/Lyrics_with_Leonard_annotations_formatted.csv"
outputfilename="Nirvana/Leonard/VADER_Nirvana_Leonard.csv"
outputfile = "Nirvana/Leonard/VADER_Nirvana_Leonard_detailed_overview.txt"
f_out=open(outputfile,"w+")



def preprocess_token(token):
    ## token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha, token.is_stop
    # key=token.lemma_ ## the input is the lemma
    key=token.text
    return(key)

def sentence_doc():
	# analyzing file line per line

	with open(outputfilename, 'w', newline='') as file:
		writer = csv.writer(file,delimiter=";")
		writer.writerow(["ID", "Gold", "Pred","Text"])
		f_out.write("ID;Pred;details\n")
		with open(filename, newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=';', quotechar='|')
			next(reader)  # skip header
			for row in reader:
				sentence=row[2]
				doc=nlp(sentence)
				s=""
				#print(nltk.pos_tag(sentence))
				for token in doc:
						s=s+" "+preprocess_token(token)
				ss = analyzer.polarity_scores(s)
				pred_value=""
				for i in ss:
					# {'neg': 0.195, 'neu': 0.531, 'pos': 0.274, 'compound': 0.2228}
					if i == "compound":
						if ss[i]> 0:
							pred_value="pos"
						elif ss[i] < 0:
							pred_value = "neg"
						else:
							pred_value = "ntr"
				f_out.write(row[0]+";"+pred_value +";"+str(ss)+"\n")
				writer.writerow([row[0], row[1], pred_value,row[2]])
				print(s)




def main():
    sentence_doc()


if __name__ == "__main__": main()
