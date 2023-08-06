"""
雪球产品测算
"""
import hbshare as hbs
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime, timedelta
from hbshare.fe.common.util.data_loader import get_trading_day_list
from hbshare.quant.Kevin.quant_room.MyUtil.util_func import cal_max_drawdown, cal_annual_return, cal_annual_volatility


def snow_ball_simulation(start_date, end_date, benchmark_id, duration, knock_in_price, knock_out_price, alpha):
    """
    start_date: 回测起始时间
    end_date: 回测结束时间
    benchmark_id: 基准id
    duration: 合约期限, 以日计算
    knock_in_price: 敲入价格
    knock_out_price: 敲出价格
    alpha: 对比指增的年化超额收益&票息
    """
    sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                 "and JYRQ >= {} and JYRQ <= {}".format(benchmark_id, start_date, end_date)
    index_df = pd.DataFrame(hbs.db_data_query('readonly', sql_script, page_size=5000)['data'])
    index_series = index_df.set_index('TRADEDATE')['TCLOSE']
    # 每个交易日发一只雪球产品
    date_list = get_trading_day_list(start_date, end_date)

    res_df = pd.DataFrame(index=date_list[:-duration], columns=[
        '敲出且未敲入', '敲入后敲出', '未敲入且未敲出', '敲入未敲出', '敲出时间（月）', '结束时间', '雪球收益', '指增收益'])
    for i in range(len(date_list) - duration):
        start_dt, end_dt = date_list[i], date_list[i + duration]
        period_data = index_series.loc[start_dt: end_dt]
        period_data = period_data / period_data.iloc[0]
        ko_date = period_data.index.tolist()[::21][3:]

        knock_out_series = period_data.loc[ko_date].gt(knock_out_price)
        knock_in_series = period_data[1:].lt(knock_in_price)

        if knock_out_series.sum() > 0:
            tmp = period_data.loc[ko_date].to_frame('nav')
            tmp.loc[tmp['nav'] > knock_out_price, 'sign'] = 1
            first_ko_date = tmp['sign'].first_valid_index()
            ko_time = tmp.index.to_list().index(first_ko_date) + 3
            if knock_in_series.loc[:first_ko_date].sum() == 0:  # 情形1：敲出且未敲入
                res_df.loc[start_dt, '敲出且未敲入'] = 1
                res_df.loc[start_dt, '敲出时间（月）'] = ko_time
            else:  # 情形2：敲入后敲出
                res_df.loc[start_dt, '敲入后敲出'] = 1
                res_df.loc[start_dt, '敲出时间（月）'] = ko_time
            res_df.loc[start_dt, '结束时间'] = first_ko_date
            enhance_ret = period_data.loc[first_ko_date] - 1 + alpha * (ko_time / 12)
            snow_ball_ret = alpha * (ko_time / 12)
        else:
            if knock_in_series.sum() == 0:  # 情形3：未敲入且未敲出
                res_df.loc[start_dt, '未敲入且未敲出'] = 1
                snow_ball_ret = (duration / 252) * alpha
            else:  # 情形4：敲入未敲出
                res_df.loc[start_dt, '敲入未敲出'] = 1
                lose_ratio = \
                    max(0, (period_data.loc[start_dt] - period_data.loc[end_dt]) / period_data.loc[start_dt])
                snow_ball_ret = (-1) * lose_ratio
            res_df.loc[start_dt, '结束时间'] = end_dt
            enhance_ret = period_data.iloc[-1] - 1 + alpha * (duration / 252)

        res_df.loc[start_dt, '雪球收益'] = snow_ball_ret
        res_df.loc[start_dt, "指增收益"] = enhance_ret

    # 回测的统计
    # res_df.loc[(res_df['敲出且未敲入'] == 1.) | (res_df['敲入后敲出'] == 1.), 'type'] = 'A'
    # res_df.loc[res_df['未敲入且未敲出'] == 1., 'type'] = 'B'
    # res_df.loc[res_df['敲入未敲出'] == 1, 'type'] = 'C'

    # 连续回测
    ret_list = []
    for i in range(100):
        interval_start = date_list[:-duration][i]
        d_list = [interval_start]
        while interval_start in date_list[:-duration]:
            interval_start = res_df.loc[interval_start, '结束时间']
            # 间隔10个交易日
            interval_start = date_list[date_list.index(interval_start) + 10]
            d_list.append(interval_start)

        sub_df = res_df.loc[d_list[:-1]]
        s_date, e_date = sub_df.index[0], sub_df['结束时间'][-1]
        sub_list = [x for x in date_list if s_date <= x <= e_date]
        tmp = sub_df.set_index('结束时间')['雪球收益'].reindex(sub_list)

        ret_list.append(tmp)

    # ret_df = pd.concat(ret_list, axis=1)
    # (1 + ret_df.fillna(0.).mean(axis=1)).cumprod().to_clipboard()
    # summary
    summary_df = pd.DataFrame(index=res_df.columns[:4],
                              columns=['数量', '占比', '平均敲出时间（月）', '指增平均收益', '雪球平均收益'])
    summary_df.loc[:, '数量'] = res_df[res_df.columns[:4]].sum()
    summary_df['占比'] = summary_df['数量'] / summary_df['数量'].sum()
    summary_df.loc['敲出且未敲入', '平均敲出时间（月）'] = res_df[res_df['敲出且未敲入'] == 1]['敲出时间（月）'].mean()
    summary_df.loc['敲入后敲出', '平均敲出时间（月）'] = res_df[res_df['敲入后敲出'] == 1]['敲出时间（月）'].mean()
    for i in range(4):
        col = summary_df.index.tolist()[i]
        summary_df.loc[col, '指增平均收益'] = res_df[res_df[col] == 1]['指增收益'].mean()
        summary_df.loc[col, '雪球平均收益'] = res_df[res_df[col] == 1]['雪球收益'].mean()

    return summary_df


def snow_ball_like_simulation(start_date, end_date, benchmark_id, duration, KI, annual_alpha):
    """
    start_date: 回测起始时间
    end_date: 回测结束时间
    benchmark_id: 基准id
    duration: 合约期限, 以日计算
    KI: 止盈收益
    annual_alpha: 年化超额收益
    """
    sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                 "and JYRQ >= {} and JYRQ <= {}".format(benchmark_id, start_date, end_date)
    index_df = pd.DataFrame(hbs.db_data_query('readonly', sql_script, page_size=5000)['data'])
    index_series = index_df.set_index('TRADEDATE')['TCLOSE']
    # 每个交易日发一只产品
    future_dt = datetime.strptime(end_date, '%Y%m%d') + timedelta(days=550)
    future_date = datetime.strftime(future_dt, '%Y%m%d')
    date_list = get_trading_day_list(start_date, future_date)
    # 指数填充到future_date
    index_series = index_series.reindex(date_list).fillna(index_series.loc[end_date])

    res_df = pd.DataFrame(index=date_list[:-duration], columns=['end_date', 'mode', '持续天数', '年化收益', '指数年化收益'])
    for i in tqdm(range(len(date_list) - duration)):
        start_dt, end_dt = date_list[i], date_list[i + duration]
        period_data = index_series.loc[start_dt: end_dt]
        period_data = period_data / period_data.iloc[0]
        ko_date = period_data.index.tolist()[::21]
        add_list = [ko_date[0]]
        for j in range(1, 6):
            p_data = period_data.loc[ko_date[j - 1]: ko_date[j]][:-1].copy()
            p_data /= p_data.iloc[0]
            if p_data[p_data.lt(0.95)].first_valid_index() is None:
                date = ko_date[j]
            else:
                date = p_data[p_data.lt(0.95)].first_valid_index()
            add_list.append(date)
        # 指增的净值序列 = beta + annual_alpha
        nav_series = ((period_data.pct_change() + annual_alpha / 252).fillna(0.) + 1).cumprod()
        nav_df = pd.DataFrame(index=period_data.index, columns=['n_{}'.format(i) for i in range(6)])
        nav_df['n_0'] = nav_series
        for k in range(1, len(add_list)):
            tmp = nav_series.loc[add_list[k]:].copy()
            tmp /= tmp.iloc[0]
            nav_df['n_{}'.format(k)] = tmp
        nav_df = nav_df.fillna(0.)
        weight_series = pd.Series(index=nav_df.columns, data=[0.40, 0.12, 0.12, 0.12, 0.12, 0.12])
        # 现金项
        cash_series = pd.Series(index=add_list, data=[0.40, 0.12, 0.12, 0.12, 0.12, 0.12])
        cash_series = (1 - cash_series.cumsum()).reindex(nav_df.index).fillna(method='ffill')
        # 组合
        port_nav = nav_df.dot(weight_series) + cash_series
        # 计算止盈时点
        port_nav = port_nav.to_frame('port_nav').merge(
            period_data.to_frame('benchmark'), left_index=True, right_index=True)
        port_nav['trading_days'] = range(len(port_nav))
        port_nav['annual_return'] = port_nav['port_nav'] ** (252 / port_nav['trading_days']) - 1
        port_nav['bm_annual'] = port_nav['benchmark'] ** (252 / port_nav['trading_days']) - 1
        tmp = port_nav.loc[ko_date[3]:, 'annual_return'].copy()
        tmp.loc[tmp.lt(KI - 1)] = np.NaN
        if tmp.first_valid_index() is None:
            if end_dt > end_date:  # 存续
                stop_profit_date = end_date
                res_df.loc[start_dt, 'mode'] = '存续'
            else:  # 结算
                stop_profit_date = end_dt
                res_df.loc[start_dt, 'mode'] = '结算'
        else:
            if tmp.first_valid_index() > end_date:  # 存续
                stop_profit_date = end_date
                res_df.loc[start_dt, 'mode'] = '存续'
            else:
                stop_profit_date = tmp.first_valid_index()
                res_df.loc[start_dt, 'mode'] = '止盈'
        port_nav = port_nav.loc[:stop_profit_date]
        res_df.loc[start_dt, 'end_date'] = stop_profit_date
        res_df.loc[start_dt, '持续天数'] = date_list.index(stop_profit_date) - date_list.index(start_dt)
        res_df.loc[start_dt, '年化收益'] = port_nav.loc[stop_profit_date, 'annual_return']
        res_df.loc[start_dt, '指数年化收益'] = port_nav.loc[stop_profit_date, 'bm_annual']

        port_nav[['port_nav', 'benchmark']].to_csv('D:\\思勰类雪球指增模拟\\{}.csv'.format(start_dt))

    # summary
    # d_list = res_df.index.tolist()
    # summary_df = pd.DataFrame(index=d_list[:100], columns=['年化收益', '指数年化收益'])
    # for i in range(100):
    #     sim_start = d_list[i]
    #     ret_list = []
    #     while sim_start in d_list:
    #         sim_data = pd.read_csv('D:\\思勰类雪球指增模拟\\{}.csv'.format(sim_start), dtype={"TRADEDATE": str})
    #         sim_data = sim_data.set_index('TRADEDATE')
    #         sim_data = sim_data.pct_change().fillna(0.)
    #         ret_list.append(sim_data)
    #         sim_start = res_df.loc[sim_start, 'end_date']
    #         sim_start = date_list[date_list.index(sim_start) + 1]
    #
    #     ret_df = pd.concat(ret_list).sort_index()
    #     nav_df_compare = (1 + ret_df.loc["20210509":]).cumprod()
    #     summary_df.loc[d_list[i], '年化收益'] = \
    #         nav_df_compare.iloc[-1]['port_nav'] ** (252 / len(nav_df_compare - 1)) - 1
    #     summary_df.loc[d_list[i], '指数年化收益'] = \
    #         nav_df_compare.iloc[-1]['benchmark'] ** (252 / len(nav_df_compare - 1)) - 1

    return res_df


def dividends_strategy_simulation(start_date, dividend, threshold):
    """
    start_date: 起始时间
    dividend: 每月分红比例
    threshold: 分红阈值
    """
    return_df = pd.read_csv('D:\\指增平均收益数据.csv', dtype={"t_date": str}).set_index('t_date')
    # return_df.loc["20161230"] = 0.
    return_df = return_df.sort_index().loc[start_date:]
    return_df.loc[start_date] = 0.

    return_df['actual_nav'] = (1 + return_df['average']).cumprod()
    return_df['sim_nav'] = return_df['actual_nav']
    return_df['sub'] = 0.
    reb_dates = sorted(return_df.index.unique())[::4]
    last_date = sorted(return_df.index.unique())[-1]
    if reb_dates[-1] < last_date:
        reb_dates.append(last_date)
    for i in range(1, len(reb_dates)):
        p_date, t_date = reb_dates[i - 1], reb_dates[i]
        period_df = return_df.loc[p_date: t_date, "actual_nav"]
        sim_start = return_df.loc[p_date, 'sim_nav']
        period_df = (period_df / period_df.iloc[0]) * sim_start
        # replace
        return_df.loc[p_date: t_date, 'sim_nav'] = period_df
        if len(period_df) < 5:
            continue
        if period_df.loc[t_date] > threshold:
            return_df.loc[t_date, 'sim_nav'] = threshold
            return_df.loc[t_date, 'sub'] = period_df.loc[t_date] - threshold
        else:
            return_df.loc[t_date, 'sim_nav'] = period_df.loc[t_date] * (1 - dividend)
            return_df.loc[t_date, 'sub'] = period_df.loc[t_date] * dividend

    return_df['sub'] = return_df['sub'].cumsum()
    return_df.eval("sim_nav_plus = sim_nav + sub", inplace=True)

    df = return_df[['actual_nav', 'sim_nav', 'sim_nav_plus', 'sub']].rename(columns={
        "actual_nav": "原始指增收益", "sim_nav": "分红指增-指增部分净值", "sim_nav_plus": "分红指增净值", "sub": "累计分红"})
    df['trade_date'] = df.index
    df['trade_date'] = df['trade_date'].apply(
        lambda x: datetime.strptime(x, "%Y%m%d").strftime("%Y-%m-%d"))
    df.set_index('trade_date', inplace=True)

    nav_df = df.copy()
    portfolio_index_df = pd.DataFrame(
        index=nav_df.columns, columns=['年化收益', '年化波动', '最大回撤'])
    portfolio_index_df.loc[:, '年化收益'] = nav_df.pct_change().dropna(how='all').apply(cal_annual_return, axis=0)
    portfolio_index_df.loc[:, '年化波动'] = \
        nav_df.pct_change().dropna(how='all').apply(cal_annual_volatility, axis=0)
    portfolio_index_df.loc[:, '最大回撤'] = nav_df.apply(cal_max_drawdown, axis=0)
    portfolio_index_df['年化收益'] = portfolio_index_df['年化收益'].apply(lambda x: format(x, '.2%'))
    portfolio_index_df['年化波动'] = portfolio_index_df['年化波动'].apply(lambda x: format(x, '.2%'))
    portfolio_index_df['最大回撤'] = portfolio_index_df['最大回撤'].apply(lambda x: format(x, '.2%'))

    return df, portfolio_index_df


if __name__ == '__main__':
    # snow_ball_simulation('20100101', '20230512', '000905', 252, 0.8, 1.0, 0.12)
    # snow_ball_like_simulation('20100101', '20230509', '000905', 504, 1.12, 0.10)
    dividends_strategy_simulation("20201231", 0.01, 1.15)