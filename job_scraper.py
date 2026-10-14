import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "http://realpython.github.io/fake-jobs/"

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Applewebkit/5.36"
}
print("job portal Data Extract Ho Raha hai")
response = requests.get(url, headers=header)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find(id="ResultsContainer")
    job_cards = results.find_all("div", class_="card-content")

    jobs_data = []

    for idx, job in enumerate(job_cards, start=101):
        title = job.find("h2", class_="title").text.strip()
        company = job.find("h3", class_="company").text.strip()
        location = job.find("p", class_="location").text.strip()
        date_posted = job.find("time").text.strip()
        # Extract Apply Link
        links = job.find_all("a")
        apply_link = links[1]["href"] if len (links) > 1 else "N/A"

        jobs_data.append({
            "Job ID": f"JOB-{idx}",
            "Job Title": title,
            "Company": company,
            "Location": location,
            "Date posted": date_posted,
            "Apply link": apply_link,
            "Source": "Demo Website"
        })
        # Save to Excel
        df = pd.DataFrame(jobs_data)
        df.to_excel("remote_jobs_data.xlsx", index=False)

        print(f"\nSuccess! Total {len(jobs_data)} Job Listings ka data 'remote_jobs_data.xlsx' mein save ho gaya hai.")
else:
    print(f"Failed to fetch data. Status Code: {response.status_code}")