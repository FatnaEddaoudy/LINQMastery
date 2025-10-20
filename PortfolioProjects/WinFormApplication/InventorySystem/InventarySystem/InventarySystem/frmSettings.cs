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
    public partial class frmSettings : Form
    {
        public frmSettings()
        {
            InitializeComponent();
        }

        private void frmSettings_Load(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void btnLoadC_Click(object sender, EventArgs e)
        {
            try
            {
                var categroyList = SqlSetting.ExecuteQuery("select DESCRIPTION from settings where VALUE='Category' ", true);
                dgCategory.DataSource = categroyList;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }

        }

        private void btnLoadu_Click(object sender, EventArgs e)
        {
            try
            {
                var categroyList = SqlSetting.ExecuteQuery("select DESCRIPTION from settings where VALUE='Unit'", true);
                dgUnit.DataSource = categroyList;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }
        private void btnSaveC_Click(object sender, EventArgs e)
        {
            try
            {
                if (txtCategory.Text != "")
                {
                    var quey = SqlSetting.ExecuteQuery("select * from settings where DESCRIPTION='" + txtCategory.Text + "'", true);
                    if (quey.Rows.Count > 0)
                    {
                        MessageBox.Show("Category already exists");
                    }
                    else
                    {
                        SqlSetting.ExecuteQuery("insert into settings(DESCRIPTION,VALUE) values('" + txtCategory.Text + "','Category')", false);
                        MessageBox.Show("Category saved successfully");
                        var sql = "INSERT INTO autonumber (STRT,END_VAL,INCREMENT,DESCRIPTION)" + " VALUES ('" + txtCategory.Text.Substring(0, 1) + "0000" + "',1,1,'" + txtCategory.Text + "')";
                        SqlSetting.ExecuteQuery(sql, false);
                        btnLoadC_Click(sender, e);
                        txtCategory.Text = "";
                    }

                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void btnsaveU_Click(object sender, EventArgs e)
        {
            try
            {
                if (txtUnit.Text != "")
                {
                    var quey = SqlSetting.ExecuteQuery("select * from settings where DESCRIPTION='" + txtUnit.Text + "'", true);
                    if (quey.Rows.Count > 0)
                    {
                        MessageBox.Show("Unit item already exists");
                    }
                    else
                    {
                        SqlSetting.ExecuteQuery("insert into settings(DESCRIPTION,VALUE) values('" + txtUnit.Text + "','Unit')", false);
                        MessageBox.Show("Unit item saved successfully");
                        btnLoadu_Click(sender, e);
                        txtUnit.Text = "";
                    }

                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void btnUpdateC_Click(object sender, EventArgs e)
        {
            try
            {
                if (dgCategory.SelectedCells.Count > 0)
                {
                    var selectedRow = dgCategory.Rows[dgCategory.SelectedCells[0].RowIndex];
                    var currentValue = selectedRow.Cells["DESCRIPTION"].Value.ToString();
                    if (txtCategory.Text != "")
                    {
                        var quey = SqlSetting.ExecuteQuery("select * from settings where DESCRIPTION='" + txtCategory.Text + "'", true);
                        if (quey.Rows.Count > 0)
                        {
                            MessageBox.Show("Category already exists");
                        }
                        else
                        {
                            SqlSetting.ExecuteQuery("update settings set DESCRIPTION='" + txtCategory.Text + "' where DESCRIPTION='" + currentValue + "'", false);
                            MessageBox.Show("Category updated successfully");
                            btnLoadC_Click(sender, e);
                            txtCategory.Text = "";
                        }

                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }

        }

        private void btnUpdateU_Click(object sender, EventArgs e)
        {
            try
            {
                if (dgUnit.SelectedCells.Count > 0)
                {
                    var quey = SqlSetting.ExecuteQuery("select * from settings where DESCRIPTION='" + txtUnit.Text + "'", true);
                    if (quey.Rows.Count > 0)
                    {
                        MessageBox.Show("Unit item already exists");
                    }
                    else
                    {
                        var selectedRow = dgUnit.Rows[dgUnit.SelectedCells[0].RowIndex];
                        var currentValue = selectedRow.Cells["DESCRIPTION"].Value.ToString();
                        if (txtUnit.Text != "")
                        {

                            SqlSetting.ExecuteQuery("update settings set DESCRIPTION='" + txtUnit.Text + "' where DESCRIPTION='" + currentValue + "'", false);
                            MessageBox.Show("Unit item updated successfully");
                            btnLoadu_Click(sender, e);
                            txtUnit.Text = "";
                        }
                    }

                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }
        private void btnDeleteC_Click(object sender, EventArgs e)
        {
            try
            {
                if (dgCategory.SelectedCells.Count > 0)
                {
                    var selectedRow = dgCategory.Rows[dgCategory.SelectedCells[0].RowIndex];
                    var currentValue = selectedRow.Cells["DESCRIPTION"].Value.ToString();
                    var confirmResult = MessageBox.Show("Are you sure to delete this item: " + currentValue + " ?", "Confirm Delete!", MessageBoxButtons.YesNo);
                    if (confirmResult == DialogResult.Yes)
                    {
                        SqlSetting.ExecuteQuery("delete from settings where DESCRIPTION='" + currentValue + "'", false);
                        MessageBox.Show("Category deleted successfully");
                        btnLoadC_Click(sender, e);
                        txtCategory.Text = "";
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);

            }
        }

        private void btnDeleteU_Click(object sender, EventArgs e)
        {
            if (dgUnit.SelectedCells.Count > 0)
            {
                var selectedRow = dgUnit.Rows[dgUnit.SelectedCells[0].RowIndex];
                var currentValue = selectedRow.Cells["DESCRIPTION"].Value.ToString();
                var confirmResult = MessageBox.Show("Are you sure to delete this item: " + currentValue + " ?", "Confirm Delete!", MessageBoxButtons.YesNo);
                if (confirmResult == DialogResult.Yes)
                {
                    SqlSetting.ExecuteQuery("delete from settings where DESCRIPTION='" + currentValue + "'", false);
                    MessageBox.Show("Unit item deleted successfully");
                    btnLoadu_Click(sender, e);
                    txtUnit.Text = "";
                }
            }
        }

        private void dgCategory_Click(object sender, EventArgs e)
        {
            try
            {
                if (dgCategory.SelectedCells.Count > 0)
                {
                    var selectedRow = dgCategory.Rows[dgCategory.SelectedCells[0].RowIndex];
                    var currentValue = selectedRow.Cells["DESCRIPTION"].Value.ToString();
                    txtCategory.Text = currentValue;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }
        private void dgUnit_Click(object sender, EventArgs e)
        {
            try
            {
                if (dgUnit.SelectedCells.Count > 0)
                {
                    var selectedRow = dgUnit.Rows[dgUnit.SelectedCells[0].RowIndex];
                    var currentValue = selectedRow.Cells["DESCRIPTION"].Value.ToString();
                    txtUnit.Text = currentValue;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }
    }
}
