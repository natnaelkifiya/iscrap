# Project Name

> Short description of the project (e.g., A multi-threaded TIN extractor for eTrade using Selenium WebDriver).

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

This project is a scraping tool built for extracting data from the Ethiopian Trade License website using TIN numbers. It employs multi-threading to load pages concurrently, ensuring efficiency. Data is extracted using Selenium WebDriver in headless mode, parsed, and logged into JSON files for later analysis.

## Features

- **Multi-threading**: Scrapes multiple TINs in parallel for fast data extraction.
- **Headless Selenium**: Uses a headless browser to extract data without rendering UI.
- **Logging**: Error handling and activity logging to `app.log` file.
- **JSON Output**: Extracted data is stored in JSON format for easy processing.

## Installation

### Prerequisites

- Python 3.x
- [Selenium WebDriver](https://www.selenium.dev/)
- Google Chrome
- ChromeDriver (automatically managed by `webdriver-manager`)

### Clone the Repository

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository

### Install Dependencies

```bash
pip install -r requirements.txt
 ### Run the scraper
```bash
python eTradeMain.py





