using Simple_Member_Management_System.Models;
using System;
using System.Security.Cryptography.X509Certificates;
using System.Xml.Linq;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;
using System.Text.Json;
namespace Simple_Member_Management_System
{
    public partial class Main : Form
    {
        public Main()
        {
            InitializeComponent();
        }
        public List<Member> members = new List<Member>();

        private void Main_Load(object sender, EventArgs e)
        {
            cbGender.Items.Add(Gender.Women);
            cbGender.Items.Add(Gender.Male);
            cbGender.Items.Add(Gender.X);
            members.Add(new Member(1, "John", "Doe", "Bloemistenstraat 9 ", 25, Gender.Male));
            members.Add(new Member(2, "Sara", "Chris", "Bloemstraat 9", 55, Gender.Male));
            members.Add(new Member(3, "Leyn", "Carl", "123 Main St", 45, Gender.Male));
            members.Add(new Member(4, "Niki", "Kni", "123 Saint nikelas", 35, Gender.Male));
            UpdateDataGrid();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                if (TxtAdress.Text == "" || textLastName.Text == "" || textAge.Text == "" || textFirstName.Text == "" || cbGender.Text == "")
                {
                    MessageBox.Show("Please fill in all required fields.");
                    return;
                }
                var id = members.Count + 1;
                MessageBox.Show(id + "    " + members.Count);
                Gender genderValue = (Gender)Enum.Parse(typeof(Gender), cbGender.Text);
                var member = new Member(id, textLastName.Text, textFirstName.Text, TxtAdress.Text, int.Parse(textAge.Text), genderValue);
                members.Add(member);
                UpdateDataGrid();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }
        void UpdateDataGrid()
        {
            dataGridMembers.DataSource = null;  // clear previous binding (important!)
            dataGridMembers.DataSource = members;
        }

        private void button2_Click(object sender, EventArgs e)
        {
            try
            {
                if (dataGridMembers.SelectedCells.Count > 0)
                {
                    // Get the selected row
                    var row = dataGridMembers.SelectedRows[0];

                    // Get the ID from the first cell (column 0)
                    var id = Convert.ToInt32(row.Cells[0].Value);

                    var member = members.Where(a => a.Id == id).FirstOrDefault();
                    if (member != null)
                    {
                        member.Gender = (Gender)Enum.Parse(typeof(Gender), cbGender.Text);
                        member.FirstName = textFirstName.Text;
                        member.LastName = textLastName.Text;
                        member.Address = TxtAdress.Text;
                        member.Age = Convert.ToInt32(textAge.Text);
                        UpdateDataGrid();
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void dataGridMembers_SelectionChanged(object sender, EventArgs e)
        {
            try
            {
                if (dataGridMembers.SelectedRows.Count > 0)
                {
                    var row = dataGridMembers.SelectedRows[0];
                    LblIdMember.Text = row.Cells[0].Value?.ToString();
                    TxtAdress.Text = row.Cells[3].Value?.ToString();
                    textFirstName.Text = row.Cells[1].Value?.ToString();
                    textLastName.Text = row.Cells[2].Value?.ToString();
                    textAge.Text = row.Cells[4].Value?.ToString();
                    cbGender.Text = row.Cells[5].Value?.ToString();

                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void button4_Click(object sender, EventArgs e)
        {
            LblIdMember.Text = "";
            TxtAdress.Clear();
            textFirstName.Clear();
            textLastName.Clear();
            textAge.Clear();
            cbGender.Text = "";
        }

        private void button3_Click(object sender, EventArgs e)
        {
            try
            {
                // Ask for confirmation
                DialogResult result = MessageBox.Show(
                    "Are you sure you want to delete this member?",  // message
                    "Confirm Delete",                               // title
                    MessageBoxButtons.YesNo,                        // buttons
                    MessageBoxIcon.Warning                          // icon
                );

                if (result == DialogResult.Yes)
                {
                    if (dataGridMembers.Rows.Count > 0)
                    {
                        var row = dataGridMembers.SelectedRows[0];
                        var id = Convert.ToInt32(row.Cells[0].Value);
                        var member = members.Where(a => a.Id == id).FirstOrDefault();
                        members.Remove(member);
                        MessageBox.Show("Memeber Deleted");
                        UpdateDataGrid();
                    }
                }
              
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }


        }

        private void button5_Click(object sender, EventArgs e)
        {
            Main.ActiveForm.Close();
        }
        private void btnExport_Click(object sender, EventArgs e)
        {
            try
            {
                using (SaveFileDialog saveFileDialog = new SaveFileDialog())
                {
                    saveFileDialog.Filter = "JSON files (*.json)|*.json|All files (*.*)|*.*";
                    saveFileDialog.Title = "Export Members to JSON";
                    saveFileDialog.FileName = "members.json"; // default name

                    if (saveFileDialog.ShowDialog() == DialogResult.OK)
                    {
                        string filePath = saveFileDialog.FileName;

                        // Convert list to JSON text
                        var json = JsonSerializer.Serialize(members, new JsonSerializerOptions { WriteIndented = true });

                        // Write to file
                        File.WriteAllText(filePath, json);

                        MessageBox.Show("Members exported successfully!", "Export", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                }
            }
            catch(Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
            
        }
        private void btnimport_Click(object sender, EventArgs e)
        {
            try
            {
                using (OpenFileDialog openFileDialog = new OpenFileDialog())
                {
                    openFileDialog.Filter = "JSON files (*.json)|*.json|All files (*.*)|*.*";
                    openFileDialog.Title = "Import Members from JSON";

                    if (openFileDialog.ShowDialog() == DialogResult.OK)
                    {
                        string filePath = openFileDialog.FileName;

                        // Read JSON from file
                        var json = File.ReadAllText(filePath);

                        // Deserialize to your list
                        members = JsonSerializer.Deserialize<List<Member>>(json);

                        // Update DataGridView
                        UpdateDataGrid();

                        MessageBox.Show("Members imported successfully!", "Import", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
           
        }
    }
}
