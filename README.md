Smart Banking is a web-based banking application developed using Python and Flask.
It allows users to securely create an account, log in using OTP verification, and perform basic banking operations online.

A).Project Features / Uses

  1)User Registration :->
  
   Users can register using name, email, mobile number, and password
   
   A unique bank account number is automatically generated

   <img width="1844" height="865" alt="Screenshot 2026-01-22 170929" src="https://github.com/user-attachments/assets/ad753a70-55c6-46ed-992b-b4fe81876dc9" />

<img width="1842" height="863" alt="Screenshot 2026-01-22 171026" src="https://github.com/user-attachments/assets/ce7290eb-caa7-4f49-bf79-fe241388f429" />


2).Login with OTP Verification :->

   Users log in using account number and mobile number
   
   OTP (One Time Password) is generated for secure authentication

   <img width="1841" height="870" alt="Screenshot 2026-01-22 171039" src="https://github.com/user-attachments/assets/3dd4525f-9301-4eec-b7fb-af5a4aa9f046" />

<img width="1858" height="864" alt="Screenshot 2026-01-22 171053" src="https://github.com/user-attachments/assets/caa06324-76e9-4d92-882b-f8b5e8ccaf2d" />

  
3).Dashboard :->

  Displays user’s name and current account balance
  
  Accessible only after successful login

  <img width="1774" height="848" alt="Screenshot 2026-01-22 171115" src="https://github.com/user-attachments/assets/8f303e01-2a87-4555-81c6-1bf85b6dd323" />


  

4).Deposit Money :->

   Users can deposit money into their account
   
   Deposit transactions are stored in the database

<img width="1825" height="863" alt="Screenshot 2026-01-22 171132" src="https://github.com/user-attachments/assets/b963cdaa-6e83-4ea6-85ec-85e35e2ff65f" />


5).Withdraw Money :->

   Users can withdraw money from their account

   System checks for sufficient balance before withdrawal

<img width="1847" height="867" alt="Screenshot 2026-01-22 171217" src="https://github.com/user-attachments/assets/5609253c-2db2-402c-8d3f-fd4a7bbe427f" />

   
6).Money Transfer :->

   Users can transfer money from their account to another account

   Sender and receiver balances are updated automatically

   <img width="1829" height="855" alt="Screenshot 2026-01-22 171146" src="https://github.com/user-attachments/assets/86723914-079a-45bb-b931-cfffc778133a" />


7).Transaction History::->

  Users can view all transactions such as deposit, withdrawal, and transfers

  Transactions are displayed in descending order by date

  <img width="1825" height="867" alt="Screenshot 2026-01-22 171159" src="https://github.com/user-attachments/assets/969e961b-aee6-4a80-a0e5-2bb2e0241c4c" />


8).Logout :->

  Users can safely log out and end their session

9).Terms & Conditions Page :->

  Displays banking rules and terms for users

  


B).Technologies / Languages Used

1️).Python :->

Core backend programming language

Handles business logic, OTP generation, and account number creation

Manages database operations and validations

2️).Flask (Python Web Framework) :->

Used to build the web application

Handles routing, requests, responses, and session management

Connects backend logic with frontend templates

3️).MySQL (SQL) :->

Used as the database system

Stores user details, account information, and transaction records

Executes CRUD operations (Create, Read, Update)

4️). HTML :->

Used to design the structure of web pages

Forms for registration, login, deposit, withdrawal, and transfer.

5️).CSS :->

Used for styling the web pages

Improves user interface with colors, layouts, and designs

C).How to Run the Smart Banking Project 

Step 1: Open the Project Folder

Open the folder where your project files are saved (app.py, dp.py, utils.py).

Open Command Prompt / Terminal inside that folder.

Step 2: Check Python Installation

python --version

Step 3: Install Required Packages

pip install flask mysql-connector-python

Step 4: Start MySQL Server

Make sure MySQL server is running

Database and tables should already be created

Step 5: Run the Flask Application

python app.py

You should see something like: Running on http://127.0.0.1:5000/

Step 6: Open Browser

Open any browser (Chrome, Edge, etc.)

Go to:
http://127.0.0.1:5000/

Step 7: Use the Application

Register a new account

Login using account number + mobile

Enter OTP

Use dashboard, deposit, withdraw, transfer, transactions

That’s it! Your Smart Banking project is now running successfully.

