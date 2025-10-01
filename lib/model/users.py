from lib.model.database import Database
from hashlib import sha256
import bcrypt

class Users:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def check_password(self, password_to_check, expected_password):
            if bcrypt.checkpw(password_to_check.encode('utf-8'), expected_password):
                print(f"Password is correct")
                return expected_password
            else:
                print(f"Password is incorrect")
                return None

    def login(self, email, password):
        print(f"In de login functie")
        print(f"Email: {email}")
        print(f"Hashed password: {password}")
        expert = self.cursor.execute('SELECT * FROM deskundigen WHERE email = ?',(email,)).fetchone()
        print(f"Expert: {expert}")
        if  expert is not None:
            print(f"Expert found: {expert}")
            print(f"Expected password expert: {expert['wachtwoord']}")
            checked_password_deskundige = self.check_password(password, expert['wachtwoord'])
            if checked_password_deskundige:
                if expert['status'] == 'GOEDGEKEURD':
                    return {"user": expert, "account_type": 'expert'}
                elif expert['status'] == 'NIEUW':
                    return "Uw registratie is in behandeling."
                elif expert['status'] == 'AFGEKEURD':
                    return "Uw registratie is afgekeurd."
        else:
            print(f"Expert not found")
            admin = self.cursor.execute('SELECT * FROM beheerders WHERE email = ?',
                                    (email,)).fetchone()
            print(f"Admin: {admin}")
            if admin is not None:
                print(f"Admin gevonden: {admin['voornaam']} {admin['achternaam']}")
                print(f"Expected password admin: {admin['wachtwoord']}")
                checked_password_admin = self.check_password(password, admin['wachtwoord'])
                if checked_password_admin:
                    return {"user": admin, "account_type": 'admin'}
            else:
                print(f"Admin not found")
                checked_password_admin = None

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
        return dict(admin)


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

# Hash password using bcrypt
def hash_password(password):
    # Encode password to bytes
    password = password.encode('utf-8')

    # Generate salt
    salt = bcrypt.gensalt()

    # Hash password
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password