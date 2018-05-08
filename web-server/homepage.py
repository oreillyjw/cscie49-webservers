from flask import Flask, render_template, jsonify
from flaskext.mysql import MySQL
import boto3
from botocore.exceptions import ClientError
import ast
import requests

def get_secret():
    secret_name = "prod/cscie49/mysql-final"
    endpoint_url = "https://secretsmanager.us-east-1.amazonaws.com"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        endpoint_url=endpoint_url
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
        else:
            print(e)
    else:
        # Decrypted secret using the associated KMS CMK
        # Depending on whether the secret was a string or binary, one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return secret
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']
            return binary_secret_data

def fetch_cms_text():
    url = "https://localhost:443/cms-text"
    r = requests.get(url,verify=False)
    return r.json()

secrets = get_secret()
secretDict = ast.literal_eval(secrets)

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = secretDict['username']
app.config['MYSQL_DATABASE_PASSWORD'] = secretDict['password']
app.config['MYSQL_DATABASE_DB'] = secretDict['dbname']
app.config['MYSQL_DATABASE_HOST'] = secretDict['host']
mysql.init_app(app)

@app.route("/")
def homepage(environ="dev", start_response=False):
    cursor = mysql.connect().cursor()
    cursor.execute("select * from product")
    data = cursor.fetchall()
    products = []

    for item in data:
        product = {}
        product['sku'] = item[0]
        product['image'] = item[1]
        product['title'] = item[2]
        products.append(product)

    textData = fetch_cms_text()
    return render_template('homepage.html', content=products, textContent=textData)

if __name__ == "__main__":
    app.run()
