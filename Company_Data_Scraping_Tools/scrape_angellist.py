
fh = open('./data/html201-300.txt')

csv_writing = open('./data/csv_angel_output.csv', 'a')

html_lines = fh.readlines()

results = []

company_name = ''
website = ''
num_employees = ''
description = ''

for line in html_lines:
    index = line.find('text-dark-aaaa font-medium antialiased text-lg')
    company_name = ''
    website = ''
    num_employees = ''
    description = ''
    if index > -1:
        company_name = line[index + 53:line.find('</div>', index + 54)]
        website_start_index = line.find('<dt class="mb-2 font-bold">Website</dt>')
        website = line[website_start_index+52:line.find('"', website_start_index + 53)]

        employees_start = line.find('<dt class="mb-2 font-bold">Employees</dt>')
        num_employees = line[employees_start+67:line.find('</dd>', employees_start + 68)]

    description_start = line.find('<div class="styles_component__481pO">')
    if description_start > -1:
        description = line[description_start + 42:line.find('</div>', description_start + 43)]

    if company_name != '' and website != '' and num_employees != '' and description != '':
        csv_writing.write(f'{company_name.replace(",", "")},{website.replace(",", "")},{num_employees.replace(",", "")},{description.replace(",", "")}\n')

csv_writing.close()
fh.close()