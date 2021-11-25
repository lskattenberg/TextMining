# this script precision, recall, F1-score
# it also generates a confusion  matrix
# the input file is a csv file with the following columns: ID, GOLD, PRED, TEXT
# the column TEXT can be omitted
# the first row of the file is the header row

import csv
from sklearn.model_selection import cross_validate
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
inputfile="inout/toy_goldandpred.csv"
inputfile="inout/toy_vader_output.csv"
outputfile = "inout/evaluation_report.txt"
f_out=open(outputfile,"w+")

y_true=[] # gold annotations
y_pred=[] # system predictions

with open(inputfile, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    next(reader)  # skip header
    for row in reader:
        y_true.append(row[1])
        y_pred.append(row[2])
    # print numbers gold and sys
    f_out.write("gold\t:"+str([[x, y_true.count(x)] for x in set(y_true)]))
    f_out.write("\npred\t:"+str([[x, y_pred.count(x)] for x in set(y_pred)]))


f_out.write("\n\ninput:"+ inputfile)

f_out.write("\n\naccuracy_score:"+ str(accuracy_score(y_true, y_pred)))

f_out.write("\n\nclassification report:\n"+ classification_report(y_true, y_pred))
f_out.write("\n\nconfusion matrix:\n\n"+str(confusion_matrix(y_true, y_pred)) )
f_out.write("\nrow is gold  /\tcolumn is predicted")


