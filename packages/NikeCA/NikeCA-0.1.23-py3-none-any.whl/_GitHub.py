

class GitHub:

    def github_dependencies(self, tables: list | str = None, token: str = None):

        import pandas as pd
        import requests
        import re
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

        # there is a search limit of 30 searches in 1 minute for github so the list is chunked by 29 and checked to
        # ensure that 75 seconds had passed
        for chunk in chunks:
            print(len(chunk), 'is chunk length')
            # time.sleep(60)
            print(chunk)

            used = requests.get('https://api.github.com/rate_limit', headers=headers).json()
            print(used['resources']['search']['used'])

            while used['resources']['search']['used'] != 0:
                print(used['resources']['search']['used'])
                time.sleep(1)
                used = requests.get('https://api.github.com/rate_limit', headers=headers).json()

            for table in chunk:
                # try:
                print('Searching ' + str(table) + '\n')
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

        return df







