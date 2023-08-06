import asyncio
import pprint
import time

import httpx
import pandas as pd


class GitHub:
    import httpx

    def github_dependencies(self, tables: list | str = None, token: str = None):

        import pandas as pd

        from warnings import simplefilter
        simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

        if tables is str:
            tables = [tables]

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(GitHub.fetch_all_queries(self, tables=tables, token=token))
        return result

    async def fetch_query(self, table, token, client: httpx.AsyncClient):

        import pandas as pd
        import re

        from github import Github as G

        g = G(token)

        df = pd.DataFrame([], index=[[], []])

        # for table in tables:
        # try:
        print('Searching ' + str(table) + '\n')
        for file in g.search_code('org:nike-impr-analytics ' + table):

            result = await client.get(file.download_url)

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

                time.sleep(2.0001)

                # print(df)

        return df

    async def fetch_all_queries(self, tables: list, token: str):
        async with httpx.AsyncClient() as client:
            n = 25
            # using list comprehension
            chunks = [tables[i:i + n] for i in range(0, len(tables), n)]
            # print(chunks)
            df = pd.DataFrame([], index=[[], []])
            l = len(tables)
            # time.sleep(60)

            # there is a search limit of 30 per minute for github so the list is chunked by 25 and checked to ensure
            # that 60 seconds had passed
            start_time = time.time()
            for chunk in chunks:
                print(chunk)
                df2 = await asyncio.gather(*[GitHub.fetch_query(self, table=table, token=token, client=client)
                                             for table in list(chunk)])
                df = df.append(df2)
                if l - len(chunk) > 0:
                    l -= len(chunk)
                    while time.time() - start_time < 60:
                        time.sleep(1)
                    start_time = time.time()
                else:
                    return df


