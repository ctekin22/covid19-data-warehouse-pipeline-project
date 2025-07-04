
import redshift_connector
# -----------------------------------------------------------------------------------------------------------------
# Connect to Redshift with redshift_connector
# -----------------------------------------------------------------------------------------------------------------

conn = redshift_connector.connect(
    host='redshift-cluster-1.cc77d1b7vqwz.us-east-1.redshift.amazonaws.com',     # Redshift Endpoint
    port=5439,
    database='dev',
    user='awsuser',
    password ='Passw0rd123'
)

conn.autocommit = True # Each SQL statement is committed immediately after execution.

# -----------------------------------------------------------------------------------------------------------------
# Create tables in Redshift, use the schema output you get
# -----------------------------------------------------------------------------------------------------------------
# import redshift_connector   
# Create a cursor used to execute the query
cursor = conn.cursor()


# factCovid
cursor.execute("""
CREATE TABLE "factCovid" (
"index" INTEGER,
  "fips" REAL,
  "province_state" TEXT,
  "country_region" TEXT,
  "confirmed" REAL,
  "deaths" REAL,
  "recovered" REAL,
  "active" REAL,
  "date" INTEGER,
  "positive" INTEGER,
  "negative" REAL,
  "hospitalizedcurrently" REAL,
  "hospitalized" REAL,
  "hospitalizeddischarged" REAL
)
""")

# dimHospital
cursor.execute("""
CREATE TABLE "dimHospital" (
"index" INTEGER,
  "fips" INTEGER,
  "state_name" TEXT,
  "latitude" REAL,
  "longtitude" REAL,
  "hq_address" TEXT,
  "hospital_name" TEXT,
  "hospital_type" TEXT,
  "hq_city" TEXT,
  "hq_state" TEXT
)
""")

# dimRegion
cursor.execute("""
CREATE TABLE "dimRegion" (
"index" INTEGER,
  "fips" REAL,
  "province_state" TEXT,
  "country_region" TEXT,
  "latitude" REAL,
  "longitude" REAL,
  "county" TEXT,
  "state" TEXT
)
""")

# dimDate
cursor.execute("""
CREATE TABLE "dimDate" (
"index" INTEGER,
  "fips" REAL,
  "date" TIMESTAMP,
  "year" INTEGER,
  "month" INTEGER,
  "day_of_week" INTEGER
)
""")

# -----------------------------------------------------------------------------------------------------------------
# Copy tables in Redshift
# -----------------------------------------------------------------------------------------------------------------

# Copy factCovid
cursor.execute("""
copy factCovid from 's3://covid-19-data-de/output/factCovid.csv'
credentials 'aws_iam_role=arn:aws:iam::626127091134:role/redshift-s3-access'
delimiter ','
region 'us-east-1'
IGNOREHEADER 1
""")

# Copy dimRegion
cursor.execute("""
copy dimRegion from 's3://covid-19-data-de/output/dimRegion.csv'
credentials 'aws_iam_role=arn:aws:iam::626127091134:role/redshift-s3-access'
delimiter ','
region 'us-east-1'
IGNOREHEADER 1
""")

# Copy dimDate
cursor.execute("""
copy dimDate from 's3://covid-19-data-de/output/dimDate.csv'
credentials 'aws_iam_role=arn:aws:iam::626127091134:role/redshift-s3-access'
delimiter ','
region 'us-east-1'
IGNOREHEADER 1
""")

# Copy dimHospital
cursor.execute("""
copy dimHospital from 's3://covid-19-data-de/output/dimHospital.csv'
credentials 'aws_iam_role=arn:aws:iam::626127091134:role/redshift-s3-access'
delimiter ','
region 'us-east-1'
IGNOREHEADER 1
""")
