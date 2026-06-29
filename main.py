import streamlit as st
from services.auth_service import AuthServices
from services.pet_service import PetServices

st.set_page_config(page_title="PetPals System Pro", page_icon="🐾", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #FFF0F5; }
    h1, h2, h3 { color: #FF69B4 !important; font-family: 'Comic Sans MS', sans-serif; }
    .stButton>button {
        background-color: #FF69B4; color: white; border-radius: 20px; border: 2px solid #FF1493;
    }
    .stButton>button:hover { background-color: #FF1493; color: white; }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi Session State
if "auth_service" not in st.session_state:
    st.session_state.auth_service = AuthServices()
    st.session_state.pet_service = PetServices()
    st.session_state.user_aktif = None

auth = st.session_state.auth_service
service = st.session_state.pet_service

# --- TAMPILAN LOGIN ---
if st.session_state.user_aktif is None:
    st.title("🐾 Welcome to PetPals System")
    st.subheader("Silakan login menggunakan akun Admin/Staff")
    
    with st.form("form_login"):
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        
        if st.form_submit_button("Log In"):
            sukses, hasil = auth.login(username, password)
            if sukses:
                st.session_state.user_aktif = hasil
                st.success(f"Berhasil Masuk! Halo {hasil.username} ({hasil.role})")
                st.rerun()
            else:
                st.error(hasil)

# --- TAMPILAN DASHBOARD UTAMA ---
else:
    user = st.session_state.user_aktif
    st.sidebar.title(f"🌸 PetPals Menu")
    st.sidebar.write(f"User: **{user.username}** | Role: **{user.role}**")
    
    if st.sidebar.button("Log Out"):
        st.session_state.user_aktif = None
        st.rerun()

    st.title("💖 PetPals Management Dashboard")
    tab1, tab2 = st.tabs(["🐱 CRUD Data Hewan (Pet)", "🏠 Fasilitas & Kamar (Room)"])

    # TAB 1: CRUD DATA HEWAN
    with tab1:
        st.write("Materi Terintegrasi: *Encapsulation, Input Validation, Exception Handling, JSON CRUD*")
        aksi = st.selectbox("Aksi CRUD Pet:", ["Lihat Semua (Read)", "Tambah Pet (Create)", "Update Pet (Update)", "Hapus Pet (Delete)"])
        
        if aksi == "Lihat Semua (Read)":
            st.subheader("📋 Daftar Anggota Peliharaan Aktif")
            data = service.get_all_pets()
            if not data:
                st.info("Belum ada data hewan peliharaan.")
            else:
                st.table([p.to_dict() for p in data])
                
        elif aksi == "Tambah Pet (Create)":
            st.subheader("➕ Tambah Peliharaan")
            with st.form("add_pet"):
                id_p = st.text_input("ID Pet (Unik):")
                nm_p = st.text_input("Nama Hewan:")
                jn_p = st.selectbox("Jenis:", ["Kucing", "Anjing", "Kelinci", "Hamster"])
                um_p = st.number_input("Umur (Bulan):", min_value=-5, max_value=200, value=5, step=1)
                st_p = st.selectbox("Kondisi Kesehatan:", ["Sehat/Vaksin", "Perawatan Medis", "Isolasi"])
                
                if st.form_submit_button("Simpan"):
                    s, msg = service.create_pet(id_p, nm_p, jn_p, um_p, st_p)
                    if s:
                        st.success(msg)
                    else:
                        st.error(msg)

        elif aksi == "Update Pet (Update)":
            st.subheader("🔄 Update Informasi Hewan")
            all_p = service.get_all_pets()
            if not all_p: 
                st.info("Tidak ada data pet untuk di-update.")
            else:
                target_id = st.selectbox("Pilih ID Pet yang akan di-update:", [p.id_pet for p in all_p])
                p_sel = next(p for p in all_p if p.id_pet == target_id)
                
                with st.form("up_pet"):
                    nm_p = st.text_input("Nama:", value=p_sel.nama)
                    jn_p = st.selectbox("Jenis:", ["Kucing", "Anjing", "Kelinci", "Hamster"], index=["Kucing", "Anjing", "Kelinci", "Hamster"].index(p_sel.jenis))
                    um_p = st.number_input("Umur (Bulan):", value=int(p_sel.umur))
                    st_p = st.selectbox("Kesehatan:", ["Sehat/Vaksin", "Perawatan Medis", "Isolasi"], index=["Sehat/Vaksin", "Perawatan Medis", "Isolasi"].index(p_sel.status_kesehatan))
                    
                    if st.form_submit_button("Simpan Perubahan"):
                        s, msg = service.update_pet(target_id, nm_p, jn_p, um_p, st_p)
                        if s:
                            st.success(msg)
                        else:
                            st.error(msg)

        elif aksi == "Hapus Pet (Delete)":
            st.subheader("❌ Hapus Data Peliharaan")
            all_p = service.get_all_pets()
            if not all_p: 
                st.info("Tidak ada data pet di sistem.")
            else:
                target_id = st.selectbox("Pilih ID Pet yang mau dihapus:", [p.id_pet for p in all_p])
                if st.button("Hapus Permanen Dari Sistem"):
                    s, msg = service.delete_pet(target_id)
                    st.success(msg)
                    st.rerun()

    # TAB 2: POLIMORFISME KAMAR (VIP & STANDARD)
    with tab2:
        st.write("Materi Terintegrasi: *Abstract Class, Polymorphism Overriding, Static Method & Duck Typing*")
        st.subheader("🏨 Manajemen Kamar Pet Hotel")
        menu_room = st.radio("Menu Kamar:", ["Lihat Status Kamar & Fasilitas", "Tambah Kamar Baru (Admin Only)"], horizontal=True)
        
        if menu_room == "Lihat Status Kamar & Fasilitas":
            rooms = service.get_all_rooms()
            if not rooms:
                st.info("Kamar belum terdaftar.")
            else:
                tabel_kamar = []
                for r in rooms:
                    tabel_kamar.append({
                        "ID Kamar": r.id_room,
                        "Nama Kamar": r.nama_room,
                        "Tipe": r.tipe,
                        "Kapasitas": r.kapasitas,
                        "Status": r.status,
                        "Harga (Rp)": r.harga,
                        "Fasilitas": r.get_fasilitas()
                    })
                st.table(tabel_kamar if 'tabel_kamar' in locals() else tabel_kamar)

        elif menu_room == "Tambah Kamar Baru (Admin Only)":
            if user.role != "Admin":
                st.error("🔒 Akses Ditolak: Hanya Akun dengan Role Admin yang bisa mendaftarkan unit kamar baru!")
            else:
                with st.form("add_room"):
                    id_r = st.text_input("ID Kamar (cth: VIP02, STD03):")
                    nm_r = st.text_input("Nama Ruangan:")
                    tipe_r = st.selectbox("Tipe Kamar (Inheritance Target):", ["VIP", "Standard"])
                    kp_r = st.number_input("Kapasitas Maksimal:", min_value=0, max_value=10, value=2, step=1)
                    st_r = st.selectbox("Status Awal:", ["Tersedia", "Penuh"])
                    
                    if st.form_submit_button("Daftarkan Kamar"):
                        s, msg = service.create_room(id_r, nm_r, kp_r, st_r, tipe_r)
                        if s:
                            st.success(msg)
                        else:
                            st.error(msg)