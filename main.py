#!/usr/bin/env python3
"""
Website Functionality Testing Agent

This agent automates browser interactions to test website functionality.
Currently configured to test ChatGPT's Deep Research feature.

Usage:
    python main.py
"""

import sys
import os
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


# Configuration
OUTPUT_FILE = "output.log"
CHATGPT_URL = "https://chatgpt.com"
PROMPT = "tell me the instructions to debug video stutter issue on a android phone"
TIMEOUT = 120000  # 2 minutes timeout for Deep Research (it takes time)
STEP_DELAY = 1000  # 1 second delay between steps (in milliseconds)


def log(message: str, is_error: bool = False):
    """Log message to both stdout and file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] {'ERROR: ' if is_error else ''}{message}"
    
    # Print to stdout
    if is_error:
        print(f"\033[91m{formatted_msg}\033[0m")  # Red for errors
    else:
        print(formatted_msg)
    
    # Append to file
    with open(OUTPUT_FILE, "a") as f:
        f.write(formatted_msg + "\n")
    
    sys.stdout.flush()


def human_delay(page, min_ms: int = 800, max_ms: int = 1500):
    """Add a human-like random delay."""
    delay = random.randint(min_ms, max_ms)
    page.wait_for_timeout(delay)


def type_like_human(page, element, text: str):
    """Type text with human-like delays between keystrokes."""
    element.click()
    human_delay(page, 200, 400)
    
    for char in text:
        element.type(char, delay=random.randint(30, 100))
    
    human_delay(page, 300, 600)


def save_output(content: str):
    """Save the final output to file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    separator = "=" * 60
    
    with open(OUTPUT_FILE, "a") as f:
        f.write(f"\n{separator}\n")
        f.write(f"DEEP RESEARCH OUTPUT - {timestamp}\n")
        f.write(f"{separator}\n")
        f.write(content)
        f.write(f"\n{separator}\n")
    
    print(f"\n{'=' * 60}")
    print("DEEP RESEARCH OUTPUT")
    print("=" * 60)
    print(content)
    print("=" * 60)


def run_test():
    """Main test function."""
    
    # Clear previous output file
    with open(OUTPUT_FILE, "w") as f:
        f.write(f"Web Testing Agent - Started {datetime.now()}\n")
        f.write("=" * 60 + "\n\n")
    
    log("🚀 Starting Web Testing Agent...")
    log(f"   Using {STEP_DELAY}ms delay between steps for human-like behavior")
    
    try:
        with sync_playwright() as p:
            # Step 1: Launch Google Chrome browser
            log("Step 1: Launching Google Chrome browser...")
            try:
                # Launch Google Chrome (not Chromium)
                browser = p.chromium.launch(
                    headless=False,
                    channel="chrome",  # Use installed Google Chrome
                    args=[
                        "--start-maximized",
                        "--disable-blink-features=AutomationControlled",  # Hide automation
                    ],
                    slow_mo=50,  # Slow down actions by 50ms for more human-like behavior
                )
                context = browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    locale="en-US",
                    timezone_id="America/Los_Angeles",
                )
                
                # Add extra headers to appear more human
                context.set_extra_http_headers({
                    "Accept-Language": "en-US,en;q=0.9",
                })
                
                page = context.new_page()
                log("✅ Google Chrome browser launched successfully")
            except Exception as e:
                log(f"Failed to launch Chrome: {str(e)}", is_error=True)
                log("   Make sure Google Chrome is installed on your system", is_error=True)
                return False
            
            # Delay before next step
            log(f"   Waiting {STEP_DELAY}ms before next step...")
            page.wait_for_timeout(STEP_DELAY)
            
            # Step 2: Open ChatGPT
            log(f"Step 2: Opening {CHATGPT_URL}...")
            try:
                page.goto(CHATGPT_URL, wait_until="networkidle", timeout=30000)
                log(f"✅ Successfully opened {CHATGPT_URL}")
                
                # Wait for page to fully load with human-like delay
                human_delay(page, 2000, 3000)
                
                # Take screenshot for debugging
                page.screenshot(path="step2_chatgpt_loaded.png")
                log("   Screenshot saved: step2_chatgpt_loaded.png")
                
            except PlaywrightTimeout:
                log(f"Timeout while loading {CHATGPT_URL}", is_error=True)
                browser.close()
                return False
            except Exception as e:
                log(f"Failed to open {CHATGPT_URL}: {str(e)}", is_error=True)
                browser.close()
                return False
            
            # Delay before next step
            log(f"   Waiting {STEP_DELAY}ms before next step...")
            page.wait_for_timeout(STEP_DELAY)
            
            # Step 3: Select Deep Research feature
            log("Step 3: Selecting 'Deep Research' feature...")
            try:
                # Look for model selector or Deep Research button
                # ChatGPT UI may vary, trying multiple selectors
                deep_research_selectors = [
                    "text=Deep Research",
                    "button:has-text('Deep Research')",
                    "[data-testid='model-selector']",
                    "text=Research",
                    # Dropdown menu approach
                    "[aria-label='Model selector']",
                    "button:has-text('GPT')",
                ]
                
                found_selector = False
                for selector in deep_research_selectors:
                    try:
                        element = page.locator(selector).first
                        if element.is_visible(timeout=3000):
                            human_delay(page, 500, 800)  # Human-like pause before click
                            element.click()
                            log(f"   Clicked: {selector}")
                            found_selector = True
                            human_delay(page, 800, 1200)  # Wait after click
                            break
                    except:
                        continue
                
                if not found_selector:
                    # Try to find any model/feature dropdown
                    log("   Looking for model dropdown menu...")
                    page.screenshot(path="step3_looking_for_dropdown.png")
                    
                    # Check if we need to log in first
                    if page.locator("text=Log in").is_visible(timeout=2000):
                        log("ChatGPT requires login. Please log in manually.", is_error=True)
                        log("   Waiting 60 seconds for manual login...")
                        page.wait_for_timeout(60000)
                    
                    # After potential login, try again
                    for selector in deep_research_selectors:
                        try:
                            element = page.locator(selector).first
                            if element.is_visible(timeout=3000):
                                human_delay(page, 500, 800)
                                element.click()
                                found_selector = True
                                human_delay(page, 800, 1200)
                                break
                        except:
                            continue
                
                # Try clicking on Deep Research in dropdown if it appeared
                try:
                    deep_research_option = page.locator("text=Deep Research").first
                    if deep_research_option.is_visible(timeout=3000):
                        human_delay(page, 400, 700)
                        deep_research_option.click()
                        log("✅ Selected 'Deep Research' feature")
                        human_delay(page, 800, 1200)
                    else:
                        log("⚠️  Deep Research option not found - continuing with default model")
                except:
                    log("⚠️  Could not find Deep Research - continuing with default model")
                
                page.screenshot(path="step3_after_selection.png")
                log("   Screenshot saved: step3_after_selection.png")
                
            except Exception as e:
                log(f"Warning in Step 3: {str(e)}", is_error=False)
                log("   Continuing with default model...")
            
            # Delay before next step
            log(f"   Waiting {STEP_DELAY}ms before next step...")
            page.wait_for_timeout(STEP_DELAY)
            
            # Step 4: Input prompt
            log(f"Step 4: Inputting prompt...")
            log(f"   Prompt: \"{PROMPT}\"")
            try:
                # Find the textarea/input field
                input_selectors = [
                    "textarea[placeholder*='Message']",
                    "textarea[placeholder*='Send']",
                    "#prompt-textarea",
                    "textarea",
                    "[contenteditable='true']",
                ]
                
                input_found = False
                input_element = None
                for selector in input_selectors:
                    try:
                        input_element = page.locator(selector).first
                        if input_element.is_visible(timeout=3000):
                            input_found = True
                            log(f"   Found input field: {selector}")
                            break
                    except:
                        continue
                
                if not input_found or input_element is None:
                    log("Could not find input field", is_error=True)
                    page.screenshot(path="error_no_input_field.png")
                    browser.close()
                    return False
                
                # Type like a human (with delays between keystrokes)
                log("   Typing prompt (human-like speed)...")
                type_like_human(page, input_element, PROMPT)
                
                log("✅ Prompt entered successfully")
                page.screenshot(path="step4_prompt_entered.png")
                
                # Human-like delay before submitting
                human_delay(page, 800, 1200)
                
                # Submit the prompt
                log("   Submitting prompt...")
                
                # Try pressing Enter or clicking send button
                submit_selectors = [
                    "button[data-testid='send-button']",
                    "button[aria-label='Send']",
                    "button:has-text('Send')",
                    "button[type='submit']",
                ]
                
                submitted = False
                for selector in submit_selectors:
                    try:
                        btn = page.locator(selector).first
                        if btn.is_visible(timeout=2000):
                            human_delay(page, 300, 600)
                            btn.click()
                            submitted = True
                            log(f"   Clicked send button: {selector}")
                            break
                    except:
                        continue
                
                if not submitted:
                    # Fallback: press Enter
                    human_delay(page, 200, 400)
                    page.keyboard.press("Enter")
                    log("   Pressed Enter to submit")
                
                log("✅ Prompt submitted")
                
            except Exception as e:
                log(f"Failed to input prompt: {str(e)}", is_error=True)
                page.screenshot(path="error_input_prompt.png")
                browser.close()
                return False
            
            # Delay before next step
            log(f"   Waiting {STEP_DELAY}ms before next step...")
            page.wait_for_timeout(STEP_DELAY)
            
            # Step 5: Wait for response and capture output
            log("Step 5: Waiting for response (this may take a while for Deep Research)...")
            try:
                # Wait for response to start appearing
                page.wait_for_timeout(5000)
                
                # Wait for response to complete
                # Look for indicators that response is done
                max_wait_time = TIMEOUT
                wait_interval = 5000
                total_waited = 0
                
                while total_waited < max_wait_time:
                    # Check if still generating
                    is_generating = False
                    generating_indicators = [
                        "button:has-text('Stop')",
                        "[aria-label='Stop']",
                        ".result-streaming",
                    ]
                    
                    for indicator in generating_indicators:
                        try:
                            if page.locator(indicator).first.is_visible(timeout=1000):
                                is_generating = True
                                break
                        except:
                            continue
                    
                    if not is_generating:
                        log("   Response appears complete")
                        break
                    
                    log(f"   Still generating... ({total_waited // 1000}s elapsed)")
                    page.wait_for_timeout(wait_interval)
                    total_waited += wait_interval
                
                # Extra wait for final rendering
                human_delay(page, 2000, 3000)
                
                # Capture the response
                response_selectors = [
                    "[data-message-author-role='assistant']",
                    ".markdown",
                    ".prose",
                    "[class*='response']",
                    "[class*='message']",
                ]
                
                response_text = ""
                for selector in response_selectors:
                    try:
                        elements = page.locator(selector).all()
                        if elements:
                            # Get the last (most recent) response
                            response_text = elements[-1].inner_text()
                            if len(response_text) > 100:  # Meaningful response
                                break
                    except:
                        continue
                
                if response_text:
                    log("✅ Response captured successfully")
                    save_output(response_text)
                else:
                    log("Could not capture response text", is_error=True)
                    # Take screenshot of current state
                    page.screenshot(path="step5_response_state.png", full_page=True)
                    log("   Screenshot saved: step5_response_state.png")
                
                page.screenshot(path="step5_final_output.png", full_page=True)
                log("   Final screenshot saved: step5_final_output.png")
                
            except PlaywrightTimeout:
                log("Timeout while waiting for response", is_error=True)
                page.screenshot(path="error_timeout.png")
                browser.close()
                return False
            except Exception as e:
                log(f"Failed to capture response: {str(e)}", is_error=True)
                page.screenshot(path="error_capture_response.png")
                browser.close()
                return False
            
            # Cleanup
            log("\n🎉 Test completed successfully!")
            log(f"📄 Output saved to: {OUTPUT_FILE}")
            
            # Keep browser open for review (optional)
            log("\nBrowser will close in 10 seconds...")
            page.wait_for_timeout(10000)
            
            browser.close()
            return True
            
    except Exception as e:
        log(f"Unexpected error: {str(e)}", is_error=True)
        return False


def main():
    """Entry point."""
    print("=" * 60)
    print("🌐 Website Functionality Testing Agent")
    print("=" * 60)
    print(f"Target: ChatGPT Deep Research")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Step Delay: {STEP_DELAY}ms")
    print("=" * 60 + "\n")
    
    success = run_test()
    
    if success:
        print("\n✅ All steps completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Test failed - check error messages above")
        sys.exit(1)


if __name__ == "__main__":
    main()
