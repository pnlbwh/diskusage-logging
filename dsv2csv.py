import sys
import csv

tabin = csv.reader(sys.stdin, delimiter='|')
commaout = csv.writer(sys.stdout, dialect=csv.excel)
for row in tabin:
  commaout.writerow(row)
