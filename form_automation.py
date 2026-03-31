from playwright.sync_api import sync_playwright
import json
import random
import time
from datetime import datetime

FORM_URL = "https://forms.gle/x37k6y8cxJXXoxpF8"

# --------------------------
# 💾 SAVE DATA
# --------------------------
def save_data(data):
    try:
        with open("form_logs.json", "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append(data)

    with open("form_logs.json", "w") as f:
        json.dump(logs, f, indent=4)


# --------------------------
# 📧 GET EMAIL (FINAL FIX)
# --------------------------
def get_logged_in_email(page):
    try:
        page.goto("https://accounts.google.com/ListAccounts?gpsia=1&source=ChromiumBrowser&json=standard")
        page.wait_for_timeout(2000)

        data = page.inner_text("body")
        parsed = json.loads(data)

        return parsed[1][0][3]
    except:
        return "unknown_user"


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            slow_mo=200
        )

        context = browser.new_context()
        page = context.new_page()

        # --------------------------
        # 🌐 OPEN FORM
        # --------------------------
        page.goto(FORM_URL, timeout=60000)
        print("🌐 Form opened")

        # --------------------------
        # 🔐 LOGIN WAIT
        # --------------------------
        if "accounts.google.com" in page.url:
            print("🔐 Login manually...")
            page.wait_for_url("**docs.google.com/**", timeout=120000)
            print("✅ Login done")

        # --------------------------
        # 📧 FIXED EMAIL DETECTION FLOW
        # --------------------------
        page.goto("https://www.google.com/")
        page.wait_for_timeout(3000)

        email = get_logged_in_email(page)
        print(f"👤 Logged in as: {email}")

        # --------------------------
        # 🔁 BACK TO FORM
        # --------------------------
        page.goto(FORM_URL)
        page.wait_for_selector("form", timeout=60000)

        frame = page.frame_locator("iframe") if page.locator("iframe").count() > 0 else page

        print("🤖 Filling form...")

        # --------------------------
        # 📝 TEXT INPUT
        # --------------------------
        text_inputs = frame.locator("input[type='text']")

        form_data = {
            "name": " Tasnimul Intazam Asif",
            "id": "22203139",
            "section": "A",
            "answers": []
        }

        if text_inputs.count() >= 3:
            text_inputs.nth(0).click()
            text_inputs.nth(0).fill(form_data["name"])
            time.sleep(0.3)

            text_inputs.nth(1).click()
            text_inputs.nth(1).fill(form_data["id"])
            time.sleep(0.3)

            text_inputs.nth(2).click()
            text_inputs.nth(2).fill(form_data["section"])
            time.sleep(0.3)

            print("✅ Text filled")

        # --------------------------
        # 🔘 RADIO QUESTIONS
        # --------------------------
        questions = frame.locator("div[role='radiogroup']")

        answer_labels = [
            "Way too little",
            "Too little",
            "Just Right",
            "Too Much",
            "Way Too Much"
        ]

        for i in range(questions.count()):
            group = questions.nth(i)

            group.scroll_into_view_if_needed()
            time.sleep(0.3)

            options = group.locator("[role='radio']")

            if options.count() > 0:
                rand_index = random.randint(0, options.count() - 1)
                option = options.nth(rand_index)

                option.hover()
                option.click(force=True)
                time.sleep(0.3)

                selected = (
                    answer_labels[rand_index]
                    if rand_index < len(answer_labels)
                    else f"Option {rand_index}"
                )

                form_data["answers"].append(selected)

                print(f"✅ Q{i+1}: {selected}")

        print("✅ Form filled")

        # --------------------------
        # 🚀 SUBMIT
        # --------------------------
        frame.get_by_role("button", name="Submit").click()

        print("🎉 Submitted!")

        # --------------------------
        # 💾 STORE (CORRECT USER)
        # --------------------------
        log_entry = {
            "timestamp": str(datetime.now()),
            "user_email": email,
            "form_data": form_data
        }

        save_data(log_entry)

        print("💾 Stored with correct user!")

        input("Press ENTER to close...")
        browser.close()


if __name__ == "__main__":
    run()