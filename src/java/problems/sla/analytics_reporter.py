import sqlite3


class AnalyticsReporter:
    def generate_monthly_report(self, start_date, end_date):
        """
        Generates a monthly sales report for the given date range.
        This method retrieves sales data from a database, transforms the data,
        generates an HTML report, and writes it to a file.
        Args:
            start_date (str): The start date for the report in 'YYYY-MM-DD' format.
            end_date (str): The end date for the report in 'YYYY-MM-DD' format.
        Returns:
            bool: True if the report was generated successfully.
        Raises:
            sqlite3.DatabaseError: If there is an error connecting to or querying the database.
            IOError: If there is an error writing the report to a file.
        """
        
        # get quantity and revenue for each product
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
        
        report = []
        for row in sales_data:
            # get product detailed from database
            product_details = self.fetch_product_details(row[0])  # Method call
            
            # generate html row for the product
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
        
        # generate report by concatenating all rows and write to a file
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