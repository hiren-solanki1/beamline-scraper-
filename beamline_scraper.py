from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

main_list = []

url = "https://www.beamline.fund/portfolio"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")

selected_div = soup.find_all(
    "div", class_="hFQZVn", attrs={"aria-label": "content changes on hover"}
)

for section in selected_div:
    company_name = section.find("h5").text.strip()
    short_description = section.find(
        "p", class_="font_7 wixui-rich-text__text"
    ).text.strip()
    description = (
        section.find("p", class_="font_8 wixui-rich-text__text")
        .parent.text.strip()
        .replace("Website", "")
        .replace("&ZeroWidthSpace;", "")
        .replace("â€‹", "")
    )

    try:
        company_logo = (
            section.find("div", class_="JOvy1A")
            .find("img")["src"]
            .split("/v1/fill/")[0]
        )
    except:
        company_logo = (
            section.find("div", class_="j7pOnl").find("img")["src"].split("/v1/")[0]
        )

    paragraphs = section.find_all("p", class_="font_8 wixui-rich-text__text")

    paragraphs_with_link = [p for p in paragraphs if p.find("a") is not None]
    if paragraphs_with_link:
        try:
            websoite_link = paragraphs_with_link[-1].find("a")["href"]
        except:
            websoite_link = ""
    main_dir = {
        "Company Name": company_name,
        "description": description,
        "Short Description": short_description,
        "Company Logo": company_logo,
        "Websoite Link": websoite_link,
    }
    main_list.append(main_dir)


csv = pd.DataFrame(main_list)
csv.to_csv("beamline_data.csv", index=False)
print("script run successfully")
