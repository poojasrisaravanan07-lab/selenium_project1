from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime
import pandas as pd
import time
import os

# Open Chrome
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

# Open CoinMarketCap
driver.get("https://coinmarketcap.com/")
time.sleep(60)

# Get table rows
rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

data = []

# Extract first 10 coins
for row in rows[:10]:
    try:
        cols = row.find_elements(By.TAG_NAME, "td")

        name = cols[2].text
        price = cols[3].text
        change = cols[4].text
        market_cap = cols[7].text

        data.append([name, price, change, market_cap])

    except Exception as e:
        print("Error:", e)

# Close browser AFTER scraping
driver.quit()

# Create DataFrame
df = pd.DataFrame(
    data,
    columns=["Coin Name", "Price", "24h Change", "Market Cap"]
)

# STEP 8 - Add Timestamp
df["Timestamp"] = datetime.now()

print("\nScraped Data:\n")
print(df)

# STEP 9 - Save / Append CSV (History Save)
file_name = "crypto_data.csv"

try:
    if not os.path.exists(file_name):
        df.to_csv(file_name, index=False)
        print("\n✅ CSV created and data saved!")
    else:
        df.to_csv(file_name, mode="a", header=False, index=False)
        print("\n📌 Data appended to existing CSV!")

    print("📁 File Location:")
    print(os.path.abspath(file_name))

except Exception as e:
    print("\n❌ Error Saving CSV:", e)

# ⏳ KEEP PROGRAM RUNNING FOR 1 MINUTE
print("\n⏳ Waiting for 60 seconds before exit...")
time.sleep(60)

print("\n👋 Program Ended Successfully!")