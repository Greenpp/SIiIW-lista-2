from scp import SCP

scp = SCP(method='forward',
          order='none',
          all_solutions=True)

if scp.load_data('train_data/futoshiki_5_4.txt'):
# if scp.load_data('test_data/test_futo_7_0.txt'):
    scp.run()
    scp.show_solutions()
