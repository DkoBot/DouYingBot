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
'''
作者: https://github.com/DkoBot
配置:
    cookies_list : Cooke信息
    friends_list : 待续火花用户名
    OFF_ON_Aaiqky_TEXT : 是否使用爱情公寓金言金句作为回复
    OFF_ON_ERROR_Email : 续火花异常邮箱告知
    
'''
# 基础配置
cookies_list = []
friends_list = ''
OFF_ON_Aaiqky_TEXT = True
OFF_ON_ERROR_Email = True

# 邮箱配置 [QQ邮箱]
my_sender = '@qq.com'  # 填写发信人的邮箱账号
my_pass = ''  # 发件人邮箱授权码
my_user = '@qq.com'  # 收件人邮箱账号




service = Service(executable_path=r'C:\WebDriver\edge\msedgedriver.exe')
options = webdriver.EdgeOptions()
# 防封策略 勿动
def unban_config():
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
    print('🕰️ 请登录抖音.....')
    while for_OFF:
        try:
            # 尝试获取 login_type 元素
            login_type_element = driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[4]/div[1]/div[1]/header/div/div/div[2]/div/pace-island/div/div[5]/div/div[1]/button/span/p')
        except NoSuchElementException:
            cooke = driver.get_cookies()
            print(f'✅ Cooke获取成功,您的Cooke为 [请完整复制到cookies_list变量中]:\n{cooke}')
            driver.close()
            exit()

try:
    driver.get('https://www.douyin.com/')
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
        print('✅ Cooke有效,登录成功!')
    # 开始执行定时脚本 ⏭️
    time.sleep(6.5)
    def click_msg_button():
        msg_main_button = driver.find_element(By.XPATH, '//*[@id="island_b69f5"]/div/ul[2]')
        msg_main_button.click()

    click_msg_button()

    time.sleep(3)
    friends_xpath = '//*[@id="island_b69f5"]/div/ul[2]/div/li/div/div/div[3]/div/div/div[1]/div/div[2]/div[2]/div'
    msg_main_list = driver.find_elements(By.XPATH, value=friends_xpath)
    # 创建字典存储好友名称和对应的 XPath
    friends_dict = {}
    print('\n⏭️ 好友列表:\n------------------')
    for msg_len in range(1,len(msg_main_list)):
        click_msg_button()
        friends_get = driver.find_element(By.XPATH, value=friends_xpath + f'[{msg_len}]/div/div/div[2]/div[1]/div')
        friends_text = friends_get.text
        print(friends_text)
        friends_dict[friends_text] = friends_xpath + f'[{msg_len}]/div/div/div[2]/div[1]/div'
    print('------------------')

    if friends_list == '':
        print('❓ 未选择续火花用户..')
        friends_list = input('输入待续火花用户名称:')
    for key,value in friends_dict.items():
        if key==friends_list:
            friend_id = driver.find_element(By.XPATH, value=value)
            friend_id.click()
            print(f'✅ 已选择待续火花用户 {key}')
            break
        else:
            continue
    def send_message():
        try:
            time.sleep(2.5)
            seng_get= driver.find_element(By.XPATH,'//*[@id="island_b69f5"]/div/ul[2]/div/li/div/div/div[3]/div/div/div[2]/div/div[3]/div/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div')
            if OFF_ON_Aaiqky_TEXT:
                seng_get.send_keys(AiqingGongyu_text())
            else:
                seng_get.send_keys('我来续火花啦!')
            seng_get.send_keys(Keys.ENTER)
            print(f'✅ 火花已续成功 续时间:{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}')
        except Exception as e:
            if OFF_ON_ERROR_Email:
                print(f'⚠️ 火花续异常,将邮件通知管理员|{e}')
                Email_Send(str(e))
            else:
                print(f'⚠️ 火花续异常:{e}')
    play_time = input('🕰️ 输入每日续火花时间[默认为 22:00] :')
    play_time = play_time.replace('：',':')
    if play_time=='':
        play_time = '22:00'
    schedule.every().day.at(play_time).do(send_message)
    print(f'已完成基础设置,开始固定执行续火花任务✅ [当前续火花时间: {play_time}]')
    while True:
        schedule.run_pending()
        time.sleep(1)
finally:
    driver.quit()