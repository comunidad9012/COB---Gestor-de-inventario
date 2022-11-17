from tkinter import ttk
from tkinter import *
import sqlite3


class Product:
    db_name='D:\Python\product-desktop\database.db'
    def __init__(self,window):
        self.wind = window
        self.wind.title('Products Application')
        # self.wind.geometry('420x320')
        
        
        #User a Frame Container
        user_frame = LabelFrame(self.wind,text='Login')
        user_frame.grid(row=1,column=0,columnspan=3,pady=20)

        #User Frame
        Label(user_frame,text='User: ').grid(row = 0, column=0)
        self.user = Entry(user_frame)
        self.user.focus()
        self.user.grid(row=0,column=1)

        #Password Frame
        Label(user_frame,text='Password: ').grid(row=1,column=0)
        self.passw = Entry(user_frame)
        self.passw.grid(row=1,column=1)

        #Login Button
        ttk.Button(user_frame,text='Login',command=self.login).grid(row=3,columnspan=2,sticky=W+E)

        #Register Button
        ttk.Button(user_frame,text='Register',command=self.register).grid(row=4,columnspan=2,sticky=W+E)
        
        # #Output Messages
        self.message = Label(text='',fg='red')
        self.message.grid(row=3,column=0,columnspan=2,sticky= W + E )


    def run_query(self,query,parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query,parameters)
            conn.commit()
        return result

    def get_products(self):
        #Cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #Quering data
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
  
        #Filling Data
        for row in db_rows:
            self.tree.insert('',0,text=row[1],values = row[2])
    def validation(self):
        return len(self.name.get()) !=0 and int(self.price.get()) !=0
    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters = (self.name.get(),self.price.get())
            self.run_query(query,parameters)
            self.message['text'] = 'Product {} added Successfully'.format(self.name.get())
            self.message['text']=''
            
            self.name.delete(0,END)
            self.price.delete(0,END)
            
        else:
            self.message['text'] = 'Name and Price are Required'
        query2= 'SELECT name FROM product ORDER BY name DESC'
        prods_name=self.run_query(query2)
        prod_query=self.name.get()
        for name in prods_name:
            if name == prod_query:
                print(name)
        self.get_products()
    def delete_product(self):
        print(self.tree.selection())
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please Select a Record'
            return
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query,(name,))
        self.message['text'] = 'Record {} deleted successfully'.format(name)
        self.get_products()
    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please Select a Record'
            self.message.grid(row=3,column=0,columnspan=2,sticky= W + E )
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price= self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title('Edit Product')
        #Old Name
        Label(self.edit_wind,text='Old Name: ').grid(row=0,column=1)
        Entry(self.edit_wind,textvariable=StringVar(self.edit_wind,value=name),state='readonly').grid(row=0,column=2)
        #New Name
        Label(self.edit_wind,text='New Name: ').grid(row=1,column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1,column=2)
        #Old Price
        Label(self.edit_wind,text='Old Price').grid(row=2, column=1)
        Entry(self.edit_wind,textvariable=StringVar(self.edit_wind,value=old_price),state='readonly').grid(row=2,column=2)
        #New Price
        Label(self.edit_wind,text='New Price: ').grid(row=3,column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3, column=2)
        #Button
        Button(self.edit_wind,text='Update',command= lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row=4,column = 2,sticky = W)
        
        #Register 
    def register(self):
        #Register Frame
        self.register_wind = Toplevel()
        self.register_wind.title('Register Panel')

        if self.validate_register():
            query = 'INSERT INTO account VALUES(NULL, ?, ?)'
            parameters = (self.user.get(),self.passw.get())
            self.run_query(query,parameters)
            self.message['text'] = 'User {} added Successfully'.format(self.user.get())
            self.user.delete(0,END)
            self.passw.delete(0,END)
        

        #User Frame
        Label(self.register_wind,text='User: ').grid(row = 0, column=0)
        self.user = Entry(self.register_wind)
        self.user.focus()
        self.user.grid(row=0,column=1)

        #Password Frame
        Label(self.register_wind,text='Password: ').grid(row=1,column=0)
        self.passw = Entry(self.register_wind)
        self.passw.grid(row=1,column=1)
        
        #Register Button
        ttk.Button(self.register_wind,text='Send',command= lambda: self.register_user(self.user.get(),self.passw.get())).grid(row=2,columnspan=2,sticky=W+E)
    def login(self):
        query = 'SELECT user, passw FROM account ORDER BY user DESC'
        db_rows = self.run_query(query)
        user= self.user.get()
        passw = self.passw.get()
        for name in db_rows:
            if name[0] == user and name[1] == passw:
                self.wind=Toplevel()
                self.message['text']='Access granted!'
                # #Creating a Frame Container
                frame =LabelFrame(self.wind,text='Register A new Product')
                frame.grid(row=0,column=0,columnspan=3,pady=20)

                #Name Input
                Label(frame,text='Name: ').grid(row = 1,column=0)
                self.name = Entry(frame)
                self.name.focus()
                self.name.grid(row=1,column=1)

                # #Price Input
                Label(frame,text='Price: ').grid(row=2,column=0)
                self.price =Entry(frame)
                self.price.grid(row=2,column=1)

                #Button Add Product
                ttk.Button(frame,text='Save Product',command=self.add_product).grid(row=3,columnspan=2,sticky=W + E)
                
                # #Table
                self.tree =ttk.Treeview(frame,height=10,columns=2)
                self.tree.grid(row=4,column=0,columnspan=2)
                self.tree.heading('#0',text='Name', anchor=CENTER)
                self.tree.heading('#1',text='Price',anchor=CENTER)

                # #Buttons
                ttk.Button(frame,text='DELETE',command=self.delete_product).grid(row=5,column=0,sticky= W+ E)
                ttk.Button(frame,text='EDIT',command=self.edit_product).grid(row=5,column=1,sticky= W+ E)
                # #Filling the Box
                self.get_products()
            elif name[0] != user and name[1] != passw:
                self.message['text']='User and Password is Required'
            
    
    def register_user(self,user,passw):
        
        if self.validate_register():
            query = 'INSERT INTO account VALUES(NULL, ?, ?)'
            parameters = (user,passw)
            self.run_query(query,parameters)
            # db_rows = self.run_query(query)
            # user= self.user.get()
            # for name in db_rows:
            #     if user == name[0]:
            #         print(name)
            self.register_wind.destroy()
        else:
            self.message['text'] = 'All parameters are required'
        
        pass

    #     prod_query=self.name.get()
    #     for name in prods_name:
    #         if name == prod_query:
    #             print(name)
    
    
    def validate_login(self):
        return len(self.user.get()) !=0 and len(self.passw.get()) !=0
    def validate_register(self):
        return len(self.user.get()) !=0 and len(self.passw.get()) !=0
    def edit_records(self,new_name,name,new_price,old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price)
        
        if len(new_name) !=0 and len(new_price)!=0:
            self.message['text'] = 'Record {} updated Sucessfully'.format(name)
            self.run_query(query,parameters)
            self.edit_wind.destroy()
            self.get_products()
        else:
            self.message['text']= "Name and Price are Required"
if __name__ == '__main__':
    window = Tk()
    Product(window)
    application=Product(window)
    window.mainloop()