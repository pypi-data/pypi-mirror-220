from SBO_pulp.RegressionSplines import MARS
import pandas as pd

data = pd.read_excel("D:\\正事专用文件夹\\学习资料\\仿真优化\\pyISO\\pyISBO\\Example.xlsx")
parameterInfo = pd.read_excel("D:\\正事专用文件夹\\学习资料\\仿真优化\\pyISO\\pyISBO\\Example.xlsx", 1)
y = data.pop("y")
m = MARS(parameterInfo, "neg_mean_squared_error")
m.fit(data, y)
m.MIP_transform()
print(m.MIP.variables())
print(m.MIP.coefficients())
m.optimize()
print(m.optimizedParameter)
print(m.output)