# Rk_数据集工作站

>后端技术链:flask + flask_sqlalchemy + flask_cors + flask_migrate + flask_jwt_extend + mysql8.0(docker)

前身：https://github.com/RKwork85/rk_demo_fontend_ds

## 介绍

这是一个作为后端服务的项目，包含最基础的关于用户登录，数据库CRUD操作
```
项目结构（undo待优化）

├── api_calling
│   ├── add_dataset_single .py
│   ├── add_rk_user_single.py
│   ├── add_user.py
│   ├── add_user_single.py
│   ├── add_users.py
│   ├── del_user_byID.py
│   ├── del_user_byUsername.py
│   ├── get_user_all_Datasets.py
│   ├── get_user_byID.py
│   ├── get_user_byPage.py
│   ├── get_user_by_uuid.py
│   ├── login_by_uuid.py
│   └── put_user_byID.py
├── app.py                                                  
├── config.py
├── exts.py                 
├── migrations
│   ├── alembic.ini
│   ├── script.py.mako
│   └── versions
│       ├── 1356d92cc17a_.py
│       ├── 4d4c32a7bf63_.py
│       ├── 7e35ab032e95_.py
│       └── c52d0e66c0c2_.py
├── models.py
│   ├── config.cpython-310.pyc
│   ├── exts.cpython-310.pyc
│   └── models.cpython-310.pyc
├── README.md
└── requirements.txt

路由表

Endpoint             Methods  Rule                         
-------------------  -------  -----------------------------
add_dataset          POST     /v1/work/datasets/create     
add_datasets         POST     /v1/work/datasets/synchronize
dashboard            GET      /api/dashboard               
del_dataset_by_id    DELETE   /dataset/<int:id>            
get_dataset_all      GET      /dataset                     
get_dataset_by_id    GET      /dataset/<int:id>            
get_dataset_by_uuid  GET      /v1/work/datasets/list       
hello                GET      /                            
login                GET      /api/login                   
login_by_uuid        POST     /v1/sys/auth/login           
register_by_rkwork   GET      /rkwork/register             
register_by_uuid     POST     /register                    
static               GET      /static/<path:filename>      
update_dataset       PUT      /dataset/<int:uid>   
```


### Working_record:

>t1: 更新了四个接口：6.6.2024 21:36

v1/w../create:  增加单条数据集

v1/w../synchronize: 同步用户LocalStore数据集

v1/w../list:    获取用户所有数据集

v1/s../login    登录授权

>t2: 更新了一个接口 ；完善了后台数据传输格式： 6.7.2024 14:17

v1/w../delete:  删除单条数据集

>t3: 完成更新数据集接口
v1/w../update: 更新单条数据集




