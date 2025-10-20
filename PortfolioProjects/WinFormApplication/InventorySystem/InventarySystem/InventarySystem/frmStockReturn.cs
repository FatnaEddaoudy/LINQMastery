using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Net.Mime.MediaTypeNames;

namespace InventarySystem
{
    public partial class frmStockout : Form
    {
        public frmStockout()
        {
            InitializeComponent();
        }

        private void groupBox2_Enter(object sender, EventArgs e)
        {

        }

        private void button4_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {

            try
            {
                // 1️⃣ Get the transaction number
                var sql = SqlSetting.ExecuteQuery("SELECT concat(STRT, END_VAL) as TRANSACTIONNUMBER FROM autonumber WHERE ID = 5", true);
                string stockID = sql.Rows[0]["TRANSACTIONNUMBER"].ToString();

                // 2️⃣ Validate customer and items
                if (string.IsNullOrWhiteSpace(txtcustomerId.Text))
                {
                    MessageBox.Show("There are empty fields left that must be filled!", "Invalid", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
                    return;
                }
                var querycustomID = SqlSetting.ExecuteQuery($@"SELECT * FROM person WHERE SUPLIERCUSTOMERID='{txtcustomerId.Text}' AND TYPE='Customer'", true);
                if (querycustomID.Rows.Count == 0)
                {
                    MessageBox.Show("Customer ID does not exist.", "Invalid", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
                    return;
                }
                if (dgstockout.Rows.Count == 0)
                {
                    MessageBox.Show("No items to save.");
                    return;
                }

                // 3️⃣ Get available quantities from DB
                DataTable dataTable = SqlSetting.ExecuteQuery("SELECT ITEMID, QTY FROM items", true);

                foreach (DataRow dbRow in dataTable.Rows)
                {
                    foreach (DataGridViewRow gridRow in dgstockout.Rows)
                    {
                        if (gridRow.IsNewRow) continue;

                        string itemId = gridRow.Cells[0].Value?.ToString();
                        if (itemId == dbRow["ITEMID"].ToString())
                        {
                            int availableQty = Convert.ToInt32(dbRow["QTY"]);
                            int selectedQty = Convert.ToInt32(gridRow.Cells[5].Value);

                            if (selectedQty > availableQty)
                            {
                                MessageBox.Show($"The quantity for item ({gridRow.Cells[1].Value}) exceeds the available stock.",
                                    "Invalid", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
                                return;
                            }
                        }

                        if (string.IsNullOrWhiteSpace(gridRow.Cells[4].Value?.ToString()))
                        {
                            MessageBox.Show("Set your purpose.", "Invalid", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
                            return;
                        }
                    }
                }

                // 4️⃣ Insert into stock_in_out + update items + log transaction
                foreach (DataGridViewRow row in dgstockout.Rows)
                {
                    if (row.IsNewRow) continue;

                    string itemId = row.Cells[0].Value?.ToString();
                    string qty = row.Cells[5].Value?.ToString();
                    string total = row.Cells[4].Value?.ToString();

                    string query = $@"
                INSERT INTO stock_in_out 
                (TRANSACTIONNUMBER, ITEMID, TRANSACTIONDATE, QTY, TOTALPRICE, SUPLIERCUSTOMERID, REMARKS)
                VALUES ('{stockID}', '{itemId}', '{DateTime.Now:yyyy-MM-dd}', '{qty}', '{total}', '{txtcustomerId.Text}', 'StockOut')";

                    SqlSetting.ExecuteQuery(query, false);

                    string updateQty = $"UPDATE items SET QTY = QTY - '{qty}' WHERE ITEMID = '{itemId}'";
                    SqlSetting.ExecuteQuery(updateQty, false);
                }

                // 5️⃣ Insert transaction header
                string transactionQuery = $@"
            INSERT INTO transaction_log (TRANSACTIONNUMBER, TRANSACTIONDATE, TYPE, SUPLIERCUSTOMERID)
            VALUES ('{stockID}', '{DateTime.Now:yyyy-MM-dd}', 'StockOut', '{txtcustomerId.Text}')";
                SqlSetting.ExecuteQuery(transactionQuery, false);

                // 6️⃣ Update autonumber once
                string updateAutonumber = @"UPDATE autonumber  SET STRT = SUBSTRING(STRT, 1, 1)
                + RIGHT('0000' + CAST(TRY_CAST(SUBSTRING(STRT, 2, LEN(STRT)) AS INT) + 1 AS VARCHAR(20)), 4) WHERE ID = 5; ";
                SqlSetting.ExecuteQuery(updateAutonumber, false);

                // 7️⃣ Notify and clear grid
                MessageBox.Show("Item(s) have been saved successfully.", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                dgstockout.Rows.Clear();
                frmStockReturn_Load(sender, e);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message, "Exception", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void frmStockReturn_Load(object sender, EventArgs e)
        {
            var sql = SqlSetting.ExecuteQuery("select * from person where type='Customer'", true);
            var items = SqlSetting.ExecuteQuery("select * from items", true);
            DgItems.DataSource = items;

        }

        private void txtcustomerId_TextChanged(object sender, EventArgs e)
        {
            string input = txtcustomerId.Text.Trim();

            // Build SQL safely (no quotes inside)
            string query = $@"
        SELECT TOP(1) *
        FROM person
        WHERE type = 'Customer'
        AND SUPLIERCUSTOMERID LIKE '{input.Replace("'", "''")}%'";

            // Call your SqlSetting as before
            var sql = SqlSetting.ExecuteQuery(query, true);

            if (sql.Rows.Count > 0)
            {
                txtFirstName.Text = sql.Rows[0]["FIRSTNAME"].ToString();
                txtLastName.Text = sql.Rows[0]["LASTNAME"].ToString();
            }
            else
            {
                txtFirstName.Text = "";
                txtLastName.Text = "";
            }
        }
        private void dgstockout_CellEndEdit(object sender, DataGridViewCellEventArgs e)
        {
            if (dgstockout.Columns[e.ColumnIndex].Name == "QTY")
            {
                var currentRow = dgstockout.Rows[e.RowIndex];
                string itemId = currentRow.Cells["ITEMID"].Value?.ToString();
                string qtyText = currentRow.Cells["QTY"].Value?.ToString();

                if (string.IsNullOrEmpty(itemId) || string.IsNullOrEmpty(qtyText))
                    return;

                if (!int.TryParse(qtyText, out int newQty) || newQty <= 0)
                {
                    MessageBox.Show("Please enter a valid positive quantity.");
                    currentRow.Cells["QTY"].Value = 1;
                    return;
                }

                // Find the matching item in DgItems (your stock list)
                var stockRow = DgItems.Rows
                    .Cast<DataGridViewRow>()
                    .FirstOrDefault(r => r.Cells["ITEMID"].Value?.ToString() == itemId);

                if (stockRow != null)
                {
                    int availableQty = Convert.ToInt32(stockRow.Cells["QTY"].Value);

                    if (newQty > availableQty)
                    {
                        MessageBox.Show($"Not enough stock! Available: {availableQty}");
                        currentRow.Cells["QTY"].Value = availableQty; // Reset to max available
                    }
                }

            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            foreach (DataGridViewRow row in dgstockout.SelectedRows)
            {
                if (!row.IsNewRow)
                    dgstockout.Rows.Remove(row);
            }
        }

        private void DgItems_DoubleClick(object sender, EventArgs e)
        {
            if (DgItems.CurrentRow == null)
            {
                MessageBox.Show("Please select an item first.");
                return;
            }

            // Ensure dgstockout is not null and has columns
            if (dgstockout.Columns.Count == 0)
            {
                dgstockout.AutoGenerateColumns = false;
                dgstockout.Columns.Add("ITEMID", "Item ID");
                dgstockout.Columns.Add("NAME", "Name");
                dgstockout.Columns.Add("DESCRIPTION", "Description");
                dgstockout.Columns.Add("TYPE", "Type");
                dgstockout.Columns.Add("PRICE", "Price");
                dgstockout.Columns.Add("QTY", "Quantity");
                dgstockout.Columns.Add("UNIT", "Unit");
            }

            dgstockout.Rows.Add(new object[]
            {
        DgItems.CurrentRow.Cells["ITEMID"]?.Value?.ToString() ?? "",
        DgItems.CurrentRow.Cells["NAME"]?.Value?.ToString() ?? "",
        DgItems.CurrentRow.Cells["DESCRIPTION"]?.Value?.ToString() ?? "",
        DgItems.CurrentRow.Cells["TYPE"]?.Value?.ToString() ?? "",
        DgItems.CurrentRow.Cells["PRICE"]?.Value?.ToString() ?? "",
        DgItems.CurrentRow.Cells["QTY"]?.Value?.ToString() ?? "",
        DgItems.CurrentRow.Cells["UNIT"]?.Value?.ToString() ?? ""
            });

        }

        private void button3_Click(object sender, EventArgs e)
        {
            foreach (DataGridViewRow row in dgstockout.SelectedRows)
            {
                if (!row.IsNewRow)
                    dgstockout.Rows.Remove(row);
            }

            txtcustomerId.Text = "";
            txtFirstName.Text = "";
            txtLastName.Text = "";
        }
    }
}
