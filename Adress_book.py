

#importing packages and modules

from tkinter import *
import sqlite3
import time


#The main window
root = Tk()
root.title("Databases")
root.geometry("400x300")





#create/connect to a database

try : 
	f = open('adress_book.db')
	f.close()
except: 
	cnx = sqlite3.connect('adress_book.db')

	#create a cursor
	cursor = cnx.cursor()

	#create a table (Used only once to create the table)

	cursor.execute(""" CREATE TABLE adresses (
		full_name text,
		phone_number integer,
		adress text,
		city text,
		state integer,
		zip_code integer
		)""")

	#commit changes
	cnx.commit()

	#closing the database
	cnx.close()




#Functions
def clear():
	full_name.delete(0, END)
	phone_number.delete(0, END)
	adress.delete(0, END)
	state_value.set(state_list[0])
	city.delete(0, END)
	zip_code.delete(0, END)

def clear_editor():
	global full_name_editor, phone_number_editor, adress_editor, state_value_editor, zip_code_editor, city_editor
	full_name_editor.delete(0, END)
	phone_number_editor.delete(0, END)
	adress_editor.delete(0, END)
	state_value_editor.set(state_list[0])
	city_editor.delete(0, END)
	zip_code_editor.delete(0, END)	


def submit():
	cnx = sqlite3.connect('adress_book.db')
	cursor = cnx.cursor()

	cursor.execute("INSERT INTO adresses VALUES (:full_name, :phone_number, :adress, :city, :state, :zip_code)",
		{
			'full_name' : full_name.get(), 
			'phone_number' : int(phone_number.get()),
			'adress' : adress.get(), 
			'city' : city.get(), 
			'state' : int(state_value.get()), 
			'zip_code' : int(zip_code.get())
		})

	cnx.commit()
	cnx.close()

	clear()


def records_query():
	global records
	cnx = sqlite3.connect('adress_book.db')
	cursor = cnx.cursor()

	cursor.execute("SELECT *, oid FROM adresses")
	records = cursor.fetchall()

	show_records(records)

	cnx.commit()
	cnx.close()


def show_records(records):
	global oids_and_checkboxes, window
	window = Toplevel()
	window.title("Records")
	pad=10
	fg_color = 'brown'
	Label(window, text="FULL NAME", fg=fg_color).grid(row=0, column=0, sticky=W, padx=pad)
	Label(window, text="PHONE NUMBER", fg=fg_color).grid(row=0, column=1, sticky=W, padx=pad)
	Label(window, text="ADRESS", fg=fg_color).grid(row=0, column=2, sticky=W, padx=pad)
	Label(window, text="CITY", fg=fg_color).grid(row=0, column=3, sticky=W, padx=pad)
	Label(window, text="STATE", fg=fg_color).grid(row=0, column=4, sticky=W, padx=pad)
	Label(window, text="ZIP CODE", fg=fg_color).grid(row=0, column=5, sticky=W, padx=pad)

	oids_and_checkboxes = []

	for j in range(len(records)):
		oids_and_checkboxes.append( [records[j][6], IntVar() ] )
		for i in range(7):
			Label(window, text=records[j][i] ).grid(row=j+1, column=i, sticky=W, padx=pad)
		Checkbutton(window, variable=oids_and_checkboxes[j][1]).grid(row=j+1, column=7, sticky=W, padx=pad)

	#Delete button
	delete_btn = Button(window, text="delete", command=delete_records)
	delete_btn.grid()

	#Edit button
	edit_btn = Button(window, text="edit", command=edit_records)
	edit_btn.grid()





def delete_records():
	global oids_and_checkboxes, window
	to_delete = [ oid[0] for oid in oids_and_checkboxes if oid[1].get() != 0 ]

	cnx = sqlite3.connect('adress_book.db')
	cursor = cnx.cursor()

	for oid_num in to_delete:
		cursor.execute("DELETE FROM adresses WHERE oid = " + str(oid_num))

	cnx.commit()
	cnx.close()	

	window.destroy()
	records_query()


	
def edit_records():
	global oids_and_checkboxes, window, edit_window, to_edit
	to_edit = [k for k in range(len(oids_and_checkboxes)) if oids_and_checkboxes[k][1].get() != 0 ]
	if to_edit== []: return 0
	elem = oids_and_checkboxes[to_edit[0]][0]
	edit_window = Toplevel()
	edit_window.title("record editor")
	edit_window.grid()
	editor_screen(edit_window, elem, to_edit[0])



def editor_screen(root, elem, k):
	global full_name_editor, phone_number_editor, adress_editor, state_editor, zip_code_editor, city_editor, to_edit, edit_window
	cnx = sqlite3.connect("adress_book.db")
	cursor = cnx.cursor()
	elem = str(elem)
	cursor.execute("SELECT * FROM adresses WHERE oid= " + elem )
	records = cursor.fetchall()
	record = records[0]
	cnx.commit()
	cnx.close()


	full_name_lbl_editor = Label(root, text="Full Name")
	full_name_editor = Entry(root, width=30)
	full_name_editor.insert(0, record[0])
	full_name_lbl_editor.grid(row=0, column=0, padx = 5, sticky=W)
	full_name_editor.grid(row=1, column=0, padx = 5, sticky=W)

	phone_number_lbl_editor = Label(root, text="Phone number")
	phone_number_editor = Entry(root, width=30)
	phone_number_editor.insert(0, record[1])
	phone_number_lbl_editor.grid(row=0, column=1, columnspan=2, padx = 5, sticky=W)
	phone_number_editor.grid(row=1, column=1,columnspan=2, padx = 5, sticky=W)

	adress_lbl_editor = Label(root, text="Adress")
	adress_editor = Entry(root, width=30)
	adress_editor.insert(0, record[2])
	adress_lbl_editor.grid(row=2, column=0, padx = 5, sticky=W)
	adress_editor.grid(row=3, column=0, padx = 5, sticky=W)

	city_lbl_editor = Label(root, text="city")
	city_editor = Entry(root, width=20)
	city_editor.insert(0, record[3])
	city_lbl_editor.grid(row=2, column=1, padx = 5, sticky=W)
	city_editor.grid(row=3, column=1, padx = 5, sticky=W)

	state_lbl_editor = Label(root, text="state")
	state_editor= Entry(root)
	state_editor.insert(0, record[4])
	state_lbl_editor.grid(row=2, column=2, padx = 5, sticky=W)
	state_editor.grid(row=3, column=2, padx = 5, sticky=W)

	zip_code_lbl_editor = Label(root, text="Zip code")
	zip_code_editor = Entry(root, width=10)
	zip_code_editor.insert(0, record[5])
	zip_code_lbl_editor.grid(row=4, column=0, columnspan=2, sticky=E+W)
	zip_code_editor.grid(row=5, column=0, columnspan=2, sticky=W, padx=135)


	#create save button
	save_btn_editor = Button(root, text="save", command= lambda: save(elem, k), bg="yellow", width=20, pady=10)
	save_btn_editor.grid(row=6, column=0, columnspan = 3, pady=15, sticky=S+N)

	#create clear button
	clear_btn_editor = Button(root, text="clear", command=clear_editor, bg="pink", width=20)
	clear_btn_editor.grid(row=7, column=0, columnspan = 3, sticky=S+N)



def save(oid, k):
	global window, full_name_editor, phone_number_editor, adress_editor, state_editor, zip_code_editor, city_editor, to_edit, edit_window, oids_and_checkboxes
	cnx = sqlite3.connect("adress_book.db")
	cursor = cnx.cursor()

	cursor.execute("""UPDATE adresses SET
		full_name = :full_name,
		phone_number = :phone_number ,
		adress = :adress,
		city = :city,
		state = :state,
		zip_code = :zip_code


		WHERE oid = :oid """, 
		{'full_name': full_name_editor.get(),
		'phone_number': phone_number_editor.get(),
		'adress': adress_editor.get(),
		'city': city_editor.get(),
		'state': state_editor.get(),
		'zip_code': zip_code_editor.get(),
		'oid': oid

		})



	cnx.commit()
	cnx.close()
	oids_and_checkboxes[k][1].set(0) 
	edit_window.destroy()
	to_edit.pop(0)
	try: 
		window.destroy() 
		edit_records()
		records_query()
	except: 
		window.destroy()
		records_query()


#create text boxes
full_name_lbl = Label(root, text="Full Name")
full_name = Entry(root, width=30)
full_name_lbl.grid(row=0, column=0, padx = 5, sticky=W)
full_name.grid(row=1, column=0, padx = 5, sticky=W)

phone_number_lbl = Label(root, text="Phone number")
phone_number = Entry(root, width=30)
phone_number_lbl.grid(row=0, column=1, columnspan=2, padx = 5, sticky=W)
phone_number.grid(row=1, column=1,columnspan=2, padx = 5, sticky=W)

adress_lbl = Label(root, text="Adress")
adress = Entry(root, width=30)
adress_lbl.grid(row=2, column=0, padx = 5, sticky=W)
adress.grid(row=3, column=0, padx = 5, sticky=W)

city_lbl = Label(root, text="city")
city = Entry(root, width=20)
city_lbl.grid(row=2, column=1, padx = 5, sticky=W)
city.grid(row=3, column=1, padx = 5, sticky=W)

state_list = [i for i in range(1, 49)]
state_value = IntVar()
state_value.set(state_list[0])
state_lbl = Label(root, text="state")
state = OptionMenu(root,state_value, *state_list)
state_lbl.grid(row=2, column=2, padx = 5, sticky=W)
state.grid(row=3, column=2, padx = 5, sticky=W)

zip_code_lbl = Label(root, text="Zip code")
zip_code = Entry(root, width=10)
zip_code_lbl.grid(row=4, column=0, columnspan=2, sticky=E+W)
zip_code.grid(row=5, column=0, columnspan=2, sticky=W, padx=135)


#create submit button
submit_btn = Button(root, text="Submit", command=submit, bg="yellow", width=20, pady=10)
submit_btn.grid(row=6, column=0, columnspan = 3, pady=15, sticky=S+N)

#create clear button
clear_btn = Button(root, text="clear", command=clear, bg="pink", width=20)
clear_btn.grid(row=7, column=0, columnspan = 3, sticky=S+N)

#create show_rcords button
show_records_btn = Button(root, text="Show records", command=records_query, anchor=S)
show_records_btn.grid(columnspan = 3, sticky=S, pady=10)




time.sleep(1)
root.mainloop()