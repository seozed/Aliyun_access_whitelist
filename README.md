# 定时添加本地IP至阿里云ECS安全组白名单

# 使用方法
1. 运行以下命令安装必要模块
```shell
pip install -r requirements.txt
```
2. 修改 `settings.py`中的`ak`、`secret`、`region_id`、`SecurityGroupId`参数;
3. 运行以下命令执行脚本
```shell
python main.py
```