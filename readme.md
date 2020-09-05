## elasticsearch实现faq检索召回

### 1. 环境
&nbsp;&nbsp; python3.6 + elasticsearch7.7.0 + requierments.txt

### 2. 启动
#### 2.1 启动es
    xxx$ cd es_path/bin
    xxx$ ./ elasticsearch
#### 2.1 启动es可视化工具cerebro
    xxx$ cd cerebro_path/bin
    xxx$ cerebro

### 3. 注意事项
1. 安装过程中会出现各种问题，百度自行解决即可
2. 安装ik中文分词器，在esplugins的目录下新建ik文件夹，下载后解压将目录里文件全部复制至ik文件夹中
3. 注意：ik分词器版本一定要与es版本一致, 不然启动es时候会报版本不兼容错误
要添加自定义词典，进入ik目录下的config文件夹IKAnalyzer.cfg.xml
将扩展词典的注释去掉，填入自己的自定义词典路径即可。