import sqlite3


class AnalyticsReporter:
    def generate_monthly_report(self, start_date, end_date):
        # Mixing high-level reporting logic with low-level data retrieval and formatting
        
        # Direct database query (low-level)
        conn = sqlite3.connect('sales_database.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_id, 
                   SUM(quantity) as total_quantity, 
                   SUM(price * quantity) as total_revenue 
            FROM sales 
            WHERE sale_date BETWEEN ? AND ?
            GROUP BY product_id
        """, (start_date, end_date))
        
        sales_data = cursor.fetchall()
        conn.close()
        
        # Data transformation (mid-level)
        report = []
        for row in sales_data:
            product_details = self.fetch_product_details(row[0])  # Method call
            
            # Direct HTML generation (low-level presentation)
            html_row = f"""
            <tr>
                <td>{product_details['name']}</td>
                <td>{row[1]}</td>  # Total Quantity
                <td>${row[2]:.2f}</td>  # Total Revenue
                <td style='color: {"green" if row[2] > 1000 else "red"}'>
                    {self.calculate_performance_indicator(row[2])}
                </td>
            </tr>
            """
            report.append(html_row)
        
        # Directly writing to file (low-level I/O)
        with open('monthly_report.html', 'w') as file:
            file.write("<html><table>" + "".join(report) + "</table></html>")
        
        return True

    def fetch_product_details(self, product_id):
        # Another method with mixed abstraction levels
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, category FROM products WHERE id = ?", (product_id,))
        return dict(zip(['name', 'category'], cursor.fetchone()))

    def calculate_performance_indicator(self, revenue):
        # Business logic mixed with presentation logic
        if revenue > 5000:
            return "High Performance ⭐⭐⭐"
        elif revenue > 1000:
            return "Moderate Performance ⭐⭐"
        else:
            return "Low Performance ⭐"