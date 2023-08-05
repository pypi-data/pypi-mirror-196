

class GitHub:

    def github_dependencies(self, tables: list | str, token: str):
        import requests
        import re

        import pandas as pd

        import time

        from warnings import simplefilter
        simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

        from github import Github

        g = Github(token)

        df = pd.DataFrame([], index=[[], []])

        counter = 1
        for table in tables:
            print('Searching ' + str(table) + ': \t\t Table number ' + str(counter) + '\n')
            for file in g.search_code('org:nike-impr-analytics ' + table):

                result = requests.get(file.download_url).text

                indexes = [index.start() for index in re.finditer(table.upper(), result.upper())]

                instance = 1

                for index in indexes:

                    if index < 250:
                        index = 250

                    instance += 1

                    df.loc[(table, str(file.repository.name) + '/' + str(file.path)), 'Start'] = result[:1000]

                    df.loc[(table, str(file.repository.name) + '/' + str(file.path)), str(index)] = \
                        result[index - 250: index + 250]
            counter += 1
            time.sleep(2.0001)

        return df




