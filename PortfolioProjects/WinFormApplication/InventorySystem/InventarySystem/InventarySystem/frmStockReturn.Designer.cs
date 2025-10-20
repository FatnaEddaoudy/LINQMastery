namespace InventarySystem
{
    partial class frmStockout
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(frmStockout));
            groupBox1 = new GroupBox();
            txtLastName = new TextBox();
            txtFirstName = new TextBox();
            txtcustomerId = new TextBox();
            label3 = new Label();
            label2 = new Label();
            label1 = new Label();
            groupBox2 = new GroupBox();
            DgItems = new DataGridView();
            textBox4 = new TextBox();
            label4 = new Label();
            groupBox3 = new GroupBox();
            dgstockout = new DataGridView();
            button1 = new Button();
            button2 = new Button();
            button3 = new Button();
            button4 = new Button();
            button5 = new Button();
            groupBox1.SuspendLayout();
            groupBox2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)DgItems).BeginInit();
            groupBox3.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)dgstockout).BeginInit();
            SuspendLayout();
            // 
            // groupBox1
            // 
            groupBox1.Controls.Add(txtLastName);
            groupBox1.Controls.Add(txtFirstName);
            groupBox1.Controls.Add(txtcustomerId);
            groupBox1.Controls.Add(label3);
            groupBox1.Controls.Add(label2);
            groupBox1.Controls.Add(label1);
            groupBox1.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            groupBox1.Location = new Point(12, 12);
            groupBox1.Name = "groupBox1";
            groupBox1.Size = new Size(760, 164);
            groupBox1.TabIndex = 0;
            groupBox1.TabStop = false;
            groupBox1.Text = "Customer";
            // 
            // txtLastName
            // 
            txtLastName.Enabled = false;
            txtLastName.Location = new Point(506, 69);
            txtLastName.Name = "txtLastName";
            txtLastName.Size = new Size(215, 27);
            txtLastName.TabIndex = 5;
            // 
            // txtFirstName
            // 
            txtFirstName.Enabled = false;
            txtFirstName.Location = new Point(111, 65);
            txtFirstName.Name = "txtFirstName";
            txtFirstName.Size = new Size(215, 27);
            txtFirstName.TabIndex = 4;
            // 
            // txtcustomerId
            // 
            txtcustomerId.Location = new Point(111, 30);
            txtcustomerId.Name = "txtcustomerId";
            txtcustomerId.Size = new Size(215, 27);
            txtcustomerId.TabIndex = 3;
            txtcustomerId.TextChanged += txtcustomerId_TextChanged;
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new Point(398, 72);
            label3.Name = "label3";
            label3.Size = new Size(88, 20);
            label3.TabIndex = 2;
            label3.Text = "Last Name:";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(6, 72);
            label2.Name = "label2";
            label2.Size = new Size(90, 20);
            label2.TabIndex = 1;
            label2.Text = "First Name:";
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(6, 33);
            label1.Name = "label1";
            label1.Size = new Size(99, 20);
            label1.TabIndex = 0;
            label1.Text = "Customer Id:";
            // 
            // groupBox2
            // 
            groupBox2.Controls.Add(DgItems);
            groupBox2.Controls.Add(textBox4);
            groupBox2.Controls.Add(label4);
            groupBox2.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            groupBox2.Location = new Point(12, 182);
            groupBox2.Name = "groupBox2";
            groupBox2.Size = new Size(760, 279);
            groupBox2.TabIndex = 1;
            groupBox2.TabStop = false;
            groupBox2.Text = "List of Products";
            groupBox2.Enter += groupBox2_Enter;
            // 
            // DgItems
            // 
            DgItems.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            DgItems.Location = new Point(5, 60);
            DgItems.Name = "DgItems";
            DgItems.RowHeadersWidth = 51;
            DgItems.Size = new Size(755, 213);
            DgItems.TabIndex = 7;
            DgItems.DoubleClick += DgItems_DoubleClick;
            // 
            // textBox4
            // 
            textBox4.Location = new Point(485, 20);
            textBox4.Name = "textBox4";
            textBox4.Size = new Size(215, 27);
            textBox4.TabIndex = 6;
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Location = new Point(398, 23);
            label4.Name = "label4";
            label4.Size = new Size(55, 20);
            label4.TabIndex = 3;
            label4.Text = "Search";
            // 
            // groupBox3
            // 
            groupBox3.Controls.Add(dgstockout);
            groupBox3.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            groupBox3.Location = new Point(12, 467);
            groupBox3.Name = "groupBox3";
            groupBox3.Size = new Size(760, 239);
            groupBox3.TabIndex = 2;
            groupBox3.TabStop = false;
            groupBox3.Text = "List Of Added Items";
            // 
            // dgstockout
            // 
            dgstockout.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dgstockout.Location = new Point(6, 26);
            dgstockout.Name = "dgstockout";
            dgstockout.RowHeadersWidth = 51;
            dgstockout.Size = new Size(754, 207);
            dgstockout.TabIndex = 8;
            dgstockout.CellEndEdit += dgstockout_CellEndEdit;
            // 
            // button1
            // 
            button1.Location = new Point(23, 712);
            button1.Name = "button1";
            button1.Size = new Size(94, 29);
            button1.TabIndex = 3;
            button1.Text = "Save";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // button2
            // 
            button2.Location = new Point(180, 712);
            button2.Name = "button2";
            button2.Size = new Size(94, 29);
            button2.TabIndex = 4;
            button2.Text = "Remove";
            button2.UseVisualStyleBackColor = true;
            button2.Click += button2_Click;
            // 
            // button3
            // 
            button3.Location = new Point(359, 712);
            button3.Name = "button3";
            button3.Size = new Size(94, 29);
            button3.TabIndex = 5;
            button3.Text = "Clear";
            button3.UseVisualStyleBackColor = true;
            button3.Click += button3_Click;
            // 
            // button4
            // 
            button4.Location = new Point(535, 712);
            button4.Name = "button4";
            button4.Size = new Size(94, 29);
            button4.TabIndex = 6;
            button4.Text = "Close";
            button4.UseVisualStyleBackColor = true;
            button4.Click += button4_Click;
            // 
            // button5
            // 
            button5.Location = new Point(678, 712);
            button5.Name = "button5";
            button5.Size = new Size(94, 29);
            button5.TabIndex = 7;
            button5.Text = "View List";
            button5.UseVisualStyleBackColor = true;
            // 
            // frmStockout
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 765);
            Controls.Add(button5);
            Controls.Add(button4);
            Controls.Add(button3);
            Controls.Add(button2);
            Controls.Add(button1);
            Controls.Add(groupBox3);
            Controls.Add(groupBox2);
            Controls.Add(groupBox1);
            Icon = (Icon)resources.GetObject("$this.Icon");
            Name = "frmStockout";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Stock-Out";
            Load += frmStockReturn_Load;
            groupBox1.ResumeLayout(false);
            groupBox1.PerformLayout();
            groupBox2.ResumeLayout(false);
            groupBox2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)DgItems).EndInit();
            groupBox3.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)dgstockout).EndInit();
            ResumeLayout(false);
        }

        #endregion

        private GroupBox groupBox1;
        private Label label3;
        private Label label2;
        private Label label1;
        private GroupBox groupBox2;
        private GroupBox groupBox3;
        private TextBox txtLastName;
        private TextBox txtFirstName;
        private DataGridView DgItems;
        private TextBox textBox4;
        private Label label4;
        private DataGridView dgstockout;
        private Button button1;
        private Button button2;
        private Button button3;
        private Button button4;
        private Button button5;
        private TextBox txtcustomerId;
    }
}