import os
import sys
import django
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

USER_PASSWORD = os.getenv("E2E_USER_PASSWORD")
ADMIN_PASSWORD = os.getenv("E2E_ADMIN_PASSWORD")

if not USER_PASSWORD or not ADMIN_PASSWORD:
    sys.exit("E2E_USER_PASSWORD dan E2E_ADMIN_PASSWORD belum diisi di berkas .env.")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portofolio.settings")
django.setup()
from django.contrib.auth.models import User
from main.models import Project

E2E_PREFIX = "E2E "
E2E_PROJECT = E2E_PREFIX + "Proyek AJAX"
XSS_PAYLOAD = '<img src="x" onerror="window.__xss = true">'


def setup_users():
    user, _ = User.objects.get_or_create(username="user")
    user.set_password(USER_PASSWORD)
    user.is_superuser = False
    user.is_staff = False
    user.save()

    admin, _ = User.objects.get_or_create(username="demtcsre")
    admin.set_password(ADMIN_PASSWORD)
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()


def card_names(driver):
    return driver.execute_script(
        "const grid = document.getElementById('grid');"
        "if (!grid || grid.classList.contains('hide')) return [];"
        "return [...grid.querySelectorAll('li.card h3')].map(h => h.textContent.trim());"
    )


def toast_is(title):
    return lambda d: d.execute_script(
        "const t = document.getElementById('toast-component');"
        "return t.classList.contains('toast-show') && document.getElementById('toast-title').textContent;"
    ) == title


def modal_open(driver):
    return driver.execute_script(
        "return document.getElementById('add-project-modal').matches(':popover-open');"
    )


def fill_project_modal(driver, wait, name, description):
    driver.find_element(By.CSS_SELECTOR, "button[popovertarget='add-project-modal']").click()
    wait.until(modal_open)
    fields = {"id_name": name, "id_kicker": "Dibuat oleh E2E", "id_description": description}
    for field_id, value in fields.items():
        element = driver.find_element(By.ID, field_id)
        element.clear()
        element.send_keys(value)
    driver.find_element(By.CSS_SELECTOR, "#project-form button[type='submit']").click()


def main():
    setup_users()

    options = webdriver.ChromeOptions()
    if "--headless" in sys.argv:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    else:
        options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    base_url = "http://127.0.0.1:8000"

    try:
        # 1. Cek csrf token di form login
        try:
            driver.get(f"{base_url}/login/")
        except Exception:
            print(f"Server belum berjalan di {base_url}. Jalankan 'python manage.py runserver' terlebih dahulu.")
            return
        csrf = wait.until(
            EC.presence_of_element_located((By.NAME, "csrfmiddlewaretoken"))
        )
        assert csrf.get_attribute("value")
        assert driver.get_cookie("csrftoken")
        print("[PASS] CSRF token dan cookie terverifikasi")

        # 2. Cek login user biasa dan cookie sesi
        driver.find_element(By.NAME, "username").send_keys("user")
        driver.find_element(By.NAME, "password").send_keys(USER_PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        wait.until(EC.url_to_be(f"{base_url}/"))
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "nav-user")))
        assert driver.get_cookie("sessionid")
        assert driver.get_cookie("last_login")
        assert "Sesi Terakhir Login" in driver.page_source or "Last Login" in driver.page_source
        print("[PASS] Login user biasa dan cookie sesi berhasil")

        # 3. Cek pembatasan akses user biasa ke form tambah proyek
        driver.get(f"{base_url}/project/add/")
        assert "403" in driver.title or "Forbidden" in driver.page_source
        print("[PASS] Otorisasi user biasa dibatasi (403)")

        Project.objects.create(name=E2E_PREFIX + XSS_PAYLOAD, description=XSS_PAYLOAD, order=999)
        driver.get(f"{base_url}/project/")
        wait.until(lambda d: len(card_names(d)) == Project.objects.count())
        driver.execute_script("window.__noReload = true;")
        assert E2E_PREFIX + XSS_PAYLOAD in card_names(driver)
        assert not driver.find_elements(By.CSS_SELECTOR, "#grid img[src='x']")
        assert not driver.find_elements(By.ID, "add-project-modal")
        assert not driver.find_elements(By.CSS_SELECTOR, "button[popovertarget='add-project-modal']")
        assert driver.find_elements(By.CSS_SELECTOR, "#grid .button-star")
        print("[PASS] Daftar proyek dimuat via AJAX, user biasa tidak melihat modal tambah")

        keyword = Project.objects.first().name[:4]
        search = driver.find_element(By.ID, "search-input")
        search.send_keys(keyword)
        expected = list(Project.objects.filter(name__icontains=keyword).values_list("name", flat=True))
        wait.until(lambda d: card_names(d) == expected)
        search.send_keys(Keys.CONTROL, "a")
        search.send_keys(Keys.BACKSPACE)
        wait.until(lambda d: len(card_names(d)) == Project.objects.count())
        assert driver.execute_script("return window.__noReload === true;")
        print("[PASS] Pencarian debounce berjalan tanpa reload halaman")

        assert not driver.execute_script("return window.__xss === true;")
        print("[PASS] Data JSON di-escape sebelum masuk innerHTML (XSS tidak jalan)")

        # 4. Cek akses superuser ke form tambah proyek
        driver.get(f"{base_url}/logout/")
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/login/')]")))
        driver.get(f"{base_url}/login/")
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("demtcsre")
        driver.find_element(By.NAME, "password").send_keys(ADMIN_PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        wait.until(EC.url_to_be(f"{base_url}/"))
        wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "nav-user"), "demtcsre"))

        driver.get(f"{base_url}/project/add/")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "project-form")))
        print("[PASS] Akses superuser ke form proyek berhasil")

        driver.get(f"{base_url}/project/")
        wait.until(lambda d: len(card_names(d)) == Project.objects.count())
        driver.execute_script("window.__noReload = true;")

        fill_project_modal(driver, wait, E2E_PROJECT, "Proyek dari pengujian E2E.")
        wait.until(toast_is("Berhasil"))
        wait.until(lambda d: not modal_open(d))
        wait.until(lambda d: E2E_PROJECT in card_names(d))
        assert Project.objects.filter(name=E2E_PROJECT).exists()
        assert driver.execute_script("return window.__noReload === true;")
        print("[PASS] Proyek baru ditambahkan via modal AJAX, toast sukses tampil")

        fill_project_modal(driver, wait, XSS_PAYLOAD, "Harus ditolak server.")
        wait.until(toast_is("Gagal menambahkan proyek"))
        message = driver.find_element(By.ID, "toast-message").text
        assert "tidak boleh hanya berisi tag HTML" in message, message
        assert modal_open(driver)
        driver.find_element(By.CSS_SELECTOR, "#add-project-modal .button-secondary").click()
        wait.until(lambda d: not modal_open(d))
        print("[PASS] Input berbahaya ditolak server, toast error tampil")

        card = driver.find_element(
            By.XPATH, f"//ul[@id='grid']/li[.//h3[normalize-space()='{E2E_PROJECT}']]"
        )
        card.find_element(By.CSS_SELECTOR, ".button-danger").click()
        wait.until(EC.alert_is_present()).accept()
        wait.until(lambda _: not Project.objects.filter(name=E2E_PROJECT).exists())
        wait.until(lambda d: len(card_names(d)) == Project.objects.count())
        assert E2E_PROJECT not in card_names(driver)
        print("[PASS] Hapus proyek dengan confirm() berhasil")

        # 5. Cek logout dan penghapusan cookie
        driver.get(f"{base_url}/logout/")
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/login/')]")))
        cookie_last_login = driver.get_cookie("last_login")
        assert cookie_last_login is None or cookie_last_login["value"] == ""
        print("[PASS] Logout dan pembersihan cookie berhasil")

        print("\nSemua pengujian E2E berhasil!")

    finally:
        driver.quit()
        Project.objects.filter(name__startswith=E2E_PREFIX).delete()


if __name__ == "__main__":
    main()
