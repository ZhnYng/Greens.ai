from application import db

class QueryUtils:
    def rows2dict(self, rows):
        data = []
        for row in rows:
            d = {}
            for column in row.__table__.columns:
                d[column.name] = str(getattr(row, column.name))
            data.append(d)
        return data
     
    def get_entries(self, model):
        rows = model.query.all()
        return self.rows2dict(rows)
    
    def get_entries_where(self, model, condition):
        rows = model.query.filter(condition).all()
        return self.rows2dict(rows)
    
    def get_entries_where_double(self, model, condition1, condition2):
        rows = model.query.filter(condition1, condition2).all()
        return self.rows2dict(rows)
    
    def get_entries_where_triple(self, model, condition1, condition2, condition3):
        rows = model.query.filter(condition1, condition2, condition3).all()
        return self.rows2dict(rows)
        
    def add_entry(self, new_entry):
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
        
    def remove_entry(self, id, model):
        entry = model.query.get(id)
        db.session.delete(entry)
        db.session.commit()
        return 'Entry removed'
        
    def update_entry(self, id, model, updated_entry):
        model.query.filter(model.id == id).update(updated_entry)
        db.session.commit()
        return 'Entry updated'
