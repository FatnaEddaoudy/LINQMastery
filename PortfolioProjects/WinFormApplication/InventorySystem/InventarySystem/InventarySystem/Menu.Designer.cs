namespace InventarySystem
{
    partial class Menu
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Menu));
            toolStrip1 = new ToolStrip();
            toolStripButton1 = new ToolStripButton();
            toolStripButton2 = new ToolStripButton();
            toolStripButton3 = new ToolStripButton();
            toolStripButton7 = new ToolStripButton();
            toolStripButton4 = new ToolStripButton();
            toolStripButton5 = new ToolStripButton();
            toolStripButton6 = new ToolStripButton();
            toolStrip1.SuspendLayout();
            SuspendLayout();
            // 
            // toolStrip1
            // 
            toolStrip1.ImageScalingSize = new Size(59, 59);
            toolStrip1.Items.AddRange(new ToolStripItem[] { toolStripButton1, toolStripButton2, toolStripButton3, toolStripButton7, toolStripButton4, toolStripButton5, toolStripButton6 });
            toolStrip1.Location = new Point(0, 0);
            toolStrip1.Name = "toolStrip1";
            toolStrip1.Size = new Size(1143, 86);
            toolStrip1.Stretch = true;
            toolStrip1.TabIndex = 0;
            toolStrip1.Text = "Stock Master";
            // 
            // toolStripButton1
            // 
            toolStripButton1.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            toolStripButton1.Image = (Image)resources.GetObject("toolStripButton1.Image");
            toolStripButton1.ImageTransparentColor = Color.Magenta;
            toolStripButton1.Name = "toolStripButton1";
            toolStripButton1.Size = new Size(104, 83);
            toolStripButton1.Text = "Stock Master";
            toolStripButton1.TextImageRelation = TextImageRelation.TextAboveImage;
            toolStripButton1.Click += toolStripButton1_Click;
            // 
            // toolStripButton2
            // 
            toolStripButton2.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            toolStripButton2.Image = (Image)resources.GetObject("toolStripButton2.Image");
            toolStripButton2.ImageTransparentColor = Color.Magenta;
            toolStripButton2.Name = "toolStripButton2";
            toolStripButton2.Size = new Size(86, 83);
            toolStripButton2.Text = " Stock-Out";
            toolStripButton2.TextImageRelation = TextImageRelation.TextAboveImage;
            toolStripButton2.Click += toolStripButton2_Click;
            // 
            // toolStripButton3
            // 
            toolStripButton3.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            toolStripButton3.Image = (Image)resources.GetObject("toolStripButton3.Image");
            toolStripButton3.ImageTransparentColor = Color.Magenta;
            toolStripButton3.Name = "toolStripButton3";
            toolStripButton3.Size = new Size(111, 83);
            toolStripButton3.Text = "  Stock Return";
            toolStripButton3.TextImageRelation = TextImageRelation.TextAboveImage;
            toolStripButton3.Click += toolStripButton3_Click;
            // 
            // toolStripButton7
            // 
            toolStripButton7.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            toolStripButton7.Image = (Image)resources.GetObject("toolStripButton7.Image");
            toolStripButton7.ImageTransparentColor = Color.Magenta;
            toolStripButton7.Name = "toolStripButton7";
            toolStripButton7.Size = new Size(70, 83);
            toolStripButton7.Text = "Settings";
            toolStripButton7.TextImageRelation = TextImageRelation.TextAboveImage;
            toolStripButton7.Click += toolStripButton7_Click;
            // 
            // toolStripButton4
            // 
            toolStripButton4.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            toolStripButton4.Image = (Image)resources.GetObject("toolStripButton4.Image");
            toolStripButton4.ImageTransparentColor = Color.Magenta;
            toolStripButton4.Name = "toolStripButton4";
            toolStripButton4.Size = new Size(113, 83);
            toolStripButton4.Text = "  Manage User";
            toolStripButton4.TextImageRelation = TextImageRelation.TextAboveImage;
            // 
            // toolStripButton5
            // 
            toolStripButton5.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            toolStripButton5.Image = (Image)resources.GetObject("toolStripButton5.Image");
            toolStripButton5.ImageTransparentColor = Color.Magenta;
            toolStripButton5.Name = "toolStripButton5";
            toolStripButton5.Size = new Size(89, 83);
            toolStripButton5.Text = "   Report    ";
            toolStripButton5.TextImageRelation = TextImageRelation.TextAboveImage;
            // 
            // toolStripButton6
            // 
            toolStripButton6.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            toolStripButton6.Image = (Image)resources.GetObject("toolStripButton6.Image");
            toolStripButton6.ImageTransparentColor = Color.Magenta;
            toolStripButton6.Name = "toolStripButton6";
            toolStripButton6.Size = new Size(71, 83);
            toolStripButton6.Text = "  Logout";
            toolStripButton6.TextImageRelation = TextImageRelation.TextAboveImage;
            // 
            // Menu
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = SystemColors.ControlDark;
            ClientSize = new Size(1143, 694);
            Controls.Add(toolStrip1);
            Icon = (Icon)resources.GetObject("$this.Icon");
            Name = "Menu";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Menu";
            WindowState = FormWindowState.Maximized;
            FormClosed += Menu_FormClosed;
            Load += Menu_Load;
            toolStrip1.ResumeLayout(false);
            toolStrip1.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private ToolStrip toolStrip1;
        private ToolStripButton toolStripButton1;
        private ToolStripButton toolStripButton2;
        private ToolStripButton toolStripButton3;
        private ToolStripButton toolStripButton4;
        private ToolStripButton toolStripButton5;
        private ToolStripButton toolStripButton6;
        private ToolStripButton toolStripButton7;
    }
}