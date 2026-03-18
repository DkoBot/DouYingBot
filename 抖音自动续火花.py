from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time,schedule,smtplib,requests
from email.mime.text import MIMEText
from email.utils import formataddr
from datetime import datetime
from tqdm import tqdm
import configparser
'''
作者: https://github.com/DkoBot
项目路径: https://github.com/DkoBot/DouYingBot

配置:
    cookies_list : Cooke信息
    friends_list : 待续火花用户名
    OFF_ON_Aaiqky_TEXT : 是否使用爱情公寓金言金句作为回复
    OFF_ON_ERROR_Email : 续火花异常邮箱告知
    
'''
print('正在读取配置....')
# 基础配置
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini',encoding='utf-8')
cookies_list = config.get('DEFAULT', 'cookies_list', fallback='[]')
cookies_list = eval(cookies_list)

friends_list = config.get('DEFAULT', 'friends_list', fallback='')
# OFF_ON_Aaiqky_TEXT
OFF_ON_Aaiqky_TEXT = config.getboolean('DEFAULT', 'OFF_ON_Aaiqky_TEXT', fallback=True)
# OFF_ON_ERROR_Email
OFF_ON_ERROR_Email = config.getboolean('DEFAULT', 'OFF_ON_ERROR_Email', fallback=True)
# my_sender
my_sender = config.get('DEFAULT', 'my_sender', fallback='')
# my_pass
my_pass = config.get('DEFAULT', 'my_pass', fallback='')
# my_user
my_user = config.get('DEFAULT', 'my_user', fallback='')
print('✅ 配置读取成功')
OF_OFF_headless = input('是否可视游览器 [默认回车不显示]:')
if OF_OFF_headless:
    OF_OFF_headless = False
else:
    OF_OFF_headless = True


service = Service(executable_path=r'C:\WebDriver\edge\msedgedriver.exe')
options = webdriver.EdgeOptions()
# 防封策略 勿动
def unban_config():
    if OF_OFF_headless:
        options.add_argument("--headless")  # 启用无头模式
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('log-level=3')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.177 Safari/537.36")
    options.add_experimental_option('excludeSwitches', ['enable-automation', 'useAutomationExtension'])
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-web-security')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--start-maximized')
    options.add_argument("--force-device-scale-factor=0.25")
unban_config()
driver = webdriver.Edge(service=service, options=options)
def AiqingGongyu_text():
    req = requests.get('https://v2.xxapi.cn/api/aiqinggongyu')
    if req.status_code == 200:
        json_data = req.json()
        json_data = json_data['data']
        if json_data:
            return json_data
        else:
           return '暂无今日名言'
    else:
        return '暂无今日名言'
def Email_Send(ERROR_TEXT : str):
    try:
        html_content = f"""
        <html>

        <head>
            <style>
                body {{
                    font-family: 'Microsoft YaHei', Arial, sans-serif;
                    background: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
                    color: #2c3e50;
                    min-height: 100vh;
                    margin: 0;
                    padding: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}

                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 16px;
                    box-shadow: 0 15px 35px rgba(50, 50, 93, 0.1), 0 5px 15px rgba(0, 0, 0, 0.07);
                    overflow: hidden;
                    transition: transform 0.3s ease;
                }}

                .container:hover {{
                    transform: translateY(-5px);
                }}

                .header {{
                    text-align: center;
                    padding: 25px 0;
                    background: linear-gradient(120deg, #3a7bd5 0%, #00d2ff 100%);
                    color: #fff;
                    position: relative;
                }}

                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                    font-weight: 600;
                    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
                    letter-spacing: 0.5px;
                }}

                .content {{
                    padding: 30px;
                    line-height: 1.6;
                    background-color: #ffffff;
                }}

                .content p {{
                    margin: 0 0 15px;
                    color: #4a5568;
                    font-size: 15px;
                }}

                .content pre {{
                    background-color: #f8fafc;
                    padding: 18px;
                    border-radius: 10px;
                    border: 1px solid #e2e8f0;
                    overflow-x: auto;
                    color: #dc2626;
                    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                    font-size: 13.5px;
                    line-height: 1.5;
                    margin: 12px 0;
                    white-space: pre-wrap;
                    word-break: break-all;
                    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);
                }}

                .footer {{
                    text-align: center;
                    padding: 15px 0;
                    background: linear-gradient(120deg, #2c5282 0%, #1a365d 100%);
                    color: #fff;
                    font-size: 14px;
                }}

                .footer p {{
                    margin: 0;
                    opacity: 0.9;
                    letter-spacing: 0.5px;
                }}
            </style>
        </head>

        <body>
            <div class="container">
                <div class="header">
                    <h1>⚠️ 抖音续火花出现异常</h1>
                </div>
                <div class="content">
                    <p>尊敬的用户，</p>
                    <p>我们检测到抖音自动续火花出现异常，请及时查收。</p>
                    <p>错误日志：<br>
                    <pre>{ERROR_TEXT}</pre>
                    </p>
                </div>
                <div class="footer">
                    <p>抖音续火花BOT</p>
                </div>
            </div>
        </body>

        </html>
        """
        msg = MIMEText(html_content, 'html', 'utf-8')
        msg['From'] = formataddr(["抖音自动续费火花", my_sender])
        msg['To'] = formataddr(["抖音用户", my_user])
        msg['Subject'] = "抖音自动续火花出现异常"
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
    except Exception:
        print('⚠️ 邮件发送错误')
def Get_Cooke():
    driver.get('https://www.douyin.com/')
    for_OFF = True
    print('🕰️ 请登录抖音[且保持游览器为全屏!].....')
    while for_OFF:
        try:
            # 尝试获取 login_type 元素
            login_type_element = driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[4]/div[1]/div[1]/header/div/div/div[2]/div/pace-island/div/div[5]/div/div[1]/button/span/p')
        except NoSuchElementException:
            cooke = driver.get_cookies()
            print(f'✅ Cooke获取成功,您的Cooke为 [请完整复制到cookies_list变量中]:\n{cooke}')
            driver.close()
            exit()
def format_time(time_str: str) -> str:
    """
    将时间字符串格式化为 HH:MM 格式
    例如: "9:23" -> "09:23", "9:5" -> "09:05", "09:23" -> "09:23"
    """
    if not time_str:
        return '22:00'

    # 统一替换中文冒号
    time_str = time_str.replace('：', ':').strip()

    try:
        # 分割小时和分钟
        parts = time_str.split(':')
        if len(parts) != 2:
            print(f'⚠️ 时间格式错误，使用默认时间 22:00')
            return '22:00'

        hour = int(parts[0])
        minute = int(parts[1])

        # 验证范围
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            print(f'⚠️ 时间范围错误，使用默认时间 22:00')
            return '22:00'

        # 格式化为两位数字
        return f"{hour:02d}:{minute:02d}"

    except ValueError:
        print(f'⚠️ 时间解析错误，使用默认时间 22:00')
        return '22:00'
class Douyin:
    friends_xpath_list = {}
    def __init__(self, driver):
        self.driver = driver  # 将 driver 作为实例属性
    def PrintfFrinder(self):

        print(f'\n⏭️ 好友列表 共获取{len(self.friends_xpath_list)}位:\n------------------')
        for index,value in self.friends_xpath_list.items():
            print(index)
        print('------------------')
    def Updara_FrinderList(self):
        friends_xpath = '//div[@class="conversationConversationListwrapper"]/div/div/div'
        msg_main_list = driver.find_elements(By.XPATH,friends_xpath)
        count = len(msg_main_list)
        for msg_len in range(1, len(msg_main_list) + 1):
            new_xpath = f'//div[@class="conversationConversationListwrapper"]/div/div[{msg_len+1}]/div[1]/div[2]/div[1]/div[1]'
            friends_get = driver.find_element(By.XPATH, value=new_xpath)
            friends_text = friends_get.text
            self.friends_xpath_list[friends_text] = new_xpath
        return count

    def Send_Frinder(self,name:str,text:str):
        count = self.Updara_FrinderList()
        if count==0:
            if OFF_ON_ERROR_Email:
                Email_Send(str("⚠️ 更新好友列表失败!"))
            print("⚠️ 更新好友列表失败!")
        else:
            try:
                for index,value in self.friends_xpath_list.items():
                    if index==name:
                        friend_id = driver.find_element(By.XPATH, value=value)
                        friend_id.click()
                        time.sleep(1.5)
                        seng = driver.find_element(By.XPATH, value='//div[@class="messageEditorimChatEditorContainer"]/div/div')
                        seng.send_keys(text)
                        seng.send_keys(Keys.ENTER)
                        print(f'✅ {text} | 火花已续成功 续时间:{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}')
            except Exception as e:
                print(f'⚠️ {text}  | 火花续异常:{e}')
                if OFF_ON_ERROR_Email:
                    Email_Send(str(e))




try:
    driver.set_window_size(1400, 3200)
    driver.get('https://www.douyin.com/chat?isPopup=1')
    if cookies_list:
        for cookie in tqdm(cookies_list, desc="Cooke载入中.."):
            driver.add_cookie(cookie)
    else:
        Get_Cooke()
        driver.quit()
        exit()
    print('开始登录....')
    driver.refresh()
    try:
        login_type_element = driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[4]/div[1]/div[1]/header/div/div/div[2]/div/pace-island/div/div[5]/div/div[1]/button/span/p')
        login_type = login_type_element.text
        print('⚠️ Cooke无效,请重新获取登录后的Cooke!')
        driver.quit()
        exit()
    except NoSuchElementException:
        print('✅ Cooke有效,登录成功! [请勿操作游览器]')
    douyin = Douyin(driver)
    # 开始执行定时脚本 ⏭️
    time.sleep(7.5)
    while True:
        friends_count = Douyin.Updara_FrinderList(douyin)
        if friends_count==0:
            driver.refresh()
            time.sleep(30.5)
        if friends_count!=0:
            break
    Douyin.PrintfFrinder(douyin)
    if friends_list == '':
        print('❓ 配置文件未选择续火花用户..')
        friends_list = input("请输入待续火花用户名称(多个用户用分号';'分隔):")
        friends_list = friends_list.split(';')
    else:
        print('配置文件已存在待续火花用户,已加载!')
        friends_list = friends_list.split(';')
    play_time = input('请输入每日续火花时间[默认为 22:00] :')
    play_time = play_time.replace('：', ':')
    if play_time == '':
        play_time = '22:00'
    play_time = format_time(play_time)
    text = ""
    if OFF_ON_Aaiqky_TEXT == False:
        text = input('续火文本:')
    for user in friends_list:
        schedule.every().day.at(play_time).do(
            lambda u=user: douyin.Send_Frinder(u, AiqingGongyu_text() if OFF_ON_Aaiqky_TEXT else text)
        )
    print(f'已完成基础设置,开始固定执行续火花任务✅ [当前续火花时间: {play_time}]')
    while True:
        schedule.run_pending()
        time.sleep(1)
finally:
    driver.quit()
