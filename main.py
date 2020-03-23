from selenium import webdriver  # 导入库
from time import sleep
from signIn import check_sign_in

from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException
from selenium.webdriver.support.ui import WebDriverWait


options = webdriver.ChromeOptions()
options.add_argument('disable-infobars')
options.add_experimental_option('excludeSwitches', ['enable-automation'])


browser = webdriver.Chrome(
    executable_path="./chromedriver.exe", options=options)  # 双引号内添加浏览器驱动的地址
# browser = webdriver.Edge(executable_path="./msedgedriver.exe")
url = "http://i.chaoxing.com/"
browser.get(url)


def input_usename_and_password(browser):
    inp = input("请输入账号:")
    inp_2 = input("请输入密码:")
    # # inp_3=input("请输入验证码:")
    # inp_3 = input("请输入验证码:")
    browser.find_element_by_xpath(
        '/html/body/div/div[2]/div/div[1]/div[1]/ul/li[2]').click()

    username = browser.find_element_by_id("uin_tips")
    password = browser.find_element_by_id("pwd_tips")
    # verycode = browser.find_element_by_id("numcode")
    username.send_keys(inp)
    password.send_keys(inp_2)
    # verycode.send_keys(inp_3)
    sbm = browser.find_element_by_id("login")
    # sleep(1)
    sbm.click()


# 一级页面跳转,进入首页，开始选择课程
def level_1st(schedule_name):
    browser.switch_to.window(browser.window_handles[0])
    browser.switch_to.default_content()
    browser.switch_to.frame("frame_content")
    # 进入首页，开始选择课程
    # sleep(1)
    schedule_list = browser.find_element_by_xpath(
        '/html/body/div[1]/div[2]/div[2]/ul').find_elements_by_xpath('li')
    # print(schedule_list)
    # print(len(schedule_list))
    # print(schedule_list)
    #
    for i in range(1, len(schedule_list)):
        schedule = browser.find_element_by_xpath(
            f'/html/body/div[1]/div[2]/div[2]/ul/li[{i}]/div[2]/h3/a')
        # print(schedule)
        # print(schedule.get_attribute('title'))
        if schedule_name in schedule.get_attribute('title'):
            schedule.click()
            # sleep(1)
            browser.switch_to.window(browser.window_handles[-1])  # 切换到最新打开的窗口
            return True
    print("没有找到该课程")
    return False
    # print(i)
    # # 引号内添加要刷的相应那门课程的xpath
    # c_click = browser.find_element_by_xpath("")
    # c_click.click()

    # # li_click = browser.find_element_by_xpath("")
    # # browser.execute_script("window.scrollT0(0,3000)")
    # # browser.back()#向后退 前进是forward（）
    # sleep(1)
    # browser.switch_to.window(browser.window_handles[-1])


# 判断是否有通知
def if_tongzhi():
    print('开始判断是否有通知！')
    sleep(1)
    judge = 1
    while judge:
        try:
            print('尝试关闭')
            cloes_widow = browser.find_element_by_xpath(
                "/html/body/div[10]/div/a")
            # '/html/body/div[10]/div/a'
            cloes_widow.click()
            # print(111)
        except:
            print("没有通知弹窗")
            judge = 0
            # pass


def auto_play_first_not_play_video():
    units_list = browser.find_elements_by_class_name("units")
    # print(units_list)
    # print('units_list', len(units_list))
    for units_num in range(1, len(units_list) + 1):
        # print('units_num', units_num)
        lesson_list = browser.find_elements_by_xpath(
            f'/html/body/div[5]/div[1]/div[2]/div[3]/div[{units_num}]/div')
        # print('lesson_list', len(lesson_list))
        for lesson_num in range(1, len(lesson_list) + 1):
            # print('units_num, lesson_num', units_num, lesson_num)
            class_name = browser.find_element_by_xpath(
                f'/html/body/div[5]/div[1]/div[2]/div[3]/div[{units_num}]/div[{lesson_num}]/h3/span[2]/em').get_attribute('class')
            # print(class_name)
            if class_name != 'openlock':
                browser.find_element_by_xpath(
                    f'/html/body/div[5]/div[1]/div[2]/div[3]/div[{units_num}]/div[{lesson_num}]/h3/span[3]/a').click()
                return 1
    return 0


# 进入视频并且播放
def into_vedio_window():
    # sleep(1)
    if_tongzhi()
    if not auto_play_first_not_play_video():
        print('该课程视频任务点已全部完成！')
        return False
    # browser.find_element_by_xpath("").click()  # 引号内添加从“哪节课开始”的那节课的XPATH
    # sleep(2)
    return True

# 播放课


def play_vedio(video_num):
    # sleep(1)

    # browser.switch_to.frame("iframe")
    # 这里有一个嵌套iframe
    browser.switch_to.frame(video_num)
    # begin_vedio = browser.find_element_by_xpath(
    #     "//*[@id='video']/button").click()
    wait = WebDriverWait(browser, 20)
    wait.until(lambda wait_driver: browser.find_element_by_xpath(
        "//*[@id='video']/button"))
    browser.find_element_by_xpath(
        "//*[@id='video']/button").click()
    # sleep(3)
    print("课程已经开始播放")


# 判断是否有答题框，其实这个逻辑挺简单的，只不过我不知道怎么触发答题框，
# 选择题的话依次选择ABCD直到对了就可以
def if_question():
    pass


# 判断视频是否完成
def check_vedio_play_finished():
    sleep(2)
    while(True):
        try:
            browser.find_element_by_xpath(
                "//*[@id='video']/div[4]/div[2]/span[2]").click()
            sleep(0.6)
            vedio_current_time = browser.find_element_by_xpath(
                "//*[@id='video']/div[4]/div[2]/span[2]").text
            vedio_end_time = browser.find_element_by_xpath(
                "//*[@id='video']/div[4]/div[4]/span[2]").text
            play_button_class_name = browser.find_element_by_xpath(
                '//*[@id="video"]/div[4]/button[1]').get_attribute('class')
            if 'vjs-paused' in play_button_class_name:
                # sleep(1)
                browser.find_element_by_xpath(
                    '//*[@id="video"]/div[4]/button[1]').click()
        except:
            continue
        else:
            vedio_current_time_split = vedio_current_time.split(':')
            vedio_end_time_split = vedio_end_time.split(':')
            remainder_time = (int(vedio_end_time_split[0]) - int(vedio_current_time_split[0])) * \
                60 + int(vedio_end_time_split[1]) - \
                int(vedio_current_time_split[1])
            print("当前时间是：" + vedio_current_time)
            print("结束时间是：" + vedio_end_time)
            print("剩余时间是：", remainder_time, '秒')
            if vedio_current_time == vedio_end_time:
                return
            sleep(5)  # 每10秒检测一次视频是否完成


# 判断有第二节课吗有就播放
def if_have_2nd_class(vedio_current_time, vedio_end_time):
    if vedio_current_time == vedio_end_time:
        try:
            # 开始播放第二个视频
            browser.switch_to.default_content()
            browser.switch_to.frame("iframe")
            browser.switch_to.frame(1)
            browser.find_element_by_xpath("//*[@id='video']/button").click()
            sleep(3)

        except:
            # pass
            print("没有第二节课了")


def is_video_task_completion(iframe_lists, video_num):
    # video_task_class_name = browser.find_element_by_xpath(
    #     f'/html/body/div[1]/div/p[{video_num}]/div').get_attribute('class')
    video_task_class_name = browser.find_element_by_class_name(
        'ans-attach-ct').get_attribute('class')
    video_task_class_name = iframe_lists[video_num].find_element_by_xpath(
        '..').get_attribute('class')
    print(video_task_class_name)
    if 'ans-job-finished' in video_task_class_name:
        return True
    else:
        return False


def is_can_start_next():
    xpath_address = '//*[@id="right2"]'
    try:
        # print("跳转错误处理！")
        browser.switch_to.default_content()
        # print("开始点下一页")
        next_page_class_name = browser.find_element_by_xpath(
            xpath_address).get_attribute('class')

        print(next_page_class_name)
        if 'gray' in next_page_class_name:
            return False
        # print("?????????????????????????")
        # sleep(0.5)
        # browser.find_element_by_xpath(
        #     "/html/body/div[3]/div/div[2]/div[1]/div[4]").click()
        # sleep(0.5)
        # browser.find_element_by_xpath(
        #     "/html/body/div[3]/div/div[2]/div[1]/div[6]").click()
        # sleep(0.5)
        # browser.find_element_by_xpath(
        #     "/html/body/div[3]/div/div[2]/div[1]/div[8]").click()
        # sleep(0.5)
    except:
        xpath_address = '//*[@id="mainid"]/div[1]/div[2]'

    return True


def start_next():
    try:
        print("跳转错误处理！")
        # browser.switch_to.default_content()
        print("开始点下一页")
        browser.find_element_by_xpath(
            '//*[@id="right2"]').click()
        # print("?????????????????????????")
        # sleep(0.5)
        # browser.find_element_by_xpath(
        #     "/html/body/div[3]/div/div[2]/div[1]/div[4]").click()
        # sleep(0.5)
        # browser.find_element_by_xpath(
        #     "/html/body/div[3]/div/div[2]/div[1]/div[6]").click()
        # sleep(0.5)
        # browser.find_element_by_xpath(
        #     "/html/body/div[3]/div/div[2]/div[1]/div[8]").click()
        # sleep(0.5)
    except:
        print("开始点没有小节的下一页")
        browser.switch_to.default_content()
        browser.find_element_by_xpath(
            "//*[@id='mainid']/div[1]/div[2]").click()
        sleep(1)
        # pass
    # else:
    #     sleep(3)


if __name__ == '__main__':
    # input_usename_and_password(browser)

    user_name = check_sign_in(browser)
    print(user_name, '登陆成功！欢迎回来！')
    while True:
        # schedule_name = input('请输入您要学习的课程名称：')
        have_schedule = level_1st('中国近现代史纲要')

        # bool_into_video_window = False
        while (not have_schedule) or (not into_vedio_window()):
            if have_schedule:
                browser.close()  # 关闭当前页面
            # browser.switch_to.window(browser.window_handles[0])
            schedule_name = input('请输入您要学习的课程名称：')
            have_schedule = level_1st(schedule_name)
        # start_next(0, 0)
        # if_tongzhi()
        while True:
            # print("一次循环开始！")
            video_count = 0
            while not video_count:
                wait = WebDriverWait(browser, 20)
                wait.until(lambda wait_driver: browser.find_element_by_xpath(
                    '//*[@id="iframe"]'))
                browser.switch_to.frame('iframe')
                sleep(2)
                iframe_lists = browser.find_elements_by_tag_name('iframe')
                video_count = len(iframe_lists)
                print('iframe个数：', video_count)
                if not video_count:
                    if not is_can_start_next():
                        break
                    # sleep(2)
                    start_next()

                # try:
                #     if len(browser.find_elements_by_tag_name('iframe')):
                #         have_video = True
                #     print('iframe个数：', len(browser.find_elements_by_tag_name('iframe')))
                #     # wait = WebDriverWait(browser, 5)
                #     # wait.until(lambda wait_driver: browser.switch_to.frame(0))
                # except NoSuchFrameException:
                #     start_next()
                # except NoSuchElementException:
                #     start_next()
            # print('iframe个数：', len(browser.find_elements_by_tag_name('iframe')))
            # print("一次循环结束！")
            for video_num in range(video_count):
                print(f'第 {video_num + 1} 个视频/共 {video_count} 个视频')
                if not is_video_task_completion(iframe_lists, video_num):
                    print("开始播放视频！")
                    play_vedio(video_num)
                    check_vedio_play_finished()
                    browser.switch_to.default_content()
                    browser.switch_to.frame('iframe')

            if is_can_start_next():
                start_next()
            else:
                break

        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        level_1st('中国近现代史纲要')
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        if not into_vedio_window():
            choice = int(input('是否继续学习其他课程：（1、继续，2、停止并关闭）：'))
            if choice == 1:
                continue
            else:
                break
            # time_tuple = if_vedio_finished()
        #     while time_tuple[0] != time_tuple[1]:
        #         time_tuple = if_vedio_finished()
        #         try:
        #             if_have_2nd_class(time_tuple[0], time_tuple[1])
        #             if time_tuple[0] == time_tuple[1]:
        #                 print("开始测试第二节课时间")
        #                 time_tuple_2 = if_vedio_finished()
        #                 while time_tuple_2[0] != time_tuple_2[1]:
        #                     time_tuple_2 = if_vedio_finished()
        #                     start_next(time_tuple_2[0], time_tuple_2[1])
        #         except:
        #             start_next(time_tuple[0], time_tuple[1])

        browser.quit()
