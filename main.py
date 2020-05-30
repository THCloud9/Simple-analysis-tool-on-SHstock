from functions import Stock

while True:
    print('''
输入help来获取帮助.
按enter键以退出.''')
    first_judge = input('请选择你想进行的操作：')
    if first_judge == 'inquire':
        while True:
            print('按enter键结束查询')
            code = input('请输入你想要查询的沪A股票代码（格式为6位数字，如600004，一般以6开头）：')
            if '599999' < code <= '999999':
                start = input('输入起始日期(如20190101)：')
                end = input('输入终止日期(如20200525)：')
                stock = Stock(code, int(start), int(end))
                print(stock.stock_name())
                while True:
                    function_judge = input('''
按enter退出详细查询.
输入k获取k线图.
输入data获取该股的每日数据.
输入rate获取该股的日涨幅
输入beta计算这段时间该股对于大盘的beta值.
请输入:''')
                    if function_judge == 'k':
                        time_str = input('请输入天数以获得最近x天的k线图(直接enter默认为30天)：')
                        if time_str == '':
                            stock.draw_k_chart_latest_x_days()
                        else:
                            stock.draw_k_chart_latest_x_days(int(time_str))
                    elif function_judge == 'data':
                        print(stock.get_stock_data())
                    elif function_judge == 'rate':
                        print(stock.show_daily_increasing_rate())
                    elif function_judge == 'beta':
                        print(f'该股票的beta值为{stock.calculate_beta()}')
                    elif function_judge == '':
                        break
                    else:
                        print('请输入正确的命令')
            if code == '':
                break
    if first_judge == 'portfolio':
        portfolio = dict()
        total_proportion = 0
        while True:
            add_code = input('''
按enter键结束添加.
请输入要添加的股票代码:''')
            if add_code == '':
                break
            proportion = eval(input('请输入要添加的这只股票的持仓比例(不能大于1)：'))
            portfolio[add_code] = proportion
            total_proportion += proportion
            if total_proportion >= 1:
                print(f'无效的持仓比例，请输入小于{1-(total_proportion - proportion)}的持仓')
                total_proportion = total_proportion - proportion
        print(portfolio)
        judge_beta = input('是否计算这个portfolio的beta以衡量其受大盘波动的影响程度？(y/n)')
        if judge_beta == 'y':
            beta_total = 0
            for key, value in portfolio.items():
                beta_total += Stock(key, 20190101, 20200501).calculate_beta() * value
            if beta_total > 0.6:
                print(f'这个portfolio的beta值为{beta_total}，随大盘波动较大，风险较高')
            else:
                print(f'这个portfolio的beta值为{beta_total},随大盘波动较小，风险较低')

        if judge_beta == 'n':
            break

    if first_judge == '':
        break
    if first_judge == 'help':
        print('''
输入inquire来查询有关某只股票的数据和一段时间内的k线图
输入portfolio来进入你的股票组合并进行调整
        ''')


print('程序已结束运行')
