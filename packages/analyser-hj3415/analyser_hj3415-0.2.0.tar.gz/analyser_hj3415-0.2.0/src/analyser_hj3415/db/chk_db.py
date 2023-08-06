import time
from typing import Dict
from multiprocessing import Process, Queue
from . import mongo
from util_hj3415 import utils

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)


"""
chk_integrity_corps 함수로 종목코드를 데이터베이스명으로 가지는 DB의 유효성을 검사한다. 
"""


def test_corp_one(client1, test_code: str) -> dict:
    """
    종목 하나의 컬렉션의 유효성을 검사하여 부족한 컬렉션을 딕셔너리로 만들어서 반환한다.
    리턴값 - {'005930': ['c104','c103'...]}
    """

    def is_same_count_of_docs(col_name1: str, col_name2: str) -> bool:
        corp_one.page = col_name1
        count_doc1 = corp_one.count_docs_in_col()
        corp_one.page = col_name2
        count_doc2 = corp_one.count_docs_in_col()
        if count_doc1 == count_doc2:
            return True
        else:
            return False

    proper_collections = {'c101', 'c104y', 'c104q', 'c106y', 'c106q', 'c103손익계산서q', 'c103재무상태표q',
                          'c103현금흐름표q', 'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y'}

    logger.debug('In test_corp_one function...')
    return_dict = dict()

    logger.debug(f'return_dict is ... {return_dict}')
    # 한 종목의 유효성 검사코드
    corp_one = mongo.Corps(client1, test_code, 'c101')

    # 차집합을 사용해서 db내에 없는 컬렉션이 있는지 확인한다.
    set_deficient_collentions = set.difference(proper_collections, set(corp_one.list_collection_names()))

    logger.debug(f'After take a set of difference : {set_deficient_collentions}')

    return_dict[test_code] = set()
    # 컬렉션이 아예 없는 것이 있다면 falied_codes에 추가한다.
    if set_deficient_collentions != set():
        for item in set_deficient_collentions:
            # 컬렉션 이름 중 앞의 네글자만 추려서 추가해준다.(ex - c103손익계산서q -> c103)
            return_dict[test_code].add(item[:4])

    # 각 컬렉션의 q와 y의 도큐먼트 갯수를 비교하여 차이가 있는지 확인한다.
    if not is_same_count_of_docs('c104y', 'c104q'):
        return_dict[test_code].add('c104')
    if not is_same_count_of_docs('c106y', 'c106q'):
        return_dict[test_code].add('c106')
    if not is_same_count_of_docs('c103손익계산서q', 'c103손익계산서y') \
            or not is_same_count_of_docs('c103재무상태표q', 'c103재무상태표y') \
            or not is_same_count_of_docs('c103현금흐름표y', 'c103현금흐름표q'):
        return_dict[test_code].add('c103')

    # 집합을 리스트로 바꿔서 다시 저장한다.
    return_dict[test_code] = list(return_dict[test_code])
    return return_dict


def working_with_parts(db_addr, divided_code_list: list, my_q: Queue):
    # 각 코어별로 디비 클라이언트를 만들어야만 한다. 안그러면 에러발생
    client = mongo.connect_mongo(db_addr)
    t = len(divided_code_list)

    for i, code in enumerate(divided_code_list):
        my_dict = test_corp_one(client, code)
        print(f'{i + 1}/{t} {code} {my_dict[code]}')
        if my_dict[code] == list():
            continue
        else:
            pass
            my_q.put(my_dict)


# 멀티프로세싱을 사용하기 위해서 독립된 함수로 제작하였음(피클링이 가능해야함)
def chk_integrity_corps(client, code: str = 'all') -> Dict[str, list]:
    """
    몽고 디비의 corps들의 integrity 검사후 이상이 있는 코드 리스트 반환
    이상을 찾는 방법 - 각 컬렉션이 다 있는가. 각 컬렉션에서 연도와 분기의 도큐먼트 갯수가 같은가
    return - {'코드': ['cxxx',...], '코드': ['cxxx',...]...}
    """
    failed_codes = {}
    codes_in_db = mongo.Corps.get_all_codes(client)
    if code == 'all':
        logger.debug('If argument is all...')

        print('*' * 25, f"Check Corp db integrity all using multiprocess", '*' * 25)
        print(f'Total {len(codes_in_db)} items..')
        logger.debug(codes_in_db)
        n, divided_list = utils.code_divider_by_cpu_core(codes_in_db)

        # client에서 mongodb주소 추출
        ip = str(list(client.nodes)[0][0])
        port = str(list(client.nodes)[0][1])
        addr = 'mongodb://' + ip + ':' + port

        logger.debug(addr)

        start_time = time.time()
        q = Queue()
        ths = []
        for i in range(n):
            ths.append(Process(target=working_with_parts, args=(addr, divided_list[i], q)))
        for i in range(n):
            ths[i].start()

        for i in range(n):
            failed_codes.update(q.get())

        for i in range(n):
            ths[i].join()
        print(f'Total spent time : {round(time.time() - start_time, 2)} sec.')
    else:
        logger.debug(f'If argument is {code}')
        if code in codes_in_db:
            result_dict = test_corp_one(client, code)
            if result_dict[code] != list():
                failed_codes.update(test_corp_one(client, code))
        else:
            Exception(f'{code} is not in db..')
    return failed_codes
