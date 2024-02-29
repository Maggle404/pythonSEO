from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import Error
from itertools import islice
from urllib.parse import urlparse, urljoin

def connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='pythonseo'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return None

def extract_domain_name(url):
    if 'www' in url:
        www_domain = url.split('.')
        return www_domain[1]
    else:
        domain = urlparse(url).netloc
        domain_parts = domain.split('.')
        return domain_parts[0]

def get_links(url, soup):
    links = soup.find_all('a')
    domain_name = extract_domain_name(url)
    internal_links = list(islice((link for link in links if domain_name in urlparse(link.get('href')).netloc or link.get('href').startswith(('/', '#'))), 10))
    external_links = list(islice((link for link in links if link.get('href') and not link.get('href').startswith(('/', '#')) and domain_name not in urlparse(link.get('href')).netloc), 10))

    broken_internal_links = []
    broken_external_links = []

    for link in internal_links:
        href = link.get("href")
        full_url = urljoin(url, href)
        response = requests.get(full_url)
        if response.status_code == 404:
            broken_internal_links.append(href)

    for link in external_links:
        href = link.get("href")
        full_url = urljoin(url, href)
        response = requests.get(full_url)
        if response.status_code == 404:
            broken_external_links.append(href)

    return links, internal_links, external_links, broken_internal_links, broken_external_links


def analyze_url(url):
    conn = connection()
    cursor = None
    if conn is not None:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            title_tag = soup.title
            links, internal_links, external_links, broken_internal_links, broken_external_links = get_links(url, soup)
            h1_tag = soup.h1
            h2_tags = soup.find_all('h2')
            h3_tags = soup.find_all('h3')
            images = soup.find_all('img')
            images_without_alt = [img for img in images if not img.get('alt')]
            header_tag = soup.header is not None
            main_tag = soup.main is not None
            footer_tag = soup.footer is not None
            nav_tags = soup.find_all('nav')
            div_tags = soup.find_all('div')

            cursor = conn.cursor()
            query = ("INSERT INTO analysis (user_id, url, title_tag,"
                     "internal_links, external_links, broken_internal_links,"
                     "broken_external_links, h1_tag, h2_tags, h3_tags, img_without_alt,"
                     "header_tag, main_tag, footer_tag, nav_tags, div_nesting)"
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            params = [
                1,
                url if url is not None else None,
                title_tag.string if title_tag and title_tag.string is not None else None,
                len(internal_links) if internal_links is not None else None,
                len(external_links) if external_links is not None else None,
                ', '.join(broken_internal_links) if broken_internal_links is not None else None,
                ', '.join(broken_external_links) if broken_external_links is not None else None,
                h1_tag.string if h1_tag and h1_tag.string is not None else None,
                len(h2_tags) if h2_tags is not None else None,
                len(h3_tags) if h3_tags is not None else None,
                len(images_without_alt) if images_without_alt is not None else None,
                header_tag if header_tag is not None else None,
                main_tag if main_tag is not None else None,
                footer_tag if footer_tag is not None else None,
                len(nav_tags) if nav_tags is not None else None,
                len(div_tags) if div_tags is not None else None
            ]

            cursor.execute(query, params)
            conn.commit()
        except Error as e:
            print(f"Erreur lors de l'ajout de l'analyse : {e}")
        finally:
            cursor.close()
            conn.close()