from datetime import datetime
from flask import Flask, jsonify, render_template, request, session, g
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from flask_migrate import Migrate
from flask_cors import CORS
from models import UserModel, DatasetsModel
from exts import db
import config

app = Flask(__name__)

# 绑定配置文件
app.config.from_object(config)

# 初始化
CORS(app, supports_credentials=True)
jwt = JWTManager(app)
db.init_app(app)  
migrate = Migrate(app, db)


@app.route("/")
def hello():
    return "你好啊，木子！这是测数据集接口的服务"


@app.post("/v1/sys/auth/login")
def login_by_uuid():

    # 获取uuid
    data = request.get_json()
    uuid = data.get("uuid")

    # 为用户创建access_token
    access_token = create_access_token(identity=uuid)
    # 查询该用户    
    user = UserModel.query.filter_by(uuid=uuid).first()
    if user:
        return jsonify(access_token=access_token, msg= f'已经为老用户生成{uuid}的access_token')
    else:
        new_user = UserModel(uuid=uuid, join_time=datetime.now())
        db.session.add(new_user)
        db.session.commit()
        return jsonify(access_token=access_token, msg= f'已经为新用户生成{uuid}的access_token')


    # print(g.user)
    # data = request.get_json()
    # uuid = data.get("uuid")
    # user = UserModel.query.filter_by(uuid=uuid).first()
    # if user:
    #     return jsonify(msg="错误,用户已注册请登录")
    # else:
    #     new_user = UserModel(uuid=uuid, join_time=datetime.now())

    #     db.session.add(new_user)
    #     db.session.commit()
    #     return jsonify(msg="注册成功！已连接到数据库")
    return jsonify(msg="为该用户生成access_token失败")

@app.route("/v1/work/datasets/list", methods=["GET"])
@jwt_required()  # 
def get_dataset_by_uuid():
    current_user = get_jwt_identity()           # 验证会过期 待解决
    print('|/v1/work/datasets/list| 当前登录的用户：登录后自动获取用户所有数据:',current_user)
    user = UserModel.query.filter_by(uuid=current_user).first()

    datasets = user.datasets  # 序列化之后变得无序，所以还是在前端组织顺序？
    print(datasets)
    allDataset = []
    for dataset in datasets:
        allDataset.append([dataset.id, dataset.get_dataset()])
    print(allDataset)
    return jsonify(msg="用户数据查询成功", allDataset=allDataset) 


@app.post("/register")
def register_by_uuid():
    data = request.get_json()
    uuid = data.get("uuid")
    user = UserModel.query.filter_by(uuid=uuid).first()
    if user:
        return jsonify(msg="错误,用户已注册请登录")
    else:
        new_user = UserModel(uuid=uuid, join_time=datetime.now())

        db.session.add(new_user)
        db.session.commit()
        return jsonify(msg="注册成功！已连接到数据库")


@app.get("/rkwork/register")  # 走后门的接口
def register_by_rkwork():
    username = request.args.get("username")
    password = request.args.get("password")
    user = UserModel.query.filter_by(username=username).first()
    if user:
        return jsonify(msg="错误,用户已注册请登录")
    else:
        new_user = UserModel(
            username=username,
            password=password,
            uuid=username,
            join_time=datetime.now(),
        )

        db.session.add(new_user)
        db.session.commit()
        return jsonify(msg="注册成功！已连接到数据库")


# 添加单条数据集
@app.post("/v1/work/datasets/create")
@jwt_required()
def add_dataset():
    current_user = get_jwt_identity()          
    print('|/v1/work/datasets/create"| 用户添加单条数据到数据库: 当前登录的用户：',current_user)
    # 获取用户
    user = UserModel.query.filter_by(uuid=current_user).first()

    data = request.get_json()
    # 拿    # [[id,{dataset}],[],[]]                                                 
    instruction = data.get("instruction")
    output = data.get("output")
    dataset = DatasetsModel(
        instruction=data.get("instruction"),
        output=data.get("output"),
        user_id=user.id,
    )
    db.session.add(dataset)
    db.session.commit()
    print("用户添加单条数据成功")
    return jsonify(msg="用户单条数据添加成功", dataset=[dataset.id,dataset.get_dataset()])

# 删除单条数据集
@app.delete("/v1/work/datasets/delete/<int:id>")
@jwt_required()
def delete_dataset(id):
    current_user = get_jwt_identity()          
    print('|/v1/work/datasets/delete"| 用户删除数据库单条数据: 当前登录的用户：',current_user)
    # 获取用户
    dataset = DatasetsModel.query.filter_by(id=id).first()  # first(), all(), order_by()
    if dataset:
        db.session.delete(dataset)
        db.session.commit()
        return jsonify(msg =f"删除第 {id} 数据集成功!" )
    else:
        return jsonify({"msg": "数据库中没有该数据集！"})




# 添加多条数据集 要和用户关联
@app.post("/v1/work/datasets/synchronize")
@jwt_required()  # 
def add_datasets():
    current_user = get_jwt_identity()           # 验证会过期 待解决
    print('|/v1/work/datasets/synchronize| 当前登录的用户：同步用户localStore所有数据添加到数据库:',current_user)
    # 获取用户
    user = UserModel.query.filter_by(uuid=current_user).first()
    data = request.get_json()
    # 拿
    datasets = data.get("datasets")  # [[id,{dataset}],[],[]]
    for i in datasets:
        instruction = i['instruction']               # 这里获取对象的值['关键字']
        output = i['output']
        print(instruction, output)
        # 存
        dataset = DatasetsModel(instruction=instruction, output=output, user_id=user.id,)
        db.session.add(dataset)
        db.session.commit()
    
    # 返回user的所有数据，需要带上数据集的id
    datasets = user.datasets 
    allDataset = []
    for dataset in datasets:
        allDataset.append([dataset.id, dataset.get_dataset()])
    print(allDataset)
    return jsonify(msg="同步本地数据到数据库成功，返回数据库用户数据", allDataset=allDataset) 



@app.get("/dataset")
def get_dataset_all():
    datasets = DatasetsModel.query.all()
    datasets_json = [(dataset.id, dataset.get_dataset()) for dataset in datasets]
    for i in datasets_json:
        print(i, "\n")

    return jsonify(msg="ok", data=datasets_json)


@app.route("/dataset/<int:id>", methods=["GET"])
def get_dataset_by_id(id):
    print(id)
    try:
        dataset = db.get_or_404(
            DatasetsModel, id
        )  # 在尝试数据库查询的的时候，可能会报错，导致程序直接返回，要有对应的处理
        if dataset:
            data = dataset.get_dataset()  # 序列化之后变得无序，所以还是在前端组织顺序？
            print(data)
            return jsonify(data)
    except:
        # 如果没有找到用户，返回一个错误消息
        return jsonify(msg=f"{id}数据集不存在！！！")


@app.put("/v1/work/datasets/update/<int:id>")
def update_dataset(id):
    try:
        data = request.get_json()
        instruction = data.get("instruction")
        output = data.get("output")
        print(instruction, output)
        dataset = db.get_or_404(DatasetsModel, id)
        olddataset = dataset.get_dataset()
        if dataset:
            print(dataset)
            dataset.instruction = instruction
            dataset.output = output
            db.session.commit()
            dataset = db.get_or_404(DatasetsModel, id)

            return {
                "msg": "数据集数据更新成功",
                "oldDataset": olddataset,
                "newDataset": [dataset.id, dataset.get_dataset()],
            }
        else:
            return jsonify({"msg": "数据库中没有数据！"})
    except Exception as e:
        # 打印异常信息并返回错误响应
        print(f"An error occurred: {e}")
        return jsonify({"msg": "发生内部错误，无法删除用户！", "error": str(e)}), 500



# 通过字段删除数据, query用法
@app.delete("/dataset/<int:id>")
def del_dataset_by_id(id):
    try:
        # 使用 username 来查询用户
        dataset = DatasetsModel.query.filter_by(
            id=id
        ).first()  # first(), all(), order_by()

        if dataset:
            db.session.delete(dataset)
            db.session.commit()
            return jsonify({"msg": "删除成功!", "data": f"{id}"})
        else:
            return jsonify({"msg": "数据库中没有该数据集！"})
    except Exception as e:
        # 打印异常信息并返回错误响应
        print(f"An error occurred: {e}")
        return jsonify({"msg": "发生内部错误，无法删除用户！", "error": str(e)}), 500


@app.route("/api/login", methods=["GET"])
def login():
    # 这里应该有验证用户名和密码的逻辑
    session["uuid"] = "rkwork"
    return jsonify({"uuid": session["uuid"]})


@app.route("/api/dashboard")
def dashboard():
    print(g.user.uuid)
    if "uuid" in session:
        return jsonify({"message": f'Welcome! Your session UUID is: {session["uuid"]}'})
    else:
        return jsonify({"error": "Not logged in"})


@app.before_request  #  在请求之前就自动获取变量值， 每次请求都要写代码，获取用户的信息
def my_before_request():
    uuid = session.get("uuid")
    print("before_request", uuid)
    if uuid:
        user = UserModel.query.filter_by(uuid=uuid).first()
        setattr(g, "user", user)
    else:

        setattr(g, "user", None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
"""
1 返回到前端的数据无序 需在前端重新处理数据
2 
"""
