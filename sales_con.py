import mysql.connector
import streamlit as st


conn = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user="root",
    passwd="1234@864m",
    db="my_project"
)

c=conn.cursor()

def view_all_data():
    c.execute("select * from SalesForCourse_quizz_table")
    data=c.fetchall()
    return data
