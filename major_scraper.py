import requests, bs4
import re
import csv
res = requests.get('http://www.dickinson.edu/homepage/486/women_s_and_gender_studies_curriculum')

res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')
pattern = re.compile('COURSES')
h3 = soup.find("h3", string="Courses")
print(h3)
course_descriptions = soup.find_all("p", attrs={'style': 'margin-left:20px;'})
course_details = []
for course in course_descriptions:
    #print(course)
    print(course.contents[0].text)
    title = 'WGSS ' + course.contents[0].text
    description = course.find("span").next_sibling.getText()
    print(description)
    course_details.append((title, description))

with open('courses.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in course_details:
        writer.writerow(row)
with open('rotc.csv', 'a', newline='') as rotcfile:
    writer = csv.writer(rotcfile)
    for row in course_details:
        writer.writerow(row)
# for header3 in h3:
#     print(header3.getText())
#     if header3.getText() == 'Courses':
#         print("hell yeahs")