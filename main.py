from dotenv import load_dotenv,find_dotenv
import os
import pprint
from pymongo import MongoClient
load_dotenv(find_dotenv())
password=os.environ.get("MONGODB_PWD")

connect_string=f"mongodb+srv://nhattanit:{password}@tutorial.hu5u7wa.mongodb.net/?retryWrites=true&w=majority"


client = MongoClient(connect_string, tls=True, tlsAllowInvalidCertificates=True) 
dbs=client.list_database_names()
test_db=client.test 
collections=test_db.list_collection_names()
# print(collections)

# def insert_test_doc():
#     collection=test_db.test
#     test_doc={
#         "name":"Tan",
#         "type":"Test"
#     }

#     inserted_id=collection.insert_one(test_doc).inserted_id
#     print(inserted_id)

production=client.production
sinhvien_collection=production.sinhvien_collection

#taodb
def create_documents():
    ids=[1,2,3,4,5]
    names=["tan","vu","tuan","linh","quang"]
    tuois=[22,33,11,32,25]
    gioitinhs=["nam","nu","nam","nu","nam"]
    toans=[10,2,4,7,5]
    lys=[10,7,8,4,5]
    hoas=[5,2,3,4,9]

    docs=[]
    for id,name,tuoi,gioitinh,toan,ly,hoa in zip(ids,names,tuois,gioitinhs,toans,lys,hoas):
        doc={"id":id,
            "name":name,
            "tuoi":tuoi,
            "gioitinh":gioitinh,
            "diem":{
                "toan":toan,
                "ly":ly,
                "hoa":hoa,
        }}
        docs.append(doc)
    sinhvien_collection.insert_many(docs)
# create_documents()

printer=pprint.PrettyPrinter()

#layDS
def get_all_SV():
    svs=sinhvien_collection.find()
    for sv in svs:
        printer.pprint(sv)

#timtheoten
def find_SV_name(name):
    print(f"==========SV CO ten {name}============")
    sv=sinhvien_collection.find_one({"name":f"{name}"})
    printer.pprint(sv)

#timtheotuoi
def find_SV_age(tuoi):
    print(f"==========SV tuoi {tuoi}============")
    sv=sinhvien_collection.find_one({"tuoi":tuoi})
    printer.pprint(sv)

#xoatheoid
def del_SV(id):
    try:
        sinhvien_collection.delete_one({"id":id})
        print(f"Xoa Thanh cong id :{id} !")
    except:
        print("Xoa khong thanh cong!")

#timtheodiemmon
def find_sv_diem(mon,tdiem):
    print(f"==========SV co diem mon {mon} > {tdiem}============")
    svs=sinhvien_collection.find({ f"diem.{mon}" : { "$gt": tdiem } })
    for sv in svs:
        printer.pprint(sv)

#timtheotongdiem
def find_sv_tongdiem(td):
    svs=sinhvien_collection.aggregate(
    [
        { "$project": { "name":1,"tuoi":1,"gioitinh":1, "TONGDIEM": { "$add": [ '$diem.toan','$diem.ly','$diem.hoa' ] } } },
        {
                "$match":{"TONGDIEM":{"$gt":td}}
            }
    ]
)
    print(f"==========SV CO TONG DIEM >{td}============")
    for sv in svs:
        printer.pprint(sv)




# find_SV_age(22)

def CT(num):
    if num==1:
            get_all_SV()
    elif num==2:
        id=int(input("Mời bạn nhập ID can xoa:"))
        del_SV(id)
    elif num==3:
        name=input("Mời bạn nhập tên cần tìm:")
        find_SV_name(name)
    elif num==4:
        age=int(input("Mời bạn nhập tuổi cần tìm:"))
        find_SV_age(age)
    elif num==5:
        mon=input("Moi ban nhap mon hoc:")
        tdiem=float(input("Moi ban nhap diem:"))
        find_sv_diem(mon,tdiem)
    elif num==6:
        tdiem=float(input("Moi ban nhap diem:"))
        find_sv_tongdiem(tdiem)
    else:
        print("Ban nhap sai format r!")
while True:
    print("============CHUONG TRINH=============")
    print("1.Hiển thị tất cả sinh viên")
    print("2.Xóa sinh viên theo ID")
    print("3.Tìm kiếm sinh viên theo tên")
    print("4.Tìm kiếm sinh viên theo tuổi")
    print("5.Tìm kiếm sinh viên có điểm >n")
    print("6.Tìm kiếm sinh viên có điểm tổng >n")
    print("7.Thoat!")
    number=int(input("Mời bạn nhập lựa chọn của mình:"))
    if number==7:
        break
    CT(number)

