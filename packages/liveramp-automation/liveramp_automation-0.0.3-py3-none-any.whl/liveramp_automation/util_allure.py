import allure


# Call allure_page_screenshot to show the screenshot while using Playright
def allure_page_screenshot(page, name):
    allure.attach(page.screenshot(), name=name, attachment_type=allure.attachment_type.PNG)


# Call allure_drive_screenshot to show the screenshot while using Selenium
def allure_drive_screenshot(driver, name):
    allure.attach(driver.save_screenshot(), name=name, attachment_type=allure.attachment_type.PNG)


# Call allure_attach_video to show the recording video,the video path should be provided.
def allure_attach_video(path, video_name):
    allure.attach.file(path, name=video_name, attachment_type=allure.attachment_type.MP4)


# Call allure_attach_text to show the content in text format.
def allure_attach_text(content, description):
    allure.attach(content, description, attachment_type=allure.attachment_type.TEXT)


# Call allure_attach_json to show the content in json format.
def allure_attach_json(content, description):
    allure.attach(content, description, attachment_type=allure.attachment_type.JSON)
