

class GitHub:

    def github_dependencies(self, tables: list | str = None, token: str = None, save_path: str = None):

        import pandas as pd
        import requests
        import re
        import random
        import time
        from github import Github as g

        from warnings import simplefilter
        simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

        if tables is str:
            tables = [tables]

        g = g(token)
        headers = {'Authorization': 'token ' + token}

        tables = [*set(tables)]
        print(len(tables))

        n = 29
        # using list comprehension
        chunks = [tables[i:i + n] for i in range(0, len(tables), n)]

        df = pd.DataFrame([], index=[[], []])

        counter = 1

        # there is a search limit of 30 searches in 1 minute for github so the list is chunked by 29 and checked to
        # ensure that 75 seconds had passed
        for chunk in chunks:
            print(len(chunk), 'is chunk length')
            # time.sleep(60)
            print(chunk)

            used = requests.get('https://api.github.com/rate_limit', headers=headers).json()
            print(used['resources']['search']['used'])

            while used['resources']['search']['used'] > 0:
                dice = random.choice([2, 3, 4, 6, 7, 9, 10, 11, 12])
                print(f"\nWant to play?\nLet's roll the dice: \n\tYou rolled a {dice}\n\nIn the Jungle you must wait "
                      f"until the dice roll 5 or 8")

                print('\nYou must wait ' + str(int(used['resources']['search']['reset']) - int(time.time()) + 3) +
                      ' seconds before rolling again.\n')

                time_now = int(time.time())
                if int(used['resources']['search']['reset']) - int(time_now) > 0:
                    time.sleep(int(used['resources']['search']['reset']) - (time.time()) + 3)

                used = requests.get('https://api.github.com/rate_limit', headers=headers).json()

            dice = random.choice([5, 8])

            print(f"\nLet's roll the dice: \n\tYou rolled a {dice}\nPlease proceed:\n")

            for table in chunk:
                # try:
                print('Searching ' + str(table) + ':\t\t\t\ttable number: ' + str(counter))
                for file in g.search_code('org:nike-impr-analytics ' + table):

                    result = requests.get(file.download_url)

                    result = result.text

                    indexes = [index.start() for index in re.finditer(table.upper(), result.upper())]

                    instance = 1

                    for index in indexes:

                        if index < 250:
                            index = 250

                        instance += 1

                        df.loc[(table, str(file.repository.name) + '/' + str(file.path)), 'Start'] = result[:1000]

                        df.loc[(table, str(file.repository.name) + '/' + str(file.path)), str(index)] = \
                            result[index - 250: index + 250]
                time.sleep(2.001)
                counter += 1

            df.to_csv(save_path, mode='a', index=True)

        return df






