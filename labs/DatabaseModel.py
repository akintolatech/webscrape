import sqlite3

def Update_Single_Client_Field(update_info):

    # Extract the filtering keys and the field to update
    fname = update_info.get("First Name")
    lname = update_info.get("Last Name")
    country = update_info.get("Country")
    value = update_info.get("Status")

    try:
        # Connect to the database
        conn = sqlite3.connect('clients.db')
        cursor = conn.cursor()

        # Create the SQL UPDATE statement
        sql = f"""UPDATE users SET Status = ? WHERE "first_name" = ? AND "last_name" = ? AND "country" = ?"""

        # Execute the update
        cursor.execute(sql, (value, fname, lname, country))

        # Commit the changes and close the connection
        conn.commit()
        return cursor.rowcount > 0  # Return True if at least one row was updated
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        if conn:
            conn.close()

def Create_Database():
    #Create the database clients.db if not created and make a table of users
    conn = sqlite3.connect("clients.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        gender TEXT NOT NULL,
                        date_of_birth TEXT NOT NULL,
                        nationality TEXT NOT NULL,
                        migris TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone_code TEXT NOT NULL,
                        phone_number TEXT NOT NULL,
                        passport TEXT NOT NULL,
                        passport_expiry_date TEXT NOT NULL,
                        country TEXT NOT NULL,
                        status TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

def Insert_Data(data : list):
    #Insert data into the databaser
    conn = sqlite3.connect("clients.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (first_name, last_name, gender, date_of_birth, nationality, migris, email, phone_code, phone_number, passport, passport_expiry_date, country, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12]))
    conn.commit()
    conn.close()

def Get_Treeview_Selection_Values(tree, messagebox, country_code):

    data = {}
    selected_item = tree.selection()  # Get the selected item from the Treeview

    if not selected_item:
        messagebox.showwarning("NO SELECTION", "Please select atleast 1 client to start Booking!.")
        return

    # Get the value (ID) of the selected item (assuming the ID is in the first column)
    item_values = tree.item(selected_item, 'values')
    fname = item_values[0]
    lname = item_values[1]

    # Delete the selected record from the database
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()

    # Assuming the table has a primary key column named 'id'
    cursor.execute("SELECT * FROM users WHERE first_name = ? AND last_name = ? AND country = ?", (fname,lname, country_code))
    data_list = cursor.fetchall()
    if len(data_list) > 0:
        data_list = data_list[0]
        data['First Name'] = data_list[1]
        data['Last Name'] = data_list[2]
        data['Gender'] = data_list[3]
        data['DOB'] = data_list[4]
        data['Nationality'] = data_list[5]
        data['Migris'] = data_list[6]
        data['Email'] = data_list[7]
        data['Ph. Code'] = data_list[8]
        data['Phone'] = data_list[9]
        data['Passport Num'] = data_list[10]
        data['Passport Expiry'] = data_list[11]
        data['Country'] = data_list[12]
        data['Status'] = data_list[13]

    conn.close()
    return data

def Update_Treeview(tree, country_code):
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()

    # Query to fetch all rows from a table (assuming a table named 'clients')
    cursor.execute(f"SELECT * FROM users where country='{country_code}'")
    rows = cursor.fetchall()
    '''
    data = {'First Name': 'KUDZAI', 'Last Name': 'MANHONGO', 'Gender': 'Male', 'DOB': '08/08/1987', 'Nationality': 'PAKISTAN', 'Migris': '2408-LLG-2408', 'Email': 'as28257400@gmail.com', 'Ph. Code': '92', 'Phone': '3161333533', 'Passport Num': 'AE613386', 'Passport Expiry': '05/06/2033', 'Country': 'South Africa', 'Status': 'HEGW'}
    '''
    # Clear the Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Insert new data into the Treeview
    if len(rows) > 0:
        for row in rows:
            tree.insert('', 'end', values=(row[1], row[2], row[-1]))

    # Close the database connection
    conn.close()

def Delete_Selected(tree,messagebox, country):
    selected_item = tree.selection()  # Get the selected item from the Treeview

    if not selected_item:
        messagebox.showwarning("NO SELECTION", "Please select an item to delete.")
        return

    # Get the value (ID) of the selected item (assuming the ID is in the first column)
    item_values = tree.item(selected_item, 'values')
    fname = item_values[0]
    lname = item_values[1]

    # Confirm deletion
    confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this record?")
    if not confirm:
        return

    # Delete the selected record from the database
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()

    # Assuming the table has a primary key column named 'id'
    cursor.execute("DELETE FROM users WHERE first_name = ? AND last_name = ? AND country = ?", (fname,lname, country))
    conn.commit()
    conn.close()

    # Remove the selected item from the Treeview
    tree.delete(selected_item)