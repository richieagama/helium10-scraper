from playwright.sync_api import sync_playwright
import time

def capture_login_screenshot():
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        
        # Create context with realistic viewport
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        )
        
        # Open a new page
        page = context.new_page()
        
        # Navigate to Helium 10 login page
        page.goto('https://members.helium10.com/user/signin')
        
        # Wait for the page to be fully loaded
        page.wait_for_load_state('networkidle')
        
        # Take a screenshot and save it
        page.screenshot(path="helium10_login.png", full_page=True)
        
        print("Screenshot saved as 'helium10_login.png'")
        
        # Close the browser
        browser.close()

if __name__ == "__main__":
    capture_login_screenshot()