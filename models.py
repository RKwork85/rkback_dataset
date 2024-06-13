import json
import os
from exts import db
from datetime import datetime
from collections import OrderedDict


class UserModel(db.Model):
    __tablename__= "user"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    username = db.Column(db.String(100),nullable=True, unique=True)
    password = db.Column(db.String(255),nullable=True)
    uuid = db.Column(db.String(255), nullable=False)
    join_time = db.Column(db.DateTime,default=datetime.now)
    datasets = db.relationship('DatasetsModel', backref='user')
    
    def generate_dataset(self, dataset_path):

        dataset_dir = os.path.join(dataset_path, 'static', 'datasets')
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)

        try:
            dataset_path = os.path.join(dataset_dir, f"{self.uuid}-dataset-1.jsonl")
            with open(dataset_path, 'w') as f:
                for dataset in self.datasets:
                    data = dataset.get_dataset()
                    f.write(json.dumps(data, ensure_ascii=False) + '\n')

                return dataset_dir, dataset_path
        except Exception as error:
            print(error)
            return None
        
class DatasetsModel(db.Model):

    __tablename__="datasets"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    instruction = db.Column(db.Text,nullable=True)
    input = db.Column(db.Text,default='')
    output = db.Column(db.Text,nullable = True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))       # 和 user表中的 id列进行关联；通过backref 即user.datasets 访问用户的所有数据集

    def get_dataset(self):
        data = {
            "instruction": self.instruction,
            "input": self.input,
            "output": self.output
        }
        return data

    # def get_dataset(self):
    #     data = OrderedDict([
    #         ("instruction", self.instruction),
    #         ("input", self.input),
    #         ("output", self.output)
    #     ])
    #     return data