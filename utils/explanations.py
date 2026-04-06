def decimal_to_binary_steps(n):
    steps = []
    num = n

    while num > 0:
        q = num // 2
        r = num % 2
        steps.append(f"{num} ÷ 2 = {q} والباقي {r}")
        num = q

    result = ''.join(str(int(s.split()[-1])) for s in steps[::-1])
    return "\n".join(steps), result