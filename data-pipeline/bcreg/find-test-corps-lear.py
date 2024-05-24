#!/usr/bin/python
import psycopg2
import datetime
import os
import logging

from bcreg.config import config
from bcreg.eventprocessor import EventProcessor
from bcreg.bcreg_lear import BCReg_Lear, lear_system_type, LEAR_CORP_TYPES_IN_SCOPE

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARNING').upper()
logging.basicConfig(level=LOG_LEVEL)


specific_corps = []

specific_corps_keep = [
    'CP0000672',
    'CP0001309',
    'CP0001311',
    'CP0001316',
    'FM0020270',
    'FM0222860',
    'FM0268275',
    'FM0272479',
    'BC0870921',
    'BC0870922',
    'FM1000038',
    'FM1000042',
    'FM1000047',
    'FM1000046',
    'FM0346897',
    'FM0346781',
    'FM0346815',
    'FM1017072',
    'BC1255957',
    'FM0814438',
    'FM0562853',
    'FM0575361',
    'FM0842476',
    'FM1004542',
    'FM1016197','FM0272889','FM0554287','FM0647554','FM0556572','FM0558680','FM0555836','FM0556028',
'FM0054588',
'FM0081561',
'FM0086546',
'FM0109121',
'FM0133415',
'FM0159814',
'FM0159962',
'FM0188751',
'FM0257508',
'FM0257509',
'FM0291579',
'FM0300499',
'FM0314345',
'FM0317954',
'FM0329568',
'FM0347655',
'FM0371490',
'FM0393433',
'FM0407880',
'FM0416637',
'FM0417824',
'FM0419486',
'FM0425900',
'FM0436851',
'FM0438685',
'FM0440317',
'FM0450241',
'FM0456494',
'FM0471526',
'FM0485277',
'FM0485497',
'FM0486439',
'FM0488401',
'FM0490783',
'FM0505623',
'FM0508878',
'FM0512963',
'FM0512974',
'FM0522283',
'FM0524628',
'FM0531655',
'FM0559520',
'FM0565072',
'FM0568714',
'FM0573687',
'FM0573695',
'FM0575004',
'FM0575737',
'FM0578619',
'FM0583154',
'FM0593946',
'FM0594297',
'FM0598018',
'FM0601717',
'FM0601877',
'FM0603056',
'FM0604725',
'FM0604892',
'FM0604915',
'FM0604920',
'FM0606252',
'FM0612377',
'FM0612401',
'FM0614314',
'FM0614316',
'FM0614320',
'FM0614321',
'FM0616490',
'FM0616491',
'FM0617274',
'FM0617289',
'FM0617323',
'FM0617329',
'FM0618732',
'FM0619952',
'FM0620606',
'FM0622612',
'FM0644099',
'FM0646523',
'FM0646525',
'FM0646527',
'FM0647782',
'FM0651810',
'FM0653550',
'FM0654697',
'FM0656125',
'FM0656129',
'FM0658268',
'FM0662620',
'FM0662914',
'FM0663815',
'FM0664011',
'FM0670211',
'FM0670213',
'FM0671292',
'FM0675010',
'FM0676604',
'FM0677081',
'FM0679497',
'FM0680526',
'FM0680527',
'FM0680529',
'FM0682065',
'FM0683225',
'FM0683226',
'FM0689215',
'FM0691626',
'FM0693086',
'FM0696541',
'FM0697392',
'FM0700411',
'FM0703141',
'FM0703143',
'FM0703668',
'FM0707348',
'FM0707349',
'FM0707776',
'FM0708118',
'FM0711066',
'FM0711112',
'FM0711115',
'FM0711517',
'FM0712104',
'FM0714604',
'FM0735809',
'FM0744665',
'FM0746638',
'FM0748347',
'FM0761070',
'FM0761367',
'FM0766310',
'FM0776457',
'FM0782268',
'FM0782269',
'FM0785710',
'FM0786687',
'FM0791985',
'FM0794864',
'FM0801676',
'FM0810232',
'FM0816652',
'FM0818330',
'FM0819762',
'FM0822307',
'FM0822310',
'FM0822557',
'FM0823104',
'FM0823108',
'FM0823355',
'FM0825708',
'FM0830301',
'FM0834228',
'FM0836869',
'FM0836965',
'FM0840190',
'FM0841769',
'FM0852951',
'FM0856229',
'FM1003299',
'FM1030599',
'FM1045631',
'FM1045640',
'FM1045641',
'FM1045659',
'FM1045683',
'FM1045687',
'FM1045692',
'FM1045693',
'FM1045696',
'FM1045697',
'FM1045698',
'FM1045700',
'FM1045701',
'FM1045705',
'FM1045706',
'FM1045708',
'FM1045709',
'FM1045716',
'FM1045718',
'FM1045719',
'FM1045722',
'FM1045729',
'FM1045730',
'FM1045731',
'FM1045739',
'FM1045741',
'FM1045750',
'FM1045755',
'FM1045758',
'FM1045775',
'FM1045780',
'FM1045784',
'FM1045788',
'FM1045795',
'FM1045798',
'FM1045801',
'FM1045811',
'FM1045814',
'FM1045815',
'FM1045818',
'FM1045820',
'FM1045822',
'FM1045823',
'FM1045836',
'FM1045842',
'FM1045853',
'FM1045855',
'FM1045861',
'FM1045873',
'FM1045877',
'FM1045885',
'FM1045893',
    'FM0055113',
    'FM0020924',
'FM0159814',
'FM0314345',
'FM0417824',
'FM0436851',
'FM0575737',
'FM0604892',
'FM0604920',
'FM0617274',
'FM0617289',
'FM0617323',
'FM0617329',
'FM0662620',
'FM0664011',
'FM0679497',
'FM0735809',
'FM0744665',
'FM0785710',
'FM0823104',
'FM0823108',
'FM0836965',
'FM0841769',
'FM1003299',
'FM1030599',
'FM0072706',
'BC0880294',
'FM0159814',
'FM0314345',
'FM0417824',
'FM0436851',
'FM0575737',
'FM0604892',
'FM0604920',
'FM0617274',
'FM0617323',
'FM0617329',
'FM0662620',
'FM0664011',
'FM0679497',
'FM0735809',
'FM0744665',
'FM0785710',
'FM0836965',
'FM0841769',
'FM1003299',
'FM1003299',
'FM1030599',
]

num_corps_per_type = 20


with BCReg_Lear() as bc_registries:
    # get 5 corps for each type in scope (in addition to the above list)
    corp_types_to_load = ['BEN', 'BC',]
    corp_types_to_load.extend(LEAR_CORP_TYPES_IN_SCOPE)
    for corp_type in corp_types_to_load:
        print(corp_type)
        sql = """
               select identifier as corp_num
               from businesses
               where legal_type = '""" + corp_type + """'
               order by last_modified desc
              """
        corps = bc_registries.get_bcreg_sql("corps_by_type", sql, cache=False)
        n_corps = min(len(corps), num_corps_per_type)
        for i in range(n_corps):
           specific_corps.append(corps[i]['corp_num'])

    with EventProcessor() as event_processor:
        print("Get last processed event")
        prev_event_id = 0

        print("Get last max event")
        max_event_date = bc_registries.get_max_event_date()
        max_event_id = bc_registries.get_max_event(max_event_date)
        print(">>> max event --> ", max_event_id, max_event_date)
        
        # get specific test corps (there are about 6)
        print("Get specific corps")
        corps = bc_registries.get_specific_corps(specific_corps)

        print("Find unprocessed events for each corp")
        last_event_dt = bc_registries.get_event_effective_date(prev_event_id)
        max_event_dt = bc_registries.get_event_effective_date(max_event_id)
        corps = bc_registries.get_unprocessed_corp_events(prev_event_id, last_event_dt, max_event_id, max_event_dt, corps)
        
        print("Update our queue")
        event_processor.update_corp_event_queue(lear_system_type, corps, max_event_id, max_event_date)
