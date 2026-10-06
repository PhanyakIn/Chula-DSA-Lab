def greedy(arr, k):
    n = len(arr)

    used = [False] * n
    count = 0

    for i in range(n):

        # ถ้าเป็น Grab
        if arr[i] == 'G':

            left = max(0, i - k)
            right = min(n - 1, i + k)

            # หา Passenger ที่อยู่ในระยะ
            # และเลือกคนที่อยู่ซ้ายสุด
            for j in range(left, right + 1):

                if arr[j] == 'P' and not used[j]:
                    used[j] = True
                    count += 1
                    break

    return count

arr = 'GGGGGGGGGGGGGGGGGGPGPGPPPPPPPPPPPPPPPPPP'
k = 2

print(greedy(arr,k))