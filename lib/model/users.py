from lib.model.database import Database

class Users:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def login(self, email):
        user = self.cursor.execute('SELECT * FROM deskundigen WHERE email = ?', (email,)).fetchone()
        if user is not None:
            return user, 'user'
        else:
            admin = self.cursor.execute('SELECT * FROM beheerders WHERE email = ?', (email,)).fetchone()
            if admin is not None:
                return admin, 'admin'


    def admin_create(self, first_name, last_name, email, password):
        self.cursor.execute('INSERT into beheerders (voornaam, achternaam, email, wachtwoord) VALUES (?, ?, ?, ?)',
                            (first_name, last_name, email, password))
        self.conn.commit()
        return True


    def get_admins(self):
        admins = self.cursor.execute('SELECT * FROM beheerders').fetchall()
        return admins


    def get_single_admin(self, admin_id):
        admin = self.cursor.execute('SELECT * FROM beheerders WHERE beheerder_id = ?', (admin_id,)).fetchone()
        return admin


    def admin_edit(self, admin_id, first_name, last_name, email, password):
        self.cursor.execute('UPDATE beheerders '
                            'SET voornaam = ?, achternaam = ?, email = ?, wachtwoord = ?  '
                            'WHERE beheerder_id = ?', (first_name, last_name, email, password, admin_id))
        self.conn.commit()
        return True


    def admin_delete(self, admin_id):
        self.cursor.execute('DELETE FROM beheerders WHERE beheerder_id = ?', (admin_id,))
        self.conn.commit()
        return True