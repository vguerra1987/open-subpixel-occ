import numpy as np

# 5 ones - half byte - 0 - half byte

num_bits = 8

matrix = np.ones((256, 5), dtype=np.int)
symbol_period = 4/30.0
frame_period = 1/30.0

temp = np.empty((0, num_bits))
for i in range(np.power(2, num_bits)):
    unpacked = np.unpackbits(np.array(i, dtype=np.uint8), axis=0, count=num_bits)
    temp = np.concatenate((temp, unpacked[np.newaxis, ...]), axis=0)

matrix = np.concatenate((matrix, np.zeros((256, 1)), temp[:, :4], np.zeros((256, 1)), temp[:, 4:]), axis=1)

oversampling = np.round(symbol_period/frame_period).astype(int)

matrix = np.repeat(matrix, oversampling, axis=1).astype(np.float)
L_matrix = matrix.shape[1]

matrix -= np.repeat(np.mean(matrix, axis=1)[..., np.newaxis], L_matrix, axis=1)
matrix /= np.repeat(np.std(matrix, axis=1)[..., np.newaxis], L_matrix, axis=1)


def decode(buffer, threshold):

    buffer_ = buffer.copy()

    L_buffer = len(buffer_)

    L_res = L_buffer - L_matrix + 1

    result = np.zeros((np.power(2, num_bits), L_res))

    for pos in range(L_res):
        buffer__ = buffer_[pos:pos + L_matrix] - np.mean(buffer_[pos:pos + L_matrix])
        buffer__ /= np.std(buffer__) if np.std(buffer__) > 5 else 10000
        result[:, pos] = np.matmul(matrix, buffer__)/L_matrix

    arg_max = np.argwhere(result == np.max(result.flatten()))[0]

    if result[arg_max[0], arg_max[1]] > threshold:
        return arg_max[0]
    else:
        return None
