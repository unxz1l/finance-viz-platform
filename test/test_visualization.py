import pytest
import pandas as pd
import plotly.graph_objects as go
from finance_analyzer.visualization.plotter import FinancialPlotter

@pytest.fixture
def sample_data():
    """Create sample financial data for testing."""
    return pd.DataFrame({
        'ROE': [10.5, 11.2, 12.1, 11.8],
        'Operating_Margin': [15.2, 16.1, 15.8, 16.5],
        'Debt_Ratio': [45.3, 44.8, 43.9, 44.2],
        'Revenue_Growth': [8.5, 9.2, 8.8, 9.5]
    }, index=pd.date_range('2020-01-01', periods=4, freq='Y'))

def test_create_metric_bar_chart(sample_data):
    """Test bar chart creation."""
    fig = FinancialPlotter.create_metric_bar_chart(sample_data, 'ROE')
    
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    assert fig.data[0].type == 'bar'
    assert len(fig.data[0].x) == len(sample_data)
    assert len(fig.data[0].y) == len(sample_data)
    assert fig.layout.title.text == 'ROE Trend'

def test_create_metric_line_chart(sample_data):
    """Test line chart creation."""
    fig = FinancialPlotter.create_metric_line_chart(sample_data, 'Operating_Margin')
    
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    assert fig.data[0].type == 'scatter'
    assert len(fig.data[0].x) == len(sample_data)
    assert len(fig.data[0].y) == len(sample_data)
    assert fig.layout.title.text == 'Operating Margin Trend'

def test_create_multi_metric_chart(sample_data):
    """Test multi-metric chart creation."""
    metrics = ['ROE', 'Operating_Margin']
    fig = FinancialPlotter.create_multi_metric_chart(sample_data, metrics)
    
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == len(metrics)
    for trace in fig.data:
        assert trace.type == 'scatter'
        assert len(trace.x) == len(sample_data)
        assert len(trace.y) == len(sample_data)
    assert fig.layout.title.text == 'Financial Metrics Comparison'

def test_error_handling():
    """Test error handling in visualization."""
    empty_df = pd.DataFrame()
    invalid_metric = 'InvalidMetric'
    
    with pytest.raises(ValueError):
        FinancialPlotter.create_metric_bar_chart(empty_df, 'ROE')
    
    sample_data = pd.DataFrame({'ValidMetric': [1, 2, 3]})
    with pytest.raises(KeyError):
        FinancialPlotter.create_metric_bar_chart(sample_data, invalid_metric)

def test_chart_customization(sample_data):
    """Test chart customization options."""
    custom_title = 'Custom Chart Title'
    custom_color = 'rgb(55, 83, 109)'
    
    fig = FinancialPlotter.create_metric_bar_chart(
        sample_data,
        'ROE',
        title=custom_title,
        color=custom_color
    )
    
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == custom_title
    assert fig.data[0].marker.color == custom_color 