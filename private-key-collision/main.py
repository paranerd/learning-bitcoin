NUM_TOTAL_KEYS = 115792089237316195423570985008687907852837564279074904382605163141518161494336
NUM_COMPUTERS = 1000000
NUM_KEYS_PER_SEC = 1000000

def calculate_years_to_collision():
    total_keys_per_second = NUM_COMPUTERS * NUM_KEYS_PER_SEC

    seconds_per_year = 60 * 60 * 24 * 365
    years_to_collision = NUM_TOTAL_KEYS / total_keys_per_second / seconds_per_year

    return years_to_collision

if __name__ == "__main__":
    print(f'Years to collision: {calculate_years_to_collision()}')