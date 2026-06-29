import uuid
from storage.json_storage import JSONStorage
from models.user import Admin, Customer

class AuthServices:
    def __init__(self):
        self.storage = JSONStorage('users.json')
        self.users_data = self.storage.load()
        self._inisialisasi_admin_default()

    def _inisialisasi_admin_default(self):
        # Menyediakan akun default jika users.json kosong demi simulasi sistem
        if not self.users_data:
            admin_default = Admin(str(uuid.uuid4()), "admin", "admin@petpals.com", "admin123")
            staff_default = Customer(str(uuid.uuid4()), "staff", "staff@petpals.com", "staff123")
            self.users_data.append(admin_default.to_dict())
            self.users_data.append(staff_default.to_dict())
            self.storage.save(self.users_data)

    def login(self, username, password):
        # Validasi Input Lapisan Pertama
        if not username or not password:
            return False, "Username dan password tidak boleh kosong!"

        for u in self.users_data:
            if u['username'] == username:
                # Rekonstruksi Objek Polimorfis berdasarkan Role data JSON
                if u['role'] == 'Admin':
                    user_obj = Admin(u['id_user'], u['username'], u['email'], u['password'])
                else:
                    user_obj = Customer(u['id_user'], u['username'], u['email'], u['password'])
                
                if user_obj.check_password(password):
                    return True, user_obj
        return False, "Username atau Password salah!"