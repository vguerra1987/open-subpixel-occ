from matplotlib import pyplot as plt
import numpy as np
import Decoder


def decode(connection, pos):
    plt.ion()

    fig_handle = plt.figure(pos)
    position_string = f'+{np.mod(pos, 2)*800}+{0 if pos < 2 else 500}'
    ax_handle = fig_handle.add_subplot(111)
    ax_handle.set_ylim(0, 255)
    #
    plt.get_current_fig_manager().window.wm_geometry(position_string)
    buffer = np.random.randn(100)
    curve_handle = ax_handle.plot(buffer)[0]

    print('Process started!')

    while True:
        pixel = connection.get()
        buffer = np.roll(buffer, -1, axis=0)
        buffer[-1] = pixel

        estimated_symbol = Decoder.decode(buffer,  0.9)

        if estimated_symbol is not None:
            print(estimated_symbol)
            curve_handle.set_ydata(buffer)
            fig_handle.canvas.draw()
            fig_handle.canvas.flush_events()
            buffer = np.random.randn(100)

    # plt.show()