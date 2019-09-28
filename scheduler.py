TESTER_CYCLE = 3600
GETTER_CYCLE = 14400
API_HOST = 'localhost'
API_PORT = 4783
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

import time
import asyncio
from multiprocessing import Process
from api import app
from getter import Getter
from tester import Tester

class Scheduler():


    def schedule_tester(self, cycle=TESTER_CYCLE):
        """Cycle test proxy"""
        tester = Tester()
        while True:
            tester.run()
            time.sleep(cycle)


    def schedule_getter(self, cycle=GETTER_CYCLE):
        """Cycle get proxy"""
        coroutine = Getter()
        while True:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(coroutine.run())
            time.sleep(cycle)


    def schedule_api(self):
        """Open API"""
        app.run(API_HOST, API_PORT)


    def run(self):
        print('代理池正在运行...')
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()

