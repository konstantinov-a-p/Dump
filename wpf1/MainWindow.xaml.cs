using System;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.IO;

namespace wpf1
{
    /// <summary>
    /// Логика взаимодействия для MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();

        }
     
        //Переменные, устанавливаемые пользователем
        string read_path = String.Empty; //Путь к обрабатываемому файлу
        string write_path = String.Empty; //Путь к записываемому файлу
        int sym_to_del;                   //Слова длиной <= sym_to_del удаляются
        bool comma_remove = false;        //Удалять ли запятые

        //Обработка ошибок
        bool wrong_sym_to_del;   
        bool wrong_input_path;
        bool wrong_output_path;             

        private void input_path_TextChanged(object sender, TextChangedEventArgs e)
        {
            read_path = input_path.Text;
            wrong_input_path = !File.Exists(read_path);
        }
       
        private void input_path_LostFocus(object sender, RoutedEventArgs e)
        {            
            if (wrong_input_path)
            {
                MessageBox.Show("ОШИБКА!\nУказанный файл не существует.");
            }
            
        }
        private void output_path_TextChanged(object sender, TextChangedEventArgs e)
        {
            write_path = output_path.Text;
            string output_file = System.IO.Path.GetFileName(write_path);
            wrong_output_path = !Directory.Exists(write_path.Substring(0, write_path.Length - output_file.Length)) | Directory.Exists(write_path);
        }
        private void output_path_LostFocus(object sender, RoutedEventArgs e)
        {
            if (File.Exists(write_path))
            {
                MessageBox.Show("Внимание!\nВыбран существующий файл\n" + write_path + "\n При продолжении работы программы он будет будет перезаписан.");
            }

            if (Directory.Exists(write_path))
            {
                MessageBox.Show("Внимание!\nНе указан файл для записи обработанных данных.");
            }

        }    
        private void letters_TextChanged(object sender, TextChangedEventArgs e)
        {
            try
            {
                sym_to_del = Convert.ToInt32(letters.Text);
            }
            catch (FormatException)
            {
                wrong_sym_to_del = true;
            }
        }

        private void comma_status_Checked(object sender, RoutedEventArgs e)
        {
            comma_remove = true;
           
        }

        private void run_program_click(object sender, RoutedEventArgs e)
        {
            if ( wrong_output_path | wrong_input_path | wrong_sym_to_del )
            {
                MessageBox.Show("ОШИБКА:\nПрограмма не божет быть выполнена,\nпроверьте правильность введенных данных\n");
                return;
            }

            if (read_path == write_path)
            {
                MessageBox.Show("Ошибка! \nНевозможно продолжить исполнение программы\nИмена исходного и конечного файлов совпадают.");
                return;
            }

            if (sym_to_del == 0 & comma_remove == false)
            {
                MessageBox.Show("ВНИМАНИЕ! \n При указанных параметрах текст не изменяется. \n Результат обработки файла не сохранён.");
                return;
            }
            string messageBoxText = "Внимание!\nВыбранный файл будет перезаписан. Продолжить?";
            string caption = "Предупреждение";
            MessageBoxButton button = MessageBoxButton.YesNo;
            MessageBoxImage icon = MessageBoxImage.Warning;

            if (File.Exists(write_path))
            {
                MessageBoxResult res = MessageBox.Show(messageBoxText, caption, button, icon);
                switch (res)
                {
                    case MessageBoxResult.No:
                        return;
                }
            }

            run_program.IsEnabled = false;

            int block_size = 10240;                                                    // Количество считываемых байтов за цикл
            byte[] block = new byte[block_size];
            int block_len = block_size;
            string word = String.Empty;
            string result = String.Empty;

            using (FileStream SourceStream = new FileStream(read_path, FileMode.Open, FileAccess.Read))
            {
                using (StreamWriter OutStream = File.CreateText(write_path))
                {
                    while (block_len == block_size)
                    {
                        block_len = SourceStream.Read(block, 0, block_size);
                        string part = word + Encoding.ASCII.GetString(block, 0, block_len);
                        word = String.Empty;

                        foreach (char symbol in part)
                        {
                            if (!" \n\t\v".Contains(symbol))
                            {
                                word += symbol;
                            }
                            else
                            {
                                if (word.Length > sym_to_del)
                                {
                                    result += word;
                                }
                                word = String.Empty;
                                result += symbol;
                            }
                        }
                        if (word.Length > sym_to_del)
                        {
                            result += word.Substring(0, word.Length - sym_to_del - 1);
                            word = word.Substring(word.Length - sym_to_del - 1);
                        }

                        if (comma_remove)
                        {
                            result = result.Replace(",", String.Empty);
                        }
                        OutStream.Write(result);
                        result = String.Empty;
                    }
                    if (comma_remove)
                    {
                        word = word.Replace(",", String.Empty);
                    }
                    OutStream.Write(word);
                }
                

            }
            run_program.IsEnabled = true;
        }
        
    }
}
