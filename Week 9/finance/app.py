import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session.get("user_id")
    stocks = db.execute("SELECT * FROM stocks WHERE user_id = ? AND shares > 0;", user_id)
    user = db.execute("SELECT * FROM users WHERE id = ?;", user_id)[0]

    total = user["cash"]

    for stock in stocks:
        quoted = lookup(stock["symbol"])
        stock["name"] = quoted["name"]
        stock["price"] = usd(quoted["price"])
        stock_total = quoted["price"] * stock["shares"]
        stock["total"] = usd(stock_total)
        total += stock_total

    user["total"] = usd(total)
    user["cash"] = usd(user["cash"])
    return render_template("summary.html", stocks=stocks, user=user)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except:
            shares = None
        if (not symbol):
            return apology("must provide symbol", 400)
        if (not shares):
            return apology("must provide shares (Must be an integer bigger than 0))", 400)

        quoted = lookup(symbol)
        if (quoted == None):
            return apology("provided symbol does not exist", 400)

        if (not isinstance(shares, int) or shares < 1):
            return apology("shares must be a positive integer", 400)

        user_id = session.get("user_id")
        user = db.execute("SELECT cash FROM users WHERE id = ?;", user_id)
        cash = user[0]["cash"]
        price = quoted["price"]
        total_price = price * shares
        modified_cash = cash - total_price
        if (modified_cash < 0):
            return apology("cannot afford the number of shares", 400)

        db.execute("UPDATE users SET cash = ? WHERE id = ?;",
                   modified_cash, user_id)
        stockEntry = db.execute(
            "SELECT * FROM stocks WHERE user_id = ? AND symbol = ?;", user_id, symbol.upper())
        if (stockEntry):
            newShares = stockEntry[0].get("shares") + shares
            db.execute("UPDATE stocks SET shares = ? WHERE user_id = ? AND symbol = ?;",
                       newShares, user_id, symbol.upper())
        else:
            db.execute("INSERT INTO stocks (user_id, symbol, shares) VALUES (?,?,?);",
                       user_id, symbol.upper(), shares)
        db.execute("INSERT INTO transactions (operation, user_id, symbol, shares, unitary_price, total_price) VALUES (?,?,?,?,?,?);",
                   "buy", user_id, symbol.upper(), shares, price, total_price)

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    user_id = session.get("user_id")
    history = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY date ASC;", user_id)
    for entry in history:
        entry["unitary_price"] = usd(entry["unitary_price"])
        entry["total_price"] = usd(entry["total_price"])

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if (not symbol):
            return apology("must provide symbol", 400)
        quoted = lookup(symbol)
        if (quoted == None):
            return apology("symbol not found", 400)
        return render_template("quoted.html", quoted=quoted)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if request.method == "POST":
        if (not username):
            return apology("must provide username", 400)
        if (not password):
            return apology("must provide password", 400)
        if (not confirmation):
            return apology("must confirm password", 400)
        if (password != confirmation):
            return apology("password and confirmation must match", 400)

        user = db.execute(
            "SELECT username FROM users WHERE username = ?;", username)

        if (len(user) >= 1):
            return apology("user already registered", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (?,?);",
                   username, generate_password_hash(password))
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except:
            shares = None
        if (not symbol):
            return apology("must provide symbol", 400)
        if (not shares):
            return apology("must provide shares (Must be an integer bigger than 0)", 400)

        quoted = lookup(symbol)
        if (quoted == None):
            return apology("provided symbol does not exist", 400)

        user_id = session.get("user_id")
        user = db.execute("SELECT cash FROM users WHERE id = ?;", user_id)
        cash = user[0]["cash"]
        stockEntry = db.execute(
            "SELECT * FROM stocks WHERE user_id = ? AND symbol = ?;", user_id, symbol.upper())
        if (not stockEntry):
            return apology("user must have stock", 400)

        if (not isinstance(shares, int)):
            return apology("shares must be a positive integer", 400)
        if (shares > stockEntry[0].get("shares")):
            return apology("can't sell more shares than the user has", 400)

        price = quoted["price"]
        total_price = price * shares
        modified_cash = cash + total_price

        db.execute("UPDATE users SET cash = ? WHERE id = ?;",
                   modified_cash, user_id)
        newShares = stockEntry[0].get("shares") - shares
        db.execute("UPDATE stocks SET shares = ? WHERE user_id = ? AND symbol = ?;",
                   newShares, user_id, symbol.upper())
        db.execute("INSERT INTO transactions (operation, user_id, symbol, shares, unitary_price, total_price) VALUES (?,?,?,?,?,?);",
                   "sell", user_id, symbol.upper(), shares, price, total_price)

        return redirect("/")
    else:
        user_id = session.get("user_id")
        stocks = db.execute("SELECT * FROM stocks WHERE user_id = ? AND shares > 0;", user_id)
        return render_template("sell.html", stocks=stocks)


@app.route("/change-password", methods=["POST", "GET"])
@login_required
def change_password():
    """Changes password"""

    if request.method == "POST":
        old_password = request.form.get("old-password")
        new_password = request.form.get("new-password")

        if (not old_password or not new_password):
            return apology("must provide old and new passwords", 400)

        user_id = session.get("user_id")
        user = db.execute("SELECT hash FROM users WHERE id = ?;", user_id)

        if not check_password_hash(user[0]["hash"], request.form.get("old-password")):
            return apology("Old password provided doesn't match", 400)

        db.execute("UPDATE users SET hash = ? WHERE id = ?;",
                   generate_password_hash(new_password), user_id)
        return redirect("/")
    else:
        return render_template("change-password.html")
