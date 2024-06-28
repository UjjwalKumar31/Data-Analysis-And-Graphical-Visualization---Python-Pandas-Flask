from flask import Flask, render_template, render_template_string
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from io import BytesIO
import base64
import main


app = Flask(__name__)

# Route to display the dataframe and plot

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/dataframe')
def dataframe():
    # Convert DataFrame to HTML table
    table_html = main.df3.to_html(classes='table table-striped')
    # highlevel = main.high_level_summary_data.to_html(classes='table table-striped')

    # Render HTML template with the table
    return render_template('index.html', table=table_html, display = 'Dataset Table')

@app.route('/dataframe/highlevel')
def high_level_summary_data():
    # Function to generate plot and return it as a base64-encoded string
    def high_level_plot():
        plt.figure(figsize=(8, 6))
        ax = main.high_level_summary_data.plot(kind='bar')
        for p in ax.patches:
            yval = p.get_height()
            plt.text(p.get_x() + p.get_width()/2, yval + 0.2, yval, ha='center', va='bottom')  
        plt.title('Bar Chart')
        plt.xlabel('Category')
        plt.ylabel('Values')

        # Save plot to a BytesIO object
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_data = buffer.getvalue()

        # Encode plot data to base64
        encoded_plot = base64.b64encode(plot_data).decode('utf-8')
        plt.close()

        return encoded_plot
    # Convert DataFrame to HTML table
    plot = high_level_plot()
    highlevel = main.high_level_summary_data.to_html(classes='table table-striped')

    # Render HTML template with the table
    return render_template('high_level.html', table=highlevel, plot=plot, title = 'High Level Summary Display')

@app.route('/dataframe/locationwise')
def LocationWiseAnalysis ():
    # Function to generate plot and return it as a base64-encoded string
    def LocationAnalysis():
        plt.figure(figsize=(8, 6))
        ax = main.df4.plot(kind='bar', x='Location', y=['Order Count', 'Revenue Generated',  'Profit'], colormap='Greens', rot=1)
        for p in ax.patches:
            yval = p.get_height()
            plt.text(p.get_x() + p.get_width()/2, yval, yval, ha='center', va='bottom')  
        plt.title('Bar Chart')
        plt.xlabel('Cities')
        plt.ylabel('Values')

        # Save plot to a BytesIO object
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_data = buffer.getvalue()

        # Encode plot data to base64
        encoded_plot = base64.b64encode(plot_data).decode('utf-8')
        plt.close()

        return encoded_plot
    
    plot = LocationAnalysis()
    # Convert DataFrame to HTML table
    dataframe = main.df4.to_html(classes='table table-striped')

    # Render HTML template with the table
    return render_template('high_level.html', table=dataframe, plot=plot, title = 'Location Wise Analysis')

@app.route('/dataframe/commissiontrend')
def MonthlyCommissionTrend():
    # Function to generate plot and return it as a base64-encoded string
    def generate_plot():
        plt.figure(figsize=(8, 6))
        ax = main.df5.plot(kind='bar', x='Month', color='green', rot=1)
        for p in ax.patches:
            yval = p.get_height()
            plt.text(p.get_x() + p.get_width()/2, yval + 0.2, yval, ha='center', va='bottom')  
        plt.title('Bar Chart')
        plt.xlabel('Month')
        plt.ylabel('Revenue')

        # Save plot to a BytesIO object
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_data = buffer.getvalue()

        # Encode plot data to base64
        encoded_plot = base64.b64encode(plot_data).decode('utf-8')
        plt.close()

        return encoded_plot
    
    plot = generate_plot()
    # Convert DataFrame to HTML table
    dataframe = main.df5.to_html(classes='table table-striped')

    # Render HTML template with the table
    return render_template('high_level.html', table=dataframe, plot=plot, title = 'Monthly Commission/Revenue Trend')


@app.route('/dataframe/discountsoffers')
def utilization_count_discount_offer():
    # Function to generate plot and return it as a base64-encoded string
    def generate_plot():
        plt.figure(figsize=(8, 6))
        ax = main.utilization_count_discount_offer.plot(kind='bar', x='Discounts and Offers', y=['Applied',  'Profit'], rot=1)
        for p in ax.patches:
            yval = p.get_height()
            plt.text(p.get_x() + p.get_width()/2, yval + 0.2, yval, ha='center', va='bottom')  
        plt.title('Bar Chart')
        plt.xlabel('Discounts and Offers')
        plt.ylabel('Values')

        # Save plot to a BytesIO object
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_data = buffer.getvalue()

        # Encode plot data to base64
        encoded_plot = base64.b64encode(plot_data).decode('utf-8')
        plt.close()

        return encoded_plot
    
    plot = generate_plot()
    # Convert DataFrame to HTML table
    dataframe = main.utilization_count_discount_offer.to_html(classes='table table-striped')

    # Render HTML template with the table
    return render_template('high_level.html', table=dataframe, plot=plot, title = 'Discounts & Offers Utilization')

@app.route('/dataframe/popularpaymentmethod')
def PopularPaymentMethod():
    dataframe = main.datafrmm_.to_html(classes='table table-striped')

    # Render HTML template with the table
    return render_template('index.html', table=dataframe, display = 'Popular Payment Method Restaurant Wise')

@app.route('/dataframe/timevariantanalysis')
def Time_variant_analysis_Month():
    # Function to generate plot and return it as a base64-encoded string
    def generate_plot():
        plt.figure(figsize=(10, 8))
        ax = main.avg_cost_per_month.plot(kind='bar', x='Month', rot=0)
        for p in ax.patches:
            yval = p.get_height()
            plt.text(p.get_x() + p.get_width()/2, yval + 0.2, round(yval,2), ha='center', va='bottom')  
        plt.title('Bar Chart')
        plt.xlabel('Months')
        plt.ylabel('Values')

        # Save plot to a BytesIO object
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_data = buffer.getvalue()

        # Encode plot data to base64
        encoded_plot = base64.b64encode(plot_data).decode('utf-8')
        plt.close()

        return encoded_plot

    def generate_plot2():
        plt.figure(figsize=(10, 8))
        ax = main.avg_cost_per_week.plot(kind='bar', x='Week', rot=0)
        for p in ax.patches:
            yval = p.get_height()
            plt.text(p.get_x() + p.get_width()/2, yval + 0.2, round(yval,2), ha='center', va='bottom')  
        plt.title('Bar Chart')
        plt.xlabel('Weeks')
        plt.ylabel('Values')

        # Save plot to a BytesIO object
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_data = buffer.getvalue()

        # Encode plot data to base64
        encoded_plot = base64.b64encode(plot_data).decode('utf-8')
        plt.close()

        return encoded_plot

    plot1 = generate_plot()
    plot2 = generate_plot2()

    dataframe = main.avg_cost_per_month.to_html(classes='table table-striped')
    dataframe2 = main.avg_cost_per_week.to_html(classes='table table-striped')

    # Render HTML template with the table
    return render_template('timevariantanalysis.html', table1=dataframe, table2=dataframe2, 
                           display1 = 'Avg. Cost/Expense Per Month',
                           display2 = 'Avg. Cost/Expense Per Week',
                           plot1 = plot1, plot2 = plot2)

if __name__ == '__main__':
    app.run(debug=True)
