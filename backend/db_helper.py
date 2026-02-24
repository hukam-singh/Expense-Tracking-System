# talk to database, Retrietve record, update it. 
# Create Retrietve Update Delete (CRUD)

import mysql.connector
from contextlib import contextmanager
from .logging_setup import setup_logger

logger = setup_logger("db_helper")


@contextmanager
def get_db_cursor(commit = False):
    connection = mysql.connector.connect(
        host = "127.0.0.1",
        user = "root",
        password = "password",
        database ="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()



def fetch_expense_for_date(expense_date):
    logger.info(f"fetch_expense_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses

# function to insert the expense
def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date : {expense_date}, amount : {amount},category : {category},notes : {notes}")
    with get_db_cursor(commit =True) as cursor:
        cursor.execute("INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s,%s,%s,%s)",(expense_date, amount, category, notes) )


def delete_expense_for_date(expense_date):
    logger.info(f"delete_expense_for_date called with {expense_date}")
    with get_db_cursor(commit =True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start : {start_date}, end : {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute('''  SELECT category, SUM(amount) as total
                            FROM expenses 
                            WHERE expense_date  
                            BETWEEN  %s and %s 
                            GROUP BY category;   ''', 
                            (start_date, end_date) )   
        data = cursor.fetchall()
        return data

def fetch_expense_by_month():
    logger.info(f"fetch_expense_by_month called")
    with get_db_cursor() as cursor:
        cursor.execute('''
                        SELECT 
                        MONTH(expense_date) AS month_num,
                        MONTHNAME(expense_date) AS month,
                        SUM(amount) AS total_expense
                        FROM expenses
                        GROUP BY MONTH(expense_date), MONTHNAME(expense_date)
                        ORDER BY month_num; ''')
        data = cursor.fetchall()
        return data
    
    

        
if __name__=="__main__":
    # Testing function
    # print(fetch_expense_by_month())
    pass
