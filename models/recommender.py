import os
import tensorflow.compat.v1 as tf

tf.get_logger().setLevel("ERROR")
import pandas as pd
from recommenders.utils.timer import Timer
from recommenders.utils.constants import SEED
from recommenders.models.deeprec.deeprec_utils import prepare_hparams
from recommenders.datasets.amazon_reviews import (
    download_and_extract,
    data_preprocessing,
)
from recommenders.models.deeprec.models.sequential.sli_rec import (
    SLI_RECModel as SeqModel,
)
from recommenders.models.deeprec.io.sequential_iterator import SequentialIterator
from app.db import init_db_connection
import json
import sqlite3

EPOCHS = 10
BATCH_SIZE = 400
RANDOM_SEED = SEED

data_path = os.path.join("resources", "slirec")

yaml_file = "D:/LEARN/RS/final/models/sli_rec.yaml"
train_file = os.path.join(data_path, r"train_data")
valid_file = os.path.join(data_path, r"valid_data")
test_file = os.path.join(data_path, r"test_data")
user_vocab = os.path.join(data_path, r"user_vocab.pkl")
item_vocab = os.path.join(data_path, r"item_vocab.pkl")
cate_vocab = os.path.join(data_path, r"category_vocab.pkl")
output_file = os.path.join(data_path, r"output.txt")

reviews_name = "reviews_Movies_and_TV_5.json"
meta_name = "meta_Movies_and_TV.json"
reviews_file = os.path.join(data_path, reviews_name)
meta_file = os.path.join(data_path, meta_name)
train_num_ngs = 4
valid_num_ngs = 4
test_num_ngs = 9
sample_rate = 0.01

input_files = [
    reviews_file,
    meta_file,
    train_file,
    valid_file,
    test_file,
    user_vocab,
    item_vocab,
    cate_vocab,
]


input_creator = SequentialIterator


class Recommender:
    def __init__(self):
        if not os.path.exists(train_file):
            download_and_extract(reviews_name, reviews_file)
            download_and_extract(meta_name, meta_file)
            data_preprocessing(
                *input_files,
                sample_rate=sample_rate,
                valid_num_ngs=valid_num_ngs,
                test_num_ngs=test_num_ngs
            )
        self.hparams = prepare_hparams(
            yaml_file,
            embed_l2=0.0,
            layer_l2=0.0,
            learning_rate=0.001,
            epochs=EPOCHS,
            batch_size=BATCH_SIZE,
            show_step=20,
            MODEL_DIR=os.path.join(data_path, "model/"),
            SUMMARIES_DIR=os.path.join(data_path, "summary/"),
            user_vocab=user_vocab,
            item_vocab=item_vocab,
            cate_vocab=cate_vocab,
            need_sample=True,
            train_num_ngs=train_num_ngs,
        )
        self.model = self.load_model()
        self.db = init_db_connection()

    def train(self):
        self.model = SeqModel(self.hparams, input_creator, seed=RANDOM_SEED)
        with Timer() as train_time:
            self.model = self.model.fit(
                train_file, valid_file, valid_num_ngs=valid_num_ngs
            )
        print(
            "Time cost for training is {0:.2f} mins".format(train_time.interval / 60.0)
        )

    def load_model(self):
        model_best_trained = SeqModel(self.hparams, input_creator, seed=RANDOM_SEED)
        path_best_trained = os.path.join(self.hparams.MODEL_DIR, "best_model")
        print("loading saved model in {0}".format(path_best_trained))
        model_best_trained.load_model(path_best_trained)
        return model_best_trained

    def model_pre_predict(self):
        return self.model.predict(test_file, output_file)

    def predict(self, userId):
        data = pd.read_csv(test_file, sep="\t")
        predict = pd.read_csv(output_file, sep="\t")
        predict.columns = ["prediction"]
        data.columns = [
            "label",
            "user_id",
            "item_id",
            "category_id",
            "time",
            "history_item_ids",
            "history_category_ids",
            "history_time",
        ]
        data["prediction"] = predict["prediction"]
        data = data[(data["user_id"] == userId)]
        result = data[(data["prediction"] > 0.5)].to_dict(orient="records")
        return result

    def pre_data(self):
        meta_name = "meta_Movies_and_TV.json"
        current_dir = os.path.dirname(os.path.realpath(__file__))
        data_path = os.path.join(current_dir, "..", "resources", "slirec")
        meta_file = os.path.join(data_path, meta_name)
        meta_r = open(meta_file, "r")
        with sqlite3.connect("movies.db") as con:
            cur = con.cursor()
            for line in meta_r:
                line_new = eval(line)
                cur.execute(
                    "INSERT INTO movies (asin,data) VALUES (?,?)",
                    (line_new["asin"], json.dumps(line_new)),
                )
            con.commit()

    def get_movies(self, movieId):
        try:
            with sqlite3.connect("movies.db") as con:
                cur = con.cursor()
                cur.execute(
                    "select data from movies where asin = ? limit 0,1", (movieId,)
                )
                (data,) = cur.fetchone()
                return data
        except Exception as e:
            print(e)
            return None
