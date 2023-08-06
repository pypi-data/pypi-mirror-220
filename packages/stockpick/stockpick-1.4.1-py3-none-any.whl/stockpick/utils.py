def max_backward_match(word_list, vocab, max_k=10):
    res = []
    end = len(word_list)

    while end > 0:
        break_flag = False
        for i in range(max_k):
            start = end - max_k + i
            start = start if start >= 0 else 0
            temp = "".join(word_list[start:end])
            if temp in vocab:
                res.append([temp, start, end])
                end = start
                break_flag = True
                break
        if not break_flag:
            end -= 1
    res.reverse()
    return res

# text = "债券和债券逆回购和现金，债券，逆回购。"
# vocab = ["债券", "债券逆回购", "逆回购"]
# res = max_backward_match(text, vocab)
# print(res)