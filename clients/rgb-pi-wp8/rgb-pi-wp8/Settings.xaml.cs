using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Navigation;
using Microsoft.Phone.Controls;
using Microsoft.Phone.Shell;
using System.IO.IsolatedStorage;

namespace RGB
{
    public partial class Settings : PhoneApplicationPage
    {
        public string IP { get; set; }
        public int Port { get; set; }
        private IsolatedStorageSettings settings = IsolatedStorageSettings.ApplicationSettings;

        public Settings()
        {
            InitializeComponent();

            LoadSettings();

            BuildLocalizedApplicationBar();
        }

        private void LoadSettings()
        {
            settings = IsolatedStorageSettings.ApplicationSettings;
            if (settings.Contains("ip"))
            {
                IP = (string)settings["ip"];
            }
            else
            {
                settings.Add("ip", IP = "192.168.0.10");
            }

            if (settings.Contains("port"))
            {
                Port = int.Parse(settings["port"].ToString());
            }
            else
            {
                settings.Add("port", Port = 4321);
            }

            txtSettingsIP.Text = IP;
            txtSettingsPort.Text = Port + "";
        }

        protected override void OnNavigatedTo(NavigationEventArgs e)
        {
            base.OnNavigatedTo(e);
            LoadSettings();
        }

        private void BuildLocalizedApplicationBar()
        {
            // Set the page's ApplicationBar to a new instance of ApplicationBar.
            ApplicationBar = new ApplicationBar();

            // Create a new button and set the text value to the localized string from AppResources.
            ApplicationBarIconButton abbOn = new ApplicationBarIconButton(new Uri("/Assets/Icons/save.png", UriKind.Relative));
            abbOn.Text = "Save";
            abbOn.Click += delegate(object s, EventArgs ea)
            {
                int e = 0;
                try
                {
                    e++;
                    IP = txtSettingsIP.Text;
                    e++;
                    Port = int.Parse(txtSettingsPort.Text);
                    e++;
                    settings["ip"] = IP;
                    settings["port"] = Port;
                    settings.Save();
                    e++;
                    NavigationService.Navigate(new Uri("/MainPage.xaml", UriKind.Relative));
                    ShellToast toast = new ShellToast();
                    toast.Title = "RGB-Pi";
                    toast.Content = "Saved!";
                    toast.Show();
                }
                catch(Exception ex)
                {
                    ShellToast toast = new ShellToast();
                    toast.Title = "RGB-Pi";
                    toast.Content = e == 1 ? "Invalid IP" : e == 2 ? "Invalid Port" : e == 3 ? "Error during saving: " + ex.Message : ex.Message;
                    toast.Show();
                }
            };
            ApplicationBar.Buttons.Add(abbOn);

            ApplicationBarIconButton abbOff = new ApplicationBarIconButton(new Uri("/Assets/Icons/cancel.png", UriKind.Relative));
            abbOff.Text = "Cancel";
            abbOff.Click += delegate(object s, EventArgs ea)
            {
                NavigationService.Navigate(new Uri("/MainPage.xaml", UriKind.Relative));
            };
            ApplicationBar.Buttons.Add(abbOff);

            
        }
    }
}