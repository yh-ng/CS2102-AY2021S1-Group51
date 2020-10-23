from flask_table import Table, Col, LinkCol

class petList(Table):
    classes = ['table', 'table-bordered', 'table-striped']
    pet_name = Col('pet_name')
    category = Col('category')
    age = Col('age')
