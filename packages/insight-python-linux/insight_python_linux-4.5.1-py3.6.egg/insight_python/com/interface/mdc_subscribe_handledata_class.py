from datetime import datetime


def subscribe_tick_handle(marketdatajson):
    # print(marketdatajson)
    tick_map_dict = {
        # 指数
        'htsc_code': 'HTSCSecurityID', 'prev_close': 'PreClosePx', 'volume': 'TotalVolumeTrade',
        'value': 'TotalValueTrade', 'last': 'LastPx', 'open': 'OpenPx', 'high': 'HighPx', 'low': 'LowPx',
        'close': 'ClosePx', 'num_trades': 'NumTrades',
        # 股票
        'trading_phase_code': 'TradingPhaseCode', 'exchange': 'securityIDSource', 'security_type': 'securityType',
        'max': 'MaxPx', 'min': 'MinPx', 'buy_price_queue': 'BuyPriceQueue', 'buy_order_qty_queue': 'BuyOrderQtyQueue',
        'sell_price_queue': 'SellPriceQueue', 'sell_order_qty_queue': 'SellOrderQtyQueue',
        # 基金
        'iopv': 'IOPV',
        # 期权
        'pre_settle': 'PreSettlePrice', 'open_interest': 'OpenInterest', 'settle': 'SettlePrice',
        # 期货
        'trading_day': 'TradingDate', 'pre_open_interest': 'PreOpenInterest',
        # 南北资金流向
        'total_buy_value_trade': 'TotalBuyValueTrade', 'total_sell_value_trade': 'TotalSellValueTrade',
    }

    # 需要除的键
    divisor_list = ['max', 'min', 'prev_close', 'last', 'open', 'high', 'low', 'close', 'buy_price_queue',
                    'sell_price_queue', 'iopv', 'settle', 'pre_settle']

    exchange_code_map = {
        101: 'XSHG',  # 上交所
        102: 'XSHE',  # 深交所
        703: 'CSI',  # 中证指数
        702: 'CNI',  # 国证指数
        106: 'XBSE',  # 北交所
        204: 'HKSC',  # 港股通
        302: 'XSGE',  # 上期所
        601: 'XDCE',  # 大商所
        602: 'XZCE',  # 郑商所
        301: 'CCFX',  # 中金所
        801: 'HTIS',  # 华泰INSIGHT
    }

    security_type_map = {
        1: 'index',
        2: 'stock',
        3: 'fund',
        4: 'bond',
        7: 'option',
        8: 'future',
    }

    data = None
    result = None
    if "mdIndex" in marketdatajson:  # 指数

        data = marketdatajson["mdIndex"]
        result = {'htsc_code': '', 'time': '', 'exchange': '', 'security_type': '', 'prev_close': '', 'volume': '',
                  'value': '', 'last': '', 'open': '', 'high': '', 'low': '', 'close': ''}

    elif "mdStock" in marketdatajson:  # 股票

        data = marketdatajson["mdStock"]
        result = {'htsc_code': '', 'time': '', 'trading_phase_code': '', 'exchange': '', 'security_type': '', 'max': '',
                  'min': '', 'prev_close': '', 'num_trades': '', 'volume': '', 'value': '', 'last': '', 'open': '',
                  'high': '', 'low': '',
                  'buy_price_queue': '', 'buy_order_qty_queue': '', 'sell_price_queue': '', 'sell_order_qty_queue': '',
                  'close': ''}

    elif "mdFund" in marketdatajson:  # 基金

        data = marketdatajson["mdFund"]
        result = {'htsc_code': '', 'time': '', 'trading_phase_code': '', 'exchange': '', 'security_type': '', 'max': '',
                  'min': '', 'prev_close': '', 'num_trades': '', 'volume': '', 'value': '', 'last': '', 'open': '',
                  'high': '', 'low': '',
                  'iopv': '', 'buy_price_queue': '', 'buy_order_qty_queue': '', 'sell_price_queue': '',
                  'sell_order_qty_queue': '', 'close': ''}

    elif "mdBond" in marketdatajson:  # 债券

        data = marketdatajson["mdBond"]
        result = {'htsc_code': '', 'time': '', 'trading_phase_code': '', 'exchange': '', 'security_type': '', 'max': '',
                  'min': '', 'prev_close': '', 'num_trades': '', 'volume': '', 'value': '', 'last': '', 'open': '',
                  'high': '', 'low': '',
                  'buy_price_queue': '', 'buy_order_qty_queue': '', 'sell_price_queue': '', 'sell_order_qty_queue': '',
                  'close': ''}

    elif "mdOption" in marketdatajson:  # 期权

        data = marketdatajson["mdOption"]
        result = {'htsc_code': '', 'time': '', 'trading_phase_code': '', 'exchange': '', 'security_type': '', 'max': '',
                  'min': '', 'prev_close': '', 'num_trades': '', 'volume': '', 'value': '', 'last': '', 'open': '',
                  'high': '', 'low': '',
                  'pre_settle': '', 'open_interest': '', 'buy_price_queue': '', 'buy_order_qty_queue': '',
                  'sell_price_queue': '', 'sell_order_qty_queue': '', 'close': '', 'settle': ''}

    elif "mdFuture" in marketdatajson:  # 期货

        data = marketdatajson["mdFuture"]
        result = {'htsc_code': '', 'time': '', 'trading_phase_code': '', 'exchange': '', 'security_type': '', 'max': '',
                  'min': '', 'prev_close': '', 'volume': '', 'value': '', 'last': '', 'open': '', 'high': '', 'low': '',
                  'trading_day': '', 'pre_open_interest': '', 'pre_settle': '', 'open_interest': '',
                  'buy_price_queue': '', 'buy_order_qty_queue': '', 'sell_price_queue': '', 'sell_order_qty_queue': '',
                  'close': '', 'settle': ''}

    try:
        if data and result:

            # 判断是否是南北向资金流向
            if data.get("HTSCSecurityID") in ['SCHKSBSH.HT', 'SCHKSBSZ.HT', 'SCSHNBHK.HT', 'SCSZNBHK.HT']:
                name_map = {'SCHKSBSH.HT': '北向资金（香港-上海）', 'SCHKSBSZ.HT': '北向资金（香港-深圳）',
                            'SCSHNBHK.HT': '南向资金（上海-香港）', 'SCSZNBHK.HT': '南向资金（深圳-香港）'}
                result = {'name': name_map.get(data.get("HTSCSecurityID")), 'htsc_code': '', 'time': '', 'exchange': '',
                          'security_type': '', 'value': '',
                          'total_buy_value_trade': '', 'total_sell_value_trade': ''}

            md_time = datetime.strptime(str(data['MDDate']) + str(data['MDTime']), '%Y%m%d%H%M%S%f')
            md_time = datetime.strftime(md_time, '%Y-%m-%d %H:%M:%S.%f')

            exchange = exchange_code_map.get(data.get("securityIDSource"))
            security_type = security_type_map.get(data.get('securityType'))
            result['time'] = md_time
            result['exchange'] = exchange
            result['security_type'] = security_type

            divisor = pow(10, int(data.get("DataMultiplePowerOf10")))  # 除数

            for key in list(result.keys()):
                if not result[key]:

                    value = data.get(tick_map_dict.get(key))

                    if isinstance(value, str):
                        result[key] = value

                    elif isinstance(value, int):

                        if key == 'trading_day':
                            result[key] = '{}-{}-{}'.format(str(value)[:4], str(value)[4:6], str(value)[6:])
                        else:
                            if key in divisor_list:
                                value = value / divisor
                            result[key] = value

                    elif isinstance(value, list):
                        if key in divisor_list:
                            value = list(map(lambda x: x / divisor, value))

                        count = 1
                        key_name = ''
                        for i in value:
                            if key == 'buy_price_queue':
                                key_name = 'bid' + str(count)
                            elif key == 'buy_order_qty_queue':
                                key_name = 'bid_size' + str(count)
                            elif key == 'sell_price_queue':
                                key_name = 'ask' + str(count)
                            elif key == 'sell_order_qty_queue':
                                key_name = 'ask_size' + str(count)
                            result[key_name] = i
                            count += 1
                        del result[key]

            return result

    except Exception as e:
        print(e)


def subscribe_kline_handle(marketdatajson):
    kline_map_dict = {'htsc_code': 'HTSCSecurityID', 'exchange': 'securityIDSource', 'security_type': 'securityType',
                      'frequency': 'PeriodType', 'open': 'OpenPx', 'close': 'ClosePx', 'high': 'HighPx', 'low': 'LowPx',
                      'volume': 'TotalVolumeTrade', 'value': 'TotalValueTrade', 'open_interest': 'OpenInterest',
                      'settle': 'SettlePrice'}

    exchange_code_map = {
        101: 'XSHG',  # 上交所
        102: 'XSHE',  # 深交所
        703: 'CSI',  # 中证指数
        702: 'CNI',  # 国证指数
        106: 'XBSE',  # 北交所
        204: 'HKSC',  # 港股通
        302: 'XSGE',  # 上期所
        601: 'XDCE',  # 大商所
        602: 'XZCE',  # 郑商所
        301: 'CCFX',  # 中金所
    }

    security_type_map = {
        1: 'index',
        2: 'stock',
        3: 'fund',
        4: 'bond',
        7: 'option',
        8: 'future',
    }

    frequency_map = {1: "1min", 10: "15s"}

    # 需要除的键
    divisor_list = ['open', 'high', 'low', 'close', 'settle']
    if "mdKLine" in marketdatajson:
        if marketdatajson['mdKLine'].get('KLineCategory'):
            result = None
            data = marketdatajson["mdKLine"]
            security_type = security_type_map.get(data.get('securityType'))

            if security_type in ["index", "stock", "fund", "bond"]:

                result = {'htsc_code': '', 'time': '', 'exchange': '', 'security_type': '', 'frequency': '', 'open': '',
                          'close': '', 'high': '', 'low': '', 'volume': '', 'value': ''}

            elif security_type in ['option', 'future']:

                result = {'htsc_code': '', 'time': '', 'exchange': '', 'security_type': '', 'frequency': '', 'open': '',
                          'close': '', 'high': '', 'low': '', 'volume': '', 'value': '', 'open_interest': '',
                          'settle': ''}

            if data and result:

                md_time = datetime.strptime(str(data['MDDate']) + str(data['MDTime']), '%Y%m%d%H%M%S%f')
                md_time = datetime.strftime(md_time, '%Y-%m-%d %H:%M:%S.%f')
                exchange = exchange_code_map.get(data.get("securityIDSource"))
                frequency = frequency_map[data['PeriodType']]

                result['time'] = md_time
                result['exchange'] = exchange
                result['security_type'] = security_type
                result['frequency'] = frequency

                divisor = pow(10, int(data.get("DataMultiplePowerOf10")))  # 除数

                for key in list(result.keys()):
                    if not result[key]:

                        value = data.get(kline_map_dict.get(key))

                        if isinstance(value, str):
                            result[key] = value

                        elif isinstance(value, int):
                            if key in divisor_list:
                                value = value / divisor
                            result[key] = value

                return result


def subscribe_trans_and_order_handle(marketdatajson):
    columns_map = {'htsc_code': 'HTSCSecurityID', 'trade_index': 'TradeIndex', 'trade_buy_no': 'TradeBuyNo',
                   'trade_sell_no': 'TradeSellNo', 'trade_bs_flag': 'TradeBSFlag', 'trade_price': 'TradePrice',
                   'trade_qty': 'TradeQty', 'trade_money': 'TradeMoney', 'app_seq_num': 'ApplSeqNum',
                   'channel_no': 'ChannelNo',
                   'order_index': 'OrderIndex', 'order_type': 'OrderType', 'order_no': 'OrderNO',
                   'order_bs_flag': 'OrderBSFlag', 'order_price': 'OrderPrice', 'order_qty': 'OrderQty'}

    exchange_code_map = {
        101: 'XSHG',  # 上交所
        102: 'XSHE',  # 深交所
    }

    security_type_map = {
        2: 'stock',
        3: 'fund',
        4: 'bond',
    }

    # 需要除的键
    divisor_list = ['trade_price', 'trade_money', 'order_price']

    data = None
    data_type = None
    if "mdTransaction" in marketdatajson:
        data = marketdatajson["mdTransaction"]
        data_type = 'transaction'

    elif 'mdOrder' in marketdatajson:
        data = marketdatajson['mdOrder']
        data_type = 'order'

    if data:

        result = {}

        security_type = security_type_map.get(data.get('securityType'))
        md_time = datetime.strptime(str(data['MDDate']) + str(data['MDTime']), '%Y%m%d%H%M%S%f')
        md_time = datetime.strftime(md_time, '%Y-%m-%d %H:%M:%S.%f')
        exchange = exchange_code_map.get(data.get("securityIDSource"))

        if data_type == 'transaction':
            result = {'htsc_code': '', 'time': md_time, 'data_type': data_type, 'exchange': exchange,
                      'security_type': security_type, 'trade_index': '', 'trade_buy_no': '',
                      'trade_sell_no': '', 'trade_bs_flag': '', 'trade_price': '', 'trade_qty': '', 'trade_money': '',
                      'app_seq_num': '', 'channel_no': ''}

        if data_type == 'order':
            if exchange == 'XSHG':
                result = {'htsc_code': '', 'time': md_time, 'data_type': data_type, 'exchange': exchange,
                          'security_type': security_type, 'order_index': '', 'order_type': '',
                          'order_price': '', 'order_qty': '', 'order_bs_flag': '', 'order_no': '',
                          'app_seq_num': '', 'channel_no': ''}
            elif exchange == 'XSHE':
                result = {'htsc_code': '', 'time': md_time, 'data_type': data_type, 'exchange': exchange,
                          'security_type': security_type, 'order_index': '', 'order_type': '',
                          'order_price': '', 'order_qty': '', 'order_bs_flag': '',
                          'app_seq_num': '', 'channel_no': ''}

        result['time'] = md_time
        result['exchange'] = exchange
        result['security_type'] = security_type

        divisor = pow(10, int(data.get("DataMultiplePowerOf10")))  # 除数

        for key in list(result.keys()):
            if not result[key]:

                value = data.get(columns_map.get(key))

                if isinstance(value, str):
                    result[key] = value

                elif isinstance(value, int):
                    if key in divisor_list:
                        value = value / divisor
                    result[key] = value

        return result


def subscribe_news_handle(marketdatajson):
    if 'mdNews' in marketdatajson:

        search_type_map = {'0': '新闻', '1': '公告', '2': '舆情'}
        is_valid_map = {'0': '已删除的消息', '1': '有效的消息'}
        exchange_code_map = {
            101: 'XSHG',  # 上交所
            102: 'XSHE',  # 深交所
        }

        data = marketdatajson['mdNews']

        md_time = datetime.strptime(str(data['MDDate']) + str(data['MDTime']), '%Y%m%d%H%M%S%f')
        md_time = datetime.strftime(md_time, '%Y-%m-%d %H:%M:%S.%f')
        exchange = exchange_code_map.get(data.get("securityIDSource"))

        result = {'time': md_time, 'exchange': exchange, 'security_type': 'stock'}

        content_list = data.get('sentimentContent')
        if content_list:
            for column_dict in content_list:

                column_key = column_dict['key']
                column_value = column_dict['value']

                if column_key == 'is_valid':
                    column_value = is_valid_map.get(column_value)

                elif column_key == 'search_type':
                    column_value = search_type_map.get(column_value)

                result[column_key] = column_value
        return result

    else:
        return marketdatajson
