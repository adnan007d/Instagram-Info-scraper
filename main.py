#!/usr/bin/python3
import requests
import re
import json
from bs4 import BeautifulSoup
from termcolor import colored
url = input("Enter the url of instagram user:")
# This adds https in the url if the user doesn't include it
r = re.search(r'http[s]?://', url)
if not r:
    url = 'https://' + url
r = re.search(r'instagram.com', url)  # Checks if the url includes instagram.
if not r:
    print(colored("[-] This program only works for Instagram", 'red'))
    exit(0)

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'
}
r = requests.get(url,headers=headers)
if r.status_code != 200:  # If the status code is not 200 means user doesn't exists
    print(colored("[-] User doesn't exits", 'red'))
    exit(0)

# Dictionary contains the name as the key and value as its regex to find it
Configs = {
    'Followers': r'"edge_followed_by":{"count":(\d*)}',
    'Following': r'"edge_follow":{"count":(\d*)}',
    'Posts': r'"edge_owner_to_timeline_media":{"count":(\d*),',
    'External_Link': r'external_url":"?([^"]*|null)',
    'Full_Name': r'full_name":"?([^"]*)',
    'Private': r'"is_private":(\w*)',
    'Verified': r'"is_verified":(\w*)',
    'Has AR effects': r'has_ar_effects":(\w*)',
    'Has Clips': r'has_clips":(\w*)',
    'Has Guides': r'has_guides":(\w*)',
    'Has Channel': r'has_channel":(\w*)',
    'Highlight Reel Count': r'highlight_reel_count":(\w*)',
    'Joined Recently': r'is_joined_recently":(\w*)',
    'Business_Email': r'business_email":"?(null|[^"]*)',
    'Business Account': r'"is_business_account":([a-z]*),',
    'Business Category Name': r'business_category_name":"?(null|[^"]*)',
    'Overall Category Name': r'overall_category_name":"?(null|[^"]*)',
    'Category Enum': r'category_enum":"?(null|[^"]*)',
    'Profile Pic Url': r'profile_pic_url":"?(null|[^"]*)',
    'Profile Pic Url HD': r'profile_pic_url_hd":"?(null|[^"]*)',
    'Bio': r'biography":"(.*)(?=","blocked)'
}
soup = BeautifulSoup(r.text, 'lxml')
soup.prettify
text = soup.findAll('script')  # Only selecting script tags
# Selecting the required script tag
for i in text:
    if "edge_followed_by" in str(i):
        soup = str(i)
# Searching for the values of the key and replacing the previous regex with the obtained value
for i in Configs:
    pattern = re.compile(Configs[i])
    r = pattern.finditer(soup)
    for j in r:
        Configs[i] = json.loads('"'+j.group(1)+'"')
        break
# Displaying the Result
for i in Configs:
    print(colored(i, 'green'), "=", Configs[i])
