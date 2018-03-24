# -*- coding:utf-8 -*-
import os
from flask import Flask, request, url_for, send_from_directory
from werkzeug import secure_filename
import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO
import time
from cassandra.cluster import Clust


"""
post 上传图片允许的格式设置
像素，支持格式
"""
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


"""
html表单，可视化上传界面
"""

html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>upload</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=上传>
    </form>
    '''


"""
读取以存在的训练模型
"""
def model_ini():
    sess = tf.Session()
    saver = tf.train.import_meta_graph("./tmp/model.ckpt.meta")
    saver.restore(sess,tf.train.latest_checkpoint('./tmp'))
    return sess


"""
数字识别函数
"""
def Number_recognition(file,sess):
    im = Image.open(BytesIO(file))
    imout=im.convert('L')
    xsize, ysize=im.size
    if xsize != 28 or ysize!=28:
        imout=imout.resize((28,28),Image.ANTIALIAS)
    arr = []
    for i in range(28):
        for j in range(28):
            pixel = float(1.0 - float(imout.getpixel((j, i)))/255.0)
            arr.append(pixel)
    keep_prob=tf.get_default_graph().get_tensor_by_name('dropout/Placeholder:0')
    x=tf.get_default_graph().get_tensor_by_name('x:0')
    y=tf.get_default_graph().get_tensor_by_name('fc2/add:0')
    arr1 = np.array(arr).reshape((1,28*28))
    pre_vec=sess.run(y,feed_dict={x:arr1,keep_prob:1.0})
    pre=str(np.argmax(pre_vec[0],0))+'\n'
    return pre



"""
建立数据库链接，构建数据库的界面
"""

def database_ini():
    cluster = Cluster(["172.20.0.1"],port=9142)
    session = cluster.connect()
    keyspacename='mnist'
    session.execute("create keyspace if not exists mnist with replication = {'class': 'SimpleStrategy', 'replication_factor': 1};")
    session.set_keyspace('mnist')
    session.execute("create table if not exists picdatabase(timestamp double, filedata blob ,answer int ,primary key(timestamp));")
    return session



"""
传输数据进cassandra的功能函数
"""

def database_insert(session,file,pre):
    times=time.time()
    params=[times,bytearray(file),int(pre)]
    session.execute("INSERT INTO picdatabase (timestamp,filedata,answer) VALUES (%s, %s,%s)",params)
    result=session.execute("SELECT * FROM picdatabase")
    for x in result:
        print (x.timestamp,x.filedata,x.answer)
    return 0


#将数据读取出来传递给其他函数使用
sess=model_ini()
session=database_ini()

"""
基于flask框架的图片上传函数
"""

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')

def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/', methods=['GET', 'POST'])

def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):


            data = file.read()

            pre=Number_recognition(data,sess)
            database_insert(session,file,pre)

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = url_for('uploaded_file', filename=filename)
            return pre
            #下一行代码为返回一个网页显示你上传的图片和结果，根据需求选择是否使用
            #return html + '<br><img src=' + file_url + '>' + pre

    return html


#使该程序运行在主机段的80端口
if __name__ == '__main__':
    app.run('0.0.0.0',port=80)






