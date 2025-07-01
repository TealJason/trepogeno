   
def style_html(html_path):
 # Inject filter UI and JS into the HTML file
    filter_html = """
    <label for="supportFilter">Filter by Total support (≥ %): </label>
    <input type="number" id="supportFilter" value="0" min="0" max="100" step="1" />
    <button onclick="filterTable()">Apply Filter</button>

    <script>
    function filterTable() {
        const input = document.getElementById("supportFilter");
        const filter = parseFloat(input.value) || 0;
        const table = document.querySelector("table");
        const rows = table.querySelectorAll("tbody tr");

        rows.forEach(row => {
            const supportCell = row.cells[4];  // 5th column: Total support
            const supportValue = parseFloat(supportCell.textContent);
            if (supportValue >= filter) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    }
    </script>
    """

    # Read the saved HTML file
    with open(html_path, 'r') as file:
        html_content = file.read()

    # Insert the filter UI before </body> or at the end if no </body> tag
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', filter_html + '</body>')
    else:
        html_content += filter_html

    # Write back the updated HTML
    with open(html_path, 'w') as file:
        file.write(html_content)