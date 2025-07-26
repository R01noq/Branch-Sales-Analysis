import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

f = pd.read_csv("sales_branches.csv", nrows=30)
print(f)
df= f.drop(["Revenue","Profit"], axis=1)
missing_rateo = df.isnull().mean()*100
print(missing_rateo)
df_clean = df.copy()
cols = ["Unit_Price", "Cost_per_Unit"]
for col in cols:
    df_clean[col] = df_clean.groupby("Product")[col].transform(lambda x: x.fillna(x.mean()))

print(df_clean)
df_clean["Unit_Price"] = pd.to_numeric(df_clean["Unit_Price"], errors="coerce").round(2) 
df_clean["Quantity"] = pd.to_numeric(df_clean["Quantity"], errors="coerce").round(2)
df_clean["Cost_per_Unit"] = pd.to_numeric(df_clean["Cost_per_Unit"], errors="coerce").round(2)
df_clean["Total_Cost"] = (df_clean["Quantity"] * df_clean["Cost_per_Unit"]).round(2)
df_clean["Revenue"] = (df_clean["Unit_Price"] * df_clean["Quantity"]).round(2)
df_clean["Profit"] = df_clean["Revenue"] - df_clean["Total_Cost"]
 

branch_summary = df_clean.groupby("Branch").agg({
    "Revenue": "sum",
    "Profit": "sum" ,
}).reset_index()
date_summary = df_clean.groupby("Date").agg({
    "Revenue": "mean",
    "Profit": "mean"
})
branch_summary["Margin(%)"] = (branch_summary["Profit"]/branch_summary["Revenue"])*100
branch_summary["Margin(%)"] = branch_summary["Margin(%)"].round(2)
rows = ["Revenue", "Profit"]
for row in rows:
    branch_summary[row]= branch_summary[row].round(2)
    date_summary[row]= date_summary[row].round(2)
print("the revenue and the profit per beach are:\n", branch_summary)
print(" the average (revenue/profit) according to date :\n", date_summary)
revenues = []
branches = []
profits = []
data = branch_summary[["Branch", "Revenue", "Profit"]].to_numpy()
branches.extend(data[:,0])
revenues.extend(data[:,1])
profits.extend(data[:,2])

max_rev = max(revenues)
mask = data[:,1]==max_rev
branch_max = data[mask][:,0]
for branch in branch_max:
    print(f"the highest branch revenue is : {branch}")
   

n = len(branches)
x = np.arange(n)
width=0.3

plt.figure(figsize=(10,10))
plt.bar(x+width/2, revenues, width=width, label="revenue", color="skyblue" )
plt.bar(x-width/2, profits, width=width, label="profit", color="orange" )
plt.legend()
plt.title(f"compare between revenues/profit of three branches ({branches})")
plt.xlabel("branch")
plt.ylabel("revenue/profit")
plt.xticks(ticks=range(len(branches)), labels=branches)
plt.ylim(0,2000)
plt.tight_layout()
plt.savefig("revenue_branche.png", bbox_inches="tight", dpi=300)
plt.show()








