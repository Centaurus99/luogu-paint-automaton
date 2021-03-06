import json, requests, time

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#delta_x = 500 # set to move the picture
#delta_y = 391 # real_x = gived_x + delta_x
delta_x = 0
delta_y = 0

headers = {
        'referer': 'https://www.luogu.org/paintBoard',
        'User-agent': 'wxw_ak_ioi'
}

cookies = { '__client_id': '', '_uid': '' }

def requests_get(url):
        while True:
                try:
                        req = requests.get(url, verify=False,headers=headers, cookies=cookies, timeout=10)
                        break
                except:
                        pass
        return req

def requests_post(url, data=None):
        while True:
                try:
                        req = requests.post(url, verify=False,headers=headers, cookies=cookies, data=data, timeout=10)
                        break
                except:
                        pass
        return req


def get_real_color(c):
        if len(c) > 1:
                return int(c)
        if ord(c) >= ord('a'):
                return ord(c) - ord('a') + 10
        else:
                return ord(c) - ord('0')

class info:
        def __init__(self, x, y, c):
                self.x = int(x) + delta_x
                self.y = int(y) + delta_y
                self.c = get_real_color(c)

global flag
global content
def get_board2():
        global content
        global flag
        if flag == 1:
                request = requests_get('https://www.luogu.org/paintBoard/board')
                with open('board.out', 'wb+') as file:
                        file.write(request.content)
                        file.close()
                content = str(request.content).split('\\n')
                print('--get request')
                flag = 0
                
        board = []
        for i in range(0, 800):
                line = []
                for j in range(0, 400):
                        color = content[i][j]
                        line.append(color)
                        # print(i, j, point)
                board.append(line)
        return board

def get_board():
        nowboard = []
        global flag
        while True:
                try:
                        nowboard = get_board2()
                        break
                except:
                        print('-----!!! request error !!!-----')
                        flag = 1
                        time.sleep(1)
        return nowboard

        
global nowstatus
def paint(x, y, color):
        data = { 'x': x, 'y': y, 'color': color }
        request = requests_post('https://www.luogu.org/paintBoard/paint', data=data)
        status = json.loads(request.content)['status']
        global nowstatus
        nowstatus = status
        if status == 200:
                print('[200] Success by', cookies['_uid'], '!')
        elif status == 401:
                print('[401] Not login.')
        elif status == 500:
                print('[500] Please wait for trying again.')
        else:
                print('[???] Unknown error.')

def get_todo():
        content = open('todo.list', 'r+').read()
        todolist = []
        for line in content.split('\n'):
                if len(line.split(' ')) < 3:
                        continue
                x, y, c = line.split(' ')
                todolist.append(info(x, y, c))
        return todolist


def check(x, y, color):
        board = get_board()
        now_color = get_real_color(board[x][y])
        #print('now_color:',now_color)
        #print('check (', todo.x, ',', todo.y, ') to', todo.c)
        if color == now_color:
                #print('True')
                return True
        else:
                #print('False')
                return False

def get_cookies():
        content = open('cookies.list', 'r+').read()
        cookies_list = []
        for line in content.split('\n'):
                cookies = {}
                if len(line.split(' ')) < 2:
                        continue
                cookies['__client_id'], cookies['_uid'] = line.split(' ')
                cookies_list.append(cookies)
        return cookies_list

def clear_todo(todolist):
        board = get_board()
        answer = []
        for todo in todolist:
                if get_real_color(board[todo.x][todo.y]) != todo.c:
                        answer.append(todo)
        return answer

user_list = get_cookies()
SleepLim =0
while True:
        print('')
        print('Start!!!')
        print('Top user :',user_list[0]['_uid'])
        global flag
        flag = 1
        todolist = clear_todo(get_todo())
        if len(todolist):
                print('length of todolist is', len(todolist))
                SleepLim = 0
        else:
                print('nothing to do.')
                SleepLim = 5
        print('Now SleepLim :',SleepLim)
        time.sleep(SleepLim)
        for todo in todolist:
                print('todo (', todo.x, ',', todo.y, ') to', todo.c)
                try:
                        while not check(todo.x, todo.y, todo.c):
                                print('paint (', todo.x, ',', todo.y, ') to', todo.c)
                                for userid in range(len(user_list)):
                                        cookies = user_list[userid]
                                        paint(todo.x, todo.y, todo.c)
                                        #print('nowstatus :',nowstatus)
                                        if nowstatus == 500:
                                                break
                                        if nowstatus == 200:
                                                flag = 1
                                                for j in range(userid,len(user_list)-1):
                                                        temp=user_list[j]
                                                        user_list[j]=user_list[j+1]
                                                        user_list[j+1]=temp
                                                break
                                     #   if check(todo.x, todo.y, todo.c):
                                     #           break
                except:
                        print('error')
