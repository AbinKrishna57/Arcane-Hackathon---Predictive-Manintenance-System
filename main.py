# TOPIC: "Industrial operations are hindered by various inefficiencies, culminating in diminished productivity, escalated expenditures, and compromised profitability."
# Sub Topic: Predictive maintenance System
# DUE TO LACK OF MAINTENANCE IN INDUSTRIES THERE IS A HUGE LOSE IN EFFICIENCY OF MACHINES AND PROFIT
# THIS PROGRAM HELPS TO GIVE NOTIFICATION FOR EVERY MACHINE THAT NEEDS MAINTENANCE

# START

import mysql.connector as sq
from tabulate import tabulate
from getpass import getpass
from plyer import notification
from datetime import datetime, timedelta
import time
import schedule

# [!] - for errors
# [⁎] - for goods (i dont know what to write here)
# [#] - if something is not available or not found or if nothing is changed
# [+] - if something new is added
# [&] - for showing info
# [$] - for showing warning
# [—] - for Unknown Command
# [>] - for questions like "do you want to quit" etc.

default="\033[0m"
bold="\033[1m"
underline="\033[4m"

Default="\033[0m"
Light_Red="\033[91m"
Light_Green="\033[92m"
Light_Yellow="\033[93m"
Light_Blue="\033[94m"
Light_Magenta="\033[95m"
Light_Cyan="\033[96m"
Light_White="\033[97m"
Orange="\033[38;5;214m"
not_availabe_color="\033[90m"



fmt="double_grid"

# Functions

# Connection
def connection():
    host=input(f"\n{Light_Green}(Hostname) > {default}")
    user=input(f"{Light_Green}(Username) > {default}")
    # db=input(f"{Light_Green}(Database Name) > {default}")
    passwd=getpass(f"{Light_Green}(Database Connection Password) > {default}")
    # conn=sq.connect(host=host, username=user, database="manufacturing", passwd=passwd)
    conn=sq.connect(host="localhost", username="root", database="manufacturing", passwd="Server###Beast69#")

def show_table(s_table):
    if s_table.upper() in ["AUTOMOTIVE_MACHINES", "MAINTENANCE_LOGS", "USAGE_DATA"]:
        curs=conn.cursor()
        curs.execute("SELECT * FROM "+s_table)
        item=curs.fetchall()
        if len(item)==0:
            print(f"\n{Light_Green}[#]{default} No values availabe (Empty table)")
        else:
            if s_table.upper()=="AUTOMOTIVE_MACHINES":
                m_h=[]
                m_header=["Machine ID", "Model", "Duration", "Machine Name", "Days"]
                for m in m_header:
                    m_h.append(f"{m}{default}")
                print(tabulate(item, headers=m_h, tablefmt=fmt))

            elif s_table.upper()=="MAINTENANCE_LOGS":
                maint_logs_h=[]
                maint_logs_header=["Machine ID", "Date Of Maintenance", "Type of Maintenance"]
                for maint_logs in maint_logs_header:
                    maint_logs_h.append(f"{maint_logs}{default}")
                print(tabulate(item, headers=maint_logs_h, tablefmt=fmt))

            elif s_table.upper()=="USAGE_DATA":
                usaged_h=[]
                usaged_header=["Machine ID", "Date", "Operational Hours"]
                for usaged in usaged_header:
                    usaged_h.append(f"{usaged}{default}")
                print(tabulate(item, headers=usaged_h, tablefmt=fmt))
            else:
                print(f"{Light_Red}[!]{default} Error: Wrong Table Name")
    else:
        print(f"\n{Light_Red}[!]{default} Error: Wrong Table Name\n")

def insert_values():
    curs=conn.cursor()
    try:
        table=input(f"(Enter Table Name (automotive_machines, maintenance_logs, usage_data)) > ")
    except sq.ProgrammingError:
                print(f"\n{Light_Red}[!]{default} Error: Enter the correct Value")
    try:
        entries=int(input(f"(Enter Number Of Entries) > "))
        try:
            print(f"\n{Light_Yellow}[&]{default} The Columns Of The Table is as Follows: ")
            curs.execute(f"DESCRIBE {table}")
            table_desc=curs.fetchall()
            columns={}
            for i in table_desc:
                if i!=table_desc[0]: #Excluding Entry of ID Of Main Tables To Implement AUTO_INCREMENT
                    columns.update({i[0]:i[1].upper()})
            print(f"    {columns}")

            print(f"\n{Light_Yellow}[&]{default} After every value put a '/' (Example: type/model)")
            print(f"{Light_Yellow}[&]{default} There is no need of typing the Machine_ID")
            print(f"{Light_Yellow}[&]{default} The format for writing date is (yyyymmdd)\n")
            for _ in range(entries):
                try:
                    show_table(table)
                    entry=tuple(input(f"\n(Enter values) > ").split("/"))
                    
                    if not entry:
                        print(f"{Light_Red}[!]{default} Error: No value is entered")
                        break
                    else:
                        if table.upper() == "AUTOMOTIVE_MACHINES":
                            e=list(entry) #Forms a List Of Entered Values

                            curs.execute("""INSERT INTO automotive_machines
                            (model, maintenance_frequency, machine_types, days_between_maintenance) VALUES (%s, %s, %s, %s)""", e)
                            
                            col=["model", "maintenance_frequency", "machine_types", "days_between_maintenance"]
                            for it in col:
                                query=f"""UPDATE automotive_machines
                                            SET {it}=NULL
                                            WHERE {it}=''"""
                                try:
                                    curs.execute(query)
                                except:
                                    pass
                            
                            date_of_maintenance=input(f"(Enter date of maintenance) > ")
                            type_of_maintenance=input(f"(Enter the type of maintenance) > ")

                            curs.executemany("INSERT INTO maintenance_logs VALUES (%s, %s)", (date_of_maintenance, type_of_maintenance))

                        elif table.upper() == "USAGE_DATA":
                            data=list(entry)
                            curs.execute("""INSERT INTO usage_data
                            (date, operational_hours)
                            VALUES (%s, %s)""", data)
                    
                    commit=input("(Do you want to commit changes?) Y/n > ")
                    if commit.upper() in ["YES", "Y"]:
                        print(f"\n{Light_Magenta}[+]{default} Database Updated")
                        conn.commit()
                    elif commit.upper() in ["NO", "N"]:
                        print(f"\n[#] No changes took place")
                    else:
                        print(f"\n{Light_Red}[!]{default} Error: Wrong input")
                        
                except sq.ProgrammingError:
                    print(f"\n{Light_Red}[!]{default} Error: Enter the correct Value")

        except ValueError:
            print(f"\n{Light_Red}[!]{default} Error: Enter the correct Value\n")
    except ValueError:
        print(f"\n{Light_Red}[!]{default} Error: Enter the correct Value")


def update_data():
    curs=conn.cursor()
    table = input(f"(Enter Table Name (automotive_machines, maintenance_logs, usage_data)) > ")
    if table.upper() in ["AUTOMOTIVE_MACHINES", "MAINTENANCE_LOGS", "USAGE_DATA"]:
        curs.execute("SELECT * FROM "+table)
        item=curs.fetchall()
        
        if len(item)==0:
            print(f"\n{not_availabe_color}[#] No values available (Empty table){default}\n")

        elif len(item)!=0:
            if table.upper()=="AUTOMOTIVE_MACHINE":
                am_header=["Machine ID", "Model", "Duration", "Machine Name", "Days"]
                print()
                print(tabulate([am_header], tablefmt=fmt))
                print()
            
            elif table.upper()=="MAINTENANCE_LOGS":
                ml_header=["Machine ID", "DATE OF MAINTENANCE", "TYPE OF MAINTENANCE"]
                print()
                print(tabulate([ml_header], tablefmt=fmt))
                print()
            
            elif table.upper()=="USAGE_DATA":
                ud_header=["Machine ID", "Date", "Operational Hours"]
                print()
                print(tabulate([ud_header], tablefmt=fmt))
                print()

            try:
                column_change = input(f"(Enter Column Of Record To Update) > ")
                column_value = input(f"(Enter Value To Update To) > ")
                change = f"{column_change} = '{column_value}'"
            
                print(f"\n[&] If there are no conditions the whole '{column_change}' column will be changed to '{column_value}'")
                
                try:
                    condition_count = int(input(f"(Number Of Conditions) > "))
                    # curs.execute(f"UPDATE {table} SET {change} WHERE ")
                
                    if condition_count == 0:
                        confirm = input(f"\n(This Will Modify Every Record In '{table}' Table) Commit? Y/n > ")
                        if confirm.upper() in ["YES", "Y"]:
                            conn.commit()
                            print(f"[+] Database Updated{default}")
                        elif confirm.upper() in ["NO", "N"]:
                            print(f"[#] Change Reverted{default}\n")
                        else:
                            print(f"\n[!] Error: Wrong input{default}")
                    
                    elif condition_count > 0:
                        conditions = ""
                        for i in range(condition_count):
                            condition_column = input(f"(Enter Column To Use As Condition {i+1}) > ")
                            condition_value = input(f"(Enter Value To Search With Respect To Column Condition {i+1}) > ")
                            
                            if not condition_value.isdigit():
                                condition_value = f"{condition_value}"
                            conditions += f"{condition_column} = '{condition_value}'"
                            
                            if condition_count == 1:
                                pass
                            elif i == (condition_count - 1):
                                pass
                            else:
                                conditions += " AND "

                        curs.execute(f"UPDATE {table} SET {change} WHERE {conditions}")
                        confirm = input(f"\n(This Will Modify Every Record In '{table}' Table) Commit? Y/n > ")
                        if confirm.upper() in ["YES", "Y"]:
                            conn.commit()
                            print(f"\n[+] Database Updated{default}\n")
                        elif confirm.upper() in ["NO", "N"]:
                            print(f"\n{not_availabe_color}[#] Change Reverted{default}\n")
                        else:
                            print(f"\n[!] Error: Wrong input{default}")
                    else:
                        print("Something went Wrong")
                    
                except ValueError:
                    print(f"\n[!] Error: Number of conditions must be interger{default}\n")
                    
            except ValueError:
                print(f"\n[!] Error: Type the Values correctly{default}\n")
            except sq.ProgrammingError:
                print(f"\n[!] Error: Enter the values correctly{default}\n")
    else:
        print(f"\n[!] Error: Wrong Table Name{default}\n")


# Main
print(f"\n{bold}[@] Starting the Predictive Maintenance System Console.../{default}")
print(f"\n      {Light_Cyan}[Credits]{default} {Light_Blue}Abin Krishna, Sabarinath R Nambiar{default}")
print("-"*81+"\033[37m")

try:
    print(f"\t\t{bold}       {underline}Enter SQL Server Connection Details{default}")
    print("—"*81)

    print("""\033[1;95m
                        ██████╗ ███╗   ███╗███████╗
                        ██╔══██╗████╗ ████║██╔════╝
                        ██████╔╝██╔████╔██║███████╗
                        ██╔═══╝ ██║╚██╔╝██║╚════██║
                        ██║     ██║ ╚═╝ ██║███████║
                        ╚═╝     ╚═╝     ╚═╝╚══════╝                                                                             
    \033[0m""")

    host=input(f"\n{Light_Green}(Hostname) > {default}")
    user=input(f"{Light_Green}(Username) > {default}")
    # db=input(f"{Light_Green}(Database Name) > {default}")
    passwd=getpass(f"{Light_Green}(Database Connection Password) > {default}")

    conn=sq.connect(host=host, username=user, database="manufacturing", passwd=passwd)

except KeyboardInterrupt:
    print("\nExiting Program..")
    print("Done")

def main():
    if(conn.is_connected()):
        print(f"\n{bold}[⁎] Connected to {host}{default}")
        print(f"{bold}[⁎] Welcome To The Automotive Maintenance Databse Interface{default}")
        print(f"{bold}[⁎] Connected Successfully{default}\n")

        while conn.is_connected():
            print(f"\n{bold}Options")
            print(f"""{Light_Red}
\t•———————————————————•
 \t1. Insert Value(s)
 \t2. Show table
 \t3. Maintenance Logs
 \t4. Update Value(s)
\t•———————————————————•{default}\n""")
            
            options=input("(Enter Option) > ")
            if(options.upper() in ["1", "INSERT VALUE", "INSERT VALUES"]):
                insert_values()
            elif(options.upper() in ["2", "SHOW TABLE"]):
                print("""Available Tables:
                      1. automotive_machines
                      2. maintenance_logs
                      3. usage_data""")
                t_name=input("(Enter Table Name) > ")
                show_table(t_name.lower())
            elif(options.upper() in ["3", "MAINTENANCE_LOGS"]):
                show_table("maintenance_logs")
            elif(options.upper() in ["4", "UPDATE VALUE", "UPDATE VALUES"]):
                update_data()
            else:
                print(f"{Light_Red}[-]{default} Unknown Command")

# NOTIFICATION
def send_notification(message):
    notification.notify(title="MAINTENANCE ALERT!!! DO MAINTENANCE ON THESE MACHINES", message=message, app_name="Predictive Maintenance System")

def automatic():
    curs=conn.cursor()
    curs.execute("SELECT machine_type, days_between_maintenance FROM automotive_machines")
    checks={row[0]:row[1] for row in curs.fetchall()}
    
    start_date=datetime.now().date()

    while True:
        current_date = datetime.now().date()
        days_passed = (current_date - start_date).days

        # Always send the daily notification
        daily_message = "Daily Maintenance Check: Please review all machines."
        send_notification(daily_message)

        # Send notifications for machines with specific intervals on the correct day
        for machine, interval in checks.items():
            if interval != 1 and days_passed % interval == 0:  # Skip daily machine here
                specific_message = f"{machine} requires maintenance today!"
                send_notification(specific_message)

        # Wait until the next day (24 hours)
        time.sleep(86400)  # 86400 seconds = 24 hours

print("•—————————————————————————————•")
print("  1. Main Program (Console)")
print("  2. Automatic Service")
print("•—————————————————————————————•")
try:
    choice=int(input("(Enter Choice) > "))
    match(choice):
        case 1:
            main()
        case 2:
            automatic()
        case _:
            print(f"{Light_Red}[!] Error: Wrong Option{default}")
except KeyboardInterrupt:
    print(f"\n{bold}Exiting Program...{default}")
# END
