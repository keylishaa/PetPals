from abc import ABC, abstractmethod

# 1. Abstraction & Abstract Class
class Room(ABC):
    def __init__(self, id_room, nama_room, kapasitas, status, harga):
        self._id_room = id_room
        self._nama_room = nama_room
        self.kapasitas = kapasitas  # Melalui setter validasi
        self._status = status
        self._harga = harga

    @property
    def id_room(self): return self._id_room

    @property
    def nama_room(self): return self._nama_room

    @property
    def status(self): return self._status
    
    @status.setter
    def status(self, nilai): self._status = nilai

    @property
    def harga(self): return self._harga

    @property
    def kapasitas(self): return self._kapasitas

    @kapasitas.setter
    def kapasitas(self, nilai):
        if nilai < 1:
            raise ValueError("Kapasitas maksimal kamar tidak boleh kurang dari 1!")
        self._kapasitas = nilai

    # Abstract Method yang harus di-override (Polymorphism)
    @abstractmethod
    def get_fasilitas(self):
        pass


# 2. Inheritance & Method Overriding (RoomStandard)
class RoomStandard(Room):
    def __init__(self, id_room, nama_room, kapasitas=3, status="Tersedia", harga=100000):
        super().__init__(id_room, nama_room, kapasitas, status, harga)
        self.tipe = "Standard"

    # Method Overriding
    def get_fasilitas(self):
        return "Kandang Standar, Makan 2x Sehari, Air Minum Steril"


# 3. Inheritance & Method Overriding (RoomVIP)
class RoomVIP(Room):
    def __init__(self, id_room, nama_room, kapasitas=1, status="Tersedia", harga=250000):
        super().__init__(id_room, nama_room, kapasitas, status, harga)
        self.tipe = "VIP"
        self._layanan_grooming = True

    # Method Overriding
    def get_fasilitas(self):
        return "Kandang Luas (Full AC), Makan 3x Sehari, Layanan Grooming Gratis, CCTV Akses"