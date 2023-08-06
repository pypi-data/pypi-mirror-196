import datetime as dt

from feeds.services import articles, feeds, opengraph

from feeds.models import Article
from demo.conf.celery.app import app


@app.task
def daily_digest() -> None:
    yesterday = dt.date.today() - dt.timedelta(days=1)
    articles.digest_for_date(yesterday)


@app.task()
def load_feeds() -> None:
    feeds.load_feeds()


@app.task
def load_opengraph_tags(pk: str) -> None:
    opengraph.load_tags(Article.objects.get(pk=pk))
