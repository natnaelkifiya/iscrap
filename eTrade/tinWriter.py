import csv
import os
from param import parameters

class TinManager:
    def __init__(self, csv_path, field_names: str) -> None:
   
        self.csv_path = csv_path
        self.fieldnames = parameters().eTradeParam['fieldName']


        csv_dir = os.path.dirname(self.csv_path)
        if csv_dir and not os.path.exists(csv_dir):  # Check if directory exists and create if not
            os.makedirs(csv_dir)


        
        # Check if the file exists; if not, create it with the appropriate header
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()

    def insert_or_update_tin(self, tin: str, name: str) -> None:
        rows = []
        updated = False

        # Read the existing data and check for the TIN
        if os.path.exists(self.csv_path):
            with open(self.csv_path, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['TIN'] == tin:
                        row['Name'] = name  # Update the name if TIN exists
                        updated = True
                    rows.append(row)

        # If the TIN was not found, add it
        if not updated:
            rows.append({'TIN': tin, 'Name': name})

        # Write the updated data back to the CSV file
        with open(self.csv_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

#     def read_all(self) -> list:
#         """
#         Read all records from the CSV file.

#         :return: A list of dictionaries representing each row in the CSV.
#         """
#         if os.path.exists(self.csv_path):
#             with open(self.csv_path, 'r', newline='') as csvfile:
#                 reader = csv.DictReader(csvfile)
#                 return list(reader)
#         return []

# # # Example usage:
# # tin_manager = TinManager('tins.csv')

# # # Insert or update a TIN
# # tin_manager.insert_or_update_tin('123456789', 'Company A')
# # tin_manager.insert_or_update_tin('987654321', 'Company B')

# # # Update an existing TIN
# # tin_manager.insert_or_update_tin('123456789', 'Updated Company A')

# # # Read all records
# # all_records = tin_manager.read_all()
# # print(all_records)
