# Financial Superintendence Web Scraper  
### By: Santiago Ospina Ferreira  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Santiago%20Ospina-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/ospinaferreira/)  

Effortlessly scrape Colombian XBRLs and PDFs for the enterprises you need. Just set the parameters and let the script do the work!  

---

## 🚀 Features  
- Fetch financial reports (XBRLs and PDFs) from Colombian enterprises.
- Customize the parameters to suit your needs.
- Specify download paths for better organization.
- Includes an automated renaming functionality for downloaded files.
- Fast, reliable, and straightforward.

---

## ⚙️ Usage  

### Step 1: Clone the Repository  
```bash
git clone https://github.com/your-repo-name.git
cd your-repo-name
```

### Step 2: Define Your Parameters  
Update the parameters in the `main` function of the script. Example:

```python
# Parameters to define:
nits = ["1234", "5678"]         # Enterprise NITs
anios = ["2024"]                # Years of interest
tipos_reporte = ["Intermedios"] # Report types
periodos = ["Septiembre"]       # Reporting periods

# Define the path where the files will be downloaded:
download_path = "/Users/santiospina/Documents/Projects/finance_market_scraping/scraped_files"

# Set up the Selenium WebDriver with the specified download path
driver = setup_driver(download_path)
```

The script will save all downloaded files to the specified `download_path` and execute the renaming function automatically after the download completes.

### Step 3: Run the Script  
```bash
python scraper.py
```

---

## 🛠️ Requirements  

- Python 3.8+
- Install the required packages:  
  ```bash
  pip install -r requirements.txt
  ```

---

## 📚 Parameters Explained  

| **Parameter**    | **Description**                                      | **Example**            |
|-------------------|------------------------------------------------------|------------------------|
| `nits`           | List of enterprise NITs (taxpayer identification).    | `["1234", "5678"]`     |
| `anios`          | List of years for which reports are required.         | `["2024"]`             |
| `tipos_reporte`  | Type of reports (e.g., "Intermedios", "Anuales").     | `["Intermedios"]`      |
| `periodos`       | Periods to scrape reports for (e.g., months).         | `["Septiembre"]`       |
| `download_path`  | Directory to save downloaded files.                   | `"/path/to/directory"` |

---

## 🧑‍💻 Author  

**Santiago Ospina Ferreira**  
- 💼 [LinkedIn](https://www.linkedin.com/in/ospinaferreira/)  
- 📫 santiospina910@gmail.com

---

## 📄 License  
This project is licensed under the [MIT License](LICENSE).

---

### 🌟 Contributions Welcome!  
If you'd like to contribute or suggest improvements, feel free to create an issue or submit a pull request.

### 📝 Disclaimer  
Future versions won't have the comments and variables in Spanglish—**promise!** 😅