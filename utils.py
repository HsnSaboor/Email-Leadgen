# utils.py
import csv

def save_results_to_csv(results, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Website', 'Phone', 'Email', 'Address'])
        for entry in results:
            writer.writerow([
                entry.get('name', 'N/A'),
                entry.get('website', 'N/A'),
                ', '.join(entry.get('phone', [])),
                ', '.join(entry.get('email', [])),
                entry.get('address', 'N/A')
            ])
