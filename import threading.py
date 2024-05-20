import threading
import time
import sys
import keyboard
# 创建一个事件对象
exit_event = threading.Event()

# 检测键盘输入的函数
def keyboard_listener():
    keyboard.wait('q')  # 等待用户按下 'q'
    exit_event.set()  # 设置事件，表示退出

# 打印数字的函数
def print_numbers():
    for i in range(1, 101):
        print(i)
        if exit_event.is_set():  # 检查事件是否被设置
            print("Exiting program...")
            sys.exit()  # 如果事件被设置，退出程序
        time.sleep(1)

# 创建线程
thread_keyboard = threading.Thread(target=keyboard_listener)
thread_print = threading.Thread(target=print_numbers)

# 启动线程
thread_keyboard.start()
thread_print.start()

# 等待线程结束
thread_print.join()

print("Program finished.")