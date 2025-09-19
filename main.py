import asyncio
import os
import time
import httpx
from playwright.async_api import async_playwright
from datetime import datetime, timezone, timedelta


# --- Import Configuration ---
try:
    from config import (
        PHONE_NUMBER,
        PASSWORD,
        TELEGRAM_BOT_TOKEN,
        TELEGRAM_CHAT_ID,
        REQUEST_INTERVAL_SECONDS,
        PAGE_REFRESH_INTERVAL_MINUTES,
    )
except ImportError:
    print("[ERROR] config.py not found or missing variables. Please create it based on the example.")
    exit(1)

# --- Constants ---
WEBSITE_URL = "https://www.alditalk-kundenportal.de/portal/auth/uebersicht/"
SESSION_DIR = "session_data"
IPHONE_DEVICE = "iPhone 11"
API_URL = "https://www.alditalk-kundenportal.de:443/scs/bff/scs-209-selfcare-dashboard-bff/selfcare-dashboard/v1/offer/updateUnlimited"
USER_DATA_URL = "https://www.alditalk-kundenportal.de/scs/bff/scs-209-selfcare-dashboard-bff/selfcare-dashboard/v1/account-overview/content"
CONTRACT_URL = "https://www.alditalk-kundenportal.de/scs/bff/scs-207-customer-master-data-bff/customer-master-data/v1/navigation-list"

class Notifier:
    """Handles sending notifications."""
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    async def send_message(self, text):
        """Sends a message to the configured Telegram chat."""
        if not self.bot_token or not self.chat_id or "YOUR_TELEGRAM" in self.bot_token:
            print("[Notifier] Telegram credentials not configured. Skipping notification.")
            return

        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown",
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, json=payload)
                response.raise_for_status()
                print("[Notifier] Successfully sent Telegram notification.")
        except httpx.HTTPStatusError as e:
            print(f"[Notifier] Error sending Telegram notification: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"[Notifier] An unexpected error occurred while sending notification: {e}")

class AldiTalkRefresher:
    """Manages the AldiTalk data refresh process."""
    def __init__(self, notifier):
        self.notifier = notifier
        self.gigabytes_counter = 0
        self.renewal_date = time.time() - 1000000  # Initialize to a past time
        self.billing_account_id = ""
        self.api_payload = {
            "amount": "1048576",
            "offerId": "",
            "refillThresholdValue": "1048576",
            "subscriptionId": "",
            "updateOfferResourceID": "",
        }
        self.api_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Origin": "https://www.alditalk-kundenportal.de",
            "Referer": "https://www.alditalk-kundenportal.de/portal/auth/uebersicht/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

    def _printer(self, text):
        """Custom print function with a prefix."""
        prefix = f"[AldiTalkRefresher] {self.gigabytes_counter} GB >>"
        print(f"{prefix} {text}")

    async def _login(self, page):
        """Handles the login process."""
        self._printer("Login page detected. Attempting to log in automatically...")
        try:
            if "YOUR_PHONE_NUMBER" in PHONE_NUMBER or "YOUR_PASSWORD" in PASSWORD:
                self._printer("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                self._printer("!!! PLEASE SET YOUR CREDENTIALS in config.py               !!!")
                self._printer("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return False
            
            # Handle cookie banner with a timeout
            await asyncio.sleep(5)  # Wait a moment for the banner to appear
            try:
                self._printer("Checking for cookie banner...")
                await page.locator('button[data-testid="uc-accept-all-button"]').click(timeout=5000)
                self._printer("Accepted cookies.")
            except Exception:
                self._printer("Cookie banner not found or already accepted.")
                pass
            await asyncio.sleep(2)  # Wait a moment after accepting cookies
            username_input = page.locator('input[name="callback_2_od"]')
            await username_input.fill(PHONE_NUMBER)
            await page.locator('input[name="callback_3_od"]').fill(PASSWORD)
            await page.locator('one-checkbox[name="loginRemember_od"]').click()
            await page.locator('one-button[id="IDToken5_4_od_2"]').click()
            
            await page.wait_for_url(lambda url: "login" not in url, timeout=120000)
            self._printer("Login successful.")
            return True
        except Exception as e:
            self._printer(f"Automatic login failed: {e}")
            return False

    async def _fetch_user_data(self, page) -> tuple[bool, bool]:
        """Fetches user data and updates the API payload."""
        self._printer("Fetching user data...")
        try:
            response = await page.request.get(USER_DATA_URL)
            if not response.ok:
                error_text = await response.text()
                raise Exception(f"HTTP error {response.status} while fetching user data: {error_text}")
            
            data = await response.json()
            
            account_details = data.get("accountDetails", {})
            self.billingAccountId = account_details.get("billingAccountId", "")
            customer_id = self.billingAccountId[-10:]

            response = await page.request.get(CONTRACT_URL)
            if not response.ok:
                error_text = await response.text()
                raise Exception(f"HTTP error {response.status} while fetching user data: {error_text}")
            
            data = await response.json()

            subscriptions = data['userDetails'].get("subscriptions", [])
            for subscription in subscriptions:
                if subscription.get("offerName") in ["ALDI TALK Tarif L", "ALDI TALK Tarif M", "ALDI TALK Tarif S"]:
                    self.api_payload["subscriptionId"] = subscription.get("contractId")
                    self.api_payload["offerId"] = subscription.get("productId")
                    break
            if not self.api_payload["subscriptionId"]:
                await self.notifier.send_message("❌ No valid subscription found. Please check your tariff.")
                return True, False

            resourceIdUrl = f"https://www.alditalk-kundenportal.de/scs/bff/scs-209-selfcare-dashboard-bff/selfcare-dashboard/v1/offers/C-{customer_id}?contractId={self.api_payload['subscriptionId']}&productType=Mobile_Product_Offer"
            try:
                response = await page.request.get(resourceIdUrl)
                if not response.ok:
                    error_text = await response.text()
                    raise Exception(f"HTTP error {response.status} while fetching user data: {error_text}")
                data = await response.json()
                for subscription in data.get("subscribedOffers", []):
                    if subscription.get("offerId") == self.api_payload["offerId"]:
                        self.api_payload["updateOfferResourceID"] = subscription.get("resourceId")

                        # --- Correctly parse the renewal date ---
                        renewal_str = subscription.get("renewalDate", "")
                        if renewal_str:
                            # Parse the UTC string into a timezone-aware datetime object
                            # The 'Z' (Zulu time) is replaced with +00:00 for ISO format compatibility
                            renewal_date_obj = datetime.fromisoformat(renewal_str.replace('Z', '+00:00'))
                            self.renewal_date = renewal_date_obj.timestamp()

                            # --- Check if the plan is about to expire ---
                            now_utc = datetime.now(timezone.utc)
                            time_left = renewal_date_obj - now_utc

                            self._printer(f"Plan renews in: {time_left}")

                            # Notify if expiring within 24 hours
                            if time_left < timedelta(days=1):
                                await self.notifier.send_message(f"⚠️ Your AldiTalk plan will expire in less than 24 hours! ({time_left})")

                        self._printer("API payload updated with dynamic data.")
                        return True, True
                self._printer("No matching offer found to extract Resource ID.")
                return False, False
            except Exception as e:
                self._printer(f"An error occurred while fetching resource ID: {e}")
                return False, False
        except Exception as e:
            self._printer(f"An error occurred while fetching user data: {e}")
            return False, False

    async def _refresh_data_volume(self, page):
        """Sends the API request to refresh the data volume."""
        try:
            response = await page.request.post(
                API_URL,
                headers=self.api_headers,
                data=self.api_payload
            )
            if not response.ok:
                error_text = await response.text()
                raise Exception(f"HTTP error {response.status} while refreshing data volume: {error_text}")
            
            response_json = await response.json()
            message = response_json.get('message', 'No message found.')
            is_updated = response_json.get('isUpdated', False)

            if is_updated:
                self.gigabytes_counter += 1
                self._printer(f"Data volume successfully refreshed! Status: {message}")
                await self.notifier.send_message(f"✅ AldiTalk data refreshed! Total: {self.gigabytes_counter} GB")
            else:
                self._printer(f"Data volume refresh status: {message}")

        except Exception as e:
            self._printer(f"API Request failed: {e}")

    async def run(self):
        """Main execution loop for the refresher."""
        async with async_playwright() as p:
            if not os.path.exists(SESSION_DIR):
                os.makedirs(SESSION_DIR)

            self._printer("Launching browser...")
            device_params = p.devices[IPHONE_DEVICE].copy()
            device_params.pop('default_browser_type', None)
            
            context = await p.chromium.launch_persistent_context(
                SESSION_DIR,
                headless=False,
                args=[
                    '--headless=new',
                    '--no-sandbox',
                    '--disable-dev-shm-usage'
                ],
                **device_params,
            )
            page = await context.new_page()

            try:
                self._printer(f"Navigating to {WEBSITE_URL}...")
                await page.goto(WEBSITE_URL, timeout=60000, wait_until='domcontentloaded')

                if "login" in page.url:
                    if not await self._login(page):
                        await self.notifier.send_message("❌ AldiTalk login failed. Please check credentials.")
                        return
                else:
                    self._printer("Already logged in.")

                # --- Initial Data Fetch ---
                self._printer("Performing initial data fetch to check subscription status...")
                success, subscribed = await self._fetch_user_data(page)
                if not success:
                    await self.notifier.send_message("❌ Could not fetch initial user data. Exiting.")
                    return
                
                last_page_refresh_time = time.time()
                await self.notifier.send_message("🚀 AldiTalk Refresher started successfully!")
                if not subscribed:
                     await self.notifier.send_message("🤔 No active subscription found. Will check periodically.")

                # --- Main Loop ---
                self._printer("Starting main loop...")
                while True:
                    now = time.time()

                    # --- State 1: Subscription is active, renewal date is in the future ---
                    if subscribed and self.renewal_date > now:
                        # Refresh page session if needed
                        if now - last_page_refresh_time >= PAGE_REFRESH_INTERVAL_MINUTES * 60:
                            self._printer("Refreshing page to keep session active...")
                            await page.reload(wait_until='domcontentloaded')
                            last_page_refresh_time = time.time()
                            self._printer("Page refreshed.")
                        
                        # Refresh the data volume
                        await self._refresh_data_volume(page)

                    # --- State 2: No subscription or renewal date has passed ---
                    else:
                        if subscribed: # This means the renewal date just passed
                            self._printer("Subscription has likely expired. Searching for a new one...")
                            await self.notifier.send_message("⏳ Subscription expired. Looking for the new plan details.")
                        
                        # Attempt to find a new subscription
                        success, subscribed = await self._fetch_user_data(page)
                        if not success:
                            self._printer("Could not fetch user data. Retrying after interval.")
                        elif not subscribed:
                            self._printer("Still no active subscription found. Retrying after interval.")
                        else:
                            self._printer("New subscription found! Resuming data refresh.")
                            await self.notifier.send_message("✅ New subscription plan found! Resuming normal operation.")

                    await asyncio.sleep(REQUEST_INTERVAL_SECONDS)

            except Exception as e:
                self._printer(f"A critical error occurred: {e}")
                await self.notifier.send_message(f"🔥 Critical error in AldiTalk Refresher: {e}")
            finally:
                self._printer("Closing browser context.")
                await context.close()

async def main():
    """Initializes and runs the AldiTalk Refresher."""
    notifier = Notifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    refresher = AldiTalkRefresher(notifier)
    try:
        await refresher.run()
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting.")
        await notifier.send_message("🛑 AldiTalk Refresher stopped by user.")

if __name__ == "__main__":
    asyncio.run(main())