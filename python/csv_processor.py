import pandas as pd

def analyze_sales(df):
    """
    Analyze sales data from a DataFrame containing month, revenue, and cost columns.
    Returns a DataFrame with additional analysis including margins.
    
    Parameters:
    df (pandas.DataFrame): DataFrame with columns 'month', 'revenue', and 'cost'
    
    Returns:
    pandas.DataFrame: Original data with additional analysis columns
    """
    # Create a copy to avoid modifying the original DataFrame
    analysis = df.copy()
    
    # Calculate margin (profit) in dollars
    analysis['margin'] = analysis['revenue'] - analysis['cost']
    
    # Calculate margin percentage
    analysis['margin_percentage'] = (analysis['margin'] / analysis['revenue'] * 100).round(2)
    
    # Calculate month-over-month revenue growth
    analysis['revenue_growth'] = analysis['revenue'].pct_change() * 100
    
    # Calculate month-over-month cost changes
    analysis['cost_growth'] = analysis['cost'].pct_change() * 100
    
    # Calculate cost as percentage of revenue
    analysis['cost_to_revenue_ratio'] = (analysis['cost'] / analysis['revenue'] * 100).round(2)
    
    # Add summary statistics
    summary = {
        'total_revenue': analysis['revenue'].sum(),
        'total_cost': analysis['cost'].sum(),
        'total_margin': analysis['margin'].sum(),
        'average_margin_percentage': analysis['margin_percentage'].mean(),
        'average_cost_to_revenue': analysis['cost_to_revenue_ratio'].mean(),
        'highest_cost_month': analysis.loc[analysis['cost'].idxmax(), 'month'],
        'lowest_cost_month': analysis.loc[analysis['cost'].idxmin(), 'month'],
        'highest_cost_growth': analysis['cost_growth'].max(),
        'average_cost_growth': analysis['cost_growth'].mean(),
        'best_margin_month': analysis.loc[analysis['margin'].idxmax(), 'month'],
        'worst_margin_month': analysis.loc[analysis['margin'].idxmin(), 'month']
    }
    
    return analysis, summary

def extract_matching_columns(source_file, target_template_file, output_file):
    """
    Extract data from source CSV to match the structure of a target template CSV.
    
    Parameters:
    source_file (str): Path to the source CSV file with 224 columns
    target_template_file (str): Path to the template CSV file with 16 columns
    output_file (str): Path where the output CSV will be saved
    """
    try:
        # Read the source and template files
        source_df = pd.read_csv(source_file)
        template_df = pd.read_csv(target_template_file)
        
        # Get the column names from the template
        target_columns = template_df.columns.tolist()
        
        # Verify all template columns exist in source
        missing_columns = [col for col in target_columns if col not in source_df.columns]
        if missing_columns:
            raise ValueError(f"The following columns are missing from the source file: {missing_columns}")
        
        # Extract only the matching columns from source
        output_df = source_df[target_columns]
        
        # Clean the data
        for column in output_df.columns:
            output_df[column] = output_df[column].apply(clean_data)
        
        # Save to new CSV file
        output_df.to_csv(output_file, index=False)
        
        print(f"Successfully extracted {len(target_columns)} columns to {output_file}")
        print(f"Number of rows processed: {len(output_df)}")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find one of the input files - {str(e)}")
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def clean_data(value):
    """
    Clean data by removing currency symbols, mathematical operators, and special characters.
    
    Parameters:
    value: The value to clean
    
    Returns:
    str: The cleaned value
    """
    if pd.isna(value):
        return ''
    
    # Convert to string
    value = str(value)
    
    # Remove currency symbols
    value = value.replace('£', '').replace('$', '').replace('€', '').replace('¥', '')
    
    # Remove mathematical operators
    value = value.replace('+', '').replace('-', '').replace('*', '').replace('/', '').replace('=', '').replace('%', '')
    
    # Remove parentheses and brackets
    value = value.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('{', '').replace('}', '')
    
    # Remove multiple spaces and trim
    value = ' '.join(value.split())
    
    return value

# Example usage
if __name__ == "__main__":
    source_file = "source.csv"  # Your source CSV with 224 columns
    template_file = "template.csv"  # Your template CSV with 16 columns
    output_file = "extracted_data.csv"  # Where you want to save the result
    
    extract_matching_columns(source_file, template_file, output_file)