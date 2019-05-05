from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'
# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.scrape_db

@app.route("/")
def index():
    # Store the collections in lists
    listings = list(db.nasalistings.find())
    print(listings)
    
    table_listings = list(db.tablelisting.find())
    print(table_listings)

    return render_template("index.html", listings=listings, tablelistings=table_listings)

@app.route("/scrape")
def scraper():
    listings_data, tables_data = scrape_mars.scrape()
    print(type(tables_data))

    final_data = []
    for data in tables_data:
        d = dict([(k, v) for k,v in zip (data[0], data[1])])
        final_data.append(d)

    # Drops collections if available to remove duplicates
    db.nasalistings.drop()
    db.tablelisting.drop()

    # Inserts documents into a collections in the database
    db.nasalistings.insert_many(listings_data)
    db.tablelisting.insert_many(final_data)

    for listitem in tables_data:
        for fact in listitem.items():
            print('{}: {}'.format(fact[0], fact[1]))
        

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
