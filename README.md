# 🤖 SRMIST Student Portal Auto Login Bot

This Python script automates the login process to the [SRMIST Student Portal](https://sp.srmist.edu.in/srmiststudentportal/students/loginManager/youLogin.jsp) using **Selenium WebDriver** and **Tesseract OCR** to solve captcha challenges.

---

## 📌 Features

- 🔐 Secure login with hidden password input
- 🧠 Automatic captcha detection and recognition via OCR
- 🔄 Retry mechanism (up to 5 attempts) if captcha fails
- 🖼️ Captures and preprocesses captcha images for improved accuracy
- 🛑 Manual captcha fallback if OCR fails
- 🧹 Cleanup: removes temporary captcha image and logs out cleanly

---

## 🛠️ Requirements

- Python 3.6 or higher
- Google Chrome browser
- ChromeDriver (auto-managed via `webdriver-manager`)
- Tesseract OCR

---
