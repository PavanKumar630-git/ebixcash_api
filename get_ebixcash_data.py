from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
from queries import *
import time

def search_ebix_agents(pincode):
    # Step 1: Launch headless browser and get CSRF + cookies
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://ebixcash.com/find-our-agents/"
    driver.get(url)
    time.sleep(5)

    # Get cookies and CSRF token
    cookies_list = driver.get_cookies()
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies_list}
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    csrf_token = csrf_input['value'] if csrf_input else None
    driver.quit()

    # Step 2: Build request
    cookies = {
        'csrftoken': cookies_dict.get('csrftoken', ''),
        'sessionid': cookies_dict.get('sessionid', ''),
        '_gcl_au': cookies_dict.get('_gcl_au', ''),
        '_gid': cookies_dict.get('_gid', ''),
        '_ga': cookies_dict.get('_ga', ''),
        '_ga_EBMCPJ1BQP': cookies_dict.get('_ga_EBMCPJ1BQP', ''),
        '_gat_UA-155139764-1': cookies_dict.get('_gat_UA-155139764-1', ''),
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://ebixcash.com',
        'referer': url,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    }

    data = {
        'csrfmiddlewaretoken': csrf_token,
        'search_text': pincode,
    }

    # Step 3: Submit the POST request
    response = requests.post(url, cookies=cookies, headers=headers, data=data)
    return response

# Example usage:
# html_data = search_ebix_agents('110001')

def clean_agent_data(data):
    cleaned = {}
    for key, value in data.items():
        # Remove the prefix before the first colon (e.g., "Agent Name:") from the value
        if ":" in value:
            cleaned[key] = value.split(":", 1)[1].strip()
        else:
            cleaned[key] = value.strip()
    return cleaned


def extract_agents_from_html(html_content,pincode):
    soup = BeautifulSoup(html_content.text, 'html.parser')
    agents = []

    accordion = soup.find(id="accordion")
    if not accordion:
        return []

    # Find all cards inside the accordion
    cards = accordion.find_all("div", class_="card")
    for card in cards:
        agent_data = {}

        # Title of agent (e.g. BHATIA BROTHERS NEW DELHI IBP)
        header = card.find("h6")
        if header:
            agent_data["Agency"] = header.get_text(strip=True)

        # Body of card
        body = card.find("div", class_="card-body")
        if body:
            paragraphs = body.find_all("p")
            for p in paragraphs:
                strong = p.find("strong")
                if strong:
                    key = strong.get_text(strip=True).rstrip(":")
                    value = p.get_text(strip=True).replace(strong.get_text(), "").strip()
                    agent_data[key] = value

        if agent_data:
            final_agent_data = clean_agent_data(agent_data)
            agentcy = final_agent_data.get("Agency","")
            agentname = final_agent_data.get("Agent Name","")
            contact = final_agent_data.get("Contact","")
            email = final_agent_data.get("Email","")
            address = final_agent_data.get("Address","")
            city = final_agent_data.get("City","")
            pincode = final_agent_data.get("Pincode","")


            final_params = (pincode,agentcy,agentname,contact,email,address,city,pincode)
            # execute_insert_query(insert_query_ebixcash,final_params)
            agents.append(final_agent_data)

    return agents

# agent_list = extract_agents_from_html(html_data)
# print(agent_list)

#   "Agency": "NARESH KUMAR CHAUHAN",
#       "Agent Name": "Naresh Kumar Chauhan",
#       "Contact": "9210480809",
#       "Email": "nk1467632@gmail.com",
#       "Address": "HOUSE NO 07 PARDA BAGH DARYA GANJ, HOUSE NO 07 PARDA BAGH DARYA GANJ, PARDA BAGH , DARYA GANJ",
#       "City": "Delhi",
#       "Pincode": "110002"

#       searchpincode,
#     agency,
#     agentname,
#     contact,
#     email,
#     address,
#     city,
#     pincode