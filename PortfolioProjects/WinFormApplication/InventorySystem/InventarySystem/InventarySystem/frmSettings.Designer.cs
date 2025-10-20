namespace InventarySystem
{
    partial class frmSettings
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(frmSettings));
            label1 = new Label();
            txtCategory = new TextBox();
            dgCategory = new DataGridView();
            groupBox1 = new GroupBox();
            btnLoadC = new Button();
            btnDeleteC = new Button();
            btnUpdateC = new Button();
            btnSaveC = new Button();
            groupBox2 = new GroupBox();
            btnLoadU = new Button();
            dgUnit = new DataGridView();
            btnDeleteU = new Button();
            txtUnit = new TextBox();
            btnUpdateU = new Button();
            label2 = new Label();
            btnsaveU = new Button();
            ((System.ComponentModel.ISupportInitialize)dgCategory).BeginInit();
            groupBox1.SuspendLayout();
            groupBox2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)dgUnit).BeginInit();
            SuspendLayout();
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            label1.Location = new Point(6, 43);
            label1.Name = "label1";
            label1.Size = new Size(77, 20);
            label1.TabIndex = 0;
            label1.Text = "Category:";
            // 
            // txtCategory
            // 
            txtCategory.Location = new Point(89, 43);
            txtCategory.Name = "txtCategory";
            txtCategory.Size = new Size(175, 27);
            txtCategory.TabIndex = 1;
            // 
            // dgCategory
            // 
            dgCategory.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dgCategory.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dgCategory.Location = new Point(6, 86);
            dgCategory.Name = "dgCategory";
            dgCategory.RowHeadersVisible = false;
            dgCategory.RowHeadersWidth = 51;
            dgCategory.Size = new Size(258, 277);
            dgCategory.TabIndex = 2;
            dgCategory.Click += dgCategory_Click;
            // 
            // groupBox1
            // 
            groupBox1.Controls.Add(btnLoadC);
            groupBox1.Controls.Add(btnDeleteC);
            groupBox1.Controls.Add(btnUpdateC);
            groupBox1.Controls.Add(btnSaveC);
            groupBox1.Controls.Add(dgCategory);
            groupBox1.Controls.Add(txtCategory);
            groupBox1.Controls.Add(label1);
            groupBox1.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            groupBox1.Location = new Point(12, 34);
            groupBox1.Name = "groupBox1";
            groupBox1.Size = new Size(375, 378);
            groupBox1.TabIndex = 2;
            groupBox1.TabStop = false;
            groupBox1.Text = "Add New Category";
            // 
            // btnLoadC
            // 
            btnLoadC.Location = new Point(270, 227);
            btnLoadC.Name = "btnLoadC";
            btnLoadC.Size = new Size(94, 29);
            btnLoadC.TabIndex = 6;
            btnLoadC.Text = "Load";
            btnLoadC.UseVisualStyleBackColor = true;
            btnLoadC.Click += btnLoadC_Click;
            // 
            // btnDeleteC
            // 
            btnDeleteC.Location = new Point(270, 181);
            btnDeleteC.Name = "btnDeleteC";
            btnDeleteC.Size = new Size(94, 29);
            btnDeleteC.TabIndex = 5;
            btnDeleteC.Text = "Delete";
            btnDeleteC.UseVisualStyleBackColor = true;
            btnDeleteC.Click += btnDeleteC_Click;
            // 
            // btnUpdateC
            // 
            btnUpdateC.Location = new Point(270, 131);
            btnUpdateC.Name = "btnUpdateC";
            btnUpdateC.Size = new Size(94, 29);
            btnUpdateC.TabIndex = 4;
            btnUpdateC.Text = "Update";
            btnUpdateC.UseVisualStyleBackColor = true;
            btnUpdateC.Click += btnUpdateC_Click;
            // 
            // btnSaveC
            // 
            btnSaveC.Location = new Point(270, 86);
            btnSaveC.Name = "btnSaveC";
            btnSaveC.Size = new Size(94, 29);
            btnSaveC.TabIndex = 3;
            btnSaveC.Text = "Save";
            btnSaveC.UseVisualStyleBackColor = true;
            btnSaveC.Click += btnSaveC_Click;
            // 
            // groupBox2
            // 
            groupBox2.Controls.Add(btnLoadU);
            groupBox2.Controls.Add(dgUnit);
            groupBox2.Controls.Add(btnDeleteU);
            groupBox2.Controls.Add(txtUnit);
            groupBox2.Controls.Add(btnUpdateU);
            groupBox2.Controls.Add(label2);
            groupBox2.Controls.Add(btnsaveU);
            groupBox2.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            groupBox2.Location = new Point(419, 34);
            groupBox2.Name = "groupBox2";
            groupBox2.Size = new Size(375, 378);
            groupBox2.TabIndex = 3;
            groupBox2.TabStop = false;
            groupBox2.Text = "Add new Item Unit";
            // 
            // btnLoadU
            // 
            btnLoadU.Location = new Point(270, 227);
            btnLoadU.Name = "btnLoadU";
            btnLoadU.Size = new Size(94, 29);
            btnLoadU.TabIndex = 10;
            btnLoadU.Text = "Load";
            btnLoadU.UseVisualStyleBackColor = true;
            btnLoadU.Click += btnLoadu_Click;
            // 
            // dgUnit
            // 
            dgUnit.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dgUnit.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dgUnit.Location = new Point(6, 86);
            dgUnit.Name = "dgUnit";
            dgUnit.RowHeadersVisible = false;
            dgUnit.RowHeadersWidth = 51;
            dgUnit.Size = new Size(258, 277);
            dgUnit.TabIndex = 2;
            dgUnit.Click += dgUnit_Click;
            // 
            // btnDeleteU
            // 
            btnDeleteU.Location = new Point(270, 181);
            btnDeleteU.Name = "btnDeleteU";
            btnDeleteU.Size = new Size(94, 29);
            btnDeleteU.TabIndex = 9;
            btnDeleteU.Text = "Delete";
            btnDeleteU.UseVisualStyleBackColor = true;
            btnDeleteU.Click += btnDeleteU_Click;
            // 
            // txtUnit
            // 
            txtUnit.Location = new Point(89, 40);
            txtUnit.Name = "txtUnit";
            txtUnit.Size = new Size(175, 27);
            txtUnit.TabIndex = 1;
            // 
            // btnUpdateU
            // 
            btnUpdateU.Location = new Point(270, 131);
            btnUpdateU.Name = "btnUpdateU";
            btnUpdateU.Size = new Size(94, 29);
            btnUpdateU.TabIndex = 8;
            btnUpdateU.Text = "Update";
            btnUpdateU.UseVisualStyleBackColor = true;
            btnUpdateU.Click += btnUpdateU_Click;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            label2.Location = new Point(6, 46);
            label2.Name = "label2";
            label2.Size = new Size(80, 20);
            label2.TabIndex = 0;
            label2.Text = "Item Unit:";
            // 
            // btnsaveU
            // 
            btnsaveU.Location = new Point(270, 86);
            btnsaveU.Name = "btnsaveU";
            btnsaveU.Size = new Size(94, 29);
            btnsaveU.TabIndex = 7;
            btnsaveU.Text = "Save";
            btnsaveU.UseVisualStyleBackColor = true;
            btnsaveU.Click += btnsaveU_Click;
            // 
            // frmSettings
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.DarkCyan;
            ClientSize = new Size(820, 420);
            Controls.Add(groupBox2);
            Controls.Add(groupBox1);
            Icon = (Icon)resources.GetObject("$this.Icon");
            Name = "frmSettings";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Settings";
            Load += frmSettings_Load;
            ((System.ComponentModel.ISupportInitialize)dgCategory).EndInit();
            groupBox1.ResumeLayout(false);
            groupBox1.PerformLayout();
            groupBox2.ResumeLayout(false);
            groupBox2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)dgUnit).EndInit();
            ResumeLayout(false);
        }

        #endregion
        private DataGridView dgCategory;
        private TextBox txtCategory;
        private Label label1;
        private GroupBox groupBox1;
        private Button btnLoadC;
        private Button btnDeleteC;
        private Button btnUpdateC;
        private Button btnSaveC;
        private GroupBox groupBox2;
        private Button btnLoadU;
        private DataGridView dgUnit;
        private Button btnDeleteU;
        private TextBox txtUnit;
        private Button btnUpdateU;
        private Label label2;
        private Button btnsaveU;
    }
}