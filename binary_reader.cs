using System;
using System.Net.Http;
using System.Threading.Tasks;
using System.Runtime.Serialization.Formatters.Binary;
using System.IO;
using System.Text.Json;

namespace BinaryReader
{
    class Program
    {
        static async Task Main(string[] args)
        {
            if (args.Length > 0)
            {
                string url = args[0];
                await ReadFromUrl(url);
            }
            else
            {
                Console.WriteLine("No URL provided.");
            }
        }

        private static async Task ReadFromUrl(string url)
        {
            var httpClient = new HttpClient();

            try
            {
                var response = await httpClient.GetStreamAsync(url);
                var formatter = new BinaryFormatter();
                var obj = formatter.Deserialize(response);

                string jsonString = JsonSerializer.Serialize(obj, new JsonSerializerOptions { WriteIndented = true });
                Console.WriteLine(jsonString);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }
    }
}
