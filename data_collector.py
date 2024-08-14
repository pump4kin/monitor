import sqlite3
import psutil
import time

def init_db():
    conn = sqlite3.connect('monitor.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS monitor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            cpu_usage REAL,
            memory_usage REAL
        )
    ''')
    conn.commit()
    conn.close()

def store_data(cpu, memory):
    conn = sqlite3.connect('monitor.db')
    c = conn.cursor()
    c.execute('INSERT INTO monitor_data (timestamp, cpu_usage, memory_usage) VALUES (?, ?, ?)',
              (time.strftime("%Y-%m-%d %H:%M:%S"), cpu, memory))
    conn.commit()
    conn.close()

def collect_data():
    # 指定挂载的目录
    proc_dir = '/host/proc'
    # sys_dir = '/host/sys'

    # 修改psutil的路径设置，使其指向宿主机的目录
    psutil.PROCFS_PATH = proc_dir
    # psutil.SYSFS_PATH = sys_dir

    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        store_data(cpu_percent, memory_percent)
        time.sleep(2)

if __name__ == "__main__":
    init_db()
    collect_data()
