import fitz
import csv

def formatDate(dateString):
    dateString=dateString.replace("Jan","01")
    dateString=dateString.replace("Feb","02")
    dateString=dateString.replace("Mar","03")
    dateString=dateString.replace("Apr","04")
    dateString=dateString.replace("May","05")
    dateString=dateString.replace("Jun","06")
    dateString=dateString.replace("Jul","07")
    dateString=dateString.replace("Aug","08")
    dateString=dateString.replace("Sep","09")
    dateString=dateString.replace("Oct","10")
    dateString=dateString.replace("Nov","11")
    dateString=dateString.replace("Dec","12")

    dateString=dateString.split("/")
    dateString=dateString[2]+"-"+dateString[1]+"-"+dateString[0]

    return dateString

def formatNumber(numberString):
    numberString=numberString.strip('"')
    return numberString.replace(",","")

def doc1formatter(row):
    row[1]=formatDate(row[1])
    row[-3]=formatNumber(row[-3])
    return row

def doc2formatter(row):
    row[2]=formatDate(row[2])
    row[3]=formatDate(row[3])
    row[4]=formatDate(row[4])
    row[-4]=formatNumber(row[-4])
    return row

doc = fitz.open("EB_Redemption_Details.pdf")
with open("EB_Redemption_Details.csv",mode="w",newline="") as file:
    i=0
    writer=csv.writer(file,delimiter="+")
    for page in doc:
        table=page.find_tables().tables[0].extract()
        writer.writerows(list(map(doc1formatter,table[1:])))
        i+=1
        print(i)
doc.close()

doc = fitz.open("EB_Purchase_Details.pdf")
with open("EB_Purchase_Details.csv",mode="w",newline="") as file:
    i=0
    writer=csv.writer(file,delimiter="+")
    for page in doc:
        table=page.find_tables().tables[0].extract()
        writer.writerows(list(map(doc2formatter,table[1:])))
        i+=1
        print(i)
doc.close()
