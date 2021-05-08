import pandas as pd
import math
import scipy.stats as st

"""
 Test that he null hypothesis that the probability of conversion in the treatment group minus the probability of conversion in the control group equals zero. And set the alternative hypothesis to be that the probability of conversion in the treatment group minus the probability of conversion in the control group does not equal zero.

 H0 = treatment_conversion - treatment_control = 0
 H1 = treatment_conversion - treatment_control > 0

 practical_significance = 0.01 #user defined
 confidence_level = 0.05 #user defined, for a 95% confidence interval
 sensitivity = 0.8 #user defined
"""

dataset = pd.read_csv(r"link_to_datasource")

def cleanup(mask, data):
    index_to_drop1 = data[mask].index
    dataset = data.drop(index_to_drop1)
    return dataset

def abStatistics(n1, n2, prob, alpha, x1,x2,practical_significance):
    SE = math.sqrt(prob * (1-prob) * (1/n1 + 1/n2))
    zscore = st.norm.ppf(1-alpha/2)
    margin_of_error = SE * zscore

    mean_diff = x2-x1
    lower_bound = mean_diff-margin_of_error
    upper_bound = mean_diff + margin_of_error

    if practical_significance < lower_bound:
        print("Reject null Hypothesis")
    else:
        print ("Accept null Hypothesis")

    print(f"Standard Error: {SE}, margin of error: {margin_of_error}, CI ({lower_bound},{upper_bound})")
#EDA
#identify inconsistent records
mask1 = (dataset["group"] == "control") & (dataset["landing_page"] == "new_page")
data = cleanup(mask1, dataset)

mask2 = (dataset["group"] == "treatment") & (dataset["landing_page"] == "old_page")
df = cleanup(mask2,data)

##Check unique users
print(f"Total users: {df['user_id'].count()} and Unique: {df['user_id'].nunique()}. Duplicate record: {df['user_id'].count() - df['user_id'].nunique()}")
#drop duplicates
df.drop_duplicates(subset = 'user_id', keep='first', inplace = True)


## Calculate the probability of users that got converted
#total users
total_users = df['converted'].count()
## controls
total_control_users = df["converted"][df["group"] == "control"].count()
converted_controls = df["converted"][df["group"] == "control"].sum()
mean_controls = converted_controls/total_control_users

#experiments
total_experiment_users = df["converted"][df["group"] == "treatment"].count()
converted_experiment = df["converted"][df["group"] == "treatment"].sum()
mean_experiment = converted_experiment/total_experiment_users

#probability of conversion
prob = (converted_controls + converted_experiment)/total_users
practical_significance = 0.01 #user defined
confidence_level = 0.05 #user defined, for a 95% confidence interval
sensitivity = 0.8 #user defined


abStatistics(total_control_users, total_experiment_users, prob, confidence_level, mean_controls,mean_experiment,practical_significance)
    

