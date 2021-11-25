import csv

# open input CSV file as source
# open output CSV file as result
with open("Lyrics_with_annotations.csv", "r") as source:
    reader = csv.reader(source)

    bla = 0
    with open("A6/Nirvana/Leonard/Lyrics_with_Leonard_annotations_formatted.csv", "w") as result:
        writer = csv.writer(result, delimiter=';')
        for r in reader:
            id = "ID-" + str(bla)
            # Use CSV Index to remove a column from CSV
            #r[3] = r['year']
            writer.writerow((id, r[3].strip(), r[1]))
            bla += 1
