using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Navigation;
using Microsoft.Phone.Controls;
using Microsoft.Phone.Shell;
using RGB.Resources;
using System.Threading;
using Coding4Fun.Toolkit.Controls;

namespace RGB
{
    public partial class MainPage : PhoneApplicationPage
    {
        private SocketClient client = new SocketClient();
        private Thread worker;

        private readonly Queue<RGBCommand> commandQ = new Queue<RGBCommand>();

        private enum RGBCommandType
        {
            ChangeColor = 1,
            RandomFader = 2,
            DimColor = 3,
            FadeCurrentColor = 4,
            Specials = 5
        }

        private struct RGBCommand
        {
            public float R, G, B;
            public RGBCommandType Type;
            public string Command;

            public RGBCommand(RGBCommandType type, float r, float g, float b)
            {
                Command = string.Empty;
                Type = type;
                R = r;
                G = g;
                B = b;
            }

            public RGBCommand(RGBCommandType type, string command)
            {
                this.Command = command;
                Type = type;
                R = 0;
                G = 0;
                B = 0;
            }
        }

        // Constructor
        public MainPage()
        {
            InitializeComponent();

            // Set the data context of the listbox control to the sample data
            DataContext = App.ViewModel;

            // Sample code to localize the ApplicationBar
            BuildLocalizedApplicationBar();

            ColorPicker colorPicker = new ColorPicker();
            colorPicker.ColorChanged += colorPicker_ColorChanged;
            gridChooseColor.Children.Add(colorPicker);

            worker = new Thread(rgbWorking);
            worker.IsBackground = true;
            worker.Start();

        }

        void colorPicker_ColorChanged(object sender, System.Windows.Media.Color color)
        {
            lock (commandQ)
            {
                if (commandQ.Count > 0) commandQ.Clear();
                commandQ.Enqueue(new RGBCommand(RGBCommandType.ChangeColor, color.R / 255.0f, color.G / 255.0f, color.B / 255.0f));
                Monitor.PulseAll(commandQ);
            }
        }


        private void rgbWorking()
        {
            while (true)
            {
                try
                {
                    RGBCommand c;
                    lock (commandQ)
                    {

                        while (commandQ.Count == 0)
                        {
                            Monitor.Wait(commandQ, 1000);
                        }


                        c = commandQ.Dequeue();
                    }

                    
                    client.Connect("192.168.1.150", 4321);
                    switch(c.Type){
                        case RGBCommandType.ChangeColor:
                            client.Send("cc " + c.R.ToString("F3") + " " + c.G.ToString("F3") + " " + c.B.ToString("F3"));
                            break;
                        case RGBCommandType.RandomFader:
                            client.Send("rf "+c.Command);
                            break;
                        case RGBCommandType.DimColor:
                            client.Send("dim " + c.Command);
                            break;
                        case RGBCommandType.FadeCurrentColor:
                            client.Send("fade " + c.Command);
                            break;
                        case RGBCommandType.Specials:
                            client.Send("special " + c.Command);
                            break;
                    }
                    client.Close();
                }
                catch { }
            }
        }


        // Load data for the ViewModel Items
        protected override void OnNavigatedTo(NavigationEventArgs e)
        {
            if (!App.ViewModel.IsDataLoaded)
            {
                App.ViewModel.LoadData();
            }
        }



        // Sample code for building a localized ApplicationBar
        private void BuildLocalizedApplicationBar()
        {
            // Set the page's ApplicationBar to a new instance of ApplicationBar.
            ApplicationBar = new ApplicationBar();

            // Create a new button and set the text value to the localized string from AppResources.
            ApplicationBarIconButton abbOn = new ApplicationBarIconButton(new Uri("/Assets/Icons/on.png", UriKind.Relative));
            abbOn.Text = "On";
            abbOn.Click += delegate(object s, EventArgs ea)
            {
                lock (commandQ)
                {
                    commandQ.Enqueue(new RGBCommand(RGBCommandType.FadeCurrentColor, "2 FFFFFF"));
                    Monitor.PulseAll(commandQ);
                }
            };
            ApplicationBar.Buttons.Add(abbOn);

            ApplicationBarIconButton abbOff = new ApplicationBarIconButton(new Uri("/Assets/Icons/off.png", UriKind.Relative));
            abbOff.Text = "Off";
            abbOff.Click += delegate(object s, EventArgs ea)
            {
                lock (commandQ)
                {
                    commandQ.Enqueue(new RGBCommand(RGBCommandType.FadeCurrentColor, "2 000000"));
                    Monitor.PulseAll(commandQ);
                }
            };
            ApplicationBar.Buttons.Add(abbOff);

            // Create a new menu item with the localized string from AppResources.
            //ApplicationBarMenuItem appBarMenuItem = new ApplicationBarMenuItem(AppResources.AppBarMenuItemText);
            //ApplicationBar.MenuItems.Add(appBarMenuItem);
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            lock (commandQ)
            {
                commandQ.Enqueue(new RGBCommand(RGBCommandType.RandomFader, slMinSpeed.Value+" "+slMaxSpeed.Value+" "+slMinBrightness.Value+ " "+slMaxBrightness.Value));
                Monitor.PulseAll(commandQ);
            }
        }

        private void btnDim_Click(object sender, RoutedEventArgs e)
        {
            lock (commandQ)
            {
                commandQ.Enqueue(new RGBCommand(RGBCommandType.DimColor, "900 "+txtDimColor.Text));
                Monitor.PulseAll(commandQ);
            }
        }

        private void btnSpecialsJamaica_Click(object sender, RoutedEventArgs e)
        {
            lock (commandQ)
            {
                commandQ.Enqueue(new RGBCommand(RGBCommandType.Specials, "jamaica 2"));
                Monitor.PulseAll(commandQ);
            }
        }


    }
}