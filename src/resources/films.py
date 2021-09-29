from datetime import datetime

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload

from services.film_service import FilmService
from src import db
from src.database.models import Film
from src.resources.auth import token_required
from src.schemas.films import FilmSchema


class FilmListApi(Resource):
	film_schema = FilmSchema()
	
	#	@token_required
	def get(self, uuid=None):
		if not uuid:
			films = FilmService.fetch_all_films(db.session).options(
				joinedload(Film.actors)
			).all()
			return self.film_schema.dump(films, many=True), 200
		film = FilmService.fetch_film_by_uuid(db.session, uuid)
		if not film:
			return '', 404
		return self.film_schema.dump(film), 200
	
	def post(self):
		try:
			film = self.film_schema.load(request.json, session=db.session)
		except ValidationError as e:
			return {'message': str(e)}, 400
		
		db.session.add(film)
		db.session.commit()
		return self.film_schema.dump(film), 201
	
	def put(self, uuid):
		film = FilmService.fetch_film_by_uuid(db.session, uuid)
		if not film:
			return "", 404
		try:
			film = self.film_schema.load(request.json, instance=film, session=db.session)
		except ValidationError as e:
			return {'message': str(e)}, 400
		db.session.add(film)
		db.session.commit()
		return self.film_schema.dump(film), 200
	
	def patch(self, uuid):
		film = FilmService.fetch_film_by_uuid(db.session, uuid)
		if not film:
			return '', 404
		film_json = request.json
		title = film_json.get('title')
		release_date = datetime.strftime(film_json.get('release_date'), '%B %d, %Y') if film_json.get(
			'release_date') else None
		distributed_by = film_json.get('distributed_by')
		description = film_json.get('description')
		length = film_json.get('length')
		rating = film_json.get('rating')
		
		if title:
			film.title = title
		elif release_date:
			film.release_date = release_date
		elif distributed_by:
			film.distributed_by = distributed_by
		elif description:
			film.description = description
		elif length:
			film.length = length
		elif rating:
			film.rating = rating
		db.session.add(film)
		db.session.commit()
		return {'message': 'Updated successufully'}, 201
	
	def delete(self, uuid):
		film = FilmService.fetch_film_by_uuid(db.session, uuid)
		if not film:
			return '', 404
		db.session.delete(film)
		db.session.commit()
		return "", 204
