# LinkedIn Profile Scraper

## Clone Project
```commandline
git clone https://github.com/sohail-eng/linkedin-profile-scrapper.git
```

## Prerequisites
- Python 3.8+
- pip
- Virtual environment support

## Setup Instructions

### 1. Create Virtual Environment

#### On Ubuntu:
```bash
# Navigate to your project directory
cd linkedin-profile-scrapper

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

#### On Windows:
```cmd
# Navigate to your project directory
cd linkedin-profile-scrapper

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

### 2. Install Dependencies
```bash
# With virtual environment activated
pip install -r requirements.txt
```

### 3. Configure Credentials
Open the `CONSTANTS.py` file in the main directory and set the following:

```python
# CONSTANTS.py
LINKEDIN_URL = "https://www.linkedin.com/search/results/people/..."  # Your specific search URL
```

**IMPORTANT:** 
- Ensure the LinkedIn URL is a valid search results page
- Keep this file private and do not commit to version control

### 4. Run the Application

#### Login to LinkedIn:
```bash
python login.py
```
This script will log into your LinkedIn account. it will require you to enter email and password in the terminal (where you run the program).

#### Prepare input data
Please create `input.json` file in the project folder and input the data in this format
```
[
  {
    "name": "first search file name",
    "url": "https://www.linkedin.com/search/results/people/?keywords=mary"
  }
]
```
#### Start Scraping:
```bash
python main.py
```
This script will scrape data by using `input.json` file.

## Troubleshooting
- Ensure you have the latest version of Chrome/ChromeDriver
- Check your internet connection
- Verify LinkedIn URL is accessible

## Legal Notice
- Respect LinkedIn's Terms of Service
- Ensure you have permission to scrape data
- Use this tool responsibly and ethically
