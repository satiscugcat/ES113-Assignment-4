from flask import Flask,render_template,url_for,request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="Survivor@2005"
app.config["MYSQL_DB"]="assignment4"
app.config["MYSQL_HOST"]="localhost"

mysql=MySQL(app)

def tupleToList(tuple2d):
    return list(map(lambda x: list(x),tuple2d))

@app.get("/")
def hello():
    bond_number=request.args.get("bond-number")
    bond_number_data=None

    company_individual_name=request.args.get("company-individual-name")
    company_individual_bond_data=None

    political_party_name=request.args.get("political-party-name")
    political_party_bond_data=None

    political_donations_name=request.args.get("political-donations-name")
    political_donations_data=None

    company_donations_name=request.args.get("company-donations-name")
    company_donations_data=None

    cur=mysql.connection.cursor()
    cur.execute("""USE assignment4;""")
    if bond_number:
        headers=(("Sr No.", "Date of Encashment", "Name of the Political Party", "Account no. of the Political Party", "Prefix", "Bond Number", "Denominations", "Pay Branch Code", "Pay Teller"),
                ("Sr No.", "Reference No (URN)", "Journal Date", "Date of Purchase", "Date of Expiry","Name of the Purchaser", "Prefix", "Bond Number", "Denominations", "Issue Branch Code", "Issue Teller", "Status"))

        cur.execute("""select * from eb_redemption_details where Bond_Number = {num}; """.format(num=bond_number))
        redemption_data=cur.fetchall()
        cur.execute("""select * from eb_purchase_details where Bond_Number = {num}; """.format(num=bond_number))
        purchase_data=cur.fetchall()
        
        bond_number_data=[{"headers": headers[0], "data": redemption_data},{"headers": headers[1], "data": purchase_data}]

    if company_individual_name:
        cur.execute("""select extract(year from Date_of_Purchase),count(Bond_Number),sum(Denominations) from eb_purchase_details where Name_of_the_Purchaser = '{name}' group by extract(year from Date_of_Purchase);""".format(name=company_individual_name.upper()))
        company_individual_bond_data=tupleToList(cur.fetchall())
        
    
    if political_party_name:
        cur.execute("""select extract(year from Date_of_Encashment),count(Bond_Number),sum(Denominations) from eb_redemption_details where Name_of_the_Political_Party = '{name}' group by extract(year from Date_of_Encashment);""".format(name=political_party_name.upper()))
        political_party_bond_data=tupleToList(cur.fetchall())

    if political_donations_name:
        cur.execute("""select P.Name_of_the_Purchaser, sum(P.Denominations) from eb_purchase_details as P, (select Bond_Number from eb_redemption_details where Name_of_the_Political_Party = '{name}') as E where P.Bond_Number = E.Bond_Number group by P.Name_of_the_Purchaser;""".format(name=political_donations_name.upper()))
        political_donations_data=tupleToList(cur.fetchall())

    if company_donations_name:
        cur.execute("""select P.Name_of_the_Political_Party, sum(P.Denominations) from eb_redemption_details as P, (select Bond_Number from eb_purchase_details where Name_of_the_Purchaser = '{name}') as E where P.Bond_Number = E.Bond_Number group by P.Name_of_the_Political_Party;""".format(name=company_donations_name.upper()))
        company_donations_data=tupleToList(cur.fetchall())
        
    total_donations_data=None
    cur.execute("""select Name_of_the_Political_Party, sum(Denominations) from eb_redemption_details group by Name_of_the_Political_Party;""")
    total_donations_data=tupleToList(cur.fetchall())

    return render_template("index.html",
                           bond_number_data=bond_number_data,
                           company_individual_bond_data=company_individual_bond_data,
                           political_party_bond_data=political_party_bond_data,
                           political_donations_data=political_donations_data,
                           company_donations_data=company_donations_data,
                           total_donations_data=total_donations_data)