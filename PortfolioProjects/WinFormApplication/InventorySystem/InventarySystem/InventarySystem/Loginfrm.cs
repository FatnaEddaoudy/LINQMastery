using System.Data;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

namespace InventarySystem
{
    public partial class Loginfrm : Form
    {
        public Loginfrm()
        {
            InitializeComponent();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(txtUsername.Text) || string.IsNullOrEmpty(txtPassword.Text))
            {
                MessageBox.Show("Vul gebruikersnaam en wachtwoord in.");
                return;
            }
            string hashedPassword = SqlSetting.ComputeSha1Hash(txtPassword.Text);
            string query = $"SELECT user_id, name FROM [user] " +
                       $"WHERE user_name = '{txtUsername.Text}' AND pass = '{hashedPassword}'";
            DataTable result = SqlSetting.ExecuteQuery(query,true);
            if (result.Rows.Count > 0)
            {
                int userId = Convert.ToInt32(result.Rows[0]["user_id"]);
                string name = result.Rows[0]["name"].ToString();

                Menu menu = new Menu();
                menu.Show();
                this.Hide();
            }
            else
            {
                MessageBox.Show("Onjuiste gebruikersnaam of wachtwoord.");
            }
        }

        private void Loginfrm_Load(object sender, EventArgs e)
        {
            SqlSetting.MakeButtonsRounded(this, 20);
        }
    }
}
