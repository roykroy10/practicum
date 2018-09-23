from flask import Flask, render_template, request, url_for, redirect
import pandas as pd


app = Flask(__name__)
DATABASE_PATH = '/home/ubuntu/nei_filtered_sj.csv'
DF = pd.read_csv(DATABASE_PATH)
ZIPS = DF.postal_code.unique()

def get_panda_data(zip,by):
    df = pd.read_csv(DATABASE_PATH)
    df = df.loc[df['postal_code'] == int(zip)]
    df = df[['zpid','address','city','postal_code','price','price_sqft','sale_price_sign','pricepersqft_sign','yearSold','lat','lon','url']].copy()

    if(by=='price'):
        df = df.sort_values(by='sale_price_sign', ascending=True).head(10)
    else:
        df = df.sort_values(by='pricepersqft_sign', ascending=True).head(10)
    tags_html = df.to_html(escape=False)
    return tags_html

@app.route('/index')
@app.route('/')
def index():
    return render_template("dropdown.html", postal_codes=ZIPS)

@app.route('/show', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        zip = request.form.get("postal_code", None)
        by = request.form.get("by", None)
        if zip!="0":
            html_data = get_panda_data(zip,by)
            return render_template("dropdown2.html", postal_codes=ZIPS, postal_code = zip, html_data = html_data)
    return render_template("dropdown2.html", postal_codes=ZIPS)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
