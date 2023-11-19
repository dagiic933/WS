import csv

def save_to_csv(product_data, file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['title', 'price']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the product data
        writer.writerows(product_data)
