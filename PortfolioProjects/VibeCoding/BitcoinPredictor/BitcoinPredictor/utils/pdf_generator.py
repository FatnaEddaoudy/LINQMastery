from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def create_prediction_pdf(predictions_data, current_price, forecast_type="Next Day"):
    """Generate PDF report for predictions
    
    Args:
        predictions_data: Dictionary with model predictions
        current_price: Current Bitcoin price
        forecast_type: Type of prediction (Next Day, Multi-Day, Backtest)
    """
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2ca02c'),
        spaceAfter=12
    )
    
    # Title
    title = Paragraph("₿ Bitcoin Price Prediction Report", title_style)
    elements.append(title)
    
    # Report metadata
    report_date = datetime.now().strftime("%B %d, %Y %H:%M:%S")
    metadata = Paragraph(f"<b>Report Generated:</b> {report_date}<br/><b>Forecast Type:</b> {forecast_type}", styles['Normal'])
    elements.append(metadata)
    elements.append(Spacer(1, 20))
    
    # Current Price Section
    current_section = Paragraph("Current Market Status", heading_style)
    elements.append(current_section)
    
    current_data = [
        ['Current Bitcoin Price', f'${current_price:,.2f}'],
        ['Report Type', forecast_type],
        ['Number of Models', str(len(predictions_data))]
    ]
    
    current_table = Table(current_data, colWidths=[3*inch, 3*inch])
    current_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(current_table)
    elements.append(Spacer(1, 20))
    
    # Predictions Section
    pred_section = Paragraph("Model Predictions", heading_style)
    elements.append(pred_section)
    
    # Create predictions table
    pred_table_data = [['Model', 'Predicted Price', 'Change ($)', 'Change (%)', 'Trend']]
    
    for model_name, pred_price in predictions_data.items():
        change = pred_price - current_price
        change_pct = (change / current_price) * 100
        trend = '↑ Bullish' if change > 0 else '↓ Bearish' if change < 0 else '→ Neutral'
        
        pred_table_data.append([
            model_name,
            f'${pred_price:,.2f}',
            f'${change:+,.2f}',
            f'{change_pct:+.2f}%',
            trend
        ])
    
    pred_table = Table(pred_table_data, colWidths=[1.5*inch, 1.5*inch, 1.2*inch, 1.2*inch, 1.1*inch])
    pred_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    
    elements.append(pred_table)
    elements.append(Spacer(1, 20))
    
    # Summary Statistics
    if len(predictions_data) > 1:
        summary_section = Paragraph("Summary Statistics", heading_style)
        elements.append(summary_section)
        
        prices = list(predictions_data.values())
        avg_pred = sum(prices) / len(prices)
        max_pred = max(prices)
        min_pred = min(prices)
        
        summary_data = [
            ['Average Prediction', f'${avg_pred:,.2f}'],
            ['Highest Prediction', f'${max_pred:,.2f}'],
            ['Lowest Prediction', f'${min_pred:,.2f}'],
            ['Prediction Range', f'${max_pred - min_pred:,.2f}'],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e6f3ff')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(summary_table)
    
    elements.append(Spacer(1, 20))
    
    # Disclaimer
    disclaimer_text = """
    <b>Disclaimer:</b> This report is generated for informational purposes only. 
    Cryptocurrency markets are highly volatile and unpredictable. Past performance 
    does not guarantee future results. These predictions are based on machine learning 
    models and should not be considered as financial advice. Always do your own research 
    and consult with a qualified financial advisor before making investment decisions.
    """
    disclaimer = Paragraph(disclaimer_text, styles['Normal'])
    elements.append(disclaimer)
    
    # Build PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer

def create_forecast_pdf(forecast_data, current_price, forecast_days):
    """Generate PDF report for multi-day forecast
    
    Args:
        forecast_data: Dictionary with dates and forecasts from multiple models
        current_price: Current Bitcoin price
        forecast_days: Number of days forecasted
    """
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Title
    title = Paragraph(f"₿ Bitcoin {forecast_days}-Day Forecast Report", title_style)
    elements.append(title)
    
    # Metadata
    report_date = datetime.now().strftime("%B %d, %Y %H:%M:%S")
    metadata = Paragraph(f"<b>Report Generated:</b> {report_date}<br/><b>Current Price:</b> ${current_price:,.2f}", styles['Normal'])
    elements.append(metadata)
    elements.append(Spacer(1, 20))
    
    # Forecast summary table (first few days)
    heading = Paragraph("Forecast Preview (First 7 Days)", styles['Heading2'])
    elements.append(heading)
    
    # Create sample forecast table
    preview_note = Paragraph("Download the full CSV report for complete forecast data.", styles['Normal'])
    elements.append(preview_note)
    elements.append(Spacer(1, 20))
    
    # Final forecast summary
    heading2 = Paragraph(f"Final Forecast (Day {forecast_days})", styles['Heading2'])
    elements.append(heading2)
    
    final_data = [['Model', 'Final Predicted Price', 'Total Change (%)']]
    
    for model_name, values in forecast_data.items():
        if len(values) > 0:
            final_price = values[-1]
            total_change = ((final_price - current_price) / current_price) * 100
            final_data.append([
                model_name,
                f'${final_price:,.2f}',
                f'{total_change:+.2f}%'
            ])
    
    final_table = Table(final_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
    final_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ca02c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    
    elements.append(final_table)
    elements.append(Spacer(1, 20))
    
    # Disclaimer
    disclaimer_text = """
    <b>Disclaimer:</b> Long-term cryptocurrency forecasts are highly speculative. 
    Market conditions can change rapidly. This forecast is for educational purposes only.
    """
    disclaimer = Paragraph(disclaimer_text, styles['Normal'])
    elements.append(disclaimer)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
