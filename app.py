from flask import Flask, render_template, request
import sqlite3
import json
import datetime
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/cpu', methods=['GET'])
def get_cpu_data():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if '' == start_time:
        start_time = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')
    else:
        start_time = start_time.replace('T', ' ')

    if '' == end_time:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        end_time = end_time.replace('T', ' ')

    conn = sqlite3.connect('monitor.db')
    c = conn.cursor()
    c.execute('SELECT timestamp, cpu_usage FROM monitor_data WHERE timestamp BETWEEN ? AND ?',
              (start_time, end_time))
    rows = c.fetchall()
    data = [{'timestamp': row[0], 'cpu': row[1]} for row in rows]
    conn.close()

    return json.dumps(data)


@app.route('/data/memory', methods=['GET'])
def get_memory_data():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if '' == start_time:
        start_time = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')
    else:
        start_time = start_time.replace('T', ' ')

    if '' == end_time:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        end_time = end_time.replace('T', ' ')

    conn = sqlite3.connect('monitor.db')
    c = conn.cursor()
    c.execute('SELECT timestamp, memory_usage FROM monitor_data WHERE timestamp BETWEEN ? AND ?',
              (start_time, end_time))
    rows = c.fetchall()
    data = [{'timestamp': row[0], 'memory': row[1]} for row in rows]
    conn.close()

    return json.dumps(data)


if __name__ == '__main__':
    # 启动data_collector.py
    subprocess.Popen(["python", "data_collector.py"])
    # 运行Flask应用
    app.run(debug=True, port=5000)
