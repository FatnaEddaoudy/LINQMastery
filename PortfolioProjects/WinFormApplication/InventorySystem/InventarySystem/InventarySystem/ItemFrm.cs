using Microsoft.VisualBasic.Devices;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace InventarySystem
{
    public partial class ItemFrm : Form
    {
        public ItemFrm()
        {
            InitializeComponent();
        }

        int currentPage = 1;
        int pageSize = 5; // aantal rijen per pagina
        DataTable allItems;
        private void ItemFrm_Load(object sender, EventArgs e)
        {
            try
            {
                SqlSetting.MakeButtonsRounded(this, 20);
                allItems = SqlSetting.ExecuteQuery("SELECT * FROM Items", true);

                ShowPage(currentPage);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error loading data: " + ex.Message);
            }
            try
            {
                DataTable unitList = SqlSetting.ExecuteQuery("SELECT DISTINCT UNIT FROM Items", true);
                cbunit.DataSource = unitList;
                cbunit.DisplayMember = "UNIT";
                cbunit.ValueMember = "UNIT";
                if (cbunit.Items.Count > 0)
                {
                    cbunit.SelectedIndex = 0;
                }
                DataTable catgeorylist = SqlSetting.ExecuteQuery("SELECT * FROM settings", true);
                cbCategroy.DataSource = catgeorylist;
                cbCategroy.DisplayMember = "DESCRIPTION";
                cbCategroy.ValueMember = "ID";
                if (cbCategroy.Items.Count > 0)
                {
                    cbCategroy.SelectedIndex = 0;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message);
            }
        }

        private void dgrid_Click(object sender, EventArgs e)
        {
            if (dgrid.CurrentRow != null)
            {
                txtid.Text = dgrid.CurrentRow.Cells["ITEMID"].Value.ToString();
                txtname.Text = dgrid.CurrentRow.Cells["Name"].Value.ToString();
                txtdesc.Text = dgrid.CurrentRow.Cells["Description"].Value.ToString();
                cbCategroy.Text = dgrid.CurrentRow.Cells["TYPE"].Value.ToString();
                txtprice.Text = dgrid.CurrentRow.Cells["Price"].Value.ToString();
                txtqty.Text = dgrid.CurrentRow.Cells["QTY"].Value.ToString();
                cbunit.Text = dgrid.CurrentRow.Cells["UNIT"].Value.ToString();
            }
        }

        private void textBox4_TextChanged(object sender, EventArgs e)
        {
            DataView dv = ((DataTable)dgrid.DataSource).DefaultView;
            dv.RowFilter = $"Name LIKE '%{textsearch.Text}%'";

        }

        private void ShowPage(int page)
        {
            DataTable pagedTable = SqlSetting.GetPage(allItems, pageSize, page);
            dgrid.DataSource = pagedTable;

            // kolomnamen aanpassen
            if (dgrid.Columns.Contains("ITEMID"))
                dgrid.Columns["ITEMID"].HeaderText = "ID";
            if (dgrid.Columns.Contains("Name"))
                dgrid.Columns["Name"].HeaderText = "NAME";
            if (dgrid.Columns.Contains("Description"))
                dgrid.Columns["Description"].HeaderText = "DESCRIPTION";
            if (dgrid.Columns.Contains("TYPE"))
                dgrid.Columns["TYPE"].HeaderText = "TYPE";
            if (dgrid.Columns.Contains("Price"))
                dgrid.Columns["Price"].HeaderText = "PRICE";
            if (dgrid.Columns.Contains("QTY"))
                dgrid.Columns["QTY"].HeaderText = "Stock";
            if (dgrid.Columns.Contains("UNIT"))
                dgrid.Columns["UNIT"].HeaderText = "UNIT";

            lblPage.Text = $"Page {currentPage} / {Math.Ceiling((double)allItems.Rows.Count / pageSize)}";
        }


        private void btnFirst_Click(object sender, EventArgs e)
        {
            currentPage = 1;
            ShowPage(currentPage);
        }

        private void btnLast_Click(object sender, EventArgs e)
        {
            DataTable dt = SqlSetting.ExecuteQuery("SELECT * FROM Items", true);
            currentPage = (int)Math.Ceiling((double)dt.Rows.Count / pageSize);
            ShowPage(currentPage);
        }

        private void btnPrev_Click(object sender, EventArgs e)
        {
            if (currentPage > 1)
            {
                currentPage--;
                ShowPage(currentPage);
            }
        }

        private void btnnext_Click(object sender, EventArgs e)
        {
            int totalPages = (int)Math.Ceiling((double)allItems.Rows.Count / pageSize);
            if (currentPage < totalPages)
            {
                currentPage++;
                ShowPage(currentPage);
            }
        }

        private void button4_Click(object sender, EventArgs e)
        {
            txtid.Text = "";
            txtname.Text = "";
            txtdesc.Text = "";
            txtprice.Text = "";
            txtqty.Text = "";

        }

        private void button9_Click(object sender, EventArgs e)
        {
            this.Close();
        }
        private void button1_Click(object sender, EventArgs e)
        {
            if (txtname.Text == "" || txtdesc.Text == "" || txtprice.Text == "" || txtqty.Text == "")
            {
                MessageBox.Show("Please fill in all required fields.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }
            try
            {
                string selectedUnit = (cbCategroy.Text);
                string newItemID = SqlSetting.GenerateItemID(selectedUnit);
                txtid.Text = newItemID;
                string query =
                    "INSERT INTO Items (ITEMID,Name, Description, [TYPE], Price, QTY, UNIT) VALUES (" +
                    $"'{newItemID}', " +
                    $"'{txtname.Text.Replace("'", "''")}', " +
                    $"'{txtdesc.Text.Replace("'", "''")}', " +
                    $"'{cbCategroy.Text.Replace("'", "''")}', " +
                    $"{decimal.Parse(txtprice.Text)}, " +
                    $"{int.Parse(txtqty.Text)}, " +
                    $"'{cbunit.Text.Replace("'", "''")}')";
                DataTable dataTable = SqlSetting.ExecuteQuery(query, false);
                MessageBox.Show("Item added successfully.", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                ItemFrm_Load(sender, e);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }

        }

        private void button2_Click(object sender, EventArgs e)
        {
            if (txtid.Text == "")
            {
                MessageBox.Show("Please select an item to update.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }
            var query = $"UPDATE Items SET " +
                $"NAME='{txtname.Text}', " +
                $"DESCRIPTION='{txtdesc.Text}', " +
                $"TYPE='{cbCategroy.Text}', " +
                $"PRICE={decimal.Parse(txtprice.Text)}, " +
                $"QTY={Convert.ToDecimal(txtqty.Text)}, " +
                $"UNIT='{cbunit.Text}' " +
                $"WHERE ITEMID='{txtid.Text}'";
            try
            {   
                SqlSetting.ExecuteQuery(query, false);
                MessageBox.Show("Item updated successfully.", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                ItemFrm_Load(sender, e);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }

        }

        private void button3_Click(object sender, EventArgs e)
        {
            if(txtid.Text != "")
            {
                var query = $"DELETE FROM Items WHERE ITEMID='{txtid.Text}'";
                try
                {
                    SqlSetting.ExecuteQuery(query, false);
                    MessageBox.Show("Item deleted successfully.", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    ItemFrm_Load(sender, e);
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Error: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }

            }
            else
            {
                MessageBox.Show("Please select an item to delete.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }
    }
}
