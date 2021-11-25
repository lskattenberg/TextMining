import csv

# open input CSV file as source
# open output CSV file as result
with open("Lyrics_with_annotations.csv", "r") as source:
    reader = csv.reader(source)

    bla = 0
    with open("output2.csv", "w") as result:
        writer = csv.writer(result)
        for r in reader:
            id = "lyrics_test" + str(bla)
            # Use CSV Index to remove a column from CSV
            #r[3] = r['year']
            writer.writerow((id, r[2], r[3]))
            bla += 1
