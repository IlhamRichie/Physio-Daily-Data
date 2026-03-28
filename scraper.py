import requests
import random
import os
import datetime
import time

# 1. Konfigurasi Pencarian Medis
SEARCH_TERM = "stroke physiotherapy"
# Ini triknya: Kita set bot buat ngambil 1 sampai 4 artikel secara acak tiap harinya
NUM_COMMITS = random.randint(1, 4) 

def fetch_pubmed_articles(limit):
    """Fungsi buat narik data jurnal dari API PubMed gratis"""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={SEARCH_TERM}&retmode=json&retmax={limit}&sort=pub+date"
    response = requests.get(url).json()
    id_list = response.get('esearchresult', {}).get('idlist', [])
    
    if not id_list: return []
    
    summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={','.join(id_list)}&retmode=json"
    summary_res = requests.get(summary_url).json()
    
    articles = []
    for uid in id_list:
        title = summary_res['result'][uid]['title']
        link = f"https://pubmed.ncbi.nlm.nih.gov/{uid}/"
        articles.append(f"- [{title}]({link})")
    return articles

print(f"Hari ini bot akan melakukan {NUM_COMMITS} commits...")
articles = fetch_pubmed_articles(NUM_COMMITS)
today = datetime.datetime.now().strftime("%Y-%m-%d")

# 2. Setup Identitas Git untuk GitHub Actions
os.system('git config --local user.email "ilhamrgn22@gmail.com"')
os.system('git config --local user.name "IlhamRichie"')

# 3. Looping untuk bikin Commit secara bertahap (biar kotaknya makin hijau!)
for i, article in enumerate(articles):
    # Tulis artikel ke dalam file Markdown
    with open("stroke_journals.md", "a", encoding="utf-8") as f:
        if i == 0:
            f.write(f"\n### Riset Tanggal: {today}\n")
        f.write(article + "\n")
    
    # Git add & Git commit PER ARTIKEL
    os.system('git add stroke_journals.md')
    os.system(f'git commit -m "Auto-add stroke research article part {i+1} on {today}"')
    
    # Jeda 2 detik biar log git-nya natural
    time.sleep(2)
