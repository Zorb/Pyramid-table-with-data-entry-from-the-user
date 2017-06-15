from pyramid.config import Configurator

from sqlalchemy import engine_from_config
from .models import DBSession, Base

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings,
                          root_factory='pyrtable.models.Root')
    config.include('pyramid_jinja2')
    config.include('pyramid_chameleon')
    config.add_route('home', '/')
    config.add_route('add', '/add')
    config.add_route('delete', '/delete/{uid}')
    config.add_route('edit', '/edit/{uid}')
    config.add_static_view('static', 'pyrtable:static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static/')
    config.scan('.views')
    return config.make_wsgi_app()
