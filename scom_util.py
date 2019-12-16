from SCOM_APP.models import *
from User.models import *
from random import *
from datetime import datetime
from string import ascii_lowercase as letters
from string import ascii_uppercase as big_letters

big_letters = list(big_letters)
letters = list(letters)

def genBaseName(count):
    special_letters = 'a i u e o'.split()
    another_letters = [i for i in letters if i not in special_letters]
    name = []

    name_model = randint(0, 1)
    if (name_model==0):
        for i in range(int(count/2 if count%2==0 else count/2-0.5)):
            name+=choice(special_letters)
            name+=choice(another_letters)
        if (count%2==1):
            name+=choice(special_letters)
    else:
        for i in range(int(count/2 if count%2==0 else count/2-0.5)):
            name+=choice(another_letters)
            name+=choice(special_letters)
        if (count%2==1):
            name+=choice(another_letters)

    
    name[0] = big_letters[letters.index(name[0])]
    name = "".join(name)
    return name

def genFullName(count0, count1):
    return " ".join([genBaseName(count1) for i in range(count0)])

def genNumber(count):
    start = 10**(count-1)
    stop = int("".join(["9" for i in range(count)]))
    #print(start, stop)
    return randrange(start, stop+1)

cities = ["Bojonggede", "Jakarta", "Hong-kong"]
planets = ["Merkurius", "Venus", "Bumi", "Mars", "Jupiter", "Saturnus", "Uranus", "Neptunus", "Pluto"]


def addTeachers(count):
    gagal = 0
    for i in range(count):
        nip=genNumber(10)
        nuptk=genNumber(10)
        nama=genFullName(randrange(2, 5), randrange(3, 7))
        tanggal_lahir=datetime(year=randrange(1980, 1990), month=randrange(1, 13), day=randrange(1, 29))
        born = choice(planets)
        where = choice(cities)       
        try:
            InfoGuru(
                nip=nip,
                nama=nama,
                nuptk=nuptk,
                tanggal_lahir=tanggal_lahir,
                tempat_lahir=born,      
                alamat=where,
                status_aktif=True
                ).save()
            LoginGuru(username=nip, password=born).save()
            print(f"{i} NIP: {nip} Nama: {nama} Alamat: {born}")

        except Exception as e:    
            print(e)
            gagal+=1
    
    print(f"Fail: {gagal}")


def addMapel(nameScoreDict):
    for name in nameScoreDict:
        score = nameScoreDict[name]
        Mapel(nama=name, kkm=score).save()
    

def addMajor(nama):
    teachers = list(InfoGuru.objects.all())
    nama_singkat="".join([i[0] for i in nama.split()])
    print(nama_singkat)
    Jurusan(nama_jurusan=nama, nama_singkatan_jurusan=nama_singkat, kepala_program=choice(teachers), status_aktif=True).save()


def addStudents(count):
    majors = list(Jurusan.objects.all())
    lahir_kelas = {10: 2004, 11: 2003, 12: 2002}

    gagal = 0
    for i in range(count):
        nis=genNumber(10)
        nama=genFullName(randrange(2, 5), randrange(3, 7))
        tingkat_kelas=randrange(10, 13)
        jurusan = choice(majors)
        tanggal_lahir=datetime(year=lahir_kelas[tingkat_kelas], month=randrange(1, 13), day=randrange(1, 29))
        tempat_lahir = choice(planets)
        alamat = choice(cities)        
        try:
            InfoSiswa(
                nis=nis,
                nama=nama,
                tingkat_kelas=tingkat_kelas,
                jurusan=jurusan,
                tanggal_lahir=tanggal_lahir,
                tempat_lahir=tempat_lahir,
                alamat=alamat,
                status_aktif=True
                ).save()
            print(f"{i} NIS: {nis} Nama: {nama}")
        except Exception as e:    
            print(e)
            gagal+=1
    
    print(f"Fail: {gagal}")

def genNilaiUTS(count):
    students = list(InfoSiswa.objects.all())
    mapel = list(Mapel.objects.all())
    for i in range(count):
        student = choice(students)
        mata_pel = choice(mapel)
        score = randrange(0, 101)
        print(i, student.nama, mata_pel.nama, score)
        NilaiUTS(nis=student, mapel=mata_pel, nilai=score).save()
        


def genNilaiUAS(count):
    students = list(InfoSiswa.objects.all())
    mapel = list(Mapel.objects.all())
    for i in range(count):
        student = choice(students)
        mata_pel = choice(mapel)
        score = randrange(0, 101)
        print(i, student.nama, mata_pel.nama, score)
        NilaiUAS(nis=student, mapel=mata_pel, nilai=score).save()
    
# def genClass():
#     teachers = list(InfoGuru.objects.all())
#     students = list(InfoSiswa.objects.all())
#     for jurusan in list(Jurusan.objects.all()):
#         for i in range(10, 13):
#             Kelas(
#                 tingkat=i,
#                 jurusan=jurusan,
#                 nip_wali_kelas=choice(teachers),
#                 nis_ketua_kelas=choice(students),

#                 )
