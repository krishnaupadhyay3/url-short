from flask.json import jsonify
from flask.views import MethodView
from flask import request, redirect
from exception import bad_request, not_found
import base64
import time
from datetime import datetime, timedelta
from model import HitLog, ShortUrl
from database import db
import hashlib


class UrlShortAPI(MethodView):
    name = 'urlshort'
    uri = '/'
    methods = ['POST', 'GET']

    def post(self):
        if not request.is_json:
            return bad_request('Content-Type: application/json supported only')

        data = request.get_json()
        url = data.get('url')
        if not url:
            return bad_request('url is required')
        base64_url = self.generate_short_url(url)
        new_link = ShortUrl(
            url=url, hash=base64_url, created_at=datetime.now())
        db.session.add(new_link)
        db.session.commit()
        shorten_url = request.host+"/" + base64_url
        return jsonify({'url': shorten_url})

    def generate_short_url(self, url, length=6):
        current_time = str(time.time())
        url_to_hash = current_time + url
        hashed_url = hashlib.sha256(url_to_hash.encode('utf-8')).hexdigest()
        base64_url_hash = base64.b64encode(
                hashed_url.encode('utf-8')).decode('utf-8')
        base64_url = base64_url_hash[:length]
        if ShortUrl.query.filter_by(hash=base64_url).first() is not None:
            base64_url = base64_url_hash[:8]
        return base64_url


class UrlRedirectAPI(MethodView):
    name = 'urlredirect'
    uri = '/<original_id>'
    methods = ['GET']

    def get(self, original_id):
        if original_id:
            short_url = ShortUrl.query.filter_by(hash=original_id).first()
            if short_url:
                original_url = short_url.url
                new_link = HitLog(
                    short_url_id=short_url.id, created_at=datetime.now())
                db.session.add(new_link)
                db.session.commit()
                return redirect(original_url)
            else:
                return not_found('Short url not found')
        else:
            return not_found('URL not found')


class StatsAPI(MethodView):
    name = 'stats'
    uri = '/<id>/stats'
    methods = ['GET']

    def get(self, id):
        if id:
            short_url = ShortUrl.query.filter_by(hash=id).first()
            if short_url:
                # count all the hits for this short url
                total_records = HitLog.query.filter_by(
                        short_url_id=short_url.id)
                total_hits = total_records.count()
                hourly_hits = total_records.filter(HitLog.created_at >
                                                   datetime.now() -
                                                   timedelta(hours=1)).count()

                return jsonify({
                    'url': short_url.url,
                    'total_hit': total_hits,
                    'hourly_hit': hourly_hits,
                    'created_at':
                        short_url.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            else:
                return not_found('Short url not found')
        return bad_request('URL is required')


class SearchAPI(MethodView):
    name = 'search'
    uri = '/search'
    methods = ['GET']

    def get(self):
        search_term = request.args.get('q')
        if not search_term:
            return bad_request('q is required')
        search_term = search_term.lower()
        search_result = ShortUrl.query.filter(
            ShortUrl.url.like("%"+search_term+"%")).all()

        result = [{
            'url': short_url.url,
            'short_url': short_url.url + "/" + short_url.hash}
                  for short_url in search_result]
        return jsonify({'results': result})
