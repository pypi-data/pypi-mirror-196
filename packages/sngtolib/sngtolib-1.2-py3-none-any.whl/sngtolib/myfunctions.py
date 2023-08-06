dem = 0 # biến toàn cục
def check_prime_number(n):
    #flag = 0 => không phải số nguyên tố
    #flag = 1 => số nguyên tố
    flag = 1;
    if (n <2):
        flag = 0
        return flag  #Số nhỏ hơn 2 không phải số nguyên tố => trả về 0
    
    #Sử dụng vòng lặp while để kiểm tra có tồn tại ước số nào khác không
    for i in range(2, n):
        if n % i == 0:
            flag = 0
            break #Chỉ cần tìm thấy 1 ước số là đủ và thoát vòng lặp
    return flag

"""n = int(input(">> nhap mot so n: "))
for i in range(n):
    check = check_prime_number(i)
    if( check == 1 ) :
        print(i)
ds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
for k in ds:
    if check_prime_number(k) == 1:
        dem += 1
print("So luong so nguyen to trong day la:", dem)"""
