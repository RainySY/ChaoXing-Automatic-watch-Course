# # 用来判断属性值是否存在
# def isElementPresent(browser, by, value):
#     from selenium.common.exceptions import NoSuchFrameException
#     """
#     用来判断元素标签是否存在，
#     """
#     try:
#         element = browser.find_element(by=by, value=value)
#     # 原文是except NoSuchElementException, e:
#     except NoSuchElementException as e:
#         # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
#         return False
#     else:
#         # 没有发生异常，表示在页面中找到了该元素，返回True
#         return True
