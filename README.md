# CSV Data Extraction Project

## Table of Contents
1. [Overview](#overview)
2. [Project Evolution](#project-evolution)
3. [Solutions](#solutions)
   - [Python Script](#python-script)
   - [Web Interface](#web-interface)
4. [Implementation Details](#implementation-details)
5. [Usage Instructions](#usage-instructions)
6. [Development History](#development-history)

## Overview
This project provides tools for extracting and processing data from CSV files. It originated from a need to extract specific columns from a source CSV file (224 columns) to match a template/output format (16 columns), while cleaning the data by removing currency symbols and mathematical operators.

## Project Evolution

### Initial Requirements
- Extract data from source CSV (224 columns) to match template CSV (16 columns)
- Clean data by removing currency symbols and mathematical operators
- Preserve matching column names and data integrity

### Development Phases
1. **Phase 1**: Python script for basic CSV processing
2. **Phase 2**: Web interface for easier user interaction
3. **Phase 3**: Added Excel format support (later removed for simplicity)
4. **Phase 4**: Finalized CSV-only version with enhanced features

## Solutions

### Python Script
```python
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
```

### Web Interface
The final web interface provides:
- File upload for source and output CSV files
- Data cleaning functionality
- Column matching and extraction
- Preview of processed data
- Custom filename for download

Key features of the data cleaning function:
```javascript
function cleanData(value) {
    if (value === null || value === undefined) return '';
    let cleanValue = String(value);
    // Remove currency symbols (£, $, €, ¥)
    cleanValue = cleanValue.replace(/[£$€¥]/g, '');
    // Remove mathematical operators (+, -, *, /, =, %)
    cleanValue = cleanValue.replace(/[+\-*\/=%]/g, '');
    // Remove multiple spaces and trim
    cleanValue = cleanValue.replace(/\s+/g, ' ').trim();
    // Remove parentheses and brackets
    cleanValue = cleanValue.replace(/[\(\)\[\]{}]/g, '');
    // Remove special characters but keep decimals and commas
    cleanValue = cleanValue.replace(/[^0-9a-zA-Z,.\s]/g, '');
    return cleanValue;
}
```

## Implementation Details

### Data Processing Flow
1. User uploads source and output CSV files
2. System validates column matches
3. Data is processed and cleaned
4. Preview is generated
5. Clean CSV file is available for download

### Data Cleaning Rules
- Removes currency symbols (£, $, €, ¥)
- Removes mathematical operators (+, -, *, /, =, %)
- Removes parentheses and brackets
- Preserves decimal points and commas
- Trims extra spaces
- Handles null/undefined values

## Usage Instructions

### Using the Web Interface
1. Open the HTML file in a web browser
2. Upload source CSV file (224 columns)
3. Upload output template CSV file (16 columns)
4. Enter desired output filename (optional)
5. Click "Process Files"
6. Review the preview
7. Click "Download Result" to save the processed file

### Requirements
- Modern web browser
- CSV files with headers
- Source file must contain all columns specified in output template

## Development History

### Initial Implementation
- Started with Python script for basic CSV processing
- Added data cleaning functionality
- Implemented column matching logic

### Web Interface Development
- Created user-friendly interface
- Added file upload capabilities
- Implemented real-time preview
- Added custom filename feature

### File Format Support Evolution
1. Initially CSV only
2. Added Excel support (XLSX, XLS)
3. Reverted to CSV-only for simplicity and reliability

### Debugging and Improvements
- Added detailed error messages
- Improved column name matching
- Enhanced data cleaning rules
- Added preview functionality

### Final Optimizations
- Streamlined file processing
- Improved error handling
- Enhanced user feedback
- Simplified implementation

### Code Files
The complete implementation is available in two main files:
1. `index.html`: Contains the web interface and JavaScript code
2. `README.md`: This documentation file

## Future Enhancements
Potential improvements that could be added:
1. Additional data cleaning options
2. Custom column mapping
3. Batch processing capabilities
4. Enhanced preview features
5. Excel format support (if needed)