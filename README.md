# AI-DATA
moist for cassandra( flask )


Tensorflow ( mnist )

宿主机：Pip install …【存在多个python版本时，pip安装路径为默认路径（ 易出现未安装在运行的python环境 ）。该情况创建虚拟环境，使用conda安装】
Docker容器内部署：apt-get install tensorflow【可能出现未找到该依赖库的情况】->apt-get update -> apt-get install tensorflow【若还是未能找到依赖库，则使用container内的pip安装】

Container内的pip安装：apt-get update -> apt-get install python-pip / apt-get install python3-pip

Code（ 预处理 ）：Opencv / PIL 
灰度图，像素设定，归一化处理

Ps：神经网络搭建（ tensorflow ）：https://www.bilibili.com/video/av17639833 





Docker

Container间bridge共享网络（ network ）：docker network create yournetworkname 【实现容器间通信的基础条件】

参考：http://blog.csdn.net/gezhonglei2007/article/details/51627821 

Dockerfile：ADD指令所添加的文件及文件夹需与.yml后缀的dockerfile描述文件在同一目录下。单一文件ADD：ADD yourfile.form     文件夹ADD：ADD  ./filename /文件的绝对路径/ 

参考：https://docs.docker.com/get-started/part2/#your-new-development-environment 




Linux

指令参考：http://www.runoob.com/linux/linux-command-manual.html  &  http://blog.csdn.net/immortality/article/details/792693 




Flask API

Flask基础：http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application

简单视频入门：https://www.bilibili.com/video/av10037876/?p=1 




Cassandra

Container（ Cassandra ）：创建包含cassandra服务的container时需与你需要链接的container处于同一network下，设定—network=thesamenetworkname
基于docker的Cassandra数据库使用：https://mannekentech.com/2017/01/02/playing-with-a-cassandra-cluster-via-docker/  and  https://hub.docker.com/_/cassandra/ 





Container（ mnist ）与 Container （ cassandra ）的链接

宿主机与container（ cassandra ）实现链接：  
cluster = Cluster([“0.0.0.0”],port=9042/9142…)
session = cluster.connect()

Container ( mnist )与container （ cassandra ）实现链接：  
cluster = Cluster(["yournetworkpath"],port=9142)
session = cluster.connect()
