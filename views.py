import colander
import deform.widget
import transaction
from pyramid.view import view_config
from pyramid_wtforms import Form, validators, StringField
from models import DBSession, User
from pyramid.httpexceptions import HTTPFound
import datetime

class ReusableForm(Form):
    name = StringField('Name:', validators=[validators.required()])
    lname = StringField('Last Name:', validators=[validators.required()])
    age = StringField('Age:', validators=[validators.required()])
    address = StringField('Address:', validators=[validators.required()])

class EditPage(colander.MappingSchema):
        First_Name = colander.SchemaNode(colander.String())
        Last_Name = colander.SchemaNode(colander.String())
        Address = colander.SchemaNode(colander.String())
        Age = colander.SchemaNode(colander.Integer())

class Table(object):
    def __init__(self, request):
        self.request = request

    @property
    def edit_form(self):
        schema = EditPage()
        return deform.Form(schema, buttons=('submit',))

    @property
    def reqts(self):
        return self.edit_form.get_widget_resources()


    @view_config(route_name='home', renderer='templates/tableform.jinja2')
    def my_view(request):
        form = ReusableForm()
        transaction.commit()
        users = DBSession.query(User).all()
        return dict(form=form, results=users)

    @view_config(route_name='delete', renderer='templates/tableform.jinja2')
    def delete(self):
        uid = self.request.matchdict['uid']
        form = ReusableForm()
        DBSession.query(User).filter_by(id=uid).delete()
        transaction.commit()
        users = DBSession.query(User).all()
        return dict(form=form, results=users)

    @view_config(route_name='edit',
                renderer='templates/wikipage_addedit.pt')

    def edit(self):
        uid = self.request.matchdict['uid']
        transaction.commit()
        page = DBSession.query(User).filter_by(id=uid).first()

        edit_form = self.edit_form

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = edit_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(page=page, form=e.render())

            # Change the content and redirect to the view
            page.First_Name = appstruct['First_Name']
            page.Age = appstruct['Age']
            page.Address = appstruct['Address']
            page.Last_Name = appstruct['Last_Name']
            transaction.commit()
            url = self.request.route_url('home', uid=page.id)
            return HTTPFound(url)

        form = self.edit_form.render(dict(
            uid=page.id, First_Name=page.First_Name, Address=page.Address, Last_Name=page.Last_Name, Age=page.Age)
        )
        users = DBSession.query(User).all()
        return dict(results=users, form=form)


@view_config(route_name='add', request_method='POST', renderer='templates/tableform.jinja2')
def add(request):
        form = ReusableForm()
        if request.method == 'POST':
            name = request.params['name']
            lname = request.params['lname']
            age = request.params['age']
            address = request.params['address']
            DBSession.add(User(First_Name=name, Last_Name=lname, Age=age, Address=address))
            transaction.commit()
        users = DBSession.query(User).all()
        return dict(form=form, results=users)





