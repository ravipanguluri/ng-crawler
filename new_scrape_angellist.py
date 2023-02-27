
from bs4 import BeautifulSoup

fh = open('./data/html201-300.txt')
csv_writing = open('./data/new_csv_angel_output.csv', 'a')
html_lines = fh.readlines()

counter = 0

i = 0
page = ''
while i < len(html_lines):
    page = ''
    if '<!DOCTYPE html>' in html_lines[i]:
        # counter = counter + 1
        # if counter == 2:
        #     i = 100000000000000909090909
        #     break
        while '</html>' not in html_lines[i]:
            page = page + html_lines[i]
            i = i + 1

        soup = BeautifulSoup(page, 'html.parser')
        company_boxes = soup.find_all('div', {'class': 'rounded-lg border border-gray-400 p-8 pb-0'})

        for box in company_boxes:
            try:
                company_name = box.find_all("header", {"class": "text-dark-aaaa font-medium antialiased text-lg"})[0]
                website = box.find_all('dl', {'class': 'flex flex-wrap gap-10 text-sm'})[0]
                num_of_employees = box.find_all('dl', {'class': 'flex flex-wrap gap-10 text-sm'})[0]
                description = box.find_all("div", {"class": "styles_component__481pO"})[0]


                csv_writing.write(f'{company_name.findAll(text=True)[0].replace(",", "")},'
                              f'{website.div.dd.a["href"].replace(",", "")},'
                              f'{website.find("dd", {"class": "text-gray-800"}).findAll(text=True)[0].replace(",", "")},'
                              f'{"".join(description.findAll(text=True)).replace(",", "")}\n')
            except:
                print(company_name.findAll(text=True)[0].replace(",", ""))

        # company_names = soup.find_all("header", {"class": "text-dark-aaaa font-medium antialiased text-lg"})
        # websites = soup.find_all('dt', {"class": 'mb-2 font-bold'})
        # websites = soup.find_all('dl', {'class': 'flex flex-wrap gap-10 text-sm'})
            # .find_all("a", {"class": "styles_component__UCLp3 styles_defaultLink__eZMqw"})
        # nums_of_employees = soup.find_all('dl', {'class': 'flex flex-wrap gap-10 text-sm'})
        # descriptions = soup.find_all("div", {"class": "styles_component__481pO"})
        #
        # inner_counter = 0
        #
        # while inner_counter < len(company_names):
        #     # print(company_names[inner_counter].findAll(text=True)[0])
        #     # print(websites[inner_counter].div.dd.a["href"])
        #     # print(websites[inner_counter].find("dd", {"class": "text-gray-800"}).findAll(text=True)[0])
        #     # print('description: ', ''.join(descriptions[inner_counter].findAll(text=True)).replace(",", ""))
        #     # print(type(descriptions[inner_counter].findAll(text=True)[0]))
        #     csv_writing.write(f'{company_names[inner_counter].findAll(text=True)[0].replace(",", "")},'
        #                       f'{websites[inner_counter].div.dd.a["href"].replace(",", "")},'
        #                       f'{websites[inner_counter].find("dd", {"class": "text-gray-800"}).findAll(text=True)[0].replace(",", "")},'
        #                       f'{"".join(descriptions[inner_counter].findAll(text=True)).replace(",", "")}\n')
        #     inner_counter = inner_counter + 1

        # print(len(company_names))
        # print(company_names[0].findAll(text=True)[0])
        # print(len(websites))
        # for element in websites:
        #     print(element.div.dd.a['href'])
        #     print(elementc)
        #
        # print(len(descriptions))

    i = i + 1

fh.close()
csv_writing.close()
