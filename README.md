# 📧 Google Form Automation using Playwright (Python)

## 🚀 Project Overview

This project automates the process of:

* Opening a Google Form
* Logging into a Google account (manually)
* Automatically filling the form fields
* Submitting the form
* Storing the submitted data along with user information in a JSON file

This is built using **Playwright (Python)** for browser automation.

---

## 🧰 Technologies Used

* **Python**
* **Playwright (sync API)**
* **JSON (for data storage)**

---

## 📂 Project Structure

```
project/
│
├── form_automation.py   # Main automation script
├── form_logs.json      # Stores submission logs
└── README.md           # Documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Install Python packages

```bash
pip install playwright
```

### 2️⃣ Install browsers

```bash
playwright install
```

---

## ▶️ How to Run

```bash
python form_automation.py
```

---

## 🔄 Workflow Explanation (Step-by-Step)

### 1. 🌐 Open Google Form

```python
page.goto(FORM_URL)
```

* Script opens the provided Google Form link.

---

### 2. 🔐 Manual Login

```python
if "accounts.google.com" in page.url:
    page.wait_for_url("**docs.google.com/**")
```

* If login is required, user logs in manually.
* Script waits until redirect to Google Form is complete.

---

### 3. 📧 Get Logged-in Email

```python
email = get_logged_in_email(page)
```

#### How it works:

* Script calls Google internal account endpoint:

```python
https://accounts.google.com/ListAccounts
```

* Extracts email from JSON response:

```python
parsed[1][0][3]
```

👉 If fails → returns `"unknown_user"`

---

### 4. 🔁 Reload Form

```python
page.goto(FORM_URL)
```

* Ensures fresh state after login and email detection.

---

### 5. 📝 Fill Text Fields

```python
text_inputs = frame.locator("input[type='text']")
```

Fields filled:

* Name
* ID
* Section

```python
text_inputs.nth(0).fill(name)
text_inputs.nth(1).fill(id)
text_inputs.nth(2).fill(section)
```

---

### 6. 🔘 Fill Radio Questions (Auto)

```python
questions = frame.locator("div[role='radiogroup']")
```

For each question:

* Finds all options
* Randomly selects one

```python
rand_index = random.randint(0, options.count() - 1)
options.nth(rand_index).click()
```

👉 This simulates realistic user input.

---

### 7. 🚀 Submit Form

```python
frame.get_by_role("button", name="Submit").click()
```

* Submits the form automatically

---

### 8. 💾 Store Data

```python
log_entry = {
    "timestamp": datetime.now(),
    "user_email": email,
    "form_data": form_data
}
```

Saved into:

```
form_logs.json
```

---

## 📊 Sample Output (JSON)

```json
{
    "timestamp": "2026-03-31 11:08:43",
    "user_email": "22203139@iubat.edu",
    "form_data": {
        "name": "Tasnimul Intazam Asif",
        "id": "22203139",
        "section": "A",
        "answers": [
            "Just Right",
            "Too Much",
            "Way too little"
        ]
    }
}
```

---

## 🧠 Key Concepts Used

| Feature        | Explanation                |
| -------------- | -------------------------- |
| Playwright     | Browser automation         |
| Locator API    | DOM element selection      |
| Frame handling | Google Form iframe support |
| Randomization  | Dynamic answers            |
| JSON storage   | Persistent data logging    |

---

## ⚠️ Limitations

* Google may block `ListAccounts` API (can return 400 error)
* Email detection may fail → `"unknown_user"`
* Form structure changes may break selectors
* Requires manual login (security reasons)

---

## 🔥 Possible Improvements

* ✅ Replace API-based email detection with UI method
* ✅ Add multiple form support
* ✅ Add CSV/Excel export
* ✅ Build dashboard (Django/Flask)
* ✅ Headless execution for speed

---

## 🎯 Use Cases

* Automated survey filling
* Testing Google Forms
* Data collection simulation
* Academic/demo projects

---

## 👨‍💻 Author

**Tasnimul Intazam Asif**

---

## 💡 Final Note

This project demonstrates a **real-world automation pipeline**:

> Login → Detect User → Fill Form → Submit → Store Data

---

👉 If you want:

* Dashboard 📊
* Multi-user automation 🤖
* API integration 🌐

Just ask 🔥
