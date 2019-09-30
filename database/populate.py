import sqlite3
conn = sqlite3.connect('Benchmark.db')

c = conn.cursor()

# Bids
c.execute("INSERT INTO bids (Name, Email, Phone, Date) VALUES ('Dave Hunter', 'davehunter@gmail.com', '0488195262', '2019-09-07')")
c.execute("INSERT INTO bids (Name, Email, Phone, Date) VALUES ('Frank David', 'frankdavid@gmail.com', '0432611593', '2019-09-08')")

# Listing
c.execute("INSERT INTO listing (Listing_name, Listing_price, Listing_type, Metadata_id) VALUES ('NVIDIA RTX 2080ti', '1999', 'GPU', '1')")
c.execute("INSERT INTO metadata (Listing_id, Manufacturer, Description, Chipset, Memory, Memory_Type, Core_Clock, Boost_Clock, Colour, Max_SLI_Support, Max_CrossFire_Support, Length, TDP, DVI_Ports, HDMI_Ports, Mini_HDMI_Ports, DisplayPort_Ports, Mini_DisplayPort_Ports, Cooling_Style) VALUES ('1', 'NVIDIA', 'Placeholder Text GPU', 'GeForce RTX 2080 Ti', '11', 'GDDR6', '1350', '1635', 'Black/Silver', '2', '0', '267', '260', '0', '1', '0', '3','0', 'Fan')")

c.execute("INSERT INTO listing (Listing_name, Listing_price, Listing_type, Metadata_id) VALUES ('AMD Ryzen 7 1700x', '349.99', 'CPU', '2')")
c.execute("INSERT INTO metadata (Listing_id, Manufacturer, Description, Core_Count, Core_Clock, Boost_Clock, TDP, Series, Microarchitecture, Socket, Integrated_Graphics, Includes_CPU_Cooler) VALUES ('2', 'AMD', 'Placeholder Text', '8', '3.4', '3.8', '95', 'AMD Ryzen 7', 'Zen','AM4', 'No', 'No')")



conn.commit()

conn.close()
