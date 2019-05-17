import random
import responder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Category, Question


api = responder.API()


def DB():
    engine = create_engine("sqlite:///exercise.db", echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


@api.route("/")
class Index:
    def on_get(self, req, resp):
        session = DB()
        obj = session.query(Category).order_by(Category.name.asc()).all()
        count = session.query(Question).count()
        session.close()

        resp.html = api.template("index.html", list=obj, count=count)


@api.route("/start")
class Start:
    def on_get(self, req, resp):
        session = DB()
        obj = session.query(Question, Category).outerjoin(
            Category, Category.id == Question.category_id).all()
        session.close()

        random.shuffle(obj)

        arr1 = []

        for q, c in obj:
            arr2 = [q.id, q.answer, q.question, q.category_id, c.name]
            arr1.append(arr2)

        # jsonで返す
        resp.media = arr1

############################
# Category CRUD
############################
@api.route("/category/list")
class CategoryList:
    def on_get(self, req, resp):
        session = DB()
        obj = session.query(Category).all()
        session.close()

        resp.html = api.template("category_list.html", list=obj)


@api.route("/category/insert")
class CategoryInsert:
    def on_get(self, req, resp):
        resp.html = api.template("category_insert.html")

    async def on_post(self, req, resp):
        """フォームからPOSTされたデータを取得する場合はreq.media()を使用し async await """
        data = await req.media()

        session = DB()
        obj = Category(name=data["name"])
        session.add(obj)
        session.commit()
        session.close()

        # リダイレクト
        api.redirect(
            resp=resp,
            location="/category/list"
        )


@api.route("/category/update/{id}")
class CategoryUpdate:
    def on_get(self, req, resp, *, id):
        session = DB()
        # http://omake.accense.com/static/doc-ja/sqlalchemy/ormtutorial.html
        # one() は全ての行レコードをフェッチして、 結果が一意なオブジェクトに対応しないか、複数のレコードが混在している場合に はエラーを送出します
        # first() は、SELECT に 1 レコードの制約 をかけ、得られた結果をスカラで返します
        row = session.query(Category).filter_by(id=id).one()
        session.close()
        resp.html = api.template("category_update.html", row=row)

    async def on_post(self, req, resp, *, id):
        data = await req.media()
        session = DB()
        row = session.query(Category).filter_by(id=id).one()
        row.name = data["name"]
        session.add(row)
        session.commit()
        session.close()

        api.redirect(
            resp=resp,
            location="/category/list"
        )


@api.route("/category/delete/{id}")
class CategoryDelete:
    async def on_post(self, req, resp, *, id):
        data = await req.media()
        session = DB()
        row = session.query(Category).filter_by(id=id).one()
        session.delete(row)
        session.commit()
        session.close()

        api.redirect(
            resp=resp,
            location=f"/category/list"
        )

############################
# Question CRUD
############################
@api.route("/question/list")
class QuestionList:
    def on_get(self, req, resp):

        session = DB()
        cate = session.query(Category).order_by(Category.name.asc()).all()

        # 検索追加
        sresult = ""

        if req.params.get("cate") and req.params.get("word"):
            cates = req.params.get("cate").split(",")
            word = req.params.get("word")
            obj = session.query(Question, Category).outerjoin(Category, Category.id == Question.category_id).filter(Question.answer.like(
                f'%{word}%') | Question.question.like(f'%{word}%')).filter(Question.category_id == f'{cates[0]}').order_by(Question.id.desc()).all()
            sresult = f"検索結果＝{cates[1]}＆{word}"

        elif req.params.get("cate"):
            cates = req.params.get("cate").split(",")
            obj = session.query(Question, Category).outerjoin(Category, Category.id == Question.category_id).filter(
                Question.category_id == f'{cates[0]}').order_by(Question.id.desc()).all()
            sresult = f"検索結果＝{cates[1]}"

        elif req.params.get("word"):
            word = req.params.get("word")
            obj = session.query(Question, Category).outerjoin(Category, Category.id == Question.category_id).filter(
                Question.answer.like(f'%{word}%') | Question.question.like(f'%{word}%')).order_by(Question.id.desc()).all()
            sresult = f"検索結果＝{word}"

        else:
            obj = session.query(Question, Category).outerjoin(
                Category, Category.id == Question.category_id).order_by(Question.id.desc()).all()

        session.close()

        # 取得したオブジェクトを50文字以下に書き換える
        for v in obj:
            if len(v.Question.question) > 50:
                v.Question.question = v.Question.question[:50]

        resp.html = api.template("question_list.html",
                                 list=obj, cate=cate, sresult=sresult)


@api.route("/question/insert")
class QuestionInsert:
    def on_get(self, req, resp):
        session = DB()
        obj = session.query(Category).all()
        session.close()

        resp.html = api.template("question_insert.html", list=obj)

    async def on_post(self, req, resp):
        """フォームからPOSTされたデータを取得する場合はreq.media()を使用し async await """
        data = await req.media()
        # insert
        session = DB()
        obj = Question(
            answer=data["answer"], question=data["question"], category_id=data["category_id"])
        session.add(obj)
        session.commit()
        session.close()

        # リダイレクト
        api.redirect(
            resp=resp,
            location="/question/list"
        )


@api.route("/question/update/{id}")
class QuestionUpdate:
    def on_get(self, req, resp, *, id):
        session = DB()
        cate = session.query(Category).all()
        row = session.query(Question).filter_by(id=id).one()
        session.close()
        resp.html = api.template("question_update.html", cate=cate, row=row)

    async def on_post(self, req, resp, *, id):
        data = await req.media()
        session = DB()
        row = session.query(Question).filter_by(id=id).one()
        row.answer = data["answer"]
        row.question = data["question"]
        row.category_id = data["category_id"]
        session.add(row)
        session.commit()
        session.close()

        # リダイレクト
        api.redirect(
            resp=resp,
            location="/question/list"
        )


@api.route("/question/delete/{id}")
class QuestionDelete:
    async def on_post(self, req, resp, *, id):
        data = await req.media()
        session = DB()
        row = session.query(Question).filter_by(id=id).one()
        session.delete(row)
        session.commit()
        session.close()

        # リダイレクト
        api.redirect(
            resp=resp,
            location="/question/list"
        )


if __name__ == "__main__":
    api.run()
