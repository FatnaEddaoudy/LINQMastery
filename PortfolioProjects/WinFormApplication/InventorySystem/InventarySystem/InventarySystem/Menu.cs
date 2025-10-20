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
    public partial class Menu : Form
    {
        public Menu()
        {
            InitializeComponent();
            this.IsMdiContainer = true;
        }

        private void toolStripButton1_Click(object sender, EventArgs e)
        {
            ItemFrm child = new ItemFrm();
            child.MdiParent = this;  // Set the parent
            child.Show();
        }

        private void Menu_Load(object sender, EventArgs e)
        {

        }

        private void Menu_FormClosed(object sender, FormClosedEventArgs e)
        {
            Application.Exit();
        }

        private void toolStripButton7_Click(object sender, EventArgs e)
        {
            frmSettings child = new frmSettings();
            child.MdiParent = this;
            child.Show();
        }

        private void toolStripButton3_Click(object sender, EventArgs e)
        {

        }

        private void toolStripButton2_Click(object sender, EventArgs e)
        {
            frmStockout child = new frmStockout();
            child.MdiParent = this;
            child.Show();
        }
    }
}
