from datetime import datetime

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from src import db
from src.database.models import Actor
from src.schemas.actors import ActorSchema


class ActorListApi(Resource):
	actors_schema = ActorSchema()
	
	def get(self, uuid=None):
		if not uuid:
			films = db.session.query(Actor).all()
			return self.actors_schema.dump(films, many=True), 200
		film = db.session.query(Actor).filter_by(uuid=uuid).first()
		if not film:
			return '', 404
		return self.actors_schema.dump(film), 200
	
	def post(self):
		try:
			film = self.actors_schema.load(request.json, session=db.session)
		except ValidationError as e:
			return {'message': str(e)}, 400
		
		db.session.add(film)
		db.session.commit()
		return self.actors_schema.dump(film), 201
	
	def put(self, uuid):
		film = db.session.query(Actor).filter_by(uuid=uuid).first()
		if not film:
			return "", 404
		try:
			film = self.actors_schema.load(request.json, instance=film, session=db.session)
		except ValidationError as e:
			return {'message': str(e)}, 400
		db.session.add(film)
		db.session.commit()
		return self.actors_schema.dump(film), 200
	
	def patch(self, uuid):
		actor = db.session.query(Actor).filter_by(uuid=uuid).first()
		if not actor:
			return '', 404
		actors_json = request.json
		name = actors_json.get('name')
		birthday = datetime.strftime(actors_json.get('birthday'), '%B %d, %Y') if actors_json.get(
			'birthday') else None
		active = actors_json.get('active')
		
		if name:
			actor.name = name
		elif birthday:
			actor.birthdate = birthday
		elif active:
			actor.active = active
		db.session.add(actor)
		db.session.commit()
		return {'message': 'Updated successufully'}, 201
	
	def delete(self, uuid):
		actor = db.session.query(Actor).filter_by(uuid=uuid).first()
		if not actor:
			return '', 404
		db.session.delete(actor)
		db.session.commit()
		return "", 204
