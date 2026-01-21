from flask import Flask, render_template, request, redirect
from dp import get_connection
from utils import generate_otp
from utils import generate_account_no
from flask import session

app = Flask(__name__)
app.secret_key = "bank_secret"

# Home page 
@app.route("/")
def home():
    return redirect("/register")

# Registration page
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("Username")
        email = request.form["email"]
        password = request.form["password"]
        mobile = request.form["mobile"].strip()

        con = get_connection()
        cur = con.cursor(dictionary=True)

        # Check if email already exists
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing_user = cur.fetchone()
        if existing_user:
            con.close()
            return "Email already registered! Please login."

        # NEW USER INSERT
        cur.execute(
            "INSERT INTO users (name,email,password,mobile) VALUES (%s,%s,%s,%s)",
            (name,email,password,mobile)
        )
        user_id = cur.lastrowid  # user_id मिळाला

        # ✅ ACCOUNT NUMBER GENERATE इथे
        account_no = generate_account_no()
        print("Generated account number:", account_no)


        # ✅ ACCOUNT TABLE मध्ये INSERT (account_no सहित)
        cur.execute(
            "INSERT INTO accounts (user_id, account_no, balance) VALUES (%s, %s, %s)",
            (user_id, account_no, 0)
        )

        con.commit()
        con.close()

        # 👉 account number user ला दाखवण्यासाठी success page
        return render_template(
            "account_created.html",
            name=name,
            account_no=account_no
        )

    return render_template("register.html")


# Login page (temporary placeholder for now)

# Login Page


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        account_no = request.form["account_no"].strip()
        mobile = request.form["mobile"].strip()

        print("ENTERED ACCOUNT NO:", account_no)
        print("ENTERED MOBILE:", mobile)

        con = get_connection()
        cur = con.cursor(dictionary=True)

        # ✅ FINAL & CORRECT QUERY
        cur.execute("""
            SELECT u.user_id, u.name
            FROM accounts a
            JOIN users u ON a.user_id = u.user_id
            WHERE a.account_no = %s
              AND TRIM(u.mobile) = %s
        """, (account_no, mobile))

        user = cur.fetchone()
        con.close()

        print("USER FETCHED:", user)

        if not user:
            return "Account number and mobile not matching"

        otp = generate_otp()
        session["login_otp"] = otp
        session["tmp_user_id"] = user["user_id"]
        session["user_name"] = user["name"]

        print("LOGIN OTP:", otp)

        return redirect("/verify_otp")

    return render_template("login.html")



@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        user_id = session["user_id"]
        con = get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT balance FROM accounts WHERE user_id=%s", (user_id,))
        account = cur.fetchone()
        balance = account["balance"]
        con.close()
        return render_template("dashboard.html", name=session["user_name"], balance=balance)
    else:
        return redirect("/login")
    

 # Example for deposit
@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    if request.method == "POST":
        amount = float(request.form["amount"])

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "UPDATE accounts SET balance = balance + %s WHERE user_id = %s",
            (amount, user_id)
        )

        cur.execute(
            "INSERT INTO transactions (from_account, to_account, amount, txn_type) "
            "VALUES (%s, %s, %s, 'Deposit')",
            (None, user_id, amount)
        )

        con.commit()
        con.close()

        return redirect("/dashboard")

    # GET request
    return render_template("deposit.html")


@app.route("/transfer", methods=["GET","POST"])
def transfer():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        to_account = int(request.form["to_account"])
        amount = float(request.form["amount"])
        from_account = session["user_id"]

        con = get_connection()
        cur = con.cursor(dictionary=True)

        cur.execute("SELECT balance FROM accounts WHERE user_id=%s", (from_account,))
        sender = cur.fetchone()

        if sender["balance"] < amount:
            con.close()
            return "Insufficient Balance!"

        cur.execute("UPDATE accounts SET balance = balance - %s WHERE user_id=%s", (amount, from_account))
        cur.execute("UPDATE accounts SET balance = balance + %s WHERE user_id=%s", (amount, to_account))
        cur.execute(
            "INSERT INTO transactions (from_account, to_account, amount, txn_type) VALUES (%s,%s,%s,'Transfer')",
            (from_account, to_account, amount)
        )

        con.commit()
        con.close()
        return redirect("/dashboard")

    # 🔥 THIS IS THE FIX
    return render_template("transfer.html")

@app.route("/transactions")
def transactions():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    con = get_connection()
    cur = con.cursor(dictionary=True)


    cur.execute("""
        SELECT * FROM transactions
        WHERE from_account=%s OR to_account=%s 
        ORDER BY txn_date DESC
    """, (user_id, user_id))

    txns = cur.fetchall()
    con.close()

    # THIS IS THE KEY LINE
    return render_template("transactions.html", txns=txns)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/verify_otp", methods=["GET", "POST"])
def verify_otp():
    if request.method == "POST":
        user_otp = int(request.form["otp"])

        if user_otp == session.get("login_otp"):
            session["user_id"] = session["tmp_user_id"]

            # cleanup
            session.pop("login_otp", None)
            session.pop("tmp_user_id", None)

            return redirect("/dashboard")
        else:
            return "Invalid OTP"
    return render_template(
        "verify_otp.html",
        otp=session.get("login_otp")
    )


@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]   # ✅ FIX 1

    error = None
    success = None

    con = get_connection()
    cur = con.cursor(dictionary=True)

    # 🔹 user account info
    cur.execute("""
        SELECT account_id, account_no, balance
        FROM accounts
        WHERE user_id=%s
    """, (user_id,))

    account = cur.fetchone()

    if not account:                # ✅ FIX 2
        con.close()
        return "Account not found"

    account_id = account["account_id"]
    balance = account["balance"]

    if request.method == "POST":
        try:                        # ✅ FIX 3
            amount = float(request.form["amount"])
        except:
            error = "Invalid amount format"
        else:
            if amount <= 0:
                error = "Invalid amount"

            elif amount > balance:
                error = "Insufficient balance"

            else:
                # 🔹 update balance
                cur.execute(
                    "UPDATE accounts SET balance = balance - %s WHERE account_id = %s",
                    (amount, account_id)
                )

                # 🔹 insert transaction
                cur.execute("""
                    INSERT INTO transactions
                    (from_account, to_account, amount, txn_type)
                    VALUES (%s, %s, %s, %s)
                """, (account_id, None, amount, "withdraw"))

                con.commit()
                success = "Amount withdrawn successfully"

    con.close()
    return render_template(
        "withdraw.html",
        balance=balance,
        error=error,
        success=success
    )

@app.route("/terms")
def terms():
    return render_template("terms.html")





if __name__ == "__main__":
    app.run(debug=True)
