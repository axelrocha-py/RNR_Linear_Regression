import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

def outliers_cleaner(amount_spent_arr,reach_arr):
    '''
    This function gets two data arrays and clean
    this data droped the outliers in dataset based
    on IQR calculate. Returns a list with two axis
    numpy arrays.
    '''
    amount_reach_list_clean = []
    x_clean = []
    y_clean = []

    # Create binomial data on a list <<amount_spent_list>>
    a_r = zip(amount_spent_arr, reach_arr)
    amount_spent_dict = set(a_r)
    amount_spent_list = list(amount_spent_dict)

    # Calculate IQR based on axis = 0
    Q1 = np.percentile(amount_spent_arr, q = 25)
    Q3 = np.percentile(amount_spent_arr, q = 75)

    IQR = Q3-Q1

    bottom_lim = Q1-(1.5*IQR)
    upper_lim = Q3+(1.5*IQR)

    # Create a new list <<amount_reach_list_clean >> with bonomial data without outliers
    for i in range(0, len(amount_spent_list)-1):
        if amount_spent_list[i][0] > bottom_lim and amount_spent_list[i][0] < upper_lim:
            amount_reach_list_clean.append(amount_spent_list[i])

    # Separate the binomial list in two numpy array axis
    for i in range(0, len(amount_reach_list_clean)-1):
        x_clean.append(amount_reach_list_clean[i][0])
        y_clean.append(amount_reach_list_clean[i][1])
    
    x_clean_arr = np.asarray(x_clean)
    y_clean_arr = np.asarray(y_clean)

    return(x_clean_arr, y_clean_arr)

def estimate_m_b(x , y):
    n = np.size(x)
    
    # Calculate m formula summations
    m_x = np.mean(x)
    m_y = np.mean(y)
    
    # Calculate m and b
    sum_1 = np.sum((x-m_x)*(y-m_y))
    sum_2 = np.sum((x-m_x)**2)
    
    m = sum_1/sum_2
    b = m_y - (m*m_x)
                   
    return (m , b)

def plot_regression(x, y, m, b):
    
    fig, ax = plt.subplots(figsize=(16,8))
    ax.scatter(x , y)
    ax.set_xlabel('Amount Spent (MXN)')
    ax.set_ylabel('Reach')
    
    y_pred = (m*x) + b
    plt.plot(x, y_pred, color = 'r')
    
    # Labels
    plt.xlabel('Amount Spent(MXN)')
    plt.ylabel('Reach')
    
    plt.show()

def plot_regression_pred(x, y, m, b, x_inv, y_ach):

    fig, ax = plt.subplots(figsize=(16,8))
    ax.scatter(x , y)
    ax.set_xlabel('Amount Spent (MXN)')
    ax.set_ylabel('Reach')
    
    ax.scatter(x_inv , y_ach, marker = 'o', s=150, c='r')
    
    y_pred = (m*x) + b
    plt.plot(x, y_pred, color = 'r')
    
    # Labels
    plt.xlabel('Amount Spent(MXN)')
    plt.ylabel('Reach')
    
    plt.show()


def pred_model(x, y, m, b, x_inv):
    y_ach = (m*x_inv) + b
    print(f'The reach you can probably obtain is: {int(y_ach)} people reach')
    answer_graph = input('Do you want to view the scatter graph? (y/n) ')

    if answer_graph == 'n':
        return None
    elif answer_graph == 'y':
        plot_regression_pred(x, y, m, b, x_inv, y_ach)



if __name__ == '__main__':
    
    df = pd.read_csv(input('Write the CSV file path for analyze: '))

    amount_spent_arr = df['Importe gastado (MXN)']
    reach_arr = df['Alcance']

    # Clean our dataset of outliers
    x = outliers_cleaner(amount_spent_arr,reach_arr)[0]
    y = outliers_cleaner(amount_spent_arr,reach_arr)[1]

    # Calculate our regression line
    eq = estimate_m_b(x , y)
    m = eq[0]
    b = eq[1]  
    print(f'Process was succesful. m = {m} , b = {b} \n\nAnd your regression formula is y = {round(m,2)}x + {round(b,2)}')

    # Show data and linear regression on scatter map
    plot_regression(x, y, m, b)

    # Applying prediction model 
    answer = input('Do you want to calculate a prediction with this linear regression? (y/n) ')
    if answer == 'y':
        x_inv = int(input('What is the amount you want to invest in a promotion on Facebook? '))
        pred_model(x, y, m, b, x_inv)

    elif answer == 'n':
        print('Goodbye! ;)')
    else:
        print('ERROR. Invalid answer.')

    print('The program was finished.')


