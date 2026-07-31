# El Pais Cross-Browser Automation

A Selenium-based automation suite for validating the **El Pais Opinion** workflow across multiple desktop browsers and real mobile devices using BrowserStack Automate.


## Test Workflow

The automation:

- Navigates to the El Pais **Opinion** section
- Handles responsive desktop and mobile navigation
- Scrapes the first **5 articles**
- Extracts article titles and content
- Downloads available cover images
- Translates Spanish titles to English
- Identifies words repeated more than twice across translated titles
- Executes **5 BrowserStack sessions concurrently**
- Reports individual session status as **Passed / Failed**

## Cross-Browser Execution

The suite uses BrowserStack to validate the same workflow across multiple browser, OS, and real-device combinations.

Parallel execution is implemented using Python `ThreadPoolExecutor`, allowing all five environments to execute concurrently.

## Tech Stack

`Python` · `Selenium WebDriver` · `BrowserStack Automate` · `RapidAPI` · `ThreadPoolExecutor`

## Project Structure

```text
├── main.py          # BrowserStack capabilities and parallel execution
├── elpais_core.py   # Scraping, translation and content analysis
├── images/          # Article cover images captured during execution
└── .gitignore       # Excludes credentials and local environment files
```

## Run

Install dependencies:
pip install selenium requests python-dotenv
```

Configure the required BrowserStack and translation API credentials as environment variables, then run:
python main.py
```

## Test Reliability

The implementation includes:

- Explicit waits for dynamic elements
- Desktop/mobile navigation fallbacks
- Responsive cookie-consent handling
- Security-verification detection
- BrowserStack session-level Passed/Failed reporting
- Exception handling for remote execution failures
- Parallel cross-browser execution

> Third-party security verification on El Pais may occasionally block remote automated sessions. These cases are surfaced as test failures rather than masked by the automation.
