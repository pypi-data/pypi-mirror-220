import allure


def allure_page_screenshot(page, name):
    allure.attach(page.screenshot(), name=name, attachment_type=allure.attachment_type.PNG)


def allure_page_screenshot(driver, name):
    allure.attach(driver.save_screenshot(), name=name, attachment_type=allure.attachment_type.PNG)


def allure_attach_video(path, video_name):
    allure.attach.file(path, name=video_name, attachment_type=allure.attachment_type.MP4)


def allure_attach_text(description, content):
    allure.attach(description, content, attachment_type=allure.attachment_type.TEXT)


def allure_attach_json(description, content):
    allure.attach(description, content, attachment_type=allure.attachment_type.JSON)
