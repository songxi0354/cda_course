import numpy as np
import pandas as pd
import os; 
print(os.getcwd())
# 一键生成（用随机种子，保证每次结果完全一样）
np.random.seed(42)

mu = np.log(50000)
sigma = 0.75
incomes = np.random.lognormal(mu, sigma, size=1000)

df = pd.DataFrame({'居民年收入（元）': np.round(incomes).astype(int)})

# 保存为Excel（推荐）
df.to_excel('居民年收入_1000条.xlsx', index=False)

# 同时保存CSV（万一电脑没openpyxl）
df.to_csv('居民年收入_1000条.csv', index=False, encoding='utf-8-sig')

# 打印验证
print("生成成功！")
print(f"平均值: {df['居民年收入（元）'].mean():.0f} 元")
print(f"中位数: {df['居民年收入（元）'].median():.0f} 元")
print(df.describe())