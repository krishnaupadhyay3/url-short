from flask import Flask
from views import UrlShortAPI, SearchAPI, UrlRedirectAPI, StatsAPI
from database import db

api_views = [UrlShortAPI, SearchAPI, UrlRedirectAPI, StatsAPI]
app = Flask("url-short")

for view in api_views:
    app.add_url_rule(view.uri,
                     view_func=view.as_view(view.name))

app.config.from_object('config.ProductionConfig')
db.init_app(app)
app.app_context().push()
db.create_all(app=app)
db.session.commit()
