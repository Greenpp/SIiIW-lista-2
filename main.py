from itertools import product

from collector import Collector
from scp import SCP


def run(file_name, method='back', order='none', dynamic=False, collector=None):
    scp = SCP(method=method,
              order=order,
              dynamic_ordering=dynamic
              )

    if scp.load_data(f'test_data/test_{file_name}.txt'):
        scp.run()
        if collector is None:
            scp.show_solutions()
            scp.show_stats()
        else:
            time_delta, returns, evals = scp.get_stats()
            collector.push_data(file_name, time_delta, returns, evals, scp.method, scp.order, scp.dynamic_ordering)


if __name__ == '__main__':
    postfixes = [f'_{i}_{j}' for i in range(4, 7) for j in range(3)]
    # files = ['futo', 'sky']
    files = ['sky']

    # methods = ['back', 'forward']
    methods = ['back']
    orders = ['none', 'min_dom', 'max_con']  # TODO min_con, max_dom
    dynamics = [True, False]

    with Collector() as col:
        for name, postfix in product(files, postfixes):
            file = name + postfix
            for method in methods:
                for order in orders:
                    for dynamic in dynamics:
                        run(file, method, order, dynamic, col)
                        print('.', end='', flush=True)
            print(f'{file} done')

    print('All DONE')
