using System;
using System.Configuration;
using System.Data;
using System.Data.SqlClient;
using System.Drawing;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Windows.Forms;

namespace InventarySystem
{
    public class SqlSetting
    {
        public static string connectionString = ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString;
        public static int userId;
        public static string username;
        public static SqlConnection con = null;

        /// <summary>
        /// Execute SELECT (value=true) or INSERT/UPDATE/DELETE (value=false)
        /// </summary>
        public static DataTable ExecuteQuery(string query, bool value)
        {
            DataTable dt = new DataTable();

            try
            {
                if (con == null)
                    con = new SqlConnection(connectionString);

                if (con.State != ConnectionState.Open)
                    con.Open();

                SqlCommand cmd = new SqlCommand(query, con);
                if (value) // SELECT
                {
                    SqlDataReader reader = cmd.ExecuteReader();
                    dt.Load(reader);
                    reader.Close();
                }
                else // INSERT/UPDATE/DELETE
                {
                    cmd.ExecuteNonQuery();
                }
                cmd.Dispose();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Database error: " + ex.Message);
            }
            finally
            {
                if (con != null && con.State == ConnectionState.Open)
                    con.Close();
            }

            return dt;
        }

        /// <summary>
        /// Compute SHA1 hash
        /// </summary>
        public static string ComputeSha1Hash(string input)
        {
            using (SHA1 sha1 = SHA1.Create())
            {
                byte[] inputBytes = Encoding.UTF8.GetBytes(input);
                byte[] hashBytes = sha1.ComputeHash(inputBytes);
                StringBuilder sb = new StringBuilder();
                foreach (byte b in hashBytes)
                    sb.Append(b.ToString("x2"));
                return sb.ToString();
            }
        }

        /// <summary>
        /// Round buttons inside a parent control
        /// </summary>
        public static void MakeButtonsRounded(Control parent, int radius = 20)
        {
            foreach (Control ctrl in parent.Controls)
            {
                if (ctrl is Button btn)
                {
                    var path = new System.Drawing.Drawing2D.GraphicsPath();
                    path.AddArc(0, 0, radius, radius, 180, 90);
                    path.AddArc(btn.Width - radius, 0, radius, radius, 270, 90);
                    path.AddArc(btn.Width - radius, btn.Height - radius, radius, radius, 0, 90);
                    path.AddArc(0, btn.Height - radius, radius, radius, 90, 90);
                    path.CloseAllFigures();

                    btn.Region = new Region(path);
                    btn.FlatStyle = FlatStyle.Flat;
                }

                if (ctrl.HasChildren)
                    MakeButtonsRounded(ctrl, radius);
            }
        }

        /// <summary>
        /// Return a page from a DataTable
        /// </summary>
        public static DataTable GetPage(DataTable dt, int pageSize, int currentPage)
        {
            if (dt == null || dt.Rows.Count == 0)
                return dt?.Clone() ?? new DataTable();

            var pageRows = dt.AsEnumerable()
                             .Skip((currentPage - 1) * pageSize)
                             .Take(pageSize);

            if (!pageRows.Any())
                return dt.Clone();

            return pageRows.CopyToDataTable();
        }

        /// <summary>
        /// Generate a formatted ItemID like "A000010"
        /// </summary>
        public static string GenerateItemID(string typeName)
        {
            if (con == null)
                con = new SqlConnection(connectionString);

            if (con.State != ConnectionState.Open)
                con.Open();

            string prefix = "";
            int numericPart = 0;
            int increment = 1;
            int end = 0;
            int totalDigits = 0;

            // 1️⃣ Get autonumber row for this type
            SqlCommand cmdRule = new SqlCommand(
     "SELECT TOP 1 STRT, END_VAL, INCREMENT FROM autonumber WHERE DESCRIPTION=@Type", con);
            cmdRule.Parameters.AddWithValue("@Type", typeName);
            SqlDataReader dr = cmdRule.ExecuteReader();
            if (dr.Read())
            {
                string startStr = dr["STRT"].ToString(); // e.g., "A0000"
                end = int.Parse(dr["END_VAL"].ToString());   // e.g., 4
                increment = Convert.ToInt32(dr["INCREMENT"]);

                // Separate prefix (letters) and numeric part
                int i = 0;
                while (i < startStr.Length && !char.IsDigit(startStr[i]))
                    i++;

                prefix = startStr.Substring(0, i);                // e.g., "A"
                string numberStr = startStr.Substring(i);         // e.g., "0000"
                numericPart = int.Parse(numberStr);              // e.g., 0
                totalDigits = numberStr.Length;                  // e.g., 4
            }
            dr.Close();

            // 2️⃣ Get last used ItemID for this type from Items table
            SqlCommand cmdLast = new SqlCommand(
                "SELECT MAX(ItemID) FROM Items WHERE TYPE=@Type", con);
            cmdLast.Parameters.AddWithValue("@Type", typeName);
            var result = cmdLast.ExecuteScalar();
            if (result != DBNull.Value)
            {
                string lastIdStr = result.ToString(); // e.g., "A0001"
                string numberStr = lastIdStr.Substring(prefix.Length);
                numericPart = int.Parse(numberStr);
            }
            // 3️⃣ Calculate next ID
            int nextIDNum = numericPart + increment;
            if (nextIDNum > end)
                throw new Exception($"Maximum ItemID reached for {typeName}!");

            // 4️⃣ Format ItemID: prefix + leading zeros
            string formattedID = prefix + nextIDNum.ToString("D" + totalDigits);
            return formattedID;
        }

    }
}
