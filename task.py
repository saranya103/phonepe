# Importing the required libraries
import pandas as pd
import streamlit as st
import base64

# creating Home Page
st.title(':violet[Expense Management App]')

df = pd.read_excel('user_data.xlsx')

# Function to on-boarding the users
def add_user(First_Name, Last_Name, DOB, group, contact, address,Boarding_date,vacation_date):
    users_df = pd.DataFrame({'First_Name': [First_Name], 'Last_Name': [Last_Name], 'DOB': DOB, 'Group': [group], 'Contact': [contact], 'Address': [address],'Boarding_Date':[Boarding_date],'Vacate_Date':[vacation_date]})
    user_input_df = users_df.reindex(columns=df.columns)

    # Merge the user input DataFrame with the existing data
    updated_data = pd.concat([df, user_input_df], ignore_index=True)

    # Save the updated data to the Excel sheet
    updated_data.to_excel('user_data.xlsx',index=False)

# Function to create or modify a group
def create_modify_group(group):
    cell_value = df.loc[Token_Number, 'Group']
    st.write('Existed group :',cell_value)
    if group in cell_value:
        df.at[Token_Number, 'Group']=group
        st.write(f"Modifying Group: {group}")
        df.to_excel('user_data.xlsx',index=False)
        st.success("Group modified successfully!")
    else:
        df.at[Token_Number, 'Group'] = group
        st.write(f"Creating Group: {group}")
        df.to_excel('user_data.xlsx', index=False)
        st.success("Group created successfully!")
    #st.write(df)
# Function to add a new expense
# Create an empty DataFrame to store expenses
expenses_df = pd.DataFrame(columns=['Token Number', 'Description', 'Amount', 'Date', 'Paid by', 'Receipt', 'Tagged Members'])
df1 = pd.read_excel('spends_data.xlsx')
#st.write(df1['Tagged Members'])
def add_expense(Number,description, amount, date, paid_by, receipt, tagged_members):
    expenses_df = pd.DataFrame({'Token Number':Number,'Description': description,'Amount': amount,'Date':date,'Paid by': paid_by,'Receipt': receipt,'Tagged Members':[tagged_members]})
    # Merge the user input DataFrame with the existing data
    updated_data = pd.concat([df1, expenses_df], ignore_index=True)
    # Save the updated data to the Excel sheet
    updated_data.to_excel('spends_data.xlsx', index=False)

    #st.dataframe(df1)

# Function to close the group
def close_group():
    data=df1[df1['Token Number'].isin([Number])]
    # Calculate total expenses for each friend
    friend_expenses = data.groupby('Paid by')['Amount'].sum()
    col1,col2=st.columns(2)
    with col1:
        st.write('friend_expenses : ',friend_expenses)
        # Calculate the equal share for each friend
        equal_share = friend_expenses.mean()
        st.write('Share of each person in tag list :',equal_share)
    with col2:
        #Calculate the difference for each friend to settle
        friend_expenses -= equal_share
        st.write('Settlement to each person :',friend_expenses)
    st.write(":green[Group closed. Expenses have been split equally and reconciled.]")

# Menu selection
menu = st.sidebar.radio(":violet[Select Options]", ["Home","Register-Confirmation", "Create/Modify Group","Add Expense", "Display Expenses Summary", "Close Group"],horizontal=False)

#-----------------------------------------------------------------------------------Home Section -----------------------------------------------------------------------------------------
if menu == "Home":
    st.subheader(":blue[Welcome To User Onboarding]")
    col1,col2=st.columns(2)
    with col1:
        f_name = st.text_input(":violet[Enter First Name]")
        l_name=st.text_input(":violet[Enter Last Name]")
        group = st.text_input(":violet[Group Member Names]")
        onboard_dt=st.date_input(":violet[Select Boarding Date]").strftime("%Y-%m-%d")
    with col2:
       dob = st.date_input(':violet[Select Date-Of-Birth]').strftime("%Y-%m-%d")
       contact = st.text_input(':violet[Enter Contact Number (Must Have 10 Digits)]')
       if contact and len(contact) < 10 or len(contact) > 10 :
           raise Exception("Error in contact details")
       else:
           contact = contact
       address = st.text_input(':violet[Enter the Address details]')
       vacation_dt = st.date_input(":violet[Select Vacate Date]").strftime("%Y-%m-%d")
    if st.button("Book"):
        add_user(f_name, l_name,dob, group, contact, address,onboard_dt,vacation_dt)
        st.write("### :green[Your Token Number is]", len(df))
        st.success("User signed up successfully!")


# ------------------------------------------------------------- Registration confirmation ------------------------------------------------------------------
elif menu == "Register-Confirmation":
    st.subheader(':blue[Check Your Registered Details]')
    number=st.text_input(':violet[Enter Your Token Number]')
    if number:
        number = int(number)
    if st.button('Get Details'):
        st.dataframe(df.iloc[number,:])

#--------------------------------------------------------------- Add Expenses section------------------------------------------------------------------

elif menu == "Create/Modify Group":
        st.subheader(":blue[Create/Modify Group]")
        Number = st.text_input(':violet[Enter the Token Number]')
        if Number:
            Token_Number = int(Number)
        group = st.text_input("Group")
        if st.button("Create/Modify"):
            create_modify_group(group)

#------------------------------------------------------------------- Add Expenses ------------------------------------------------------
elif menu == "Add Expense":
    st.subheader(":blue[Add Expenses]")
    col1,col2=st.columns(2)
    with col1:
        Number = st.text_input(':violet[Enter the Token Number]') or 0
        if Number:
            Number = int(Number)
        cell_value = df.loc[Number, 'Group']
        name = [i for i in cell_value.split(',')]
        names=set(name)
        description = st.text_input(":violet[Description]")
        amount = st.number_input(":violet[Amount]", min_value=100)
        date = st.date_input(":violet[Date]").strftime("%Y-%m-%d")
    with col2:
        paid_by = st.selectbox(":violet[Paid by]",list(names))
        image_file = st.file_uploader(":violet[Upload Receipt]", type=["png", "jpg", "pdf"])
        # Check if an image is uploaded and convert it to base64 string
        image_data = None
        if image_file is not None:
            image_bytes = image_file.read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            image_data =str( f"data:image/{image_file.type};base64,{image_base64}")
        tagged_members = st.multiselect(":violet[Tagged Members]",names)
    if st.button("Add Expense"):
        add_expense(Number,description, amount, date, paid_by, image_data, tagged_members)
        st.success("Expense added successfully!")
        #st.dataframe(df1)
        #st.dataframe(expenses_df)
# -------------------------------------------------------Display Expenses Summary Details-------------------------------------------------------
elif menu == "Display Expenses Summary":
    st.subheader(':blue[Expenses summary Details]')
    st.dataframe(df1)

# ---------------------------------------------------------------Close Group --------------------------------------------------------
else:
    st.subheader(":blue[Close Group]")
    Number=st.text_input(':violet[Enter The Token Number]')
    if Number:
        Number=int(Number)
    close_group()