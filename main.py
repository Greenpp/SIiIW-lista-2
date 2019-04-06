from scp import SCP

scp = SCP(method='back',
          order='none')

if scp.load_data('train_data/futoshiki_5_4.txt'):
# if scp.load_data('test_data/test_futo_9_0.txt'):
    if scp.run() is not None:
        scp.visualize()
    else:
        print('Solution not found')
