import requests
from bs4 import BeautifulSoup
from save_data import save_to_csv

def extract_price(price_element):
    # Extract text and remove spaces and commas
    price_text = price_element.get_text(strip=True).replace(' ', '').replace(',', '')

    # Check if the price contains a currency symbol and unwanted characters
    if '€' in price_text:
        # Remove the currency symbol and unwanted characters
        price_text = price_text.replace('€', '').replace('(', '').replace(')', '').replace('<sup>', '').replace('</sup>', '')

        # Extract the numeric part from the price text
        price_numeric = int(''.join(filter(str.isdigit, price_text)))

        # Convert the numeric part to a float
        formatted_price = float(price_numeric) / 100  # Convert to euros with two decimal places

        return formatted_price

    return None

def scrape_page(url, all_product_data):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find and process each product on the page
        product_elements = soup.find_all('p', class_='product-name')
        price_elements = soup.find_all('span', class_='price')

        for product_element, price_element in zip(product_elements, price_elements):
            product_title = product_element.find('a').text.strip()
            print(f"Product Title: {product_title}")

            # Extract price using the updated function
            formatted_price = extract_price(price_element)

            if formatted_price is not None:
                print(f"Product Price: {formatted_price:.2f}")
                print("-" * 30)

                # Append product data to the list
                all_product_data.append({"title": product_title, "price": formatted_price})

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

def scrape_all_pages(base_url, total_pages):
    all_product_data = []  # Initialize an empty list to store all product data

    for page in range(1, total_pages + 1):
        page_url = f"{base_url}?ob=pa&page={page}"
        scrape_page(page_url, all_product_data)

    # Save all data to the CSV file after processing all pages
    save_to_csv(all_product_data, "product_data.csv")

if __name__ == "__main__":
    base_url = "https://220.lv/lv/datortehnika/portativie-datori-un-plansetes/portativie-datori"
    total_pages = 48
    scrape_all_pages(base_url, total_pages)
