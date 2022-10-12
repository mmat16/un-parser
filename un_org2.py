import requests
import csv
from bs4 import BeautifulSoup
import lxml

with open("mails.csv", 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["№", "organisation", "email"])

url = 'https://sdgs.un.org/partnerships/browse'
schema_p = 'https://sdgs.un.org'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
}
cards = []

for i in range(379):
    url = f'https://sdgs.un.org/partnerships/browse?keys=&page={i}'
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='views-row')
    links = [schema_p+item.find('a').get('href') for item in items]
    cards.extend(links)
    print(i)

print('\ncollected cards\n')
print('collecting emails\n')

q = 0
for card in cards:
    q += 1
    response = requests.get(url=card, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    organisation = soup.find('h1', class_='separator-bottom mt-5').text.strip()

    try:
        email = soup.find('div', class_='views-field views-field-field-email').text.strip()
    except Exception as e:
        print(e)
        email = "no email"
        print(email)

    with open("mails.csv", 'a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([q, organisation, email])

    print(q)
