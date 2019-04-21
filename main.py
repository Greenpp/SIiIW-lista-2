from scp import SCP
from timeing import timeit


@timeit
def run():
    scp = SCP(method='forward',
              order='min_dom',
              dynamic_ordering=True,
              all_solutions=True)

    # if scp.load_data('test_data/test_futo_9_0.txt'):
    if scp.load_data('train_data/futoshiki_5_4.txt'):
        scp.run()
        scp.show_solutions()


if __name__ == '__main__':
    run()
