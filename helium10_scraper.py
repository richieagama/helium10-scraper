from playwright.sync_api import sync_playwright
import time

def process_asins():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # Set to False to see browser window locally
            # No executable_path needed
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        # Create context with viewport and user agent to look more like a real browser
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        )
        
        page = context.new_page()
        
        try:
            # Login process with better debugging
            print("Navigating to login page...")
            page.goto('https://members.helium10.com/user/signin')
            
            # Take screenshot before login attempt
            page.screenshot(path="1_before_login.png")
            
            print("Checking for email field...")
            # Use a more flexible selector and longer timeout
            email_selector = 'input[type="email"], #loginform-email, input[name="email"]'
            page.wait_for_selector(email_selector, timeout=10000)
            
            print("Filling email...")
            page.fill(email_selector, 'ragama@nuwattlighting.com')
            
            print("Filling password...")
            password_selector = 'input[type="password"], #loginform-password, input[name="password"]'
            page.fill(password_selector, '#pregs6023')
            
            # Take screenshot before clicking submit
            page.screenshot(path="2_filled_form.png")
            
            print("Clicking submit button...")
            # Try multiple possible selectors for the submit button
            submit_button_selectors = [
                '.login-form button[type="submit"]',
                'button[type="submit"]',
                'button:has-text("Sign In")',
                'button:has-text("Login")'
            ]
            
            for selector in submit_button_selectors:
                if page.is_visible(selector):
                    page.click(selector)
                    print(f"Clicked button with selector: {selector}")
                    break
            
            # Add a small delay to allow for any client-side validation
            page.wait_for_timeout(2000)
            
            # Take screenshot after clicking submit
            page.screenshot(path="3_after_submit.png")
            
            print("Waiting for navigation...")
            try:
                page.wait_for_navigation(wait_until='networkidle', timeout=15000)
            except Exception as e:
                print(f"Navigation timeout: {e}")
                # Continue anyway as sometimes the navigation event doesn't trigger properly
            
            # Take screenshot of resulting page
            page.screenshot(path="4_after_navigation.png")
            
            # Check if we're actually logged in
            if page.url.startswith('https://members.helium10.com/dashboard') or not page.url.endswith('/signin'):
                print('Login successful')
            else:
                print('Login may have failed. Current URL:', page.url)
                # Check for error messages
                error_messages = page.query_selector_all('.error-message, .alert, .error')
                for error in error_messages:
                    print('Error message found:', error.inner_text())
            
            # Take a pause to see what's happening
            print("Pausing for 5 seconds to observe browser state...")
            page.wait_for_timeout(5000)
            
            # Rest of your code...
            
        except Exception as e:
            print(f"Error during process: {e}")
            page.screenshot(path="error_screenshot.png")
        
        finally:
            browser.close()

if __name__ == "__main__":
    process_asins()