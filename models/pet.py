class Pet:
    def __init__(self, id_pet, nama, jenis, umur, status_kesehatan):
        self._id_pet = id_pet
        self._nama = nama
        self._jenis = jenis
        self.umur = umur  # Menggunakan setter untuk validasi
        self._status_kesehatan = status_kesehatan

    # --- Property Getter & Setter untuk Encapsulation & Validasi ---
    @property
    def id_pet(self):
        return self._id_pet

    @property
    def nama(self):
        return self._nama

    @property
    def jenis(self):
        return self._jenis

    @property
    def umur(self):
        return self._umur

    @umur.setter
    def umur(self, nilai):
        if nilai <= 0:
            raise ValueError("Umur hewan harus lebih besar dari 0 bulan!")
        self._umur = nilai

    @property
    def status_kesehatan(self):
        return self._status_kesehatan

    @status_kesehatan.setter
    def status_kesehatan(self, nilai):
        self._status_kesehatan = nilai

    # --- Konsep local JSON parsing via OOP ---
    def to_dict(self):
        return {
            "id_pet": self.id_pet,
            "nama": self.nama,
            "jenis": self.jenis,
            "umur": self.umur,
            "status_kesehatan": self.status_kesehatan
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["id_pet"], data["nama"], data["jenis"], data["umur"], data["status_kesehatan"])