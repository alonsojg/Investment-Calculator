"""
Use pyplot to plot how your 401(k) saving change with varying parameters

to add:
    yearly investing percentage of salary slider
    independent + 401k investing line graph

to fix:
    separate match_rate from ind_investing_salary_percentage to allow greater
    percentage of salary to be invested independently (+401k or solely
    independent).

"""

import sys
import subprocess

# implement pip as a subprocess:
# subprocess.check_call([sys.executable, '-m', 'pip', 'install',
# 'numpy'])
# subprocess.check_call([sys.executable, '-m', 'pip', 'install',
# 'matplotlib'])

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import numpy as np
import streamlit as st


fig = plt.figure()
plt.subplots_adjust(left=0.25, right=.8, bottom=0.4)
ax = fig.add_subplot(1,1,1)

# Set slider color and dimensions
axcolor = 'lightgoldenrodyellow'
axcolor_1 = 'green'
axannual_salary = plt.axes([0.4, 0.18, 0.5, 0.01], facecolor=axcolor)
axannual_salary_increase = plt.axes([0.4, 0.16, 0.5, 0.01], facecolor=axcolor)
axcurrent_age = plt.axes([0.4, 0.14, 0.5, 0.01], facecolor=axcolor)
axage_of_retirement = plt.axes([0.4, 0.12, 0.5, 0.01], facecolor=axcolor)
axpresent_401k_balance = plt.axes([0.4, 0.10, 0.5, 0.01], facecolor=axcolor)
axannual_ROR_1 = plt.axes([0.4, 0.04, 0.5, 0.01], facecolor=axcolor)
axannual_ROR_2 = plt.axes([0.4, 0.0, 0.5, 0.01], facecolor=axcolor_1)
axmatch = plt.axes([0.4, 0.08, 0.5, 0.01], facecolor=axcolor)
axmax_match_rate = plt.axes([0.4, 0.06, 0.5, 0.01], facecolor=axcolor)
axind_investing_salary_percentage = plt.axes([0.4, 0.02, 0.5, 0.01], facecolor=axcolor_1)
resetax = plt.axes([0.4, 0.25, 0.1, 0.02])


annual_salary = Slider(axannual_salary, 'What is your Annual Salary after taxes?', 0, 200000, valinit=65000, valstep=1)
annual_salary_increase = Slider(axannual_salary_increase, 'At what rate does your salary grow in first 10 years (in %) ', 0.0, 0.12, valinit=0.03, valstep=0.005)
current_age = Slider(axcurrent_age, 'At what age do you plan to begin contributing towards your retirement fund?', 18.0, 30.0, valinit=27.0)
age_of_retirement = Slider(axage_of_retirement, 'At what age do you plan to retire?', 31.0, 60.0, valinit=60.0, valstep=0.5)
present_401k_balance = Slider(axpresent_401k_balance, 'How much do you already have invested in your 401(k)?', 0.0, 20000.0, valinit=1000.0, valstep=500.0)
annual_ROR_1 = Slider(axannual_ROR_1, 'What is your rate of return with a 401(k) fund?', 0.0, 0.70, valinit=0.055, valstep=0.01)
annual_ROR_2 = Slider(axannual_ROR_2, 'What is your rate of return independently?', 0.0, 0.70, valinit=0.055, valstep=0.01)
match = Slider(axmatch, 'what percentage of your salary does your company match?', 0.0, 0.15, valinit=0.03, valstep=0.01)
max_match_rate = Slider(axmax_match_rate, 'At what rate does your company match that percentage?', 0.0, 1.0, valinit=1.0, valstep=0.1)
ind_investing_salary_percentage = Slider(axind_investing_salary_percentage, 'What percentage of your salary will you invest independently?', 0.0, 0.15, valinit=0.03, valstep=0.01)
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
sliders = [annual_salary,
           annual_salary_increase,
           current_age,
           age_of_retirement,
           present_401k_balance,
           annual_ROR_1,
           annual_ROR_2,
           match,
           max_match_rate,
           ind_investing_salary_percentage]


def calculate_balance_401k(annual_salary = 65000,
                          annual_salary_increase = 0.115,
                          current_age = 27,
                          age_of_retirement = 60,
                          present_401k_balance = 1000,
                          annual_ROR_1 = 0.07,
                          match = 0.03,
                          max_match_rate = 100,
                          ):

    initial_account_worth = present_401k_balance + (annual_salary * match)
    initial_account_worth = initial_account_worth  + (annual_salary * match * max_match_rate)

    year_by_year_account_total=[initial_account_worth]

    for year in range(1,int(age_of_retirement-current_age)):

        return_at_end_of_year = year_by_year_account_total[year-1] * (1+annual_ROR_1)
        if year <= 10:
            annual_salary = annual_salary * (1+annual_salary_increase)

        next_year_starting_balance = return_at_end_of_year + annual_salary * match
        next_year_starting_balance = next_year_starting_balance + annual_salary * match * max_match_rate

        year_by_year_account_total.append(np.round(next_year_starting_balance,2))

    return year_by_year_account_total

def calculate_balance_ind(annual_salary = 65000,
                          annual_salary_increase = 0.115,
                          ind_investing_salary_percentage = 0.03,
                          current_age = 27,
                          age_of_retirement = 60,
                          annual_ROR_2 = 0.07):

    initial_account_worth = annual_salary * ind_investing_salary_percentage

    year_by_year_account_total=[initial_account_worth]

    for year in range(1,int(age_of_retirement-current_age)):

        return_at_end_of_year = year_by_year_account_total[year-1] * (1+annual_ROR_2)
        if year <= 10:
            annual_salary = annual_salary * (1+annual_salary_increase)

        next_year_starting_balance = return_at_end_of_year + annual_salary * ind_investing_salary_percentage

        year_by_year_account_total.append(next_year_starting_balance)

    return year_by_year_account_total



def update(val=None):

    balance_1 = calculate_balance_401k(
        annual_salary=annual_salary.val,
        annual_salary_increase=annual_salary_increase.val,
        current_age=current_age.val,
        age_of_retirement = age_of_retirement.val,
        present_401k_balance = present_401k_balance.val,
        annual_ROR_1=annual_ROR_1.val,
        match=match.val,
        max_match_rate=max_match_rate.val
    )

    balance_2 = calculate_balance_ind(
        annual_salary = annual_salary.val,
        annual_salary_increase = annual_salary_increase.val,
        ind_investing_salary_percentage = ind_investing_salary_percentage.val,
        current_age = current_age.val,
        age_of_retirement = age_of_retirement.val,
        annual_ROR_2=annual_ROR_2.val,)


    ax.clear()
    ax.plot([x/12 for x in range(len(balance_1))], balance_1)
    ax.plot([x/12 for x in range(len(balance_2))], balance_2)
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(
        lambda x, loc: "${:,}".format(int(x))))
    ax.set_ylabel('401(k) balance')
    ax.set_xlabel('Years')
    fig.suptitle(f'Final_balance_401_k: ${balance_1[-1]:,.2f} ------ Final\_balance\_Ind: ${balance_2[-1]:,.2f}')


def reset(event):
    for s in sliders:
        s.reset()

annual_salary.on_changed(update)
ind_investing_salary_percentage.on_changed(update)
annual_salary_increase.on_changed(update)
current_age.on_changed(update)
age_of_retirement.on_changed(update)
present_401k_balance.on_changed(update)
annual_ROR_1.on_changed(update)
annual_ROR_2.on_changed(update)
match.on_changed(update)
max_match_rate.on_changed(update)

button.on_clicked(reset)
update()
st.pyplot(plt.show())
