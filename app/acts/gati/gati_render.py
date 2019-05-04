import requests
import re
import os
from datetime import datetime
import pickle

def gati_render ():
    meta_url = 'http://gati-online.ru/opendata/7803032323-DR/meta.csv'
    user_agent_string = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    try:
        meta_data = requests.get(meta_url, stream=True, headers={'user-agent': user_agent_string})
    except ConnectionError:
        print ('Ошибка запроса API')
        return ()
    result = re.search(r'data-\d{4}-\d\d-\d\d-structure-\d{4}-\d\d-\d\d', meta_data.text).group(0)
    csv_url = r'http://gati-online.ru/opendata/7803032323-DR/' + result + '.csv'
    try:
        csv_orders = requests.get(csv_url, stream=True, headers={'user-agent': user_agent_string})
    except ConnectionError:
        print ('Ошибка запроса API')
        return ()
    # decoded_content = csv_orders.content.decode('utf-8')
    # print(decoded_content[0:800])
    result_list = []
    orders_list = csv_orders.content.decode('utf-8').split('\"\r\n\"')
    for order_data_string in orders_list:
        order_data_list = order_data_string.split('\",\"')
        if order_data_list[6].__contains__('7805498649') or order_data_list[6].__contains__('7807312233'):
            work_begin_date = order_data_list[11][0:4]+'.'+ order_data_list[11][4:6]+'.'+ order_data_list[11][6:]
            work_end_date = order_data_list[12][0:4]+'.'+ order_data_list[12][4:6]+'.'+ order_data_list[12][6:]
            # print ('Ордер № : {}, Подрядчик: {}, Адрес: {}, Вид работ: {}, Начало работ: {}, Конец работ: {}'.format(
            # order_data_list[1], order_data_list[5], order_data_list[8], order_data_list[9], work_begin_date, work_end_date))
            result_list.append({'Order_N':order_data_list[1],
                                'Contractor':order_data_list[5],
                                'Address':order_data_list[8],
                                'Work_Type':order_data_list[9],
                                'Begin_Date':work_begin_date,
                                'End_Date':work_end_date})
    return (result_list)

def get_gati_data ():
    gati_data_storage_name = 'gatidata.pkl'
    # если существует файл pikle c ордерами если он младше 5 часов
    if os.path.exists(gati_data_storage_name) and os.stat(gati_data_storage_name).st_ctime + 5*60*60 > datetime.today().timestamp():
        # извлечь ордера из файла pikle и вернуть их
        input = open(gati_data_storage_name, 'rb')
        order_list = pickle.load(input)
        input.close()
        return order_list
    else:
        # получить данные из сайта и создать файл (если надо - стереть).
        if os.path.exists(gati_data_storage_name):
            os.remove(gati_data_storage_name)
        order_list = gati_render()
        output = open(gati_data_storage_name, 'wb')
        pickle.dump(order_list, output, 2)
        output.close()
        return order_list


if __name__ =='__main__':
    get_gati_data()