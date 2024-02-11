from aiohttp import ClientSession
import asyncio
from aiohttp.client_exceptions import ContentTypeError
import requests
from requests.exceptions import ChunkedEncodingError
import json
from sseclient import SSEClient
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time



class Utils:
    @staticmethod
    def not_empty_filter(obj):
        return list(filter(lambda item: item[1], obj))

    @staticmethod
    def get_data_of_key(key, data, printing=False):
        iterator = list(map(lambda item: item[key], data))
        if printing:
            print(list(filtered))
        return iterator

    @staticmethod
    def make_pair_of_data(data1, data2, printing=False):
        data = zip(data1, data2)
        return list(data)

    @staticmethod
    def separate_duals(obj):
        return list(zip(*obj))


class HttpRequester(Utils):
    def __init__(self, key):
        self.__key = key
        self.games, self.game_ids = [], []
        self.spbooks = []
        self.prms = {"key": self.__key}
        self.main_iterator = None
        self.odds = None


    async def aiorequest(self, url, session, game_id=None, spbooks=None):
        if game_id: #Sorry, couldn't comprehend it
            self.prms["game_id"] = game_id
        if spbooks:
            self.prms["sportsbook"] = spbooks

        async with session.get(url, params=self.prms) as response:
            try:
                return (await response.json())["data"]
            except ContentTypeError:
                print(response.text())
                return await response.text()
            except KeyError:
                return await response.json()

    async def aio_task_and_get(self, url, session):
        self.game_ids = self.get_data_of_key("id", self.games)
        if self.game_ids and not self.spbooks:
            api_tasks = [asyncio.create_task(self.aiorequest(url=url,
                                     game_id=game_id, session=session)) for game_id in self.game_ids[:50]]
        elif self.game_ids and self.spbooks:
            api_tasks = [asyncio.create_task(self.aiorequest(url=url,
                                     game_id=game_id, spbooks=spbooks, session=session)) for game_id, spbooks in self.main_iterator]
        elif not self.games and self.spbooks:
            pass #if you need write that option


        results = await asyncio.gather(*api_tasks)
        return results

    async def full_http_dealer(self):
        async with ClientSession() as session:
            self.games = await self.aiorequest(url="https://api-external.oddsjam.com/api/v2/games", session=session)

            self.spbooks = await self.aio_task_and_get(url="https://api-external.oddsjam.com/api/v2/sportsbooks/", session=session)
            main_iterator = self.make_pair_of_data(self.game_ids, self.spbooks)
            self.main_iterator = self.not_empty_filter(main_iterator)
            self.odds = await self.aio_task_and_get(url="https://api-external.oddsjam.com/api/v2/game-odds", session=session)

    @property
    def return_general_resp(self):
        return {"odds": self.odds, "main_it": self.main_iterator}

    def start_full_http(self):
        asyncio.run(self.full_http_dealer())


class Stream:
    url = "https://api-external.oddsjam.com/api/v2/stream/odds"

    def __init__(self, key, game, spbooks):
        self.__key = key
        self.game = game
        self.spbooks = spbooks
        self.start_stream()

    def form_param(self):
        return {
                "key": self.__key,
                "sportsbooks": self.spbooks,
                "game_id": self.game
            }


    def start_stream(self):
        while True:
            try:
                r = requests.get(
                    url=self.url,
                    params=self.form_param(),
                    stream=True
                )
                client = SSEClient(r)
                for event in client.events():
                    if event.event == "odds":
                        data = json.loads(event.data)
                        print("odds data", ":", data)
                    elif event.event == "locked-odds":
                        data = json.loads(event.data)
                        print("locked-odds data", ":", data)
                    else:
                        print(event.event, ":", event.data)
            except ChunkedEncodingError as ex:
                print("Disconnected, attempting to reconnect...")
            except Exception as e:
                print("Error:", r.status_code, r.text)
                break


class ServerCPUControler(Utils):
    def __init__(self):
        self.__key = #your_key
        self._another_games_id = set()
        self._another_bookmakers = set()


    def main_streams(self, odds, games, sportsbooks):
        with ThreadPoolExecutor() as executor:
            for i in range(len(games)):
                executor.submit(Stream, game=games.pop(), spbooks=sportsbooks[i], key=self.__key)
            print("Streams executed")


    def api_execute(self):
        with ProcessPoolExecutor() as executor:
            while True:
                request_dealer = HttpRequester(key=self.__key)
                request_dealer.start_full_http()
                print("HTTP request done")
                odds, main_it = request_dealer.return_general_resp["odds"], request_dealer.return_general_resp["main_it"]
                self._another_games_id = set(self.separate_duals(main_it)[0]) - self._another_games_id
                another_bookmakers = [it[1] for it in main_it if it[0] in self._another_games_id]
                executor.submit(self.main_streams, odds, self._another_games_id, another_bookmakers)
                print(self._another_games_id)
                time.sleep(30)




if __name__ == "__main__":
    main_test = ServerCPUControler()
    main_test.api_execute()
























t = HttpRequester(key="2898ce5f-cd9c-47e2-b3b6-44c1044aadb9")
asyncio.run(t.full_http_dealer())



