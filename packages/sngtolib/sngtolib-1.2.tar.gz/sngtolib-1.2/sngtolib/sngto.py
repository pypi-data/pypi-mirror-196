def check_prime_number(n):
    # flag = 0 => không phải số nguyên tố
    # flag = 1 => số nguyên tố
    flag = 1
    if n < 2:
        flag = 0
        return flag  # Số nhỏ hơn 2 không phải số nguyên tố => trả về 0
    
    # Sử dụng vòng lặp for để kiểm tra có tồn tại ước số nào khác không
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            flag = 0
            break  # Chỉ cần tìm thấy 1 ước số là đủ và thoát vòng lặp
    return flag
