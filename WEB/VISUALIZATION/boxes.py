from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def get_java_script(color: str) -> str:
    return f"""
    arguments[0].style.border = "3px solid {color}";
    """


target_elements = {
    "link": "blue",
    "a": "blue",
    "input": "green",
    "textarea": "green",
}

non_targed_elements = {
    "div",
    "body",
    "html",
    "head",
    "script",
    "style",
    "meta",
}


def draw_box(element: WebElement, driver: WebDriver) -> bool:
    if element.tag_name in target_elements:
        color = target_elements[element.tag_name]
        script = get_java_script(color)
        driver.execute_script(script, element)
        return True

    if element.text:
        script = get_java_script("red")
        driver.execute_script(script, element)
        return True

    return False
