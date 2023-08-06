def backtest(df_factor,df_close):
    import pandas as pd 
    import numpy as np
    import statsmodels.api as sm
    import matplotlib.pyplot as plt
    import math
    import scipy.stats as st
    import seaborn as sns
    from scipy.stats import pearsonr
    import matplotlib.dates as mdate
    from matplotlib.pyplot import rcParams 
    import matplotlib.ticker as ticker
    import warnings
    from pandas import read_parquet
    import sys
    import baostock as bs
    warnings.filterwarnings("ignore")
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    
    def process_bar(percent, start_str='', end_str='', total_length=0):
        bar = ''.join(["\033[31m%s\033[0m"%'   '] * int(percent * total_length)) + ''
        bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent*100) + end_str
        print(bar, end='', flush=True)
       
        
    class factor_analysis:
        def __init__(self,factor,return_rate,portfolio):
            self.factor=factor
            self.return_rate=return_rate
            self.portfolio=portfolio
    
    
    #画图的标准格式
        def set_picture(self):
            plt.xticks(fontsize=16)
            plt.yticks(fontsize=16)
            plt.legend(prop={'size':16})
    
    #策略的相关信息
        def strategy_information(self,rate,final_rate):
            maxDrawdown=0
            years=(len(final_rate)+time_gap)/252
            annual_return=final_rate[len(final_rate)-1]**(1/years)-1
            Abs_return=final_rate[len(final_rate)-1]-1
            sr = np.mean(rate)/np.std(rate) * np.sqrt(252)
            for i in range(len(final_rate)-1):
                for j in range(i+1,len(final_rate)-1):
                    if(final_rate[j]<final_rate[i]):
                        maxDrawdown=max((final_rate[i]-final_rate[j])/final_rate[i],maxDrawdown)
            print('该策略的年化收益为： ',end=' ')
            print(annual_return)
            print('该策略的绝对收益为： ',end=' ')
            print(Abs_return)
            print('该策略的夏普比率为： ',end=' ')
            print(sr)
            print('该策略的最大回撤为： ',end=' ')
            print(maxDrawdown)
            victory_times=0
            for i in range(0,len(rate)):
                if rate[i]>0:
                    victory_times+=1
            print('该策略的胜率为： ',end=' ')
            print(victory_times/len(rate))
            
            
    #进行OLS回归的作图
        def OLS(self,x,y,title,label,xlabel,ylabel,axvline,axvlabel):
            new_df=pd.DataFrame(index=self.factor.index)
            new_df['x']=x
            new_df['y']=y
            new_df.dropna(inplace=True)
            x = new_df['x']
            y = new_df['y']
            X = sm.add_constant(x)
            result = (sm.OLS(y,X)).fit()
            print(result.summary())
            fig, ax = plt.subplots(figsize=(20,15))
            ax.plot(x, y, 'o', label="data")
            ax.plot(x, result.fittedvalues, 'r', label=label)
            ax.legend(loc='best')
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=(x.max()-x.min())/8))
            plt.xlabel(xlabel,fontsize=16)
            plt.ylabel(ylabel,fontsize=16)
            self.set_picture()
            plt.title(title,fontdict={'size': 20})
            plt.axvline(axvline, color="red", linestyle="--",label=axvlabel)
            plt.legend(prop={'size':16},loc=0)
            plt.show()
    
    
    #OLS回归：得到相关数据以及图（单个标的的时间序列）
        def OLS_data_time(self,x,y):
            sns.set(palette="muted", color_codes=True)
            sns.set(font='SimHei', font_scale=0.8)
            if x==0 and y==0:
                for i in range(0,len(answer.portfolio)):
                    x = self.factor[self.portfolio[i]]
                    y = self.return_rate[self.portfolio[i]]
                    title=portfolio[i]+'的OLS回归图'
                    label=portfolio[i]+"的OLS回归拟合线"
                    xlabel="因子值"
                    ylabel="收益率"
                    axvline=original_factor[self.portfolio[i]].values[len(original_factor.index)-1]
                    axvlabel='目前因子值'
                    self.OLS(x,y,title,label,xlabel,ylabel,axvline,axvlabel)
    
    
            elif x==0 and y==1:
                x=int(input(('请输入你要进行回归的标的的数量: ')))
                sub_portfolio=[]
                for i in range(0,x):
                    s=input('请输入第'+str(i+1)+'个标的的名称: ')
                    sub_portfolio.append(s)
                for i in range(0,len(sub_portfolio)):
                    x = self.factor[sub_portfolio[i]]
                    y = self.return_rate[sub_portfolio[i]]
                    title=sub_portfolio[i]+'的OLS回归图'
                    label=sub_portfolio[i]+"的OLS回归拟合线"
                    xlabel="因子值"
                    ylabel="收益率"
                    axvline=original_factor[sub_portfolio[i]].values[len(original_factor.index)-1]
                    axvlabel='目前因子值'
                    self.OLS(x,y,title,label,xlabel,ylabel,axvline,axvlabel)
                    
                    
            else:
                 for i in range(x-1,y):
                    x = self.factor[self.portfolio[i]]
                    y = self.return_rate[self.portfolio[i]]
                    title=portfolio[i]+'的OLS回归图'
                    label=portfolio[i]+"的OLS回归拟合线"
                    xlabel="因子值"
                    ylabel="收益率"
                    axvline=original_factor[self.portfolio[i]].values[len(original_factor.index)-1]
                    axvlabel='目前因子值'
                    self.OLS(x,y,title,label,xlabel,ylabel,axvline,axvlabel)
    
    
    #描述不同标的的因子值的相关信息
        def describe(self, s):
            print(self.factor.describe(percentiles=s))
     
    
    #进行因子值随时间变化的作图
        def factor_scater(self,x,y,z):
            sns.set(palette="muted", color_codes=True)
            sns.set(font='SimHei', font_scale=0.8)
            if x==0 and y==0:
                for i in range(0,len(self.portfolio)):
                    fig, ax = plt.subplots(figsize=(20,15))
                    if z=='1':
                        ax.plot(self.factor.index, self.factor[self.portfolio[i]], 'o', label=portfolio[i]+"的因子值散点图")
                    elif z=='2':
                        ax.plot(self.factor.index, self.factor[self.portfolio[i]], label=portfolio[i]+"的因子值折线图")
                    ax.legend(loc='best')
                    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(self.factor)/6))
                    plt.xlabel("时间",fontsize=16)
                    plt.ylabel("因子值",fontsize=16)
                    self.set_picture()
                    if z=='1':
                        plt.title(Chinese_name[i]+'的散点图',fontdict={'size': 20})
                    elif z=='2':
                        plt.title(Chinese_name[i]+'的折线图',fontdict={'size': 20})
                    plt.show()
            elif x==0 and y==1:
                x=int(input(('请输入你要进行回归的标的的数量: ')))
                sub_portfolio=[]
                for i in range(0,x):
                    s=input('请输入第'+str(i+1)+'个标的的名称: ')
                    sub_portfolio.append(s)
                for i in range(0,len(sub_portfolio)):
                    fig, ax = plt.subplots(figsize=(20,15))
                    if z=='1':
                        ax.plot(self.factor.index, self.factor[sub_portfolio[i]], 'o', label=portfolio[i]+"的因子值散点图")
                    elif z=='2':
                        ax.plot(self.factor.index, self.factor[sub_portfolio[i]], label=portfolio[i]+"的因子值折线图")
                    ax.legend(loc='best')
                    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(self.factor)/6))
                    plt.xlabel("时间",fontsize=16)
                    plt.ylabel("因子值",fontsize=16)
                    self.set_picture()
                    if z=='1':
                        plt.title(sub_portfolio[i]+'的散点图',fontdict={'size': 20})
                    elif z=='2':
                        plt.title(sub_portfolio[i]+'的折线图',fontdict={'size': 20})
                    plt.show()
            else:
                 for i in range(x-1,y):
                    fig, ax = plt.subplots(figsize=(20,15))
                    if z=='1':
                        ax.plot(self.factor.index, self.factor[self.portfolio[i]], 'o', label=portfolio[i]+"的因子值散点图")
                    elif z=='2':
                        ax.plot(self.factor.index, self.factor[self.portfolio[i]], label=portfolio[i]+"的因子值折线图")
                    ax.legend(loc='best')
                    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(self.factor)/6))
                    plt.xlabel("时间",fontsize=16)
                    plt.ylabel("因子值",fontsize=16)
                    self.set_picture()
                    if z=='1':
                        plt.title(Chinese_name[i]+'的散点图',fontdict={'size': 20})
                    elif z=='2':
                        plt.title(Chinese_name[i]+'的折线图',fontdict={'size': 20})
                    plt.show()
    
    
    #t值分析,每一个交易日做回归可以得到因子的系数以及t值，看一下t值的稳定性
        def t_analysis(self):
            sum_t=0
            t_absolute_value=[]
            t_value=[]
            return_value=[]   #OLS之后得到的x的系数
            for i in range(0,len(self.factor)):
                x=[]
                y=[]
                for j in range(0,len(self.portfolio)):
                    x.append(self.factor[self.portfolio[j]].values[i])
                    y.append(self.return_rate[self.portfolio[j]].values[i])
                new_df=pd.DataFrame(index=self.portfolio)
                new_df['x']=x
                new_df['y']=y
                new_df.dropna(inplace=True)
                if len(new_df)==0:
                    continue
                x = new_df['x']
                y = new_df['y']
                X = sm.add_constant(x)
                result = (sm.OLS(y,X)).fit()
                if result.tvalues[1]<0:
                    t_absolute_value.append(-result.tvalues[1])
                else:
                    t_absolute_value.append(result.tvalues[1])
                t_value.append(result.tvalues[1])
                return_value.append(result.params[1])
            for i in range(0,len(t_absolute_value)):
                if t_absolute_value[i]>2:
                    sum_t+=1
            print('t的绝对值超过2占比为',end=' ')
            print(sum_t/len(t_absolute_value))
            print('t的绝对值均值为：',end=' ')
            print(np.mean(t_absolute_value))
            print('t的均值为：',end=' ')
            print(np.mean(t_value))
            print('t均值/t标准差为：',end=' ')
            print(np.mean(t_value)/np.std(t_value))
            print('因子收益率序列均值为：',end=' ')
            print(np.mean(return_value))
    
    
    #IC值分析
        def IC_value(self,IC_per):
            self.RankIC=[]
            self.IC=[]
            P_IC_value=[]
            P_RankIC_value=[]
            for i in range(0,len(self.factor)):
                x=[]
                y=[]
                for j in range(0,len(self.portfolio)):
                    x.append(self.factor[self.portfolio[j]].values[i])
                    y.append(self.return_rate[self.portfolio[j]].values[i])
                new_df=pd.DataFrame(index=self.portfolio)
                new_df['x']=x
                new_df['y']=y
                new_df.dropna(inplace=True)
                if len(new_df)==0:
                    continue
                x = new_df['x']
                y = new_df['y']
                self.RankIC.append(st.spearmanr(x,y)[0])
                self.IC.append(pearsonr(x,y)[0])
                P_IC_value.append(pearsonr(x,y)[1])
                P_RankIC_value.append(st.spearmanr(x,y)[1])
                
            sum1=0
            for i in range(0,len(self.IC)):
                if self.IC[i]<-IC_per or self.IC[i]>IC_per:
                    sum1+=1
            print('IC绝对值大于'+str(IC_per)+'的占比为',end=' ')
            print(sum1/len(self.IC))
            print('IC均值为',end=' ')
            print(np.mean(self.IC))
            self.IC_mean=np.mean(self.IC)
            print('IC标准差为',end=' ')
            print(np.std(self.IC))
            self.IC_std=np.std(self.IC)
            print('Normal IR比率为',end=' ')
            print(np.mean(self.IC)/np.std(self.IC))
            sum2=0
            for i in range(0,len(self.IC)):
                if self.IC[i]>0:
                    sum2+=1
                    
            print('IC大于0的占比为',end=' ')
            print(sum2/len(self.IC))
            print('IC的P值的均值为',end=' ')
            print(np.mean(P_IC_value))
            
            sum3=0
            for i in range(0,len(self.IC)):
                if self.RankIC[i]<-IC_per or self.RankIC[i]>IC_per:
                    sum3+=1
            print('RankIC绝对值大于'+str(IC_per)+'的占比为',end=' ')
            print(sum3/len(self.RankIC))
            print('RankIC均值为',end=' ')
            print(np.mean(self.RankIC))
            self.RankIC_mean=np.mean(self.RankIC)
            print('RankIC标准差为',end=' ')
            print(np.std(self.RankIC))
            self.RankIC_std=np.std(self.RankIC)
            print('Rank IR比率为',end=' ')
            print(np.mean(self.RankIC)/np.std(self.RankIC))
            sum4=0
            for i in range(0,len(self.RankIC)):
                if self.RankIC[i]>0:
                    sum4+=1
                    
            print('RankIC大于0的占比为',end=' ')
            print(sum4/len(self.RankIC))
            print('RankIC的P值的均值为',end=' ')
            print(np.mean(P_RankIC_value))
    
    
    #将OLS的图画得更好看
        def factor_return(self,x,y):
            sns.set(rc={'figure.figsize': (20, 15)})
            if x==0 and y==0:
                for i in range(0,len(self.portfolio)):
                    h=sns.jointplot(x=self.factor[self.portfolio[i]], y=self.return_rate[self.portfolio[i]], kind = "reg")
                    h.set_axis_labels('factor_value', 'return_rate', fontsize=16)
                    plt.show()
            elif x==0 and y==1:
                x=int(input(('请输入你要进行回归的标的的数量: ')))
                sub_portfolio=[]
                for i in range(0,x):
                    s=input('请输入第'+str(i+1)+'个标的的名称: ')
                    sub_portfolio.append(s)
                for i in range(0,len(sub_portfolio)):
                    h=sns.jointplot(x=self.factor[sub_portfolio[i]], y=self.return_rate[sub_portfolio[i]], kind = "reg")
                    h.set_axis_labels('factor_value', 'return_rate', fontsize=16)
                    plt.show()
            else:
                 for i in range(x-1,y):
                    h=sns.jointplot(x=self.factor[self.portfolio[i]], y=self.return_rate[self.portfolio[i]], kind = "reg")
                    h.set_axis_labels('factor_value', 'return_rate', fontsize=16)
                    plt.show()
    
    
    #IC的相关作图
        def IC_picture(self,gap,IC_type):
            sns.set(palette="muted", color_codes=True)
            sns.set(font='SimHei', font_scale=0.8)
            self.IC_value(0.03)
            if IC_type==1:
                fig, ax = plt.subplots(figsize=(24,10))
                plt.ylim(-1.25, 1.25)
                ax.plot(self.factor.index, self.IC, label='IC值折线图',alpha=0.3)
                ax.plot(self.factor.index, pd.Series(self.IC).rolling(gap).mean(), label='IC值的'+str(gap)+'个时间单位的均值',color='g')
                ax.legend(loc='best')
                ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(self.factor)/6))
                plt.xlabel("时间",fontsize=16)
                plt.ylabel("IC值",fontsize=16)
                self.set_picture()
                ax.text(0,0.95,'IC均值： '+str(self.IC_mean.round(3)),transform=ax.transAxes,fontsize=16)
                ax.text(0,0.9,'IC标准值： '+str(self.IC_std.round(3)),transform=ax.transAxes,fontsize=16)
                plt.title('IC值折线图',fontdict={'size': 20})
                plt.show()
            else:
                fig, ax = plt.subplots(figsize=(24,10))
                plt.ylim(-1.25, 1.25)
                ax.plot(self.factor.index, self.RankIC, label="IC值折线图",alpha=0.3)
                ax.plot(self.factor.index, pd.Series(self.RankIC).rolling(gap).mean(), label='IC值的'+str(gap)+'个时间单位的均值',color='g')
                ax.legend(loc='best')
                ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(self.factor)/6))
                plt.xlabel("时间",fontsize=16)
                plt.ylabel("RankIC值",fontsize=16)
                self.set_picture()
                ax.text(0,0.95,'RankIC均值： '+str(self.RankIC_mean.round(3)),transform=ax.transAxes,fontsize=16)
                ax.text(0,0.9,'RankIC标准值： '+str(self.RankIC_std.round(3)),transform=ax.transAxes,fontsize=16)
                plt.title('RankIC值折线图',fontdict={'size': 20})
                plt.show()
    
    
    #分组回测
        def group_test(self,groups):
            total_list=[]
            factor_value=[]
            self.return_rate=self.return_rate/time_gap
            for i in range(groups):
                total_list.append([])
                factor_value.append([])
            for i in range(0,len(self.factor)):
                process_bar(float(i)/float(len(self.factor)), start_str='', end_str='100%', total_length=0)
                x=pd.DataFrame(index=self.portfolio)
                x['factor']=self.factor.iloc[i]
                x['return_rate']=self.return_rate.iloc[i]
                x=x.T
                x.dropna(axis=1,inplace=True)
                x=x.sort_values(by='factor', axis=1)
                order=list(x.columns)
                average_number=len(order)/groups
                current_group=0
                initial_group=0
                total_rate=0
                for j in range(0,len(order)):
                    position=int(j/average_number)
                    if current_group!=position:
                        group_number=j-initial_group
                        if group_number==0:
                            total_list[current_group].append(0)
                        else:
                            total_list[current_group].append(total_rate/group_number)
                        total_rate=x[order[j]]['return_rate']
                        factor_value[position].append(x[order[j]]['factor'])
                        initial_group=j
                        current_group=position
                    else:
                        total_rate+=x[order[j]]['return_rate']
                        factor_value[position].append(x[order[j]]['factor'])
                group_number=len(order)-initial_group
                if group_number==0:
                    total_list[current_group].append(0)
                else:
                    total_list[current_group].append(total_rate/group_number)
            self.daily_rate=total_list
            rate=[]
            for i in range(groups):
                basic=1
                rate.append([])
                for j in range(0,len(total_list[i])):
                    basic+=total_list[i][j]
                    rate[i].append(basic)
            self.group_total_return=rate
            name_group=[]
            for i in range(groups):
                name_group.append(str(i+1)+'分位')
            df=pd.DataFrame(columns=name_group,index=['平均每日收益率','累计收益率','复利累计收益率','标准差','因子最小值','因子最大值','因子平均值','因子标准差'])
            for i in range(groups):
                df[str(i+1)+'分位'][0]=np.mean(total_list[i])/time_gap
            for i in range(groups):
                df[str(i+1)+'分位'][1]=np.sum(total_list[i])
            rate=[]
            for i in range(groups):
                basic=1
                base=1
                rate.append([])
                for j in range(0,len(total_list[i])):
                    if (j+1)%time_gap==0:
                        base=basic
                    basic+=total_list[i][j]*base
                    rate[i].append(basic)
                df[str(i+1)+'分位'][2]=rate[i][len(total_list[i])-1]-1
            self.group_compound_return=rate
            for i in range(groups):
                df[str(i+1)+'分位'][3]=np.std(total_list[i])
            for i in range(groups):
                df[str(i+1)+'分位'][4]=np.min(factor_value[i])
            for i in range(groups):
                df[str(i+1)+'分位'][5]=np.max(factor_value[i])
            for i in range(groups):
                df[str(i+1)+'分位'][6]=np.mean(factor_value[i])
            for i in range(groups):
                df[str(i+1)+'分位'][7]=np.std(factor_value[i])
            print()
            print(df)
            for i in range(groups):
                print('以下是'+str(i+1)+'分位的收益详情：')
                self.strategy_information(total_list[i],rate[i])
            self.return_rate=return_rate
    
    #分组回测的相关图表
        def group_picture(self,kind,x,y):
            sns.set(palette="muted", color_codes=True)
            sns.set(font='SimHei', font_scale=0.8)
            years=int(str(self.factor.index[len(self.factor)-1])[:4])-int(str(self.factor.index[0])[:4])+1
            months=[]
            for i in range(0,years):
                months.append([])
                for j in range(0,12):
                    months[i].append(0)
            if x==0 and y==0:
                fig, ax = plt.subplots(figsize=(20,15))
                for i in range(0,groups):
                    if kind==1:
                        ax.plot(self.factor.index, self.group_total_return[i], label="第"+str(i+1)+'分位的累计收益率')
                    elif kind==2:
                        ax.plot(self.factor.index, self.group_compound_return[i], label="第"+str(i+1)+'分位的复利累计收益率')
                ax.legend(loc='best')
                ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(self.factor)/6))
                plt.xlabel("时间",fontsize=16)
                plt.ylabel("收益情况",fontsize=16)
                self.set_picture()
                if kind==1:
                    plt.title('分位的累计收益率',fontdict={'size': 20})
                elif kind==2:
                    plt.title('分位的复利累计收益率',fontdict={'size': 20})
                plt.show()
                for i in range(0,groups):
                    fig, ax = plt.subplots(figsize=(20,15))
                    sns.distplot(self.daily_rate[i],bins=40,kde=True)
                    ax.legend(loc='best')
                    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(self.factor)/6))
                    plt.xlabel("收益率",fontsize=16)
                    plt.ylabel("频数",fontsize=16)
                    self.set_picture()
                    plt.title("第"+str(i+1)+'分位的收益率分布',fontdict={'size': 20})
                    plt.show()
                ylist=[self.factor.index[0].year]
                current_year=self.factor.index[0].year
                for j in range(1,len(self.group_total_return[0])):
                        if current_year!=self.factor.index[j].year:
                            ylist.append(self.factor.index[j].year)
                            current_year=self.factor.index[j].year
                
                for i in range(0,groups):
                    fig, ax = plt.subplots(figsize=(20,15))
                    current_rate=1
                    current_time=self.factor.index[0]
                    current_year=self.factor.index[0]
                    for j in range(0,years):
                        for k in range(0,12):
                            months[j][k]=0
                    for j in range(1,len(self.group_total_return[i])):
                        if current_time.month!=self.factor.index[j].month:
                            if kind==1:
                                years=int(str(self.factor.index[j-1])[:4])-int(str(self.factor.index[0])[:4])
                                months[years][current_time.month-1]=self.group_total_return[i][j]-current_rate
                                current_rate=self.group_total_return[i][j]
                            elif kind==2:
                                years=int(str(self.factor.index[j-1])[:4])-int(str(self.factor.index[0])[:4])
                                months[years][current_time.month-1]=(self.group_compound_return[i][j]-current_rate)/current_rate
                                current_rate=self.group_compound_return[i][j]
                        current_time=self.factor.index[j]
                    xlist=['1','2','3','4','5','6','7','8','9','10','11','12']
                    months=np.array(months)
                    ax=sns.heatmap(months,mask=months==0,xticklabels=xlist,yticklabels=ylist,cmap='RdYlGn_r',annot=True,annot_kws={"fontsize":20})
                    plt.xticks(fontsize=20)
                    plt.yticks(fontsize=20)
                    plt.legend(prop={'size':20})
                    cbar = ax.collections[0].colorbar
                    cbar.ax.tick_params(labelsize=20)
                    if kind==1:
                        ax.set_title(str(time_gap)+'天收益周期的第'+str(i+1)+'分位的非复利月度收益图',fontdict={'size': 24})
                    elif kind==2:
                        ax.set_title(str(time_gap)+'天收益周期的第'+str(i+1)+'分位的复利月度收益图',fontdict={'size': 24})
                    plt.show()
                                
                        
                
        
            elif x==0 and y==1:
                x=int(input(('请输入你要进行观察分位的数量: ')))
                sub_portfolio=[]
                for i in range(0,x):
                    s=int(input('请输入第'+str(i+1)+'个分位的数字: '))
                    sub_portfolio.append(s)
                fig, ax = plt.subplots(figsize=(20,15))    
                for i in range(0,len(sub_portfolio)):
                    if kind==1:
                        ax.plot(self.factor.index, self.group_total_return[sub_portfolio[i]-1], label="第"+str(sub_portfolio[i])+'分位的累计收益率')
                    elif kind==2:
                        ax.plot(self.factor.index, self.group_compound_return[sub_portfolio[i]-1], label="第"+str(sub_portfolio[i])+'分位的复利累计收益率')
                ax.legend(loc='best')
                ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(self.factor)/6))
                plt.xlabel("时间",fontsize=16)
                plt.ylabel("收益情况",fontsize=16)
                self.set_picture()
                if kind==1:
                    plt.title('分位的累计收益率',fontdict={'size': 20})
                elif kind==2:
                    plt.title('分位的复利累计收益率',fontdict={'size': 20})
                plt.show()
                for i in range(0,len(sub_portfolio)):
                    sns.distplot(self.daily_rate[sub_portfolio[i]-1],bins=40,kde=True)
                    ax.legend(loc='best')
                    plt.xlabel("收益率",fontsize=16)
                    plt.ylabel("频数",fontsize=16)
                    self.set_picture()
                    plt.title("第"+str(sub_portfolio[i])+'分位的收益率分布',fontdict={'size': 20})
                    plt.show()
                ylist=[self.factor.index[0].year]
                current_year=self.factor.index[0].year
                for j in range(1,len(self.group_total_return[0])):
                        if current_year!=self.factor.index[j].year:
                            ylist.append(self.factor.index[j].year)
                            current_year=self.factor.index[j].year
                
                for i in range(0,len(sub_portfolio)):
                    current_rate=1
                    current_time=self.factor.index[0]
                    current_year=self.factor.index[0]
                    for j in range(0,years):
                        for k in range(0,12):
                            months[j][k]=0
                    for j in range(1,len(self.group_total_return[sub_portfolio[i]-1])):
                        if current_time.month!=self.factor.index[j].month:
                            if kind==1:
                                years=int(str(self.factor.index[j-1])[:4])-int(str(self.factor.index[0])[:4])
                                months[years][current_time.month-1]=self.group_total_return[sub_portfolio[i]-1][j]-current_rate
                                current_rate=self.group_total_return[sub_portfolio[i]-1][j]
                            elif kind==2:
                                years=int(str(self.factor.index[j-1])[:4])-int(str(self.factor.index[0])[:4])
                                months[years][current_time.month-1]=(self.group_compound_return[sub_portfolio[i]-1][j]-current_rate)/current_rate
                                current_rate=self.group_compound_return[sub_portfolio[i]-1][j]
                            print('第'+str(sub_portfolio[i])+'分位的'+str(self.factor.index[j-1])[:4]+'年'+str(current_time.month)+'月的收益率为：'+str(months[years][current_time.month-1]))    
                        current_time=self.factor.index[j]
                    xlist=['1','2','3','4','5','6','7','8','9','10','11','12']
                    months=np.array(months)
                    ax=sns.heatmap(months,mask=months==0,xticklabels=xlist,yticklabels=ylist,cmap='RdYlGn_r',annot=True,annot_kws={"fontsize":20})
                    plt.xticks(fontsize=20)
                    plt.yticks(fontsize=20)
                    plt.legend(prop={'size':20})
                    cbar = ax.collections[0].colorbar
                    cbar.ax.tick_params(labelsize=20)
                    if kind==1:
                        ax.set_title(str(time_gap)+'天收益周期的第'+str(sub_portfolio[i])+'分位的非复利月度收益图',fontdict={'size': 24})
                    elif kind==2:
                        ax.set_title(str(time_gap)+'天收益周期的第'+str(sub_portfolio[i])+'分位的复利月度收益图',fontdict={'size': 24})
                    plt.show()
            else:
                fig, ax = plt.subplots(figsize=(20,15))
                for i in range(x-1,y):
                    if kind==1:
                        ax.plot(self.factor.index, self.group_total_return[i], label="第"+str(i+1)+'分位的累计收益率')
                    elif kind==2:
                        ax.plot(self.factor.index, self.group_compound_return[i], label="第"+str(i+1)+'分位的复利累计收益率')
                ax.legend(loc='best')
                plt.xlabel("时间",fontsize=16)
                plt.ylabel("收益情况",fontsize=16)
                self.set_picture()
                if kind==1:
                    plt.title('分位的累计收益率',fontdict={'size': 20})
                elif kind==2:
                    plt.title('分位的复利累计收益率',fontdict={'size': 20})
                plt.show()
                for i in range(x-1,y):
                    sns.distplot(self.daily_rate[i],bins=40,kde=True)
                    ax.legend(loc='best')
                    plt.xlabel("收益率",fontsize=16)
                    plt.ylabel("频数",fontsize=16)
                    self.set_picture()
                    plt.title("第"+str(i+1)+'分位的收益率分布',fontdict={'size': 20})
                    plt.show()
                ylist=[self.factor.index[0].year]
                current_year=self.factor.index[0].year
                for j in range(1,len(self.group_total_return[0])):
                        if current_year!=self.factor.index[j].year:
                            ylist.append(self.factor.index[j].year)
                            current_year=self.factor.index[j].year
                
                for i in range(x-1,y):
                    current_rate=1
                    current_time=self.factor.index[0]
                    current_year=self.factor.index[0]
                    for j in range(0,years):
                        for k in range(0,12):
                            months[j][k]=0
                    for j in range(1,len(self.group_total_return[i])):
                        if current_time.month!=self.factor.index[j].month:
                            if kind==1:
                                years=int(str(self.factor.index[j-1])[:4])-int(str(self.factor.index[0])[:4])
                                months[years][current_time.month-1]=self.group_total_return[i][j]-current_rate
                                current_rate=self.group_total_return[i][j]
                            elif kind==2:
                                years=int(str(self.factor.index[j-1])[:4])-int(str(self.factor.index[0])[:4])
                                months[years][current_time.month-1]=(self.group_compound_return[i][j]-current_rate)/current_rate
                                current_rate=self.group_compound_return[i][j]
                            print('第'+str(i+1)+'分位的'+str(self.factor.index[j-1])[:4]+'年'+str(current_time.month)+'月的收益率为：'+str(months[years][current_time.month-1]))
                        current_time=self.factor.index[j]
                    xlist=['1','2','3','4','5','6','7','8','9','10','11','12']
                    months=np.array(months)
                    ax=sns.heatmap(months,mask=months==0,xticklabels=xlist,yticklabels=ylist,cmap='RdYlGn_r',annot=True,annot_kws={"fontsize":20})
                    plt.xticks(fontsize=20)
                    plt.yticks(fontsize=20)
                    plt.legend(prop={'size':20})
                    cbar = ax.collections[0].colorbar
                    cbar.ax.tick_params(labelsize=20)
                    if kind==1:
                        ax.set_title(str(time_gap)+'天收益周期的第'+str(i+1)+'分位的非复利月度收益图',fontdict={'size': 24})
                    elif kind==2:
                        ax.set_title(str(time_gap)+'天收益周期的第'+str(i+1)+'分位的复利月度收益图',fontdict={'size': 24})
                    plt.show()
    
    
    #根据因子值进行策略的编写
        def strategy(self,left,right):
            final_rate=[]
            self.return_rate=self.return_rate/time_gap
            for i in range(0,len(self.factor)):
                rate=[]
                for j in range(0,len(self.portfolio)):
                    if self.factor[self.portfolio[j]].values[i]>=left and self.factor[self.portfolio[j]].values[i]<=right:
                        rate.append(self.return_rate[self.portfolio[j]].values[i])
                if rate==[]:
                    final_rate.append(0)
                else:
                    final_rate.append(np.mean(rate))
            rate=[]
            basic=1
            for i in range(0,len(final_rate)):
                basic*=(1+final_rate[i])
                rate.append(basic)
            self.strategy_information(final_rate, rate)
            sns.set(palette="muted", color_codes=True)
            sns.set(font='SimHei', font_scale=0.8)
            fig, ax = plt.subplots(figsize=(20,15))
            ax.plot(self.factor.index, rate, label='复利累计收益情况')
            ax.legend(loc='best')
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(self.factor)/6))
            plt.xlabel("时间",fontsize=16)
            plt.ylabel("收益情况",fontsize=16)
            self.set_picture()
            plt.title("因子值处于"+str(left)+'和'+str(right)+'之间的复利累计收益率',fontdict={'size': 20})
            plt.show()
            fig, ax = plt.subplots(figsize=(20,15))
            sns.distplot(final_rate,bins=40,kde=True)
            ax.legend(loc='best')
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(self.factor)/6))
            plt.xlabel("收益率",fontsize=16)
            plt.ylabel("频数",fontsize=16)
            self.set_picture()
            plt.title("因子值处于"+str(left)+'和'+str(right)+'之间的收益率分布',fontdict={'size': 20})
            plt.show()
            self.return_rate=return_rate
    
    #换手率分析
        def change_hands(self,groups,left,right):
            sns.set(palette="muted", color_codes=True)
            sns.set(font='SimHei', font_scale=0.8)
            targets=[]
            targets_container=[]
            change_times=[]
            total_times=[]
            change_rate_everyday=[]
            for i in range(groups):
                targets.append([])
                targets_container.append([])
                change_times.append(0)
                total_times.append(0)
                change_rate_everyday.append([])
            for i in range(groups):
                for j in range(0,len(self.factor)-time_gap):
                    change_rate_everyday[i].append(0)
            now_times=0
            for s in range(0,time_gap):
                for i in range(groups):
                    targets[i]=[]
                    targets_container[i]=[]
                    change_times.append(0)
                    total_times.append(0)
                for i in range(s,len(self.factor),time_gap):
                    now_times+=1
                    process_bar(now_times/float(len(self.factor)), start_str='', end_str='100%', total_length=0)
                    x=pd.DataFrame(index=self.portfolio)
                    x['factor']=self.factor.iloc[i]
                    x['return_rate']=self.return_rate.iloc[i]
                    x=x.T
                    x.dropna(axis=1,inplace=True)
                    x=x.sort_values(by='factor', axis=1)
                    order=list(x.columns)
                    average_number=len(order)/groups
                    current_group=0
                    initial_group=0
                    targets=targets_container.copy()
                    change_times_everyday=0
                    for j in range(groups):
                        targets_container[j]=[]
                    for j in range(0,len(order)):
                        position=int(j/average_number)
                        if i!=s:
                            if current_group!=position:
                                group_number=j-initial_group
                                change_rate_everyday[current_group][i-time_gap]=change_times_everyday/group_number
                                initial_group=j
                                current_group=position
                                change_times_everyday=0
                            if order[j] not in targets[position]:
                                change_times[position]+=1
                                change_times_everyday+=1
                            total_times[position]+=1
                            targets_container[position].append(order[j])
                        else:
                            targets_container[position].append(order[j])
                    group_number=len(order)-initial_group
                    if i!=s:
                        change_rate_everyday[current_group][i-time_gap]=change_times_everyday/group_number
            name_group=[]
            for i in range(groups):
                name_group.append(str(i+1)+'分位')
            df=pd.DataFrame(columns=name_group,index=['换手率'])
            for i in range(groups):
                df[str(i+1)+'分位'][0]=change_times[i]/total_times[i]
            print()
            print(df)
            if left==0 and right==0:
                for i in range(0,groups):
                    df=pd.DataFrame(index=self.factor.index[time_gap:])
                    df['第'+str(i+1)+'分位每个时间单位的换手率']=change_rate_everyday[i]
                    print(df)
                    fig, ax = plt.subplots(figsize=(20,15))
                    ax.plot(self.factor.index[time_gap:], change_rate_everyday[i], label="第"+str(i+1)+'分位的每个时间单位的换手率')
                    ax.legend(loc='best')
                    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(self.factor)/6))
                    plt.xlabel("时间",fontsize=16)
                    plt.ylabel("换手率",fontsize=16)
                    self.set_picture()
                    plt.title("第"+str(i+1)+'分位的每个时间单位的换手率',fontdict={'size': 20})
                    plt.show()
            elif left==0 and right==1:
                x=int(input(('请输入你要进行观察分位的数量: ')))
                sub_portfolio=[]
                for i in range(0,x):
                    s=int(input('请输入第'+str(i+1)+'个分位的数字: '))
                    sub_portfolio.append(s)
                for i in range(0,len(sub_portfolio)):
                    df=pd.DataFrame(index=self.factor.index[time_gap:])
                    df['第'+str(i)+'分位每个时间单位的换手率']=change_rate_everyday[sub_portfolio[i]-1]
                    print(df)
                    fig, ax = plt.subplots(figsize=(20,15))
                    ax.plot(self.factor.index[time_gap:], change_rate_everyday[sub_portfolio[i]-1], label="第"+str(sub_portfolio[i])+'分位的每个时间单位的换手率')
                    ax.legend(loc='best')
                    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(self.factor)/6))
                    plt.xlabel("时间",fontsize=16)
                    plt.ylabel("换手率",fontsize=16)
                    self.set_picture()
                    plt.title("第"+str(sub_portfolio[i])+'分位的每个时间单位的换手率',fontdict={'size': 20})
                    plt.show()
            else:
                 for i in range(left-1,right):
                    df=pd.DataFrame(index=self.factor.index[time_gap:])
                    df['第'+str(i+1)+'分位每个时间单位的换手率']=change_rate_everyday[i]
                    print(df)
                    fig, ax = plt.subplots(figsize=(20,15))
                    ax.plot(self.factor.index[time_gap:], change_rate_everyday[i], label="第"+str(i+1)+'分位的每个时间单位的换手率')
                    ax.legend(loc='best')
                    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(self.factor)/6))
                    plt.xlabel("时间",fontsize=16)
                    plt.ylabel("换手率",fontsize=16)
                    self.set_picture()
                    plt.title("第"+str(i+1)+'分位的每个时间单位的换手率',fontdict={'size': 20})
                    plt.show()
                    
    
    
        def factor_bins(self,left,right,kind,choice):
            sns.set(palette="muted", color_codes=True)
            sns.set(font='SimHei', font_scale=0.8)
            average_factor=[]
            if choice==2:
                for i in range(0,len(self.factor)):
                    if self.factor.index[i]>=left:
                        left=i+1
                        break
                for i in range(left,len(self.factor)):
                    if self.factor.index[i]>=right:
                        right=i+1
                        break
            if kind==0:
                for i in range(0,len(self.portfolio)):
                    average_factor.append(self.factor[portfolio[i]][left-1:right].mean())
            else:
                for i in range(0,len(self.portfolio)):
                    average_factor.append(self.factor[portfolio[i]][left+kind-2])
            fig, ax = plt.subplots(figsize=(20,15))
            sns.distplot(average_factor,bins=100,kde=True)
            ax.legend(loc='best')
            plt.xlabel("因子值",fontsize=16)
            plt.ylabel("比值",fontsize=16)
            self.set_picture()
            plt.title("从"+str(self.factor.index[left-1])+'至'+str(self.factor.index[right-1])+'的因子值分布',fontdict={'size': 20})
            plt.show()
    
    
    
        def panel_ols(self,left,right,kind,choice):
            sns.set(palette="muted", color_codes=True)
            sns.set(font='SimHei', font_scale=0.8)
            average_factor=[]
            average_return=[]
            if choice==2:
                for i in range(0,len(self.factor)):
                    if self.factor.index[i]>=left:
                        left=i+1
                        break
                for i in range(left,len(self.factor)):
                    if self.factor.index[i]>=right:
                        right=i+1
                        break
            if kind==0:
                for i in range(0,len(self.portfolio)):
                    average_factor.append(self.factor[portfolio[i]][left-1:right].mean())
                    average_return.append(self.return_rate[portfolio[i]][left-1:right].mean())
            else:
                for i in range(0,len(self.portfolio)):
                    average_factor.append(self.factor[portfolio[i]][left+kind-2])
                    average_return.append(self.return_rate[portfolio[i]][left+kind-2])
            x = average_factor
            y = average_return
            X = sm.add_constant(x)
            result = (sm.OLS(y,X)).fit()
            print(result.summary())
            fig, ax = plt.subplots(figsize=(20,15))
            ax.plot(x, y, 'o', label="data")
            ax.plot(x, result.fittedvalues, 'r')
            ax.legend(loc='best')
            ax.xaxis.set_major_locator(ticker.MultipleLocator(max(x)/15))
            plt.xlabel("因子值",fontsize=16)
            plt.ylabel("收益率",fontsize=16)
            self.set_picture()
            plt.title("从"+str(self.factor.index[left-1])+'至'+str(self.factor.index[right-1])+'的因子值与收益率之间的回归',fontdict={'size': 20})
            plt.show()
            while(1):
                print('根据上图，请选择您想要保留的因子值数据(原因子值为最原始数据），请先输入x，再输入y，确保x<y，如果x等于y则退出')
                left_factor=float(input('请输入起始因子值: '))
                right_factor=float(input('请输入终止因子值: '))
                if left_factor!=right_factor:
                    x1=x.copy()
                    y1=y.copy()
                    times=0
                    for i in range(len(x)):
                        if x[i]< left_factor or x[i]> right_factor:
                            x1[i]=99999
                            y1[i]=99999
                            times+=1
                    for i in range(times):
                        x1.remove(99999)
                        y1.remove(99999)
                    if len(x1)!=0:
                        X = sm.add_constant(x1)
                        result = (sm.OLS(y1,X)).fit()
                        print(result.summary())
                        fig, ax = plt.subplots(figsize=(20,15))
                        ax.plot(x1, y1, 'o', label="data")
                        ax.plot(x1, result.fittedvalues, 'r')
                        ax.legend(loc='best')
                        ax.xaxis.set_major_locator(ticker.MultipleLocator(max(x1)/15))
                        plt.xlabel("因子值",fontsize=16)
                        plt.ylabel("收益率",fontsize=16)
                        self.set_picture()
                        plt.title("从"+str(self.factor.index[left-1])+'至'+str(self.factor.index[right-1])+'的因子值与收益率之间的回归',fontdict={'size': 20})
                        plt.show()
                else:
                    break
    
    
    
        def difference_month(self,left,right,kind):
            years=int(str(self.factor.index[len(self.factor)-1])[:4])-int(str(self.factor.index[0])[:4])+1
            ylist=[self.factor.index[0].year]
            current_year=self.factor.index[0].year
            left-=1
            right-=1
            months_left=[]
            months_right=[]
            months=[]
            for i in range(0,years):
                months_left.append([])
                months_right.append([])
                months.append([])
                for j in range(0,12):
                    months_left[i].append(0)
                    months_right[i].append(0)
                    months[i].append(0)
            for j in range(1,len(self.group_total_return[0])):
                    if current_year!=self.factor.index[j].year:
                        ylist.append(self.factor.index[j].year)
                        current_year=self.factor.index[j].year
            for j in range(0,years):
                for k in range(0,12):
                    months_left[j][k]=0
                    months_right[j][k]=0
                    months[j][k]=0
            current_rate_left=1
            current_rate_right=1
            current_time=self.factor.index[0]
            current_year=self.factor.index[0]
            for j in range(1,len(self.group_total_return[left])):
                if current_time.month!=self.factor.index[j].month:
                    if kind==1:
                        years=int(str(self.factor.index[j-1])[:4])-int(str(self.factor.index[0])[:4])
                        months_left[years][current_time.month-1]=self.group_total_return[left][j]-current_rate_left
                        months_right[years][current_time.month-1]=self.group_total_return[right][j]-current_rate_right
                        current_rate_left=self.group_total_return[left][j]
                        current_rate_right=self.group_total_return[right][j]
                    elif kind==2:
                        years=int(str(self.factor.index[j-1])[:4])-int(str(self.factor.index[0])[:4])
                        months_left[years][current_time.month-1]=(self.group_compound_return[left][j]-current_rate_left)/current_rate_left
                        months_right[years][current_time.month-1]=(self.group_compound_return[right][j]-current_rate_right)/current_rate_right
                        current_rate_left=self.group_compound_return[left][j]
                        current_rate_right=self.group_total_return[right][j]
                current_time=self.factor.index[j]
            xlist=['1','2','3','4','5','6','7','8','9','10','11','12']
            years=int(str(self.factor.index[len(self.factor)-1])[:4])-int(str(self.factor.index[0])[:4])+1
            for j in range(0,years):
                for k in range(0,12):
                    months[j][k]=months_left[j][k]-months_right[j][k]
            fig, ax = plt.subplots(figsize=(20,15))
            months=np.array(months)
            ax=sns.heatmap(months,mask=months==0,xticklabels=xlist,yticklabels=ylist,cmap='RdYlGn_r',annot=True,annot_kws={"fontsize":20})
            plt.xticks(fontsize=20)
            plt.yticks(fontsize=20)
            plt.legend(prop={'size':20})
            cbar = ax.collections[0].colorbar
            cbar.ax.tick_params(labelsize=20)
            if kind==1:
                ax.set_title(str(time_gap)+'天收益周期的第'+str(left+1)+'分位减去第'+str(right+1)+'分位的非复利月度收益图',fontdict={'size': 24})
            elif kind==2:
                ax.set_title(str(time_gap)+'天收益周期的第'+str(left+1)+'分位减去第'+str(right+1)+'分位的复利月度收益图',fontdict={'size': 24})
            plt.show()
        
    

    
    from datetime import datetime
    time_gap=int(input('请输入收益率的时间间隔: '))
    factor=df_factor
    close=df_close
    ##确保index为时间序列
    factor.index=pd.to_datetime(factor.index)
    close.index=pd.to_datetime(close.index)
    
    neutralize=input('''
    请问您是否需要进行因子的中性化处理:
    0:不需要
    或者请输入代码：综合指数，例如：sh.000001 上证指数，sz.399106 深证综指 等；
    规模指数，例如：sh.000016 上证50，sh.000300 沪深300，sh.000905 中证500，sz.399001 深证成指等；
    一级行业指数，例如：sh.000037 上证医药，sz.399433 国证交运 等；
    二级行业指数，例如：sh.000952 300地产，sz.399951 300银行 等；
    策略指数，例如：sh.000050 50等权，sh.000982 500等权 等；
    成长指数，例如：sz.399376 小盘成长 等；
    价值指数，例如：sh.000029 180价值 等；
    主题指数，例如：sh.000015 红利指数，sh.000063 上证周期 等；
    ''')
        
    
    if neutralize!='0':
        while(1):
            if neutralize=='0':
                break
            try:
                lg = bs.login()  
                start_date=str(factor.index[0])[:10]
                end_date=str(factor.index[len(factor)-1])[:10]
                rs = bs.query_history_k_data_plus(neutralize,
                    "date,close",
                    start_date=start_date, end_date=end_date, frequency="d")
                data_list = []
                while (rs.error_code == '0') & rs.next():
                    data_list.append(rs.get_row_data())
                result = pd.DataFrame(data_list, columns=rs.fields)
                result.set_index('date',inplace=True)
                result.index=pd.to_datetime(result.index)
                result=result.astype(float)
                result=(result/result.shift(time_gap)-1).shift(-time_gap)
                result.replace(np.inf, np.nan,inplace=True)
                result=result[:-time_gap]
                result.rename(columns={'close':'return_rate'},inplace=True)
                print('您获取的指数收益率为：')
                print(result)
                bs.logout()  
                break
            except:
                neutralize=input('''
    输入有误！请重新输入！
    请问您是否需要进行因子的中性化处理:
    0:不需要
    或者请输入代码：综合指数，例如：sh.000001 上证指数，sz.399106 深证综指 等；
    规模指数，例如：sh.000016 上证50，sh.000300 沪深300，sh.000905 中证500，sz.399001 深证成指等；
    一级行业指数，例如：sh.000037 上证医药，sz.399433 国证交运 等；
    二级行业指数，例如：sh.000952 300地产，sz.399951 300银行 等；
    策略指数，例如：sh.000050 50等权，sh.000982 500等权 等；
    成长指数，例如：sz.399376 小盘成长 等；
    价值指数，例如：sh.000029 180价值 等；
    主题指数，例如：sh.000015 红利指数，sh.000063 上证周期 等；
    ''')
        
    
    
    ##得到收益率
    return_rate=(close/close.shift(time_gap)-1).shift(-time_gap)
    return_rate.replace(np.inf, np.nan,inplace=True)
    factor.replace(np.inf,np.nan,inplace=True)
    
    ##存一下名称（目前仍然是代号，可以替换成中文名称，但是要确保代号的顺序和中文名称的顺序一致）
    ##存一下原来的因子值，不要被筛掉了
    portfolio=list(factor.columns)
    Chinese_name=portfolio
    original_factor=factor
    factor=factor[:-time_gap]
    return_rate=return_rate[:-time_gap]
    if neutralize!='0':
        return_rate=return_rate.sub(result['return_rate'],axis=0)
    print('目前的因子值为： ')
    print(factor)
    print('目前的中性化后收益率为： ')
    print(return_rate)
    
    ##现在开始进入class
    answer=factor_analysis(factor,return_rate,portfolio)
    while(1):
        print('''
    
    
    请选择你要进行的操作:''',end=' ')
        x=input('''
    0.退出操作
    1.进行OLS的相关操作：可得到OLS相关系数以及拟合曲线图（比较丑，为单个标的的时间序列）
    2.进行散点图的制作：X轴为因子值，Y轴为收益率（该图比1得到的图好看，为单个标的的时间序列）
    3.得到不同标的的该因子的相关数据：包括分位数划分、最大值、均值、最小值、标准差、数量
    4.进行图的制作，X轴为时间，Y轴为因子值，用以观测因子值随时间的变化趋势
    5.进行t统计量的相关检验 
    6.进行IC值的统计
    7.进行IC图的制作：IC值随时间的变化关系以及一段时间内的IC均值曲线
    8.进行分组回测：得到分组后的各组收益率的相关情况以及分位数情况
    9.进行分组回测：得到分组后的各组收益率的走势图以及频率分布直方图（需要首先完成8）
    10.根据因子值制定策略：指定因子值区间，只购买处于区间内的标的
    11.换手率分析：用于分析因子的稳定性
    12.更换收益周期
    13.因子值的分布频率直方图（若时间周期为多天，因子值为该标的的平均值或者该周期内的第X天的值）
    14.因子值横截面回归
    15.任意两个分位之间的月度收益率作差（请确保完成8）
    
    
    ''')
        
        if x=='0':
            break
    
        if x=='1':
            print('''
    请输入两个数字x、y：
    确保x<y,
    表明你要对列数处于x~y的标的进行时间序列的回归
    在输入x和y的时候请确保换行
    如果想使用全部的标的，请把x和y都输入为0
    如果想使用标的名称而不是标的所处的列数：
    请x输入为0，y输入为1，
    并传入你想要进行时间序列回归标的的代码名称
    ''')
            x=int(input())
            y=int(input())
            print()
            answer.OLS_data_time(x, y)
        
        elif x=='2':
            print('''
    请输入两个数字x、y：
    确保x<y,
    表明你要对列数处于x~y的标的进行制作散点图
    在输入x和y的时候请确保换行
    如果想使用全部的标的，请把x和y都输入为0
    如果想使用标的名称而不是标的所处的列数：
    请x输入为0，y输入为1，
    并传入你想要进行图制作的代码名称
    ''')
            x=int(input())
            y=int(input())
            print()
            answer.factor_return(x,y)
        
        
        elif x=='3':
            a=int(input(('请输入你想要划分的分位数的个数: ')))
            percent=[]
            for i in range(0,a):
                s=float(input('请输入第'+str(i+1)+'个分位数，确保输入的数字在0-1之间: '))
                percent.append(s)
            answer.describe(percent)
        
        elif x=='4':
            print('''
    请输入两个数字x、y：
    确保x<y,
    表明你要对列数处于x~y的标的进行图的制作
    在输入x和y的时候请确保换行
    如果想使用全部的标的，请把x和y都输入为0
    如果想使用标的名称而不是标的所处的列数：
    请x输入为0，y输入为1，
    并传入你想要进行图制作的代码名称
    ''')
            x=int(input())
            y=int(input())
            print()
            z=input('''请问你想制作下列哪种类型的图：
    1.散点图
    2.折线图
    
    ''')
            answer.factor_scater(x, y,z)
    
    
        elif x=='5':
            answer.t_analysis()
    
    
        elif x=='6':
            IC_per=float(input('''请输入一个位于0~1之间的数字X
    该数字用以表示你想得到的|IC|>X的占比
    
    '''))
            answer.IC_value(IC_per)
    
    
        elif x=='7':
            gap=int(input('''请输入你想要得到多长时间单位的均值移动曲线：
    时间单位是因子值的index
    
    '''))
            IC_type=int(input('''请输入你想要得到哪种类型的IC图：
    1.Normal IC
    2.Rank IC
    '''))
            answer.IC_picture(gap,IC_type)
    
    
        elif x=='8':
            groups=int(input('请输入你想要将这些标的分为几组，输入的组数请不要超过标的的总数: '))
            answer.group_test(groups)
    
    
        elif x=='9':
            print('请确保在进行9之前已经进行选项8的操作，分组数量为选项8的分组数量')
            kind=int(input('''请输入你想要得到哪种收益率的走势图：
    1.累计收益率
    2.复利收益率
    '''))
            print('''
    请输入两个数字x、y：
    确保x<y,
    表明你要对处于x~y的分位进行图的制作
    在输入x和y的时候请确保换行
    如果想使用全部分位，请把x和y都输入为0
    如果想使用特定分位：
    请x输入为0，y输入为1，
    并传入你想要进行图制作的分位数字
    ''')
            x=int(input())
            y=int(input())
            print()
            answer.group_picture(kind,x,y)
    
    
        elif x=='10':
            left=float(input('请输入因子值区间的左边界: '))
            right=float(input('请输入因子值区间的右边界: '))
            answer.strategy(left,right)
    
    
        elif x=='11':
            groups=int(input('请输入你想要将这些标的分为几组，输入的组数请不要超过标的的总数: '))
            print('''
    请输入两个数字x、y：
    确保x<y,
    表明你要对处于x~y的分位进行换手率图的制作以及每日详细的换手率
    在输入x和y的时候请确保换行
    如果想使用全部分位，请把x和y都输入为0
    如果想使用特定分位：
    请x输入为0，y输入为1，
    并传入你想要进行图制作的分位数字
    ''')
            left=int(input())
            right=int(input())
            print()
            answer.change_hands(groups,left,right)
    
    
        elif x=='12':
            time_gap=int(input('请输入收益率的时间间隔: '))
            factor=df_factor
            close=df_close
            return_rate=pd.DataFrame(index=factor.index,columns=factor.columns)
            portfolio=list(factor.columns)
            return_rate=close.diff(periods=time_gap)
            return_rate=return_rate.shift(-time_gap)
            return_rate=return_rate/close
            factor=factor[:-time_gap]
            return_rate=return_rate[:-time_gap]
            print(factor)
            print(return_rate)
            answer=factor_analysis(factor,return_rate,portfolio)
    
    
        elif x=='13':
            from datetime import datetime
            print('请输入因子值的时间范围，确保输入的起始时间<终止时间')
            choice=int(input('''请输入时间的格式
    1.第X天到第Y天
    2.从2020-01-01到2020-01-31
    '''))
            if choice==1:
                left=int(input('请输入起始时间：'))
                right=int(input('请输入终止时间： '))
            else:
                left=(input('请输入起始时间：'))
                right=(input('请输入终止时间：'))
                left = datetime.strptime(left, "%Y-%m-%d")
                right = datetime.strptime(right, "%Y-%m-%d")
            kind=int(input('''请输入你想要以哪一种因子值作为最终因子值
    0.这一段时间内的平均值
    X.这一段时间的第X天的值，请注意：1<=X<=（终止时间-起始时间+1）且X为正整数
    '''))
            answer.factor_bins(left,right,kind,choice)
        
        
        elif x=='14':
            from datetime import datetime
            print('请输入因子值的时间范围，确保输入的起始时间<终止时间')
            choice=int(input('''请输入时间的格式
    1.第X天到第Y天
    2.从2020-01-01到2020-01-31
    '''))
            if choice==1:
                left=int(input('请输入起始时间：'))
                right=int(input('请输入终止时间： '))
            else:
                left=(input('请输入起始时间：'))
                right=(input('请输入终止时间：'))
                left = datetime.strptime(left, "%Y-%m-%d")
                right = datetime.strptime(right, "%Y-%m-%d")
            kind=int(input('''请输入你想要以哪一种因子值作为最终因子值
    0.这一段时间内的平均值
    X.这一段时间的第X天的值，请注意：1<=X<=（终止时间-起始时间+1）且X为正整数
    '''))
            answer.panel_ols(left,right,kind,choice)
        
        
        elif x=='15':
            print('请输入你想得到的第X分位-第Y分位的月度收益图')
            left=int(input('请输入第X分位：'))
            right=int(input('请输入第Y分位：'))
            kind=int(input('''请输入你想要得到哪种收益率的走势图：
    1.累计收益率
    2.复利收益率
    '''))
            answer.difference_month(left,right,kind)
    
if __name__=='__namin__':
    backtest('turn','close')
