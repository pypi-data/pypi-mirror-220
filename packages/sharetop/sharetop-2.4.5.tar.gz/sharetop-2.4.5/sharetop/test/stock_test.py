from sharetop.core.stock.bill_monitor import get_stock_history_capital, get_real_time_bill

from sharetop.core.stock.getter import get_stock_kline_data, get_stock_real_time_data, get_stock_market_real_time_data
from sharetop.core.stock.quarterly_report import get_stock_all_report_dates, get_stock_company_report_data, get_stock_all_company_quarterly_report
from sharetop.core.stock.rank_list import get_stock_dragon_tiger_list

from sharetop.core.stock.stock_base_info import get_stock_base_info


token = "f109298d079b5f60"

# d = get_stock_history_capital(token, "002714")

# d = get_stock_kline_data(token, ["002714", "300033"])

# d = get_real_time_bill("002714")

# d = get_history_data(token, "002714", klt=102)

# d = get_real_time_data(["002714", "516110"])

# d = get_stock_market_real_time_data(token, is_explain=True)

# d = get_stock_company_report_data(token, '002714', "一季报")

# d = get_stock_all_company_quarterly_report(token, '2021-03-31')

# d = get_stock_dragon_tiger_list(token)

# d = get_stock_base_info("002714")

# d = get_stock_all_report_dates(token)

# d = get_stock_real_time_data("002714")

# print(d.to_dict("records"))

from sharetop.core.stock import get_stock_market_real_time_data

df = get_stock_market_real_time_data(token)
print(df)
