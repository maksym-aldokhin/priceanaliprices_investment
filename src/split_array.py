def splitting_array(input_arr, count):
    out = []

    if len(input_arr) < count or len(input_arr) == count:
        for t in input_arr:
            t_thread = [t]
            out.append(t_thread)
    else:
        k, m = divmod(len(input_arr), count)
        out = (input_arr[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(count))

    return out