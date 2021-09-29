'''
SELECT QUERIES

'''
from sqlalchemy import and_

from src import db
from src.database import models

films = db.session.query(models.Film).order_by(models.Film.rating.desc()).all()
# des- убывание, вывести все с сортировкой


name1 = db.session.query(models.Film).filter(
	models.Film.title == "Harry Potter and the Deathly Hallows part 2"
).first()
# фильтр по полю

name2 = db.session.query(models.Film).filter_by(
	title="Harry Potter and the Deathly Hallows part 2"
).first()

and_stat = db.session.query(models.Film).filter(
	models.Film.title != 'Harry Potter and the Deathly Hallows part 2',
	models.Film.rating >= 7.5
).all()

and_stat = db.session.query(models.Film).filter(
	models.Film.title != 'Harry Potter and the Deathly Hallows part 2'
).filter(
	models.Film.rating >= 7.6
).all()

and_stat = db.session.query(models.Film).filter(
	and_(models.Film.title != 'Harry Potter and the Deathly Hallows part 2', models.Film.rating >= 7.6)
).all()
# like поиск , ilike поиск покс на регистр

dadly = db.session.query(models.Film).filter(
	models.Film.title.like("%Deathly%")
).all()

# in_ между, тильда - обратный запрос (!)
len = db.session.query(models.Film).filter(
	~models.Film.length.in_([146, 161])
).all()

# Можно использовать вместо олл и ферст - срезы

len = db.session.query(models.Film).filter(
	~models.Film.length.in_([146, 161])
)[:3]

len = db.session.query(models.Film).filter(
	~models.Film.length.in_([146, 161])
)
'''
querung with joins
'''

films_with_actors = db.session.query(models.Film).join(models.Film.actors).all()
