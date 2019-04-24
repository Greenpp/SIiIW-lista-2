from scp import SCP
from timeing import timeit


@timeit
def run():
    scp = SCP(method='back',
              order='none',
              dynamic_ordering=False,
              all_solutions=False)

    # if scp.load_data('test_data/test_futo_9_0.txt'):
    # if scp.load_data('train_data/futoshiki_5_4.txt'):
    # if scp.load_data('train_data/skyscrapper_4_1.txt'):
    if scp.load_data('test_data/test_sky_6_0.txt'):
        scp.run()
        scp.show_solutions()


if __name__ == '__main__':
    run()
