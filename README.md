# 🌐 Website Functionality Testing Agent

A Python-based browser automation agent that tests website functionality using Playwright.

Currently configured to test **ChatGPT's Deep Research** feature.

## Features

- 🖥️ Launches Chrome browser (visible or headless mode)
- 🌍 Navigates to specified websites
- 🖱️ Interacts with page elements (clicks, inputs)
- 📸 Takes screenshots at each step
- 📝 Logs all output to file and stdout
- ⚠️ Handles errors gracefully with clear messages

## Setup

### 1. Create Virtual Environment

```bash
cd /home/etem/web-testing-agent
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers

```bash
playwright install chromium
```

Or to use your installed Chrome:
```bash
playwright install chrome
```

## Usage

### Run the Test

```bash
source venv/bin/activate
python main.py
```

### What It Does

1. **Launches Chrome** - Opens a new browser window
2. **Opens ChatGPT** - Navigates to chatgpt.com
3. **Selects Deep Research** - Clicks on the Deep Research feature
4. **Inputs Prompt** - Enters the test query
5. **Captures Output** - Logs response to file and displays in terminal
6. **Handles Errors** - Stops and shows error message if any step fails

### Output Files

| File | Description |
|------|-------------|
| `output.log` | Complete log with timestamps and response |
| `step2_chatgpt_loaded.png` | Screenshot after loading ChatGPT |
| `step3_after_selection.png` | Screenshot after selecting Deep Research |
| `step4_prompt_entered.png` | Screenshot after entering prompt |
| `step5_final_output.png` | Screenshot of final response |

## Configuration

Edit these variables in `main.py`:

```python
OUTPUT_FILE = "output.log"           # Log file path
CHATGPT_URL = "https://chatgpt.com"  # Target URL
PROMPT = "your prompt here"          # Test prompt
TIMEOUT = 120000                      # Timeout in ms (2 minutes)
```

### Headless Mode

To run without showing the browser window:

```python
browser = p.chromium.launch(
    headless=True,  # Change to True
    ...
)
```

## Requirements

- Python 3.8+
- Chrome browser installed
- Internet connection

## Troubleshooting

### "Chrome not found"

Install Chrome or use Chromium:
```bash
playwright install chromium
```

Then change `channel="chrome"` to just use Chromium:
```python
browser = p.chromium.launch(headless=False)
```

### "Login required"

ChatGPT may require login. The agent will:
1. Detect the login page
2. Wait 60 seconds for manual login
3. Continue with the test

### "Element not found"

ChatGPT's UI may change. Check the screenshots to see current page state, then update the selectors in `main.py`.

## Example Output

```
============================================================
🌐 Website Functionality Testing Agent
============================================================
Target: ChatGPT Deep Research
Output: output.log
============================================================

[2024-12-04 10:30:00] 🚀 Starting Web Testing Agent...
[2024-12-04 10:30:01] Step 1: Launching Chrome browser...
[2024-12-04 10:30:03] ✅ Chrome browser launched successfully
[2024-12-04 10:30:03] Step 2: Opening https://chatgpt.com...
[2024-12-04 10:30:08] ✅ Successfully opened https://chatgpt.com
[2024-12-04 10:30:08] Step 3: Selecting 'Deep Research' feature...
[2024-12-04 10:30:12] ✅ Selected 'Deep Research' feature
[2024-12-04 10:30:12] Step 4: Inputting prompt...
[2024-12-04 10:30:15] ✅ Prompt submitted
[2024-12-04 10:30:15] Step 5: Waiting for response...
[2024-12-04 10:32:30] ✅ Response captured successfully

============================================================
DEEP RESEARCH OUTPUT
============================================================
[Response content here...]
============================================================

✅ All steps completed successfully!
```

## License

MIT

