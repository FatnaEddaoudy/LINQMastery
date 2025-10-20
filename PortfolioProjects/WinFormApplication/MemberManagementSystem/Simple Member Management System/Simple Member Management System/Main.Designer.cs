namespace Simple_Member_Management_System
{
    partial class Main
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
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
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Main));
            button1 = new Button();
            imageList1 = new ImageList(components);
            panel1 = new Panel();
            button5 = new Button();
            button4 = new Button();
            button3 = new Button();
            button2 = new Button();
            LblId = new Label();
            panel4 = new Panel();
            dataGridMembers = new DataGridView();
            LblIdMember = new Label();
            panel3 = new Panel();
            cbGender = new ComboBox();
            textAge = new TextBox();
            TxtAdress = new RichTextBox();
            LblFirstName = new Label();
            LblLastName = new Label();
            LblAge = new Label();
            LblGender = new Label();
            textLastName = new TextBox();
            LblAdress = new Label();
            textFirstName = new TextBox();
            btnExport = new Button();
            btnimport = new Button();
            panel1.SuspendLayout();
            panel4.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)dataGridMembers).BeginInit();
            panel3.SuspendLayout();
            SuspendLayout();
            // 
            // button1
            // 
            button1.BackColor = Color.Transparent;
            button1.FlatStyle = FlatStyle.Popup;
            button1.Location = new Point(25, 35);
            button1.Margin = new Padding(4);
            button1.Name = "button1";
            button1.Size = new Size(135, 69);
            button1.TabIndex = 0;
            button1.Text = "ADD";
            button1.UseVisualStyleBackColor = false;
            button1.Click += button1_Click;
            // 
            // imageList1
            // 
            imageList1.ColorDepth = ColorDepth.Depth4Bit;
            imageList1.ImageStream = (ImageListStreamer)resources.GetObject("imageList1.ImageStream");
            imageList1.TransparentColor = Color.Transparent;
            imageList1.Images.SetKeyName(0, "Add_User-80_icon-icons.com_57380.png");
            // 
            // panel1
            // 
            panel1.BackColor = Color.Transparent;
            panel1.BorderStyle = BorderStyle.FixedSingle;
            panel1.Controls.Add(button5);
            panel1.Controls.Add(button4);
            panel1.Controls.Add(button3);
            panel1.Controls.Add(button2);
            panel1.Controls.Add(button1);
            panel1.Location = new Point(-1, 0);
            panel1.Margin = new Padding(4);
            panel1.Name = "panel1";
            panel1.Size = new Size(197, 652);
            panel1.TabIndex = 1;
            // 
            // button5
            // 
            button5.BackColor = Color.Transparent;
            button5.FlatStyle = FlatStyle.Popup;
            button5.Location = new Point(25, 528);
            button5.Margin = new Padding(4);
            button5.Name = "button5";
            button5.Size = new Size(135, 69);
            button5.TabIndex = 4;
            button5.Text = "Exit";
            button5.UseVisualStyleBackColor = false;
            button5.Click += button5_Click;
            // 
            // button4
            // 
            button4.BackColor = Color.Transparent;
            button4.FlatStyle = FlatStyle.Popup;
            button4.Location = new Point(25, 411);
            button4.Margin = new Padding(4);
            button4.Name = "button4";
            button4.Size = new Size(135, 69);
            button4.TabIndex = 3;
            button4.Text = "Clear";
            button4.UseVisualStyleBackColor = false;
            button4.Click += button4_Click;
            // 
            // button3
            // 
            button3.BackColor = Color.Transparent;
            button3.FlatStyle = FlatStyle.Popup;
            button3.Location = new Point(25, 267);
            button3.Margin = new Padding(4);
            button3.Name = "button3";
            button3.Size = new Size(135, 69);
            button3.TabIndex = 2;
            button3.Text = "Delete";
            button3.UseVisualStyleBackColor = false;
            button3.Click += button3_Click;
            // 
            // button2
            // 
            button2.BackColor = Color.Transparent;
            button2.FlatStyle = FlatStyle.Popup;
            button2.Location = new Point(25, 146);
            button2.Margin = new Padding(4);
            button2.Name = "button2";
            button2.Size = new Size(135, 69);
            button2.TabIndex = 1;
            button2.Text = "Update";
            button2.UseVisualStyleBackColor = false;
            button2.Click += button2_Click;
            // 
            // LblId
            // 
            LblId.AutoSize = true;
            LblId.Location = new Point(1014, 9);
            LblId.Margin = new Padding(4, 0, 4, 0);
            LblId.Name = "LblId";
            LblId.Size = new Size(30, 23);
            LblId.TabIndex = 8;
            LblId.Text = "Id:";
            // 
            // panel4
            // 
            panel4.BackColor = Color.Transparent;
            panel4.BorderStyle = BorderStyle.Fixed3D;
            panel4.Controls.Add(dataGridMembers);
            panel4.Location = new Point(232, 267);
            panel4.Name = "panel4";
            panel4.Size = new Size(1037, 299);
            panel4.TabIndex = 18;
            // 
            // dataGridMembers
            // 
            dataGridMembers.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dataGridMembers.CellBorderStyle = DataGridViewCellBorderStyle.Sunken;
            dataGridMembers.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridMembers.Location = new Point(3, 3);
            dataGridMembers.Name = "dataGridMembers";
            dataGridMembers.RowHeadersWidth = 51;
            dataGridMembers.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            dataGridMembers.Size = new Size(1027, 358);
            dataGridMembers.TabIndex = 0;
            dataGridMembers.CellContentClick += dataGridMembers_SelectionChanged;
            // 
            // LblIdMember
            // 
            LblIdMember.AutoSize = true;
            LblIdMember.Location = new Point(1094, 9);
            LblIdMember.Margin = new Padding(4, 0, 4, 0);
            LblIdMember.Name = "LblIdMember";
            LblIdMember.Size = new Size(0, 23);
            LblIdMember.TabIndex = 19;
            // 
            // panel3
            // 
            panel3.BackColor = Color.Transparent;
            panel3.BorderStyle = BorderStyle.Fixed3D;
            panel3.Controls.Add(cbGender);
            panel3.Controls.Add(textAge);
            panel3.Controls.Add(TxtAdress);
            panel3.Controls.Add(LblFirstName);
            panel3.Controls.Add(LblLastName);
            panel3.Controls.Add(LblAge);
            panel3.Controls.Add(LblGender);
            panel3.Controls.Add(textLastName);
            panel3.Controls.Add(LblAdress);
            panel3.Controls.Add(textFirstName);
            panel3.Location = new Point(232, 53);
            panel3.Name = "panel3";
            panel3.Size = new Size(1037, 198);
            panel3.TabIndex = 17;
            // 
            // cbGender
            // 
            cbGender.FormattingEnabled = true;
            cbGender.Location = new Point(702, 13);
            cbGender.Name = "cbGender";
            cbGender.Size = new Size(301, 31);
            cbGender.TabIndex = 16;
            // 
            // textAge
            // 
            textAge.BorderStyle = BorderStyle.FixedSingle;
            textAge.Font = new Font("Segoe UI Emoji", 10.8F, FontStyle.Regular, GraphicsUnit.Point, 0);
            textAge.Location = new Point(155, 139);
            textAge.Name = "textAge";
            textAge.Size = new Size(245, 31);
            textAge.TabIndex = 12;
            // 
            // TxtAdress
            // 
            TxtAdress.Location = new Point(702, 73);
            TxtAdress.Name = "TxtAdress";
            TxtAdress.Size = new Size(301, 97);
            TxtAdress.TabIndex = 15;
            TxtAdress.Text = "";
            // 
            // LblFirstName
            // 
            LblFirstName.AutoSize = true;
            LblFirstName.Location = new Point(9, 13);
            LblFirstName.Margin = new Padding(4, 0, 4, 0);
            LblFirstName.Name = "LblFirstName";
            LblFirstName.Size = new Size(102, 23);
            LblFirstName.TabIndex = 2;
            LblFirstName.Text = "First Name:";
            // 
            // LblLastName
            // 
            LblLastName.AutoSize = true;
            LblLastName.Location = new Point(9, 76);
            LblLastName.Margin = new Padding(4, 0, 4, 0);
            LblLastName.Name = "LblLastName";
            LblLastName.Size = new Size(100, 23);
            LblLastName.TabIndex = 3;
            LblLastName.Text = "Last Name:";
            // 
            // LblAge
            // 
            LblAge.AutoSize = true;
            LblAge.Location = new Point(9, 139);
            LblAge.Margin = new Padding(4, 0, 4, 0);
            LblAge.Name = "LblAge";
            LblAge.Size = new Size(46, 23);
            LblAge.TabIndex = 4;
            LblAge.Text = "Age:";
            // 
            // LblGender
            // 
            LblGender.AutoSize = true;
            LblGender.Location = new Point(606, 13);
            LblGender.Margin = new Padding(4, 0, 4, 0);
            LblGender.Name = "LblGender";
            LblGender.Size = new Size(72, 23);
            LblGender.TabIndex = 5;
            LblGender.Text = "Gender:";
            // 
            // textLastName
            // 
            textLastName.BorderStyle = BorderStyle.FixedSingle;
            textLastName.Font = new Font("Segoe UI Emoji", 10.8F, FontStyle.Regular, GraphicsUnit.Point, 0);
            textLastName.Location = new Point(155, 76);
            textLastName.Name = "textLastName";
            textLastName.Size = new Size(245, 31);
            textLastName.TabIndex = 11;
            // 
            // LblAdress
            // 
            LblAdress.AutoSize = true;
            LblAdress.Location = new Point(606, 76);
            LblAdress.Margin = new Padding(4, 0, 4, 0);
            LblAdress.Name = "LblAdress";
            LblAdress.Size = new Size(67, 23);
            LblAdress.TabIndex = 7;
            LblAdress.Text = "Adress:";
            // 
            // textFirstName
            // 
            textFirstName.BorderStyle = BorderStyle.FixedSingle;
            textFirstName.Font = new Font("Segoe UI Emoji", 10.8F, FontStyle.Regular, GraphicsUnit.Point, 0);
            textFirstName.Location = new Point(155, 13);
            textFirstName.Name = "textFirstName";
            textFirstName.Size = new Size(245, 31);
            textFirstName.TabIndex = 9;
            // 
            // btnExport
            // 
            btnExport.BackColor = Color.Transparent;
            btnExport.FlatStyle = FlatStyle.Popup;
            btnExport.Location = new Point(909, 588);
            btnExport.Margin = new Padding(4);
            btnExport.Name = "btnExport";
            btnExport.Size = new Size(135, 34);
            btnExport.TabIndex = 5;
            btnExport.Text = "Export";
            btnExport.UseVisualStyleBackColor = false;
            btnExport.Click += btnExport_Click;
            // 
            // btnimport
            // 
            btnimport.BackColor = Color.Transparent;
            btnimport.FlatStyle = FlatStyle.Popup;
            btnimport.Location = new Point(1130, 588);
            btnimport.Margin = new Padding(4);
            btnimport.Name = "btnimport";
            btnimport.Size = new Size(135, 34);
            btnimport.TabIndex = 20;
            btnimport.Text = "Import";
            btnimport.UseVisualStyleBackColor = false;
            btnimport.Click += btnimport_Click;
            // 
            // Main
            // 
            AutoScaleDimensions = new SizeF(10F, 23F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.Teal;
            ClientSize = new Size(1286, 652);
            Controls.Add(btnimport);
            Controls.Add(btnExport);
            Controls.Add(panel3);
            Controls.Add(LblIdMember);
            Controls.Add(panel4);
            Controls.Add(LblId);
            Controls.Add(panel1);
            Font = new Font("Segoe UI", 10.2F, FontStyle.Bold | FontStyle.Italic, GraphicsUnit.Point, 0);
            ForeColor = Color.Black;
            FormBorderStyle = FormBorderStyle.Fixed3D;
            Icon = (Icon)resources.GetObject("$this.Icon");
            Margin = new Padding(4);
            Name = "Main";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Member Management System ";
            Load += Main_Load;
            panel1.ResumeLayout(false);
            panel4.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)dataGridMembers).EndInit();
            panel3.ResumeLayout(false);
            panel3.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button button1;
        private Panel panel1;
        private Button button5;
        private Button button4;
        private Button button3;
        private Button button2;
        private Label LblId;
        private Panel panel4;
        private DataGridView dataGridMembers;
        private Label LblIdMember;
        private Panel panel3;
        private ComboBox cbGender;
        private TextBox textAge;
        private RichTextBox TxtAdress;
        private Label LblFirstName;
        private Label LblLastName;
        private Label LblAge;
        private Label LblGender;
        private TextBox textLastName;
        private Label LblAdress;
        private TextBox textFirstName;
        private Button btnExport;
        private Button btnimport;
        private ImageList imageList1;
    }
}
