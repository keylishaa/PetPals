from storage.json_storage import JSONStorage
from models.pet import Pet
from models.room import RoomStandard, RoomVIP

# Custom Exception 
class PetpalsValidationError(Exception):
    pass


class PetServices:
    def __init__(self):
        # Dependency Injection (Engine menyuntikkan JSONStorage komponen ke service)
        self.pet_storage = JSONStorage('pets.json')
        self.room_storage = JSONStorage('rooms.json')
        
        self.pets_data = self.pet_storage.load()
        self.rooms_data = self.room_storage.load()
        self._inisialisasi_kamar_default()

    def _inisialisasi_kamar_default(self):
        if not self.rooms_data:
            # Mengisi master data kamar standard & VIP secara instan
            r1 = RoomStandard("STD01", "Kamar Standar Mungil")
            r2 = RoomStandard("STD02", "Kamar Standar Cozy")
            r3 = RoomVIP("VIP01", "Kamar VIP Luxurious Room")
            
            self.rooms_data = [
                {"id_room": r1.id_room, "nama_room": r1.nama_room, "kapasitas": r1.kapasitas, "status": r1.status, "tipe": "Standard", "harga": r1.harga},
                {"id_room": r2.id_room, "nama_room": r2.nama_room, "kapasitas": r2.kapasitas, "status": r2.status, "tipe": "Standard", "harga": r2.harga},
                {"id_room": r3.id_room, "nama_room": r3.nama_room, "kapasitas": r3.kapasitas, "status": r3.status, "tipe": "VIP", "harga": r3.harga}
            ]
            self.room_storage.save(self.rooms_data)

    # ==================== CRUD: DATA PET (HEWAN) ====================
    def get_all_pets(self):
        # READ: Mengubah data mentah dict JSON menjadi kumpulan Objek Pet
        return [Pet.from_dict(p) for p in self.pets_data]

    def create_pet(self, id_pet, nama, jenis, umur, status_kesehatan):
        try:
            # Validasi Input & Custom Exception Triggering
            if not id_pet or not nama:
                raise PetpalsValidationError("ID Pet dan Nama tidak boleh kosong!")
            
            for p in self.pets_data:
                if p["id_pet"] == id_pet:
                    raise PetpalsValidationError(f"Gagal! ID Pet '{id_pet}' sudah ada di database.")

            # Instansiasi Objek baru (Validasi Umur ditangani di dalam Property Setter)
            new_pet = Pet(id_pet, nama, jenis, umur, status_kesehatan)
            self.pets_data.append(new_pet.to_dict())
            self.pet_storage.save(self.pets_data)
            return True, f"Berhasil menambahkan {nama} ke sistem PetPals!"
        except (ValueError, PetpalsValidationError) as err:
            return False, str(err)

    def update_pet(self, id_pet, nama, jenis, umur, status_kesehatan):
        try:
            for p in self.pets_data:
                if p["id_pet"] == id_pet:
                    # Validasi via rekonstruksi objek sementara
                    updated_obj = Pet(id_pet, nama, jenis, umur, status_kesehatan)
                    p.update(updated_obj.to_dict())
                    self.pet_storage.save(self.pets_data)
                    return True, f"Data Pet ID {id_pet} berhasil diperbarui!"
            return False, "Data Pet tidak ditemukan."
        except ValueError as err:
            return False, str(err)

    def delete_pet(self, id_pet):
        for p in self.pets_data:
            if p["id_pet"] == id_pet:
                self.pets_data.remove(p)
                self.pet_storage.save(self.pets_data)
                return True, f"Pet dengan ID {id_pet} sukses dihapus dari database!"
        return False, "Gagal menghapus: Pet tidak ditemukan."

    # ==================== MANAJEMEN: ROOM (KAMAR) ====================
    def get_all_rooms(self):
        list_room_obj = []
        for r in self.rooms_data:
            if r["tipe"] == "VIP":
                obj = RoomVIP(r["id_room"], r["nama_room"], r["kapasitas"], r["status"], r["harga"])
            else:
                obj = RoomStandard(r["id_room"], r["nama_room"], r["kapasitas"], r["status"], r["harga"])
            list_room_obj.append(obj)
        return list_room_obj

    def create_room(self, id_room, nama_room, kapasitas, status, tipe):
        try:
            if not id_room or not nama_room:
                raise PetpalsValidationError("ID Kamar dan Nama Kamar wajib diisi!")
            
            for r in self.rooms_data:
                if r["id_room"] == id_room:
                    raise PetpalsValidationError(f"ID Kamar {id_room} sudah terdaftar!")

            if tipe == "VIP":
                room_obj = RoomVIP(id_room, nama_room, kapasitas, status)
            else:
                room_obj = RoomStandard(id_room, nama_room, kapasitas, status)

            self.rooms_data.append({
                "id_room": room_obj.id_room,
                "nama_room": room_obj.nama_room,
                "kapasitas": room_obj.kapasitas,
                "status": room_obj.status,
                "tipe": tipe,
                "harga": room_obj.harga
            })
            self.room_storage.save(self.rooms_data)
            return True, f"Kamar {tipe} {id_room} berhasil ditambahkan!"
        except (ValueError, PetpalsValidationError) as err:
            return False, str(err)

    # --- Implementasi Duck Typing ---
    # Fungsi ini menerima objek apa saja asal memiliki method 'get_fasilitas()'
    @staticmethod
    def ekstrak_fasilitas_kamar(objek_kamar):
        return objek_kamar.get_fasilitas()