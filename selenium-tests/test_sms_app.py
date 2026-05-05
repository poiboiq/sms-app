import uuid
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def unique_id():
    return uuid.uuid4().hex[:8]


def open_path(driver, base_url, path):
    driver.get(base_url + path)


def wait_for_text(driver, text, timeout=10):
    WebDriverWait(driver, timeout).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), text)
    )


def body_text(driver):
    return driver.find_element(By.TAG_NAME, "body").text


def submit_button(driver, text):
    return driver.find_element(By.XPATH, f"//button[normalize-space()='{text}']")


def click_link(driver, text):
    driver.find_element(By.LINK_TEXT, text).click()


def fill_student_form(driver, name, email, phone="0300-0000000", department="Computer Science"):
    driver.find_element(By.NAME, "name").clear()
    driver.find_element(By.NAME, "name").send_keys(name)
    driver.find_element(By.NAME, "email").clear()
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "phone").clear()
    driver.find_element(By.NAME, "phone").send_keys(phone)
    Select(driver.find_element(By.NAME, "department")).select_by_visible_text(department)


def fill_course_form(driver, name, code, credits="3", instructor="Dr. Test"):
    driver.find_element(By.NAME, "name").clear()
    driver.find_element(By.NAME, "name").send_keys(name)
    driver.find_element(By.NAME, "code").clear()
    driver.find_element(By.NAME, "code").send_keys(code)
    Select(driver.find_element(By.NAME, "credits")).select_by_value(str(credits))
    driver.find_element(By.NAME, "instructor").clear()
    driver.find_element(By.NAME, "instructor").send_keys(instructor)


def create_student(driver, base_url, suffix=None):
    suffix = suffix or unique_id()
    name = f"Test Student {suffix}"
    email = f"student_{suffix}@example.com"
    open_path(driver, base_url, "/students/add")
    fill_student_form(driver, name, email, "0311-1111111", "Artificial Intelligence")
    submit_button(driver, "Add Student").click()
    wait_for_text(driver, "Student added successfully!")
    return name, email


def create_course(driver, base_url, suffix=None):
    suffix = suffix or unique_id()
    name = f"Test Course {suffix}"
    code = f"TST{suffix[:5].upper()}"
    open_path(driver, base_url, "/courses/add")
    fill_course_form(driver, name, code, "4", "Dr. Selenium")
    submit_button(driver, "Add Course").click()
    wait_for_text(driver, "Course added successfully!")
    return name, code


def test_01_dashboard_loads(driver, base_url):
    open_path(driver, base_url, "/")
    wait_for_text(driver, "Welcome to SMS")
    assert "TOTAL STUDENTS" in body_text(driver)
    assert "TOTAL COURSES" in body_text(driver)
    assert "TOTAL ENROLLMENTS" in body_text(driver)


def test_02_students_page_loads(driver, base_url):
    open_path(driver, base_url, "/students")
    wait_for_text(driver, "Students")
    assert "+ Add Student" in body_text(driver)


def test_03_courses_page_loads(driver, base_url):
    open_path(driver, base_url, "/courses")
    wait_for_text(driver, "Courses")
    assert "+ Add Course" in body_text(driver)


def test_04_enrollments_page_loads(driver, base_url):
    open_path(driver, base_url, "/enrollments")
    wait_for_text(driver, "Enrollments")
    assert "+ Add Enrollment" in body_text(driver)


def test_05_navigation_links_work(driver, base_url):
    open_path(driver, base_url, "/")
    click_link(driver, "Students")
    wait_for_text(driver, "Students")
    click_link(driver, "Courses")
    wait_for_text(driver, "Courses")
    click_link(driver, "Enrollments")
    wait_for_text(driver, "Enrollments")
    click_link(driver, "Dashboard")
    wait_for_text(driver, "Welcome to SMS")


def test_06_add_student_success(driver, base_url):
    name, email = create_student(driver, base_url)
    assert name in body_text(driver)
    assert email in body_text(driver)


def test_07_duplicate_student_email_shows_error(driver, base_url):
    suffix = unique_id()
    _, email = create_student(driver, base_url, suffix)
    open_path(driver, base_url, "/students/add")
    fill_student_form(driver, f"Duplicate {suffix}", email, "0322-2222222", "Data Science")
    submit_button(driver, "Add Student").click()
    wait_for_text(driver, "Error:")
    assert "Error:" in body_text(driver)


def test_08_edit_student_success(driver, base_url):
    suffix = unique_id()
    _, email = create_student(driver, base_url, suffix)
    open_path(driver, base_url, "/students")
    edit_link = driver.find_element(By.XPATH, f"//tr[td[contains(., '{email}')]]//a[normalize-space()='Edit']")
    edit_link.click()
    updated_name = f"Updated Student {suffix}"
    fill_student_form(driver, updated_name, email, "0399-9999999", "Cyber Security")
    submit_button(driver, "Save Changes").click()
    wait_for_text(driver, "Student updated successfully!")
    assert updated_name in body_text(driver)
    assert "Cyber Security" in body_text(driver)


def test_09_delete_student_success(driver, base_url):
    suffix = unique_id()
    _, email = create_student(driver, base_url, suffix)
    open_path(driver, base_url, "/students")
    delete_link = driver.find_element(By.XPATH, f"//tr[td[contains(., '{email}')]]//a[normalize-space()='Delete']")
    delete_link.click()
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    wait_for_text(driver, "Student deleted successfully!")
    assert email not in body_text(driver)


def test_10_add_course_success(driver, base_url):
    name, code = create_course(driver, base_url)
    assert name in body_text(driver)
    assert code in body_text(driver)


def test_11_duplicate_course_code_shows_error(driver, base_url):
    suffix = unique_id()
    _, code = create_course(driver, base_url, suffix)
    open_path(driver, base_url, "/courses/add")
    fill_course_form(driver, f"Duplicate Course {suffix}", code, "3", "Dr. Duplicate")
    submit_button(driver, "Add Course").click()
    wait_for_text(driver, "Error:")
    assert "Error:" in body_text(driver)


def test_12_edit_course_success(driver, base_url):
    suffix = unique_id()
    _, code = create_course(driver, base_url, suffix)
    open_path(driver, base_url, "/courses")
    edit_link = driver.find_element(By.XPATH, f"//tr[td[contains(., '{code}')]]//a[normalize-space()='Edit']")
    edit_link.click()
    updated_name = f"Updated Course {suffix}"
    fill_course_form(driver, updated_name, code, "2", "Dr. Updated")
    submit_button(driver, "Save Changes").click()
    wait_for_text(driver, "Course updated successfully!")
    assert updated_name in body_text(driver)
    assert "Dr. Updated" in body_text(driver)


def test_13_delete_course_success(driver, base_url):
    suffix = unique_id()
    _, code = create_course(driver, base_url, suffix)
    open_path(driver, base_url, "/courses")
    delete_link = driver.find_element(By.XPATH, f"//tr[td[contains(., '{code}')]]//a[normalize-space()='Delete']")
    delete_link.click()
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    wait_for_text(driver, "Course deleted successfully!")
    assert code not in body_text(driver)


def test_14_add_enrollment_success(driver, base_url):
    suffix = unique_id()
    student_name, _ = create_student(driver, base_url, suffix)
    course_name, course_code = create_course(driver, base_url, suffix)
    open_path(driver, base_url, "/enrollments/add")
    Select(driver.find_element(By.NAME, "student_id")).select_by_visible_text(student_name)
    Select(driver.find_element(By.NAME, "course_id")).select_by_visible_text(f"{course_name} ({course_code})")
    Select(driver.find_element(By.NAME, "grade")).select_by_visible_text("A")
    submit_button(driver, "Enroll Student").click()
    wait_for_text(driver, "Enrollment added successfully!")
    assert student_name in body_text(driver)
    assert course_name in body_text(driver)
    assert "A" in body_text(driver)


def test_15_delete_enrollment_success(driver, base_url):
    suffix = unique_id()
    student_name, _ = create_student(driver, base_url, suffix)
    course_name, course_code = create_course(driver, base_url, suffix)
    open_path(driver, base_url, "/enrollments/add")
    Select(driver.find_element(By.NAME, "student_id")).select_by_visible_text(student_name)
    Select(driver.find_element(By.NAME, "course_id")).select_by_visible_text(f"{course_name} ({course_code})")
    Select(driver.find_element(By.NAME, "grade")).select_by_visible_text("B+")
    submit_button(driver, "Enroll Student").click()
    wait_for_text(driver, "Enrollment added successfully!")
    open_path(driver, base_url, "/enrollments")
    remove_link = driver.find_element(By.XPATH, f"//tr[td[contains(., '{student_name}')]]//a[normalize-space()='Remove']")
    remove_link.click()
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    wait_for_text(driver, "Enrollment removed successfully!")
    assert student_name not in body_text(driver)


def test_16_students_api_returns_json(base_url):
    response = requests.get(base_url + "/api/students", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "name" in data[0]
    assert "email" in data[0]


def test_17_courses_api_returns_json(base_url):
    response = requests.get(base_url + "/api/courses", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "name" in data[0]
    assert "code" in data[0]


def test_18_enrollments_api_returns_json(base_url):
    response = requests.get(base_url + "/api/enrollments", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
