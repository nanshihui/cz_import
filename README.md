# cz_import
将纯真IP数据导入mysql数据库

## 使用说明
１．先下载纯真IP数据软件，点击解压成txt。然后将解压的文件重命名为czdata.txt放置于当前目录下。		
２．创建数据库名字为proxy_db		
３．创建一张表存放纯真数据。建表语句如下：		
```mysql
CREATE TABLE IF NOT EXISTS `iprange_info` (
  `start` varchar(32) NOT NULL,
  `end` varchar(32) NOT NULL,
  `location` varchar(100) NOT NULL,
  `detail` varchar(200) NOT NULL,
  PRIMARY KEY (`start`, `end`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

４．运行　python czdata_import.py 即可。

注：　如果你的数据库和我的数据库名不一致，需要在代码57行改成对应你的数据库相关配置。
