<!--
 * @Author: Alex
 * @LastEditors: Alex yxfacw@163.com
 * @Date: 2023-07-18 18:19:20
 * @Description:  
-->
## Starfall

原生 python3 定时调度执行器（适配 xxl-job）

### 环境

- python: 支持 python 3.9 +
- OS:  windows、MacOS、Linux
### 安装

```python

pip install starfall

```

### 使用

安装依赖后，需要在工程目录下提供一个配置文件 `conf.ini`, 并在其中设置以下参数:

```properties
[Executor]
PORT = 9002
NAME = demo-py-executor
ADMIN_URI = http://192.168.0.96:8088/job-admin
ACCESS_TOKEN =
```

> 参数根据实际填写

调用入口方法，启动服务：

```python
from starfall import init, start_serve
import os

PROJ_ROOT = os.path.dirname(os.path.abspath(__file__))
print(f'root: {PROJ_ROOT}')

init(PROJ_ROOT)
start_serve()
```

查看控制台输出，看到 `server started...` 表示服务启动成功


### 任务代码编写

- 在工程目录下新建 `jobs` 文件夹 （文件夹名称必须固定）

- 在`jobs`目录下新建任务代码

- 一个job示例：

```python
from starfall.helper import get_logger

def add(x, y):
    logger = get_logger('demo.add')
    logger.info(x+y)
    return x+y
```





