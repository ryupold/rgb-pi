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
        public Settings()
        {
            InitializeComponent();

            InitializeAppBar();
            
        }

        private void InitializeAppBar()
        {
            ApplicationBar = new ApplicationBar();


            ApplicationBarIconButton abbSave = new ApplicationBarIconButton(new Uri("/Assets/Icons/WP8/save.png", UriKind.Relative));
            abbSave.Text = "save";
            abbSave.Click += delegate(object s, EventArgs ea)
            {
                //SetSetting("ip", txtSettingsIP.Text);
                //SetSetting("port", txtSettingsPort.Text);

                NavigationService.GoBack();
            };
            ApplicationBar.Buttons.Add(abbSave);
        }

        protected override void OnNavigatedTo(NavigationEventArgs e)
        {
            base.OnNavigatedTo(e);
        }

        

        public static object GetSetting(string name)
        {
            IsolatedStorageSettings settings = IsolatedStorageSettings.ApplicationSettings;
            return settings.Contains(name) ? settings[name] : null;
        }

        public static void SetSetting(string name, string value)
        {
            IsolatedStorageSettings settings = IsolatedStorageSettings.ApplicationSettings;
            if (!settings.Contains(name))
            {
                settings.Add(name, value);
            }
            else
            {
                settings[name] = value;
            }
        }
    }
}