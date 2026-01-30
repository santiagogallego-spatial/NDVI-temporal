import os
from fpdf import FPDF

class AgriReport(FPDF):
    def header(self):
        if self.page_no() == 1:
            self.set_font('Arial', 'B', 15)
            self.set_text_color(34, 139, 34)
            self.cell(0, 10, 'AGRICULTURAL INTELLIGENCE REPORT: HAMILTON, IA', 0, 1, 'C')
            self.set_draw_color(34, 139, 34)
            self.line(10, 22, 200, 22)
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Satellite Precision Analysis 2023 - Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, label, 0, 1, 'L', fill=True)
        self.ln(4)

    def chapter_body(self, text):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 7, text)
        self.ln(2)

def generate():
    pdf = AgriReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # --- PAGE 1: INTRODUCTION & HISTORY ---
    pdf.chapter_title('1. Executive Summary & Methodology')
    pdf.chapter_body(
        "This technical report presents the results of the biophysical monitoring conducted in Hamilton County, Iowa, "
        "during the 2023 agricultural cycle. Multi-spectral reflectance data from the Sentinel-2 mission (10m resolution) "
        "were integrated with climate variables from the ERA5-Land model (9km). The primary objective was to quantify crop "
        "resilience against soil moisture fluctuations in the topsoil layer (0-7 cm)."
    )

    pdf.chapter_title('2. Historical Climate Context (Decade Review)')
    pdf.chapter_body(
        "To understand the 2023 performance, we analyzed the last 10 years of soil moisture data. "
        "This context allows us to identify if the current season faced extreme drought or average conditions "
        "relative to the regional baseline, ensuring that current observations are statistically grounded "
        "and not merely seasonal anomalies."
    )

    if os.path.exists('outputs/diagnostico_iowa_10y.png'):
        pdf.image('outputs/diagnostico_iowa_10y.png', x=35, w=140)
        pdf.set_font('Arial', 'I', 9)
        pdf.cell(0, 10, 'Figure 1: Long-term soil moisture trends and 2023 seasonal deviation.', 0, 1, 'C')
        pdf.ln(5)

    # --- PAGE 2: VEGETATION RESPONSE & STATS ---
    pdf.add_page()
    pdf.chapter_title('3. Vegetation Response & Soil Moisture (2023)')
    pdf.chapter_body(
        "The following analysis focuses on the 2023 growing season. By overlapping the NDVI (Biomass) "
        "with the Soil Moisture availability, we can observe the 'Mirror Effect': how the plant "
        "actively depletes soil water to drive photosynthesis and growth. This synchronization "
        "is a key indicator of metabolic efficiency in high-yield corn belts."
    )

    if os.path.exists('outputs/correlation_ndvi_climate.png'):
        pdf.image('outputs/correlation_ndvi_climate.png', x=35, w=140)
        pdf.set_font('Arial', 'I', 9)
        pdf.cell(0, 10, 'Figure 2: Temporal synchronization between NDVI (Vigor) and water availability.', 0, 1, 'C')
        pdf.ln(5)

    pdf.chapter_title('4. Statistical Biophysical Correlation')
    pdf.chapter_body(
        "Applying a Pearson correlation engine, we identified an extremely strong inverse relationship (r = -0.915). "
        "This indicates that biomass development is not random but intrinsically linked to water extraction "
        "dynamics from the soil profile. The negative slope confirms the active evapotranspiration process."
    )

    if os.path.exists('outputs/scatter_correlation.png'):
        pdf.image('outputs/scatter_correlation.png', x=50, w=110)
        pdf.set_font('Arial', 'I', 9)
        pdf.cell(0, 10, 'Figure 3: Linear regression analysis demonstrating a high R-Squared confidence.', 0, 1, 'C')
        pdf.ln(5)

    # --- PAGE 3: METRICS, MAP & CONCLUSIONS ---
    pdf.add_page()
    pdf.chapter_title('5. Precision Metrics Diagnosis')
    
    # Metrics Table
    pdf.set_x(45)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(60, 10, 'Statistical Metric', 1, 0, 'C', fill=True)
    pdf.cell(60, 10, 'Value Obtained', 1, 1, 'C', fill=True)
    
    pdf.set_font('Arial', '', 10)
    metrics = [
        ("Pearson Coefficient (r)", "-0.915"),
        ("Explained Variance (R2)", "83.7%"),
        ("Significance (p-value)", "0.00388 (Highly Significant)")
    ]
    for m, v in metrics:
        pdf.set_x(45); pdf.cell(60, 10, m, 1); pdf.cell(60, 10, v, 1, 1, 'C')
    
    pdf.ln(5)
    pdf.chapter_body(
        "The R-squared coefficient of 83.7% suggests that the vast majority of NDVI variability can be explained "
        "solely by soil moisture dynamics. The p-value below 0.01 grants robust scientific validity to the analysis, "
        "allowing the rejection of coincidental correlations."
    )

    pdf.chapter_title('6. Spatial Water Sensitivity Map')
    if os.path.exists('outputs/spatial_correlation_map.png'):
        pdf.image('outputs/spatial_correlation_map.png', x=40, w=130)
        pdf.set_font('Arial', 'I', 9)
        pdf.cell(0, 10, 'Figure 4: Pixel-level sensitivity map (10m resolution) for precision management.', 0, 1, 'C')
        pdf.ln(5)

    pdf.chapter_body(
        "This map identifies micro-zones with different water-holding capacities. High positive values "
        "indicate areas where the crop is most efficient at converting water into biomass."
    )

    pdf.chapter_title('7. Conclusions & Recommendations')
    conclusions = (
        "1. High Efficiency: The Hamilton crop displays a healthy and aggressive water metabolism, optimizing the soil-plant-atmosphere continuum.\n\n"
        "2. Resilience: Despite seasonal moisture fluctuations, the NDVI remained at optimal levels (0.5+), suggesting high genetic performance.\n\n"
        "3. Recommendation: Investigate low-correlation areas identified in Figure 4, as they may indicate soil compaction or sub-optimal root development."
    )
    pdf.chapter_body(conclusions)

    pdf.output('outputs/Final_Report_Hamilton_Professional.pdf')
    print("🏆 FULL TECHNICAL REPORT GENERATED! All detailed explanations restored.")

if __name__ == "__main__":
    generate()