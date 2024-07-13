import matplotlib.pyplot as plt
import seaborn as sns


    category_totals = database_ready.groupby('Category')['Money out'].sum().reset_index()

    # Create a bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Category', y='Money out', data=category_totals, palette='viridis')
    plt.xlabel('Category')
    plt.ylabel('Total Money Out')
    plt.title('Total Money Out by Category')
    plt.show()

 
    