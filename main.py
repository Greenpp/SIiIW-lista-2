from scp import SCP

scp = SCP(method='back',
          order='none')

if scp.load_data('train_data/futoshiki_4_0.txt', 'futo'):
    scp.run()
