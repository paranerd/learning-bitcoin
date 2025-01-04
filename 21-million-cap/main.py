INITIAL_REWARD_BTC = 50
MAX_BITCOIN = 21000000
BLOCKS_BETWEEN_HALVINGS = 210000

def halve(data):
  data['halving'] += 1
  data['year'] += 4
  data['new_btc_mined'] = BLOCKS_BETWEEN_HALVINGS * data['reward_btc']
  data['total_btc'] += BLOCKS_BETWEEN_HALVINGS * data['reward_btc']
  data['reward_btc'] /= 2

  return data

if __name__ == "__main__":
  data = {
    'halving': 0,
    'year': 2008,
    'reward_btc': INITIAL_REWARD_BTC,
    'new_btc_mined': 0,
    'total_btc': 0
  }

  header = '| {:>2} | {:^4} | {:>11} | {:<20} | {:<20} | {:<17} |'.format(*['Halving', 'Year', 'Reward BTC', 'New BTC mined', 'Total BTC', '% of max BTC'])

  print(header)
  print('-' * len(header))

  # Halve until reward is < 1 Satoshi
  while data['reward_btc'] > 0.00000001:
    print('| {:^7} | {:^4} | {:>11} | {:<20} | {:<20} | {:<17} |'.format(*[data['halving'], data['year'], f"{format(data['reward_btc'], '.8f')}", data['new_btc_mined'], data['total_btc'], f"{data['total_btc'] / MAX_BITCOIN * 100}"]))

    data = halve(data)