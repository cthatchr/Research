import matplotlib.pyplot as plt


def compare_lineplot(index, sum, avg, dist):
    # create a line plot given a set of data
    plt.figure()
    plt.suptitle('Stock Difference After Algorithm', fontsize=16)
    plt.subplots_adjust(hspace=1)
    # plot sums
    plt.subplot(211)
    plt.title('Total')
    plt.xlabel('Users Rerouted')
    plt.ylabel('Stock Difference')
    plt.plot(index, sum[0], label='Default')
    plt.plot(index, sum[1], label='Distance^2')
    plt.plot(index, sum[2], label='Difference^2')
    plt.plot(index, sum[3], label='Only Distance')
    plt.plot(index, sum[4], label='Only Difference')
    plt.plot(index, sum[5], label='Random')
    plt.locator_params(axis='y', nbins=5)
    # plot avgs
    plt.subplot(212)
    plt.title('Average')
    plt.xlabel('Users Rerouted')
    plt.ylabel('Stock Difference')
    plt.plot(index, avg[0], label='Default')
    plt.plot(index, avg[1], label='Distance^2')
    plt.plot(index, avg[2], label='Difference^2')
    plt.plot(index, avg[3], label='Only Distance')
    plt.plot(index, avg[4], label='Only Difference')
    plt.plot(index, avg[5], label='Random')
    plt.locator_params(axis='y', nbins=5)
    plt.legend()
    plt.figure()

    # user distance moved
    plt.title('Distance Users Rerouted')
    plt.xlabel('Users Rerouted')
    plt.ylabel('Distance(Meters)')
    plt.plot(index, dist[0], label='Diff/Dist')
    plt.plot(index, dist[1], label='Diff/Dist^2')
    plt.plot(index, dist[2], label='Diff^2/Dist')
    plt.plot(index, dist[3], label='Only Dist')
    plt.plot(index, dist[4], label='Only Diff')
    plt.plot(index, dist[5], label='Random')
    plt.locator_params(axis='y', nbins=5)
    plt.legend()
    plt.show()


def create_dist_plot(index, dist):
    # user distance moved
    plt.figure()
    plt.title('Distance Users Rerouted')
    plt.xlabel('Users Rerouted')
    plt.ylabel('Distance(Meters)')
    plt.plot(index, dist[0], label='Diff/Dist')
    plt.plot(index, dist[1], label='Diff/Dist^2')
    plt.plot(index, dist[2], label='Diff^2/Dist')
    plt.plot(index, dist[3], label='Only Dist')
    plt.plot(index, dist[4], label='Only Diff')
    plt.plot(index, dist[5], label='Random')
    plt.locator_params(axis='y', nbins=5)
    plt.legend()
    plt.show(block=False)
