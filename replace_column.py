import csv

# open input CSV file as source
# open output CSV file as result
with open("Lyrics_with_annotations.csv", "r") as source:
    reader = csv.reader(source)

    bla = 0
    with open("Lyrics_with_annotations_formatted.csv", "w") as result:
        writer = csv.writer(result, delimiter=';')
        for r in reader:
            id = "ID-" + str(bla)
            # Use CSV Index to remove a column from CSV
            #r[3] = r['year']
            writer.writerow((id, r[2].strip(), r[1]))
            bla += 1
