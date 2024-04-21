using Android.App;
using Android.Graphics;
using Android.OS;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using AndroidX.AppCompat.App;
using System;
using System.Threading;
using static Android.Bluetooth.BluetoothClass;

namespace App1
{
    [Activity(Label = "@string/app_name", Theme = "@style/AppTheme", MainLauncher = true)]
    public class MainActivity : AppCompatActivity
    {
        string[] weekdays =
        { "星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六" };

        string[] weekdays_EnglishArray =
        {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

        string[] month_EnglishArray =
        {"December", "January","February", "March", "April", "May", "June", "July", "August", "September", "October", "November"};

        private LinearLayout linearLayout;
        private TextView textView1, textView2, textView3, textView4, textView5;

        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            Xamarin.Essentials.Platform.Init(this, savedInstanceState);

            // 设置应用程序主题
            this.SetTheme(Resource.Style.Theme_AppCompat_Light_NoActionBar);

            //// 创建一个 XmlDocument 对象
            //var xmlDocument = new XmlDocument();

            //// 加载 RSS 文档
            //xmlDocument.Load("https://www.cnblogs.com/feed");

            //// 获取 RSS 文档中的所有项
            //var items = xmlDocument.SelectNodes("rss/channel/item");

            //锁定横屏
            this.RequestedOrientation = Android.Content.PM.ScreenOrientation.Landscape;

            //设置全屏
            Window.SetFlags(WindowManagerFlags.Fullscreen, WindowManagerFlags.Fullscreen);
            Window.SetFlags(WindowManagerFlags.KeepScreenOn, WindowManagerFlags.KeepScreenOn);

            SetContentView(Resource.Layout.activity_main);

            // 初始化控件
            textView1 = FindViewById<TextView>(Resource.Id.textView1);
            textView2 = FindViewById<TextView>(Resource.Id.textView2);
            textView3 = FindViewById<TextView>(Resource.Id.textView3);
            textView4 = FindViewById<TextView>(Resource.Id.textView4);
            textView5 = FindViewById<TextView>(Resource.Id.textView5);
            linearLayout = FindViewById<LinearLayout>(Resource.Id.linearLayout1);

            // 加载字体文件
            //Typeface customFont = Typeface.CreateFromAsset(Assets, "SanJiXianYunJianTi.ttf");
            //textView1.Typeface = customFont;
            //textView2.Typeface = customFont;
            //textView3.Typeface = customFont;
            //textView4.Typeface = customFont;
            //textView5.Typeface = customFont;

            new Thread(new ThreadStart(() =>
            {
                while (true)
                {
                    //5分钟清屏一次
                    Thread.Sleep(300000);

                    //执行清屏,在主线程中更新UI
                    RunOnUiThread(() =>
                    {
                        //隐藏所有文字
                        textView1.Visibility = ViewStates.Gone;
                        textView2.Visibility = ViewStates.Gone;
                        textView3.Visibility = ViewStates.Gone;
                        textView4.Visibility = ViewStates.Gone;
                        textView5.Visibility = ViewStates.Gone;
                    });
                    Thread.Sleep(200);
                    RunOnUiThread(() =>
                    {
                        //背景设置为黑色
                        linearLayout.SetBackgroundColor(Android.Graphics.Color.ParseColor("#ff000000"));
                    });
                    Thread.Sleep(200);
                    RunOnUiThread(() =>
                    {
                        //背景设置为白色
                        linearLayout.SetBackgroundColor(Android.Graphics.Color.ParseColor("#ffffffff"));
                    });
                    Thread.Sleep(200);
                    RunOnUiThread(() =>
                    {
                        //显示所有文字
                        textView1.Visibility = ViewStates.Visible;
                        textView2.Visibility = ViewStates.Visible;
                        textView3.Visibility = ViewStates.Visible;
                        textView4.Visibility = ViewStates.Visible;
                        textView5.Visibility = ViewStates.Visible;
                    });
                }
            })).Start();


            var timer = new Timer(new TimerCallback(delegate (object state)
            {
                this.RunOnUiThread(() =>
                {
                    // 获取当前日期和时间
                    var dateTime = DateTime.Now;

                    // 获取当前年份
                    var year = dateTime.Year;
                    // 获取当前月份
                    var month = dateTime.Month;
                    // 获取当前天
                    var day = dateTime.Day;
                    var paddedDay = string.Format("{0:D2}", day);

                    //获取星期
                    var dayOfWeek = dateTime.DayOfWeek;

                    string today = weekdays[(int)dayOfWeek];
                    string today_English = weekdays_EnglishArray[(int)dayOfWeek];
                    string month_English = month_EnglishArray[(int)month];

                    //获取当前小时
                    var hour = dateTime.Hour;
                    var paddedHour = string.Format("{0:D2}", hour);

                    //获取当前分钟
                    var minute = dateTime.Minute;
                    var paddedMinute = string.Format("{0:D2}", minute);

                    //设值
                    textView1.Text = today + "  ";
                    textView5.Text = today_English;
                    //年月日
                    textView4.Text = paddedDay.ToString() + "  " + month.ToString() + "月  " + year.ToString();
                    //英文年月日
                    textView2.Text = paddedDay.ToString() + " " + month_English + " " + year.ToString();
                    //时间
                    textView3.Text = paddedHour.ToString() + ":" + paddedMinute.ToString();

                });
            }), null, 0, 60000);

        }
        public override void OnRequestPermissionsResult(int requestCode, string[] permissions, [GeneratedEnum] Android.Content.PM.Permission[] grantResults)
        {
            Xamarin.Essentials.Platform.OnRequestPermissionsResult(requestCode, permissions, grantResults);

            base.OnRequestPermissionsResult(requestCode, permissions, grantResults);
        }
    }
}