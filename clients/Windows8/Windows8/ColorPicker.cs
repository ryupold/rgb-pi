using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Documents;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;

// The Templated Control item template is documented at http://go.microsoft.com/fwlink/?LinkId=234235

namespace Windows8
{
    public sealed class ColorPicker : Control
    {
        public ColorPicker()
        {
            this.DefaultStyleKey = typeof(ColorPicker);
        }

        public bool Blink
        {
            get { return (bool)GetValue(BlinkProperty); }
            set { SetValue(BlinkProperty, value); }
        }

        // Using a DependencyProperty enables animation, styling, binding, etc.
        public static readonly DependencyProperty BlinkProperty =
            DependencyProperty.Register(
                "Blink",                  // The name of the DependencyProperty
                typeof(bool),             // The type of the DependencyProperty
                typeof(ColorPicker),       // The type of the owner of the DependencyProperty
                new PropertyMetadata(     // OnBlinkChanged will be called when Blink changes
                    false,                // The default value of the DependencyProperty
                    new PropertyChangedCallback(OnBlinkChanged)
                )
            );
        
        private static void OnBlinkChanged(
            DependencyObject d,
            DependencyPropertyChangedEventArgs e
        )
        {
            var instance = d as ColorPicker;
            if (instance != null)
            {
                //do something on property change
            }
        }

        
    }

}
