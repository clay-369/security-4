from lib.model.database import Database
from hashlib import sha256

class Users:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def login(self, email, password):
        expert = self.cursor.execute('SELECT * FROM deskundigen WHERE wachtwoord = ? AND email = ?',
                                     (password, email)).fetchone()
        if expert:
            if expert['status'] == 'GOEDGEKEURD':
                return {"user": expert, "account_type": 'expert'}
            elif expert['status'] == 'NIEUW':
                return "Uw registratie is in behandeling."
            elif expert['status'] == 'AFGEKEURD':
                return "Uw registratie is afgekeurd"
        else:
            admin = self.cursor.execute('SELECT * FROM beheerders WHERE wachtwoord= ? AND email = ?',
                                        (password, email)).fetchone()
            if admin is not None:
                return {"user": admin, "account_type": 'admin'}
            else:
                return None


    def admin_create(self, first_name, last_name, email, password):
        password = hash_password(password)
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
        if password:
            password = hash_password(password)
            self.cursor.execute('UPDATE beheerders '
                                'SET voornaam = ?, achternaam = ?, email = ?, wachtwoord = ?  '
                                'WHERE beheerder_id = ?', (first_name, last_name, email, password, admin_id))
        else:
            self.cursor.execute('UPDATE beheerders '
                                'SET voornaam = ?, achternaam = ?, email = ?'
                                'WHERE beheerder_id = ?', (first_name, last_name, email, admin_id))
        self.conn.commit()
        return True


    def admin_delete(self, admin_id):
        self.cursor.execute('DELETE FROM beheerders WHERE beheerder_id = ?', (admin_id,))
        self.conn.commit()
        return True


    def get_admin_by_email(self, email):
        self.cursor.execute("SELECT * FROM beheerders WHERE email = ?", (email,))
        return self.cursor.fetchone()

def hash_password(password):
    return sha256(password.encode('utf-8')).hexdigest()