from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pyodbc
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Azure SQL Database connection string with ODBC Driver 18
conn_str = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:memershiptest.database.windows.net,1433;Database=Membership-Test;Uid=sachindu;Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

def get_db_connection():
    """Create and return a connection to the database"""
    return pyodbc.connect(conn_str)

@app.route('/')
def index():
    return render_template('sinhala-registration-form.html')

@app.route('/api/submit', methods=['POST'])
def submit_form():
    try:
        # Get form data
        data = request.json
        
        # Extract form fields
        title = data.get('mainType', '')
        name = data.get('name', '')
        address = data.get('address', '')
        nic = data.get('NIC', '')
        profession = data.get('profession', '')
        mobile_phone = data.get('mobilePhone', '')
        email = data.get('email', '')
        province = data.get('province', '')
        district = data.get('district', '')
        p_radio = data.get('pRadio', '')
        g_radio = data.get('gRadio', '')
        constituency = data.get('constituency', '')
        primary_number = data.get('primaryNumber', '')
        birth_country = data.get('birthCountry', '')
        living_country = data.get('livingCountry', '')
        facebook = data.get('facebook', '')
        twitter = data.get('twitter', '')
        whatsapp = data.get('whatsapp', '')
        
        # Get interests (checkboxes) as a comma-separated string
        interests = ','.join(data.get('interests', []))
        
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # SQL query to insert data
        query = """
        INSERT INTO MemberRegistration (
            Title, Name, Address, NIC, Profession, MobilePhone, Email,
            Province, District, PRadio, GRadio, Constituency, 
            PrimaryNumber, BirthCountry, LivingCountry,
            Facebook, Twitter, Whatsapp, Interests
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Execute the query with parameters
        cursor.execute(query, (
            title, name, address, nic, profession, mobile_phone, email,
            province, district, p_radio, g_radio, constituency,
            primary_number, birth_country, living_country,
            facebook, twitter, whatsapp, interests
        ))
        
        # Commit the transaction
        conn.commit()
        
        # Close the connection
        cursor.close()
        conn.close()
        
        return jsonify({"status": "success", "message": "Form submitted successfully"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Database setup function to create table if it doesn't exist
def setup_database():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if table exists and create if it doesn't
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'MemberRegistration')
        BEGIN
            CREATE TABLE MemberRegistration (
                ID INT IDENTITY(1,1) PRIMARY KEY,
                Title NVARCHAR(50),
                Name NVARCHAR(255) NOT NULL,
                Address NVARCHAR(500) NOT NULL,
                NIC NVARCHAR(50) NOT NULL,
                Profession NVARCHAR(255) NOT NULL,
                MobilePhone NVARCHAR(50) NOT NULL,
                Email NVARCHAR(255),
                Province NVARCHAR(100) NOT NULL,
                District NVARCHAR(100) NOT NULL,
                PRadio NVARCHAR(255),
                GRadio NVARCHAR(255),
                Constituency NVARCHAR(255),
                PrimaryNumber NVARCHAR(50),
                BirthCountry NVARCHAR(100),
                LivingCountry NVARCHAR(100),
                Facebook NVARCHAR(255),
                Twitter NVARCHAR(255),
                Whatsapp NVARCHAR(50),
                Interests NVARCHAR(MAX),
                RegistrationDate DATETIME DEFAULT GETDATE()
            )
        END
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database setup completed successfully.")
    except Exception as e:
        print(f"Database setup error: {str(e)}")

if __name__ == '__main__':
    # Setup the database before running the app
    setup_database()
    
    # Run the Flask app
    app.run(debug=True)
