namespace InventarySystem
{
    partial class ItemFrm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            btnSave = new Button();
            btnUpdate = new Button();
            btnDelete = new Button();
            btnReset = new Button();
            btnFirst = new Button();
            btnPrev = new Button();
            btnnext = new Button();
            btnLast = new Button();
            label1 = new Label();
            label2 = new Label();
            label3 = new Label();
            label4 = new Label();
            label5 = new Label();
            label6 = new Label();
            label7 = new Label();
            txtid = new TextBox();
            txtname = new TextBox();
            txtprice = new TextBox();
            txtqty = new TextBox();
            txtdesc = new RichTextBox();
            cbCategroy = new ComboBox();
            panel1 = new Panel();
            lblPage = new Label();
            textsearch = new TextBox();
            dgrid = new DataGridView();
            cbunit = new ComboBox();
            btnClose = new Button();
            panel2 = new Panel();
            panel1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)dgrid).BeginInit();
            panel2.SuspendLayout();
            SuspendLayout();
            // 
            // btnSave
            // 
            btnSave.BackColor = Color.FromArgb(191, 87, 0);
            btnSave.Font = new Font("MS Reference Sans Serif", 9F, FontStyle.Bold);
            btnSave.Location = new Point(47, 16);
            btnSave.Name = "btnSave";
            btnSave.Size = new Size(94, 29);
            btnSave.TabIndex = 0;
            btnSave.Text = "Save";
            btnSave.UseVisualStyleBackColor = false;
            btnSave.Click += button1_Click;
            // 
            // btnUpdate
            // 
            btnUpdate.BackColor = Color.FromArgb(191, 87, 0);
            btnUpdate.Font = new Font("MS Reference Sans Serif", 9F, FontStyle.Bold);
            btnUpdate.Location = new Point(169, 16);
            btnUpdate.Name = "btnUpdate";
            btnUpdate.Size = new Size(94, 29);
            btnUpdate.TabIndex = 1;
            btnUpdate.Text = "Update";
            btnUpdate.UseVisualStyleBackColor = false;
            btnUpdate.Click += button2_Click;
            // 
            // btnDelete
            // 
            btnDelete.BackColor = Color.FromArgb(191, 87, 0);
            btnDelete.Font = new Font("MS Reference Sans Serif", 9F, FontStyle.Bold);
            btnDelete.Location = new Point(283, 16);
            btnDelete.Name = "btnDelete";
            btnDelete.Size = new Size(94, 29);
            btnDelete.TabIndex = 2;
            btnDelete.Text = "Delete";
            btnDelete.UseVisualStyleBackColor = false;
            btnDelete.Click += button3_Click;
            // 
            // btnReset
            // 
            btnReset.BackColor = Color.FromArgb(191, 87, 0);
            btnReset.Font = new Font("MS Reference Sans Serif", 9F, FontStyle.Bold);
            btnReset.Location = new Point(392, 16);
            btnReset.Name = "btnReset";
            btnReset.Size = new Size(94, 29);
            btnReset.TabIndex = 3;
            btnReset.Text = "Reset";
            btnReset.UseVisualStyleBackColor = false;
            btnReset.Click += button4_Click;
            // 
            // btnFirst
            // 
            btnFirst.BackColor = Color.FromArgb(64, 186, 191);
            btnFirst.Font = new Font("MS Reference Sans Serif", 9F, FontStyle.Bold);
            btnFirst.Location = new Point(119, 14);
            btnFirst.Name = "btnFirst";
            btnFirst.Size = new Size(58, 29);
            btnFirst.TabIndex = 4;
            btnFirst.Text = "<<";
            btnFirst.TextAlign = ContentAlignment.BottomCenter;
            btnFirst.UseVisualStyleBackColor = false;
            btnFirst.Click += btnFirst_Click;
            // 
            // btnPrev
            // 
            btnPrev.BackColor = Color.FromArgb(64, 186, 191);
            btnPrev.Font = new Font("MS Reference Sans Serif", 9F, FontStyle.Bold);
            btnPrev.Location = new Point(183, 14);
            btnPrev.Name = "btnPrev";
            btnPrev.Size = new Size(58, 29);
            btnPrev.TabIndex = 5;
            btnPrev.Text = "<";
            btnPrev.UseVisualStyleBackColor = false;
            btnPrev.Click += btnPrev_Click;
            // 
            // btnnext
            // 
            btnnext.BackColor = Color.FromArgb(64, 186, 191);
            btnnext.Font = new Font("MS Reference Sans Serif", 9F, FontStyle.Bold);
            btnnext.Location = new Point(247, 14);
            btnnext.Name = "btnnext";
            btnnext.Size = new Size(58, 29);
            btnnext.TabIndex = 6;
            btnnext.Text = ">";
            btnnext.UseVisualStyleBackColor = false;
            btnnext.Click += btnnext_Click;
            // 
            // btnLast
            // 
            btnLast.BackColor = Color.FromArgb(64, 186, 191);
            btnLast.Font = new Font("MS Reference Sans Serif", 9F, FontStyle.Bold);
            btnLast.Location = new Point(314, 14);
            btnLast.Name = "btnLast";
            btnLast.Size = new Size(58, 29);
            btnLast.TabIndex = 7;
            btnLast.Text = ">>";
            btnLast.UseVisualStyleBackColor = false;
            btnLast.Click += btnLast_Click;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("MS Reference Sans Serif", 9F, FontStyle.Bold);
            label1.Location = new Point(11, 17);
            label1.Name = "label1";
            label1.Size = new Size(80, 19);
            label1.TabIndex = 8;
            label1.Text = "Item ID:";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("MS Reference Sans Serif", 9F, FontStyle.Bold);
            label2.Location = new Point(11, 53);
            label2.Name = "label2";
            label2.Size = new Size(65, 19);
            label2.TabIndex = 9;
            label2.Text = "Name:";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Font = new Font("MS Reference Sans Serif", 9F, FontStyle.Bold);
            label3.Location = new Point(11, 87);
            label3.Name = "label3";
            label3.Size = new Size(110, 19);
            label3.TabIndex = 10;
            label3.Text = "Description:";
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Font = new Font("MS Reference Sans Serif", 9F, FontStyle.Bold);
            label4.Location = new Point(412, 13);
            label4.Name = "label4";
            label4.Size = new Size(94, 19);
            label4.TabIndex = 11;
            label4.Text = "Category:";
            // 
            // label5
            // 
            label5.AutoSize = true;
            label5.Font = new Font("MS Reference Sans Serif", 9F, FontStyle.Bold);
            label5.Location = new Point(412, 59);
            label5.Name = "label5";
            label5.Size = new Size(57, 19);
            label5.TabIndex = 12;
            label5.Text = "Price:";
            // 
            // label6
            // 
            label6.AutoSize = true;
            label6.Font = new Font("MS Reference Sans Serif", 9F, FontStyle.Bold);
            label6.Location = new Point(412, 98);
            label6.Name = "label6";
            label6.Size = new Size(88, 19);
            label6.TabIndex = 13;
            label6.Text = "Quantity:";
            // 
            // label7
            // 
            label7.AutoSize = true;
            label7.Font = new Font("MS Reference Sans Serif", 9F, FontStyle.Bold);
            label7.Location = new Point(394, 24);
            label7.Name = "label7";
            label7.Size = new Size(66, 19);
            label7.TabIndex = 14;
            label7.Text = "Search";
            // 
            // txtid
            // 
            txtid.Enabled = false;
            txtid.Location = new Point(119, 14);
            txtid.Name = "txtid";
            txtid.Size = new Size(217, 27);
            txtid.TabIndex = 15;
            // 
            // txtname
            // 
            txtname.Location = new Point(119, 50);
            txtname.Name = "txtname";
            txtname.Size = new Size(217, 27);
            txtname.TabIndex = 16;
            // 
            // txtprice
            // 
            txtprice.Location = new Point(515, 55);
            txtprice.Name = "txtprice";
            txtprice.Size = new Size(208, 27);
            txtprice.TabIndex = 17;
            // 
            // txtqty
            // 
            txtqty.Location = new Point(515, 94);
            txtqty.Name = "txtqty";
            txtqty.Size = new Size(94, 27);
            txtqty.TabIndex = 19;
            // 
            // txtdesc
            // 
            txtdesc.Location = new Point(119, 87);
            txtdesc.Name = "txtdesc";
            txtdesc.Size = new Size(259, 65);
            txtdesc.TabIndex = 20;
            txtdesc.Text = "";
            // 
            // cbCategroy
            // 
            cbCategroy.FormattingEnabled = true;
            cbCategroy.Location = new Point(515, 11);
            cbCategroy.Name = "cbCategroy";
            cbCategroy.Size = new Size(208, 28);
            cbCategroy.TabIndex = 21;
            // 
            // panel1
            // 
            panel1.BackColor = Color.FromArgb(0, 120, 120);
            panel1.Controls.Add(lblPage);
            panel1.Controls.Add(textsearch);
            panel1.Controls.Add(dgrid);
            panel1.Controls.Add(btnFirst);
            panel1.Controls.Add(btnPrev);
            panel1.Controls.Add(btnnext);
            panel1.Controls.Add(btnLast);
            panel1.Controls.Add(label7);
            panel1.Location = new Point(9, 229);
            panel1.Name = "panel1";
            panel1.Size = new Size(703, 304);
            panel1.TabIndex = 22;
            // 
            // lblPage
            // 
            lblPage.AutoSize = true;
            lblPage.Location = new Point(7, 22);
            lblPage.Name = "lblPage";
            lblPage.Size = new Size(21, 20);
            lblPage.TabIndex = 24;
            lblPage.Text = "   ";
            // 
            // textsearch
            // 
            textsearch.Location = new Point(475, 20);
            textsearch.Name = "textsearch";
            textsearch.Size = new Size(225, 27);
            textsearch.TabIndex = 23;
            textsearch.TextChanged += textBox4_TextChanged;
            // 
            // dgrid
            // 
            dgrid.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dgrid.CellBorderStyle = DataGridViewCellBorderStyle.SunkenHorizontal;
            dgrid.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dgrid.Location = new Point(3, 53);
            dgrid.Name = "dgrid";
            dgrid.RowHeadersWidth = 51;
            dgrid.Size = new Size(697, 243);
            dgrid.TabIndex = 0;
            dgrid.Click += dgrid_Click;
            // 
            // cbunit
            // 
            cbunit.FormattingEnabled = true;
            cbunit.Location = new Point(651, 94);
            cbunit.Name = "cbunit";
            cbunit.Size = new Size(72, 28);
            cbunit.TabIndex = 23;
            // 
            // btnClose
            // 
            btnClose.BackColor = Color.FromArgb(191, 87, 0);
            btnClose.Font = new Font("MS Reference Sans Serif", 9F, FontStyle.Bold);
            btnClose.Location = new Point(512, 16);
            btnClose.Name = "btnClose";
            btnClose.Size = new Size(94, 29);
            btnClose.TabIndex = 24;
            btnClose.Text = "Close";
            btnClose.UseVisualStyleBackColor = false;
            btnClose.Click += button9_Click;
            // 
            // panel2
            // 
            panel2.BackColor = Color.FromArgb(0, 120, 120);
            panel2.Controls.Add(btnUpdate);
            panel2.Controls.Add(btnClose);
            panel2.Controls.Add(btnSave);
            panel2.Controls.Add(btnDelete);
            panel2.Controls.Add(btnReset);
            panel2.Location = new Point(12, 158);
            panel2.Name = "panel2";
            panel2.Size = new Size(697, 65);
            panel2.TabIndex = 25;
            // 
            // ItemFrm
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.DarkCyan;
            ClientSize = new Size(733, 552);
            Controls.Add(panel2);
            Controls.Add(cbunit);
            Controls.Add(panel1);
            Controls.Add(cbCategroy);
            Controls.Add(txtdesc);
            Controls.Add(txtqty);
            Controls.Add(txtprice);
            Controls.Add(txtname);
            Controls.Add(txtid);
            Controls.Add(label6);
            Controls.Add(label5);
            Controls.Add(label4);
            Controls.Add(label3);
            Controls.Add(label2);
            Controls.Add(label1);
            Name = "ItemFrm";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "ItemFrm";
            Load += ItemFrm_Load;
            panel1.ResumeLayout(false);
            panel1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)dgrid).EndInit();
            panel2.ResumeLayout(false);
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button btnSave;
        private Button btnUpdate;
        private Button btnDelete;
        private Button btnReset;
        private Button btnFirst;
        private Button btnPrev;
        private Button btnnext;
        private Button btnLast;
        private Label label1;
        private Label label2;
        private Label label3;
        private Label label4;
        private Label label5;
        private Label label6;
        private Label label7;
        private TextBox txtid;
        private TextBox txtname;
        private TextBox txtprice;
        private TextBox txtqty;
        private RichTextBox txtdesc;
        private ComboBox cbCategroy;
        private Panel panel1;
        private TextBox textsearch;
        private DataGridView dgrid;
        private ComboBox cbunit;
        private Button btnClose;
        private Panel panel2;
        private Label lblPage;
    }
}