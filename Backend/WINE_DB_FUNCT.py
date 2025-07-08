import pandas as pd
import sqlalchemy as postgres
import psycopg2 as pg
import re
wines_engine = postgres.create_engine('postgresql://postgres:Bungee12?@localhost:5123/wine_cellar')
conn = wines_engine.connect()

def Drink_Bottle(Name, Year, Make):
    conn.execute(postgres.text(f'INSERT INTO "Empties" SELECT * FROM "Wines" WHERE "Wine Name" = $${Name}$$ AND "Vintage" = $${Year}$$ AND "Make" = $${Make}$$ LIMIT 1'))
    conn.execute(postgres.text(f'DELETE FROM "Wines" WHERE ctid IN(SELECT ctid FROM "Wines" WHERE "Wine Name" = $${Name}$$ AND "Vintage" = $${Year}$$ AND "Make" = $${Make}$$ LIMIT 1)'))
    conn.commit()
    print("Enjoy the Vino!")
    return


def Undrink_Bottle(Name, Year, Make):
    conn.execute(postgres.text(f'INSERT INTO "Wines" SELECT * FROM "Empties" WHERE "Wine Name" = $${Name}$$ AND "Vintage" = $${Year}$$ AND "Make" = $${Make}$$ LIMIT 1'))
    conn.execute(postgres.text(f'DELETE FROM "Empties" WHERE ctid IN(SELECT ctid FROM "Empties" WHERE "Wine Name" = $${Name}$$ AND "Vintage" = $${Year}$$ AND "Make" = $${Make}$$ LIMIT 1)'))
    conn.commit()
    print("Bottle returned to Cellar")
    return


def Rack_Bottle(Name, Year, Make, **Varietals):
    
    varietals_names = [k.replace('_', ' ') for k in Varietals]
    for k in varietals_names:
        if not re.match(r'^[a-zA-Z ][a-zA-Z ]*$', k):
            raise ValueError(f"Invalid Column Name: {k}")
                
    conn = pg.connect(host='localhost', database='wine_cellar', user='postgres', password='Bungee12?', port = '5123')
    cursor = conn.cursor()
    cursor.execute('SELECT column_name FROM information_schema.columns WHERE table_name = $$Wines$$')
    varietals_check = [row[0] for row in cursor.fetchall()]
    conn.commit()
    
    
    for k in varietals_names:
        if k not in varietals_check:
            cursor.execute(f'ALTER TABLE "Wines" ADD COLUMN IF NOT EXISTS "{k}" TEXT')
            cursor.execute(f'ALTER TABLE "Empties" ADD COLUMN IF NOT EXISTS "{k}" TEXT')
    conn.commit()
    
    
    varietal_names = ','.join(f'"{k}"' for k in varietals_names)
    varietal_vals = ','.join(f"'{v}'" for v in Varietals.values())
    
    cursor.execute(f'INSERT INTO "Wines" (\"Wine Name\", \"Vintage\", \"Make\", {varietal_names}) Values ($${Name}$$, $${Year}$$, $${Make}$$, {varietal_vals})')
    conn.commit()
    print("New bottle successfully added!")
    cursor.close()
    return

#Picklist lib
##Winery index

def get_wineries():
    Wineries = conn.execute(postgres.text('SELECT DISTINCT "Make" FROM "Wines" ORDER BY "Make"'))
    Wineries = [row[0] for row in Wineries]
    return Wineries

##filtered wines list

def Wines_by_Winery(winery_name=None):
    if winery_name:
        dynamic_wines = conn.execute(postgres.text('SELECT * FROM "Wines" WHERE "Make" = :winery'), {"winery": winery_name})
        columns = dynamic_wines.keys()
        dynamic_wines = [row for row in dynamic_wines]

    else:
        dynamic_wines = conn.execute(postgres.text('SELECT * FROM "Wines" ORDER BY "Make"'))
        columns = dynamic_wines.keys()
        dynamic_wines = [row for row in dynamic_wines]

    index = len(dynamic_wines)
    wines = []
    for i in range(index):
        wines_dict = dict(zip(columns, dynamic_wines[i]))
        clean_dict = {k:v for k, v in wines_dict.items() if v not in [None]}

        wine_info = {}
        varietals = {}

        for column, value in clean_dict.items():
            if column in ['Wine Name', 'Vintage', 'Make']:
                wine_info[column] = value
            else:
                varietals[column] = value

        wines.append({
            "name": wine_info.get('Wine Name'),
            "vintage": wine_info.get('Vintage'),
            "make": wine_info.get('Make'),
            "varietals": varietals
            })

    return wines


